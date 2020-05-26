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
from resource_management import Script
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.show_logs import show_logs
from kafka import ensure_base_directories, install_kafka

from kafka import kafka
from setup_ranger_kafka import setup_ranger_kafka


class KafkaBroker(Script):
    def install(self, env):
        self.install_packages(env)
        install_kafka()

    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        kafka(upgrade_type=upgrade_type)

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)
        install_kafka()

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        install_kafka()
        self.configure(env, upgrade_type=upgrade_type)

        if params.kerberos_security_enabled:
            kafka_kinit_cmd = format(
                "{kinit_path_local} -kt {kafka_keytab_path} {kafka_jaas_principal};"
            )
            Execute(kafka_kinit_cmd, user=params.kafka_user)

        if params.is_supported_kafka_ranger:
            setup_ranger_kafka()  #Ranger Kafka Plugin related call
        daemon_cmd = format(
            'source {params.conf_dir}/kafka-env.sh ; {params.kafka_bin} start')
        no_op_test = format(
            'ls {params.kafka_pid_file} >/dev/null 2>&1 && ps -p `cat {params.kafka_pid_file}` >/dev/null 2>&1'
        )
        try:
            Execute(daemon_cmd, user=params.kafka_user, not_if=no_op_test)
        except:
            show_logs(params.kafka_log_dir, params.kafka_user)
            raise

    def stop(self, env):
        import params
        env.set_params(params)
        # Kafka package scripts change permissions on folders, so we have to
        # restore permissions after installing repo version bits
        # before attempting to stop Kafka Broker
        ensure_base_directories()
        daemon_cmd = format(
            'source {params.conf_dir}/kafka-env.sh; {params.kafka_bin} stop')
        try:
            Execute(
                daemon_cmd,
                user=params.kafka_user,
            )
        except:
            show_logs(params.kafka_log_dir, params.kafka_user)
            raise
        File(params.kafka_pid_file, action="delete")

    def disable_security(self, env):
        import params
        if not params.zookeeper_connect:
            Logger.info(
                "No zookeeper connection string. Skipping reverting ACL")
            return
        if not params.secure_acls:
            Logger.info(
                "The zookeeper.set.acl is false. Skipping reverting ACL")
            return
        Execute(
          "{0} --zookeeper.connect {1} --zookeeper.acl=unsecure".format(params.kafka_security_migrator, params.zookeeper_connect), \
          user=params.kafka_user, \
          environment={ 'JAVA_HOME': params.java64_home }, \
          logoutput=True, \
          tries=3)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.kafka_pid_file)

    def get_log_folder(self):
        import params
        return params.kafka_log_dir

    def get_user(self):
        import params
        return params.kafka_user

    def get_pid_files(self):
        import status_params
        return [status_params.kafka_pid_file]


if __name__ == "__main__":
    KafkaBroker().execute()
