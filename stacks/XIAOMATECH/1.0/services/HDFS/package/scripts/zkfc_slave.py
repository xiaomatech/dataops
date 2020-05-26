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
# this is needed to avoid a circular dependency since utils.py calls this class
import utils
from hdfs import hdfs, install_hadoop

from resource_management.core.logger import Logger
from resource_management.core.exceptions import Fail
from resource_management.core.resources.system import Directory
from resource_management.core.resources.service import Service
from resource_management.core import shell
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.script import Script
from resource_management.core.resources.zkmigrator import ZkMigrator
from resource_management.core.resources.system import Execute
from resource_management.core.source import Template


class ZkfcSlave(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_hadoop()

    def configure(env):
        ZkfcSlave.configure_static(env)

    @staticmethod
    def configure_static(env):
        import params
        env.set_params(params)
        generate_logfeeder_input_config(
            'hdfs',
            Template("input.config-hdfs.json.j2", extra_imports=[default]))
        hdfs("zkfc_slave")
        utils.set_up_zkfc_security(params)
        pass

    def format(self, env):
        import params
        env.set_params(params)

        utils.set_up_zkfc_security(params)

        Execute(
            params.hadoop_bin_dir + "/hdfs zkfc -formatZK -nonInteractive",
            returns=[
                0, 2
            ],  # Returns 0 on success ; Returns 2 if zkfc is already formatted
            user=params.hdfs_user,
            logoutput=True)

    def start(self, env):
        install_hadoop()
        self.start_static(env)

    @staticmethod
    def start_static(env):
        import params
        install_hadoop()
        env.set_params(params)
        ZkfcSlave.configure_static(env)
        Directory(
            params.hadoop_pid_dir_prefix,
            mode=0755,
            owner=params.hdfs_user,
            group=params.user_group)

        # format the znode for this HA setup
        # only run this format command if the active namenode hostname is set
        # The Ambari UI HA Wizard prompts the user to run this command
        # manually, so this guarantees it is only run in the Blueprints case
        if params.dfs_ha_enabled and len(params.dfs_ha_namenode_active) > 0:
            success = initialize_ha_zookeeper(params)
            if not success:
                raise Fail("Could not initialize HA state in zookeeper")

        utils.service(
            action="start",
            name="zkfc",
            user=params.hdfs_user,
            create_pid_dir=True,
            create_log_dir=True)

    def stop(self, env):
        self.stop_static(env)

    @staticmethod
    def stop_static(env):
        import params

        env.set_params(params)
        utils.service(
            action="stop",
            name="zkfc",
            user=params.hdfs_user,
            create_pid_dir=True,
            create_log_dir=True)

    def status(self, env):
        self.status_static(env)

    @staticmethod
    def status_static(env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.zkfc_pid_file)

    def disable_security(self, env):
        import params

        if not params.stack_supports_zk_security:
            return

        zkmigrator = ZkMigrator(params.ha_zookeeper_quorum, params.java_exec,
                                params.java_home, params.jaas_file,
                                params.hdfs_user)
        zkmigrator.set_acls(
            params.zk_namespace if params.zk_namespace.startswith('/') else
            '/' + params.zk_namespace, 'world:anyone:crdwa')

    def get_log_folder(self):
        import params
        return params.hdfs_log_dir

    def get_user(self):
        import params
        return params.hdfs_user

    def get_pid_files(self):
        import status_params
        return [status_params.zkfc_pid_file]

    def pre_upgrade_restart(self, env):
        Logger.info("Executing Stack Upgrade pre-restart")
        import params
        env.set_params(params)


def initialize_ha_zookeeper(params):
    try:
        iterations = 10
        formatZK_cmd = params.hadoop_bin_dir + "/hdfs zkfc -formatZK -nonInteractive"
        Logger.info("Initialize HA state in ZooKeeper: %s" % (formatZK_cmd))
        for i in range(iterations):
            Logger.info('Try %d out of %d' % (i + 1, iterations))
            code, out = shell.call(
                formatZK_cmd, logoutput=False, user=params.hdfs_user)
            if code == 0:
                Logger.info("HA state initialized in ZooKeeper successfully")
                return True
            elif code == 2:
                Logger.info("HA state already initialized in ZooKeeper")
                return True
            elif code == 1 and "zkfc is running as process " in out:
                Logger.info(
                    "HA state already initialized in ZooKeeper, since '{0}'".
                    format(out))
                return True
            else:
                Logger.warning(
                    'HA state initialization in ZooKeeper failed with %d error code. Will retry'
                    % (code))
    except Exception as ex:
        Logger.error(
            'HA state initialization in ZooKeeper threw an exception. Reason %s'
            % (str(ex)))
    return False


if __name__ == "__main__":
    ZkfcSlave().execute()
