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
import os

# Local Imports
from metadata import metadata, install_atlas
from resource_management import Fail
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.resources.system import Directory
from resource_management.core.logger import Logger
from setup_ranger_atlas import setup_ranger_atlas
from resource_management.core.resources.zkmigrator import ZkMigrator


class MetadataServer(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Directory(
            format("{expanded_war_dir}/atlas"),
            action="delete",
        )

        self.install_packages(env)
        install_atlas()

    def configure(self, env):
        import params
        env.set_params(params)
        metadata()

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

    def start(self, env, upgrade_type=None):
        import params

        env.set_params(params)
        install_atlas()
        self.configure(env)

        daemon_cmd = format(
            'source {params.conf_dir}/atlas-env.sh ; {params.metadata_start_script}'
        )
        no_op_test = format(
            'ls {params.pid_file} >/dev/null 2>&1 && ps -p `cat {params.pid_file}` >/dev/null 2>&1'
        )
        atlas_hbase_setup_command = format(
            "cat {atlas_hbase_setup} | hbase shell -n")
        atlas_kafka_setup_command = format("bash {atlas_kafka_setup}")
        secure_atlas_hbase_setup_command = format(
            "kinit -kt {hbase_user_keytab} {hbase_principal_name}; "
        ) + atlas_hbase_setup_command
        # in case if principal was distributed across several hosts, pattern need to be replaced to right one
        secure_atlas_kafka_setup_command = format(
            "kinit -kt {kafka_keytab} {kafka_principal_name}; ").replace(
                "_HOST", params.hostname) + atlas_kafka_setup_command

        if params.stack_supports_atlas_ranger_plugin:
            Logger.info('Atlas plugin is enabled, configuring Atlas plugin.')
            setup_ranger_atlas(upgrade_type=upgrade_type)
        else:
            Logger.info('Atlas plugin is not supported or enabled.')

        try:

            if params.security_enabled and params.has_hbase_master:
                Execute(
                    secure_atlas_hbase_setup_command,
                    tries=5,
                    try_sleep=10,
                    user=params.hbase_user)
            elif params.enable_ranger_hbase and not params.security_enabled:
                Execute(
                    atlas_hbase_setup_command,
                    tries=5,
                    try_sleep=10,
                    user=params.hbase_user)

            if params.security_enabled:
                try:
                    Execute(
                        secure_atlas_kafka_setup_command,
                        user=params.kafka_user,
                        tries=5,
                        try_sleep=10)
                except Fail:
                    pass  # do nothing and do not block Atlas start, fail logs would be available via Execute internals

            Execute(daemon_cmd, user=params.metadata_user, not_if=no_op_test)
        except:
            show_logs(params.log_dir, params.metadata_user)
            raise

    def stop(self, env):
        import params

        env.set_params(params)
        daemon_cmd = format(
            'source {params.conf_dir}/atlas-env.sh; {params.metadata_stop_script}'
        )

        # If the pid dir doesn't exist, this means either
        # 1. The user just added Atlas service and issued a restart command (stop+start). So stop should be a no-op
        # since there's nothing to stop.
        # OR
        # 2. The user changed the value of the pid dir config and incorrectly issued a restart command.
        # In which case the stop command cannot do anything since Ambari doesn't know which process to kill.
        # The start command will spawn another instance.
        # The user should have issued a stop, changed the config, and then started it.
        if not os.path.isdir(params.pid_dir):
            Logger.info(
                "*******************************************************************"
            )
            Logger.info(
                "Will skip the stop command since this is the first time stopping/restarting Atlas "
                "and the pid dir does not exist, %s\n" % params.pid_dir)
            return

        try:
            Execute(
                daemon_cmd,
                user=params.metadata_user,
            )
        except:
            show_logs(params.log_dir, params.metadata_user)
            raise

        File(params.pid_file, action="delete")

    def disable_security(self, env):
        import params
        if not params.zookeeper_quorum:
            Logger.info(
                "No zookeeper connection string. Skipping reverting ACL")
            return
        zkmigrator = ZkMigrator(params.zookeeper_quorum, params.java_exec,
                                params.java64_home, params.atlas_jaas_file,
                                params.metadata_user)
        zkmigrator.set_acls(
            params.zk_root if params.zk_root.startswith('/') else
            '/' + params.zk_root, 'world:anyone:crdwa')
        if params.atlas_kafka_group_id:
            zkmigrator.set_acls(
                format('/consumers/{params.atlas_kafka_group_id}'),
                'world:anyone:crdwa')

    def status(self, env):
        import status_params

        env.set_params(status_params)
        check_process_status(status_params.pid_file)

    def get_log_folder(self):
        import params

        return params.log_dir

    def get_user(self):
        import params

        return params.metadata_user

    def get_pid_files(self):
        import status_params
        return [status_params.pid_file]

    def configure_atlas_for_upgrade(self, env):
        import params
        env.set_params(params)
        if params.upgrade_direction == Direction.UPGRADE:
            if params.stack_supports_atlas_ranger_plugin and params.enable_ranger_atlas:
                atlas_policycache_file_v1 = os.path.join(
                    '/etc', 'ranger', params.repo_name, 'policycache',
                    format('atlas_{repo_name}.json'))
                atlas_policycache_file_v1_rename = os.path.join(
                    '/etc', 'ranger', params.repo_name, 'policycache',
                    format('atlas_{repo_name}_v1.json'))
                if os.path.isfile(atlas_policycache_file_v1):
                    Execute(
                        format(
                            'mv {atlas_policycache_file_v1} {atlas_policycache_file_v1_rename}'
                        ),
                        user=params.metadata_user,
                        logoutput=True)
            atlas_simple_auth_policy_file_target = os.path.join(
                format('{conf_dir}'), 'atlas-simple-authz-policy.json')
            File(
                atlas_simple_auth_policy_file_target,
                group=params.user_group,
                owner=params.metadata_user,
                only_if=format(
                    "test -e {atlas_simple_auth_policy_file_target}"),
                mode=0644)

    def update_atlas_simple_authz(self, env):
        import params
        env.set_params(params)

        Directory(
            format('{metadata_home}/'),
            owner=params.metadata_user,
            group=params.user_group,
            recursive_ownership=True,
        )

        update_atlas_simple_authz_script = os.path.join(
            format('{install_dir}'), 'bin', 'atlas_update_simple_auth_json.py')
        update_atlas_simple_authz_command = format(
            'source {params.conf_dir}/atlas-env.sh ; {update_atlas_simple_authz_script} {conf_dir}'
        )
        Execute(
            update_atlas_simple_authz_command,
            only_if=format("test -e {update_atlas_simple_authz_script}"),
            user=params.metadata_user)
        atlas_simple_auth_policy_file = os.path.join(
            format('{conf_dir}'), 'atlas-simple-authz-policy.json')
        File(
            atlas_simple_auth_policy_file,
            group=params.user_group,
            owner=params.metadata_user,
            only_if=format("test -e {atlas_simple_auth_policy_file}"),
            mode=0644)


if __name__ == "__main__":
    MetadataServer().execute()
