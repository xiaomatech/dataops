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

import os

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.resources.system import File, Execute, Link
from knox import knox, update_knox_logfolder_permissions,install_knox
from knox_ldap import ldap
from setup_ranger_knox import setup_ranger_knox


class KnoxGateway(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_knox()

        File(
            os.path.join(params.knox_conf_dir, 'topologies', 'sandbox.xml'),
            action="delete",
        )

    def configure(self, env):
        import params
        env.set_params(params)
        knox()
        ldap()

    def configureldap(self, env):
        import params
        env.set_params(params)
        ldap()

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        install_knox()
        self.configure(env)
        daemon_cmd = format('{knox_bin} start')
        no_op_test = format(
            'ls {knox_pid_file} >/dev/null 2>&1 && ps -p `cat {knox_pid_file}` >/dev/null 2>&1'
        )
        setup_ranger_knox(upgrade_type=upgrade_type)
        # Used to setup symlink, needed to update the knox managed symlink, in case of custom locations
        if os.path.islink(params.knox_managed_pid_symlink):
            Link(
                params.knox_managed_pid_symlink,
                to=params.knox_pid_dir,
            )

        update_knox_logfolder_permissions()

        try:
            Execute(
                daemon_cmd,
                user=params.knox_user,
                environment={'JAVA_HOME': params.java_home},
                not_if=no_op_test)
        except:
            show_logs(params.knox_logs_dir, params.knox_user)
            raise

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        daemon_cmd = format('{knox_bin} stop')

        update_knox_logfolder_permissions()

        try:
            Execute(
                daemon_cmd,
                environment={'JAVA_HOME': params.java_home},
                user=params.knox_user,
            )
        except:
            show_logs(params.knox_logs_dir, params.knox_user)
            raise

        File(
            params.knox_pid_file,
            action="delete",
        )

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.knox_pid_file)

    def startdemoldap(self, env):
        import params
        env.set_params(params)
        self.configureldap(env)
        daemon_cmd = format('{ldap_bin} start')
        no_op_test = format(
            'ls {ldap_pid_file} >/dev/null 2>&1 && ps -p `cat {ldap_pid_file}` >/dev/null 2>&1'
        )
        Execute(
            daemon_cmd,
            user=params.knox_user,
            environment={'JAVA_HOME': params.java_home},
            not_if=no_op_test)

    def stopdemoldap(self, env):
        import params
        env.set_params(params)
        self.configureldap(env)
        daemon_cmd = format('{ldap_bin} stop')
        Execute(
            daemon_cmd,
            environment={'JAVA_HOME': params.java_home},
            user=params.knox_user,
        )
        File(params.ldap_pid_file, action="delete")

    def get_log_folder(self):
        import params
        return params.knox_logs_dir

    def get_user(self):
        import params
        return params.knox_user

    def get_pid_files(self):
        import status_params
        return [status_params.knox_pid_file]


if __name__ == "__main__":
    KnoxGateway().execute()
