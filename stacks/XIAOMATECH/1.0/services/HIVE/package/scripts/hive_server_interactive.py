#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
# Python Imports
from datetime import datetime
import json
import os
import re
import subprocess
import time
import urllib2

# Local Imports
from hive_service_interactive import hive_service_interactive
from hive_interactive import hive_interactive
from setup_ranger_hive_interactive import setup_ranger_hive_interactive

# Ambari Commons & Resource Management Imports
from resource_management.core import shell
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, Directory
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.script.script import Script
from hive import install_hive


class HiveServerInteractive(Script):
    def install(self, env):
        import params
        self.install_packages(env)
        install_hive()

    def configure(self, env):
        import params
        env.set_params(params)
        hive_interactive(name='hiveserver2')

    def pre_upgrade_restart(self, env):
        Logger.info(
            "Executing Hive Server Interactive Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        install_hive()
        self.configure(env)

        if params.security_enabled:
            # Do the security setup, internally calls do_kinit()
            self.setup_security()

        # TODO : We need have conditional [re]start of LLAP once "status check command" for LLAP is ready.
        # Check status and based on that decide on [re]starting.

        # Start LLAP before Hive Server Interactive start.
        status = self._llap_start(env)
        if not status:
            raise Fail(
                "Skipping START of Hive Server Interactive since LLAP app couldn't be STARTED."
            )

        # TODO : test the workability of Ranger and Hive2 during upgrade
        setup_ranger_hive_interactive(upgrade_type=upgrade_type)
        hive_service_interactive('hiveserver2', action='start')

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        if params.security_enabled:
            self.do_kinit()

        # Stop Hive Interactive Server first
        hive_service_interactive('hiveserver2', action='stop')

        if params.is_restart_command:
            Logger.info("LLAP stop is skipped as its a restart command")
        elif self.__other_instance_running(env):
            Logger.info(
                "LLAP stop is skipped as orher HSI instance is running")
        else:
            self._llap_stop(env)

    def __other_instance_running(self, env):
        import params
        env.set_params(params)

        for hive_server_interactive_host in params.hive_server_interactive_hosts:
            running = False
            if hive_server_interactive_host != params.hostname:
                url = format(
                    "{hive_server_interactive_webui_protocol}://{hive_server_interactive_host}:{hive_server_interactive_webui_port}/leader"
                )
                Logger.info(
                    format(
                        "Checking if there is another HSI instance running by trying to open {url}"
                    ))
                req = urllib2.Request(url)
                try:
                    resp = urllib2.urlopen(req)
                    running = True
                except urllib2.URLError as e:
                    pass
                except urllib2.HTTPError as e:
                    if e.code < 400:
                        running = True
                except socket.error as e:
                    # If we get connection reset error there is a live HS2 on other side.
                    if e.errno == 104:
                        running = True

                if running:
                    Logger.info(
                        format(
                            "Runnning HSI found on {hive_server_interactive_host}"
                        ))
                    return True
                else:
                    Logger.info(
                        format(
                            "No running HSI found on {hive_server_interactive_host}"
                        ))

        return False

    def status(self, env):
        import status_params
        env.set_params(status_params)

        # We are not doing 'llap' status check done here as part of status check for 'HSI', as 'llap' status
        # check is a heavy weight operation.

        # Recursively check all existing gmetad pid files
        check_process_status(status_params.hive_interactive_pid)

    def restart_llap(self, env):
        """
      Custom command to Restart LLAP
      """
        Logger.info("Custom Command to retart LLAP")
        import params
        env.set_params(params)

        if params.security_enabled:
            self.do_kinit()

        self._llap_stop(env)
        status = self._llap_start(env)
        if not status:
            raise Fail("LLAP app couldn't be STARTED.")

    def _llap_stop(self, env):
        import params
        Logger.info("Stopping LLAP")

        stop_cmd = ["yarn", "app", "-stop", params.llap_app_name]

        code, output, error = shell.call(
            stop_cmd,
            user=params.hive_user,
            stderr=subprocess.PIPE,
            logoutput=True)
        if code == 0:
            Logger.info(
                format(
                    "Stopped {params.llap_app_name} application on YARN Service successfully"
                ))
        elif code in [1, 56
                      ] and ((output and "File does not exist" in output) or
                             (error and "File does not exist" in error)):
            Logger.info(
                format(
                    "Application {params.llap_app_name} was already stopped on YARN Service"
                ))
        else:
            raise Fail(
                format(
                    "Could not stop application {params.llap_app_name} on YARN Service. {error}\n{output}"
                ))

        # Will exit with code 4 if need to run with "--force" to delete directories and registries.
        Execute(
            ('yarn', 'app', '-destroy', params.llap_app_name),
            user=params.hive_user,
            timeout=30,
            ignore_failures=True,
        )

    """
    Controls the start of LLAP.
    """

    def _llap_start(self, env, cleanup=False):
        import params
        env.set_params(params)

        if params.hive_server_interactive_ha:
            """
        Check llap app state
        """
            Logger.info(
                "HSI HA is enabled. Checking if LLAP is already running ...")
            status = self.check_llap_app_status(
                params.llap_app_name, 2, params.hive_server_interactive_ha)
            if status:
                Logger.info("LLAP app '{0}' is already running.".format(
                    params.llap_app_name))
                return True
            else:
                Logger.info(
                    "LLAP app '{0}' is not running. llap will be started.".
                    format(params.llap_app_name))
            pass

        # Call for cleaning up the earlier run(s) LLAP package folders.
        self._cleanup_past_llap_package_dirs()

        Logger.info("Starting LLAP")
        LLAP_PACKAGE_CREATION_PATH = Script.get_tmp_dir()

        unique_name = "llap-yarn-service_%s" % datetime.utcnow().strftime(
            '%Y-%m-%d_%H-%M-%S')

        cmd = format(
            "{stack_root}/hive/bin/hive --service llap --size {params.llap_daemon_container_size}m --startImmediately --name {params.llap_app_name} "
            "--cache {params.hive_llap_io_mem_size}m --xmx {params.llap_heap_size}m --loglevel {params.llap_log_level} "
            "--output {LLAP_PACKAGE_CREATION_PATH}/{unique_name} "
        )
        slider_placement = 0
        cmd += format(
            " --service-placement {slider_placement} --skiphadoopversion --skiphbasecp --instances {params.num_llap_daemon_running_nodes}"
        )

        # Setup the logger for the ga version only
        cmd += format(" --logger {params.llap_logger}")

        if params.security_enabled:
            llap_keytab_splits = params.hive_llap_keytab_file.split("/")
            Logger.debug("llap_keytab_splits : {0}".format(llap_keytab_splits))
            cmd += format(
                " --service-keytab-dir .yarn/keytabs/{params.hive_user}/ --service-keytab "
                "{llap_keytab_splits[4]} --service-principal {params.hive_llap_principal}"
            )

        # Add the aux jars if they are specified. If empty, dont need to add this param.
        if params.hive_aux_jars:
            cmd += format(" --auxjars {params.hive_aux_jars}")

        # Append args.
        llap_java_args = InlineTemplate(
            params.llap_app_java_opts).get_content()
        cmd += format(" --args \" {llap_java_args}\"")
        # Append metaspace size to args.
        if params.llap_daemon_container_size <= 32768:
            metaspaceSize = "256m"
        else:
            metaspaceSize = "1024m"
        cmd = cmd[:-1] + " -XX:MetaspaceSize=" + metaspaceSize + "\""

        try:
            Logger.info(format("LLAP start command: {cmd}"))
            code, output, error = shell.checked_call(
                cmd,
                user=params.hive_user,
                quiet=True,
                stderr=subprocess.PIPE,
                logoutput=True,
                env={'HIVE_CONF_DIR': params.hive_server_interactive_conf_dir})

            if code != 0 or output is None:
                raise Fail(
                    "Command failed with either non-zero return code or no output."
                )

            # We need to check the status of LLAP app to figure out it got
            # launched properly and is in running state. Then go ahead with Hive Interactive Server start.
            status = self.check_llap_app_status(
                params.llap_app_name,
                params.num_retries_for_checking_llap_status)
            if status:
                Logger.info("LLAP app '{0}' deployed successfully.".format(
                    params.llap_app_name))
                return True
            else:
                Logger.error("LLAP app '{0}' deployment unsuccessful.".format(
                    params.llap_app_name))
                return False
        except:
            if params.hive_server_interactive_ha:
                Logger.error(
                    "Exception occured. Checking if LLAP was started by another HSI instance ..."
                )
                time.sleep(20)
                status = self.check_llap_app_status(
                    params.llap_app_name, 2, params.hive_server_interactive_ha)
                if status:
                    Logger.info("LLAP app '{0}' is running.".format(
                        params.llap_app_name))
                    return True
                else:
                    Logger.info("LLAP app '{0}' is not running.".format(
                        params.llap_app_name))

                raise  # throw the original exception

    """
    Checks and deletes previous run 'LLAP package' folders, ignoring three latest packages.
    Last three are are ignore for debugging/reference purposes.
    Helps in keeping check on disk space used.
    """

    def _cleanup_past_llap_package_dirs(self):
        try:
            import params
            Logger.info(
                "Determining previous run 'LLAP package' folder(s) to be deleted ...."
            )
            llap_package_folder_name_prefix = "llap-yarn-service"  # Package name is like : llap-yarn-service_YYYY-MM-DD_HH:MM:SS
            num_folders_to_retain = 3  # Hardcoding it as of now, as no considerable use was found to provide an env param.
            file_names = [
                dir_name for dir_name in os.listdir(Script.get_tmp_dir())
                if dir_name.startswith(llap_package_folder_name_prefix)
            ]

            file_names.sort()
            del file_names[
                -num_folders_to_retain:]  # Ignore 'num_folders_to_retain' latest package folders.
            Logger.info(
                "Previous run 'LLAP package' folder(s) to be deleted = {0}".
                format(file_names))

            if file_names:
                for path in file_names:
                    abs_path = Script.get_tmp_dir() + "/" + path
                    Directory(abs_path, action="delete", ignore_failures=True)
            else:
                Logger.info("No '{0}*' folder deleted.".format(
                    llap_package_folder_name_prefix))
        except:
            Logger.exception(
                "Exception while doing cleanup for past 'LLAP package(s)':")

    """
    Does kinit and copies keytab for Hive/LLAP to HDFS.
    """

    def setup_security(self):
        import params

        self.do_kinit()

        # Copy params.hive_llap_keytab_file to hdfs://<host>:<port>/user/<hive_user>/.yarn/keytabs/<hive_user> , required by LLAP
        yarn_service_keytab_mkdir_cmd = format(
            params.hadoop_bin_dir +
            "/hdfs dfs -mkdir -p .yarn/keytabs/{params.hive_user}/")
        Execute(yarn_service_keytab_mkdir_cmd, user=params.hive_user)
        yarn_service_keytab_install_cmd = format(
            params.hadoop_bin_dir +
            "/hdfs dfs -copyFromLocal -f {params.hive_llap_keytab_file} .yarn/keytabs/{params.hive_user}/"
        )
        Execute(yarn_service_keytab_install_cmd, user=params.hive_user)

    def do_kinit(self):
        import params

        hive_interactive_kinit_cmd = format(
            "{kinit_path_local} -kt {params.hive_server2_keytab} {params.hive_principal}; "
        )
        Execute(hive_interactive_kinit_cmd, user=params.hive_user)

    """
    Get llap app status data.

    Parameters: 'percent_desired_instances_to_be_up' : A value b/w 0.0 and 1.0.
                'total_timeout' : Total wait time while checking the status via llapstatus command
                'refresh_rate' : Frequency of polling for llapstatus.
    """

    def _get_llap_app_status_info(self, percent_desired_instances_to_be_up,
                                  total_timeout, refresh_rate):
        import status_params
        import params

        # llapstatus command : llapstatus -w -r <percent containers to wait for to be Up> -i <refresh_rate> -t <total timeout for this command>
        # -w : Watch mode waits until all LLAP daemons are running or subset of the nodes are running (threshold can be specified via -r option) (Default wait until all nodes are running)
        # -r : When watch mode is enabled (-w), wait until the specified threshold of nodes are running (Default 1.0 which means 100% nodes are running)
        # -i : Amount of time in seconds to wait until subsequent status checks in watch mode (Default: 1sec)
        # -t : Exit watch mode if the desired state is not attained until the specified timeout (Default: 300sec)
        #
        #            example : llapstatus -w -r 0.8 -i 2 -t 150
        llap_status_cmd = format(
            "{stack_root}/hive/bin/hive --service llapstatus -w -r {percent_desired_instances_to_be_up} -i {refresh_rate} -t {total_timeout}"
        )
        Logger.info("\n\n\n\n\n")
        Logger.info("LLAP status command : {0}".format(llap_status_cmd))
        code, output, error = shell.checked_call(
            llap_status_cmd,
            user=status_params.hive_user,
            quiet=True,
            stderr=subprocess.PIPE,
            logoutput=True,
            env={'HIVE_CONF_DIR': params.hive_server_interactive_conf_dir})

        if code == 0:
            return self._make_valid_json(output)
        else:
            Logger.info("'LLAP status command' output : ", output)
            Logger.info("'LLAP status command' error : ", error)
            Logger.info("'LLAP status command' exit code : ", code)
            raise Fail("Error getting LLAP app status. ")

    """
    Remove extra lines from 'llapstatus' status output (eg: because of MOTD logging) so as to have a valid JSON data to be passed in
    to JSON converter.
    """

    def _make_valid_json(self, output):
        '''

      Note: It is assumed right now that extra lines will be only at the start and not at the end.

      Sample expected JSON to be passed for 'loads' is either of the form :

      Case 'A':
      {
          "amInfo" : {
          "appName" : "llap0",
          "appType" : "yarn-service",
          "appId" : "APP1",
          "containerId" : "container_1466036628595_0010_01_000001",
          "hostname" : "hostName",
          "amWebUrl" : "http://hostName:port/"
        },
        "state" : "LAUNCHING",
        ....
        "desiredInstances" : 1,
        "liveInstances" : 0,
        ....
        ....
      }

      or

      Case 'B':
      {
        "state" : "APP_NOT_FOUND"
        ...
      }

      '''
        splits = output.split("\n")

        len_splits = len(splits)
        if (len_splits < 3):
            raise Fail(
                "Malformed JSON data received from 'llapstatus' command. Exiting ...."
            )

        marker_idx = None  # To detect where from to start reading for JSON data
        for idx, split in enumerate(splits):
            curr_elem = split.strip()
            if idx + 2 > len_splits:
                raise Fail(
                    "Iterated over the received 'llapstatus' command. Couldn't validate the received output for JSON parsing."
                )
            next_elem = (splits[(idx + 1)]).strip()
            if curr_elem == "{" and (splits[len_splits - 1]).strip() == '}':
                if next_elem == "\"amInfo\" : {" or next_elem.startswith(
                        '"state" : '):
                    marker_idx = idx
                    break

        # Remove extra logging from possible JSON output
        if marker_idx is None:
            raise Fail(
                "Couldn't validate the received output for JSON parsing.")
        else:
            if marker_idx != 0:
                del splits[0:marker_idx]

        scanned_output = '\n'.join(splits)
        llap_app_info = json.loads(scanned_output)
        return llap_app_info

    def check_llap_app_status(self,
                              llap_app_name,
                              num_retries,
                              return_immediately_if_stopped=False):
        curr_time = time.time()
        total_timeout = int(num_retries) * 20
        # Total wait time while checking the status via llapstatus command
        Logger.debug(
            "Calculated 'total_timeout' : {0} using config 'num_retries_for_checking_llap_status' : {1}"
            .format(total_timeout, num_retries))
        refresh_rate = 2  # Frequency of checking the llapstatus
        percent_desired_instances_to_be_up = 80  # Out of 100.
        llap_app_info = self._get_llap_app_status_info(
            percent_desired_instances_to_be_up / 100.0, total_timeout,
            refresh_rate)

        try:
            return self._verify_llap_app_status(llap_app_info, llap_app_name,
                                                return_immediately_if_stopped,
                                                curr_time)
        except Exception as e:
            Logger.info(e.message)
            return False

    def get_log_folder(self):
        import params
        return params.hive_log_dir

    def get_user(self):
        import params
        return params.hive_user

    def _verify_llap_app_status(self, llap_app_info, llap_app_name,
                                return_immediately_if_stopped, curr_time):
        if llap_app_info is None or 'state' not in llap_app_info:
            Logger.error(
                "Malformed JSON data received for LLAP app. Exiting ....")
            return False

        # counters based on various states.
        live_instances = 0
        desired_instances = 0
        percent_desired_instances_to_be_up = 80  # Used in 'RUNNING_PARTIAL' state.
        if return_immediately_if_stopped and (llap_app_info['state'].upper() in
                                              ('APP_NOT_FOUND', 'COMPLETE')):
            return False
        if llap_app_info['state'].upper() == 'RUNNING_ALL':
            Logger.info("LLAP app '{0}' in '{1}' state.".format(
                llap_app_name, llap_app_info['state']))
            return True
        elif llap_app_info['state'].upper() == 'RUNNING_PARTIAL':
            # Check how many instances were up.
            if 'liveInstances' in llap_app_info and 'desiredInstances' in llap_app_info:
                live_instances = llap_app_info['liveInstances']
                desired_instances = llap_app_info['desiredInstances']
            else:
                Logger.info(
                  "LLAP app '{0}' is in '{1}' state, but 'instances' information not available in JSON received. " \
                  "Exiting ....".format(llap_app_name, llap_app_info['state']))
                Logger.info(llap_app_info)
                return False
            if desired_instances == 0:
                Logger.info(
                    "LLAP app '{0}' desired instance are set to 0. Exiting ...."
                    .format(llap_app_name))
                return False

            percentInstancesUp = 0
            if live_instances > 0:
                percentInstancesUp = float(
                    live_instances) / desired_instances * 100
            if percentInstancesUp >= percent_desired_instances_to_be_up:
                Logger.info("LLAP app '{0}' in '{1}' state. Live Instances : '{2}'  >= {3}% of Desired Instances : " \
                            "'{4}'.".format(llap_app_name, llap_app_info['state'],
                                            llap_app_info['liveInstances'],
                                            percent_desired_instances_to_be_up,
                                            llap_app_info['desiredInstances']))
                return True
            else:
                Logger.info("LLAP app '{0}' in '{1}' state. Live Instances : '{2}'. Desired Instances : " \
                            "'{3}' after {4} secs.".format(llap_app_name, llap_app_info['state'],
                                                           llap_app_info['liveInstances'],
                                                           llap_app_info['desiredInstances'],
                                                           time.time() - curr_time))
                raise Fail(
                    "App state is RUNNING_PARTIAL. Live Instances : '{0}', Desired Instance : '{1}'"
                    .format(llap_app_info['liveInstances'],
                            llap_app_info['desiredInstances']))
        elif llap_app_info['state'].upper() in [
                'APP_NOT_FOUND', 'LAUNCHING', 'COMPLETE'
        ]:
            status_str = format("LLAP app '{0}' current state is {1}.".format(
                llap_app_name, llap_app_info['state']))
            Logger.info(status_str)
            raise Fail(status_str)
        else:  # Covers any unknown that we get.
            Logger.info(
                "LLAP app '{0}' current state is '{1}'. Expected : 'RUNNING'.".
                format(llap_app_name, llap_app_info['state']))
            return False


if __name__ == "__main__":
    HiveServerInteractive().execute()
