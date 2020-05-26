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

Ambari Agent

"""

from resource_management.core import shell
from resource_management.core.shell import as_user, as_sudo
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import Execute, File
from resource_management.core.signal_utils import TerminateStrategy
from ambari_commons import subprocess32
from resource_management.core.logger import Logger


def service(componentName, action='start', serviceName='yarn'):
    import params
    import status_params

    if serviceName == 'mapreduce' and componentName == 'historyserver':
        delete_pid_file = True
        daemon = format("{mapred_bin}/mapred")
        pid_file = format(
            "{mapred_pid_dir}/hadoop-{mapred_user}-{componentName}.pid")
        usr = params.mapred_user
        log_dir = params.mapred_log_dir
        cmd = format(
            "export HADOOP_LIBEXEC_DIR={hadoop_libexec_dir} && {daemon} --daemon"
        )
    else:
        # !!! yarn-daemon.sh deletes the PID for us; if we remove it the script
        # may not work correctly when stopping the service
        delete_pid_file = False
        daemon = format("{yarn_bin}/yarn")
        if componentName == 'registrydns' and status_params.registry_dns_needs_privileged_access:
            pid_file = status_params.yarn_registry_dns_priv_pid_file
            usr = status_params.root_user
        else:
            pid_file = format(
                "{yarn_pid_dir}/hadoop-{yarn_user}-{componentName}.pid")
            usr = params.yarn_user

        log_dir = params.yarn_log_dir

        cmd = format(
            "export HADOOP_LIBEXEC_DIR={hadoop_libexec_dir} && source " +
            params.config_dir +
            "/yarn-env.sh && {daemon} --config {hadoop_conf_dir} --daemon")

    check_process = as_sudo(["test", "-f", pid_file]) + " && " + as_sudo(
        ["pgrep", "-F", pid_file])

    if action == 'start':
        daemon_cmd = format("{ulimit_cmd} {cmd} start {componentName}")

        if componentName == 'registrydns':
            checkAndStopRegistyDNS(cmd)
        else:
            # Remove the pid file if its corresponding process is not running.
            File(pid_file, action="delete", not_if=check_process)

        if componentName == 'timelineserver' and serviceName == 'yarn':
            File(
                params.ats_leveldb_lock_file,
                action="delete",
                only_if=format("ls {params.ats_leveldb_lock_file}"),
                not_if=check_process,
                ignore_failures=True)

        try:
            # Attempt to start the process. Internally, this is skipped if the process is already running.
            Execute(daemon_cmd, user=usr, not_if=check_process)

            # Ensure that the process with the expected PID exists.
            Execute(
                check_process,
                not_if=check_process,
                tries=5,
                try_sleep=1,
            )
        except:
            show_logs(log_dir, usr)
            raise

    elif action == 'stop':
        daemon_cmd = format("{cmd} stop {componentName}")
        if componentName == 'registrydns':
            checkAndStopRegistyDNS(cmd)
        else:
            try:
                Execute(daemon_cmd, user=usr, only_if=check_process)
            except:
                show_logs(log_dir, usr)
                raise

            # !!! yarn-daemon doesn't need us to delete PIDs
            if delete_pid_file is True:
                File(pid_file, action="delete")

    elif action == 'refreshQueues':
        rm_kinit_cmd = params.rm_kinit_cmd
        refresh_cmd = format(
            "{rm_kinit_cmd} export HADOOP_LIBEXEC_DIR={hadoop_libexec_dir} && {yarn_bin}/yarn rmadmin -refreshQueues"
        )
        Execute(
            refresh_cmd,
            user=usr,
            timeout=
            20,  # when Yarn is not started command hangs forever and should be killed
            tries=5,
            try_sleep=5,
            timeout_kill_strategy=TerminateStrategy.
            KILL_PROCESS_GROUP,  # the process cannot be simply killed by 'kill -15', so kill pg group instread.
        )


def checkAndStopRegistyDNS(cmd):
    import params
    import status_params

    hadoop_env_exports = {'HADOOP_LIBEXEC_DIR': params.hadoop_libexec_dir}
    componentName = 'registrydns'
    daemon_cmd = format("{cmd} stop {componentName}")
    log_dir = params.yarn_log_dir

    # When registry dns is switched from non-privileged to privileged mode or the other way,
    # then the previous instance of registry dns has a different pid/user.
    # Checking if either of the processes are running and shutting them down if they are.
    for dns_pid_file, dns_user in [
        (status_params.yarn_registry_dns_priv_pid_file,
         status_params.root_user),
        (status_params.yarn_registry_dns_pid_file, params.yarn_user)
    ]:
        process_id_exists_command = as_sudo([
            "test", "-f", dns_pid_file
        ]) + " && " + as_sudo(["pgrep", "-F", dns_pid_file])
        try:
            Execute(
                daemon_cmd, only_if=process_id_exists_command, user=dns_user)
        except:
            # When the registry dns port is modified but registry dns is not started
            # immediately, then the configs in yarn-env.sh & yarn-site.xml related
            # to registry dns may have already changed. This introduces a discrepancy
            # between the actual process that is running and the configs.
            # For example, when port is changed from 5300 to 53,
            # then dns port = 53 in yarn-site and YARN_REGISTRYDNS_SECURE_* envs in yarn-env.sh
            # are saved. So, while trying to shutdown the stray non-privileged registry dns process
            # after sometime, yarn daemon from the configs thinks that it needs privileged
            # access and throws an exception. In such cases, we try to kill the stray process.
            show_logs(log_dir, dns_user)
            pass

        process_id_does_not_exist_command = format(
            "! ( {process_id_exists_command} )")
        code, out = shell.call(
            process_id_does_not_exist_command,
            env=hadoop_env_exports,
            tries=5,
            try_sleep=5)
        if code != 0:
            code, out, err = shell.checked_call(("cat", dns_pid_file),
                                                sudo=True,
                                                env=hadoop_env_exports,
                                                stderr=subprocess32.PIPE)
            Logger.info("PID to kill was retrieved: '" + out + "'.")
            out = out.splitlines()[0]
            pid = out
            Execute(("kill", "-9", pid), sudo=True)
            File(dns_pid_file, action="delete")
