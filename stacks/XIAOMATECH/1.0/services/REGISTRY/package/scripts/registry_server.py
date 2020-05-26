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
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.libraries.functions import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.utils import PasswordString

from registry import ensure_base_directories
from registry import registry, install_registry


class RegistryServer(Script):
    def get_component_name(self):
        stack_name = default("/clusterLevelParams/stack_name", None)
        if stack_name == "HDP":
            return None
        return "registry"

    def execute_bootstrap(self, params):
        try:
            # If Current version >= 3.1, migrate else create
            if params.stack_registry_support_schema_migrate:
                Execute(
                    params.bootstrap_storage_run_cmd + ' migrate', user="root")
            else:
                Execute(
                    params.bootstrap_storage_run_cmd + ' create', user="root")
        except:
            show_logs(params.registry_log_dir, params.registry_user)
            raise

    def execute_bootstrap_storage_env(self, params):
        from urlparse import urlparse
        try:
            # Getting hostname where registry's database would be installed.
            registry_storage_database_hostname = \
                urlparse(urlparse(params.registry_storage_connector_connectorURI)[2])[1].split(":")[0]
            database_admin_jdbc_url = params.database_admin_jdbc_url
            if params.registry_storage_type == 'postgresql':
                database_admin_jdbc_url = database_admin_jdbc_url + '/postgres'
            bootstrap_storage_initevn_db_cmd = database_admin_jdbc_url + ' ' + params.database_admin_user_name + ' ' + PasswordString(
                params.database_admin_password
            ) + ' ' + params.registry_storage_connector_user + ' ' + PasswordString(
                params.registry_storage_connector_password
            ) + ' ' + params.registry_storage_database
            Execute(
                params.bootstrap_storage_initevn_run_cmd + ' ' +
                bootstrap_storage_initevn_db_cmd,
                user='root')
        except:
            show_logs(params.registry_log_dir, params.registry_user)
            raise

    def install(self, env):
        import params
        self.install_packages(env)
        install_registry()
        self.configure(env)
        if params.stack_registry_support_db_user_creation:
            if params.database_create_db_dbuser == "true":
                self.execute_bootstrap_storage_env(params)
        if not params.stack_registry_support_schema_migrate:
            self.execute_bootstrap(params)

    def configure(self, env):
        import params
        env.set_params(params)
        registry(env)

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        install_registry()
        self.configure(env)

        if params.stack_registry_support_schema_migrate:
            self.execute_bootstrap(params)

        daemon_cmd = format(
            'source {params.conf_dir}/registry-env.sh ; {params.registry_bin} start'
        )
        no_op_test = format(
            'ls {status_params.registry_pid_file} >/dev/null 2>&1 && ps -p `cat {status_params.registry_pid_file}` >/dev/null 2>&1'
        )
        try:
            Execute(daemon_cmd, user="root", not_if=no_op_test)
        except:
            show_logs(params.registry_log_dir, params.registry_user)

    def stop(self, env):
        import params
        import status_params
        env.set_params(params)
        ensure_base_directories()

        daemon_cmd = format(
            'source {params.conf_dir}/registry-env.sh; {params.registry_bin} stop'
        )
        try:
            Execute(
                daemon_cmd,
                user=params.registry_user,
            )
        except:
            show_logs(params.registry_log_dir, params.registry_user)
            raise
        File(status_params.registry_pid_file, action="delete")

    def status(self, env):
        import status_params
        check_process_status(status_params.registry_pid_file)

    def get_log_folder(self):
        import params
        return params.registry_log_dir

    def get_user(self):
        import params
        return params.registry_user

    def get_pid_files(self):
        import status_params
        return [status_params.registry_pid_file]


if __name__ == "__main__":
    RegistryServer().execute()
