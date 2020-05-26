from resource_management import *
from resource_management import Script
from resource_management.libraries.script.script import Script
from resource_management.core import shell, sudo
from resource_management.core.resources.system import Execute, File, Directory, Link
from resource_management.libraries.functions import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.utils import PasswordString

import os, time, glob
from streamline import ensure_base_directories
from streamline import streamline, wait_until_server_starts


def install_streamline():
    import params
    Directory([params.conf_dir],
              owner=params.streamline_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.streamline_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('/bin/rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute(
            'chown -R %s:%s %s/%s' % (params.streamline_user,
                                        params.user_group,params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.streamline_user,
                                       params.user_group, params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


class StreamlineServer(Script):
    def get_component_name(self):
        stack_name = default("/clusterLevelParams/stack_name", None)
        if stack_name == "HDP":
            return None
        return "streamline"

    def execute_bootstrap(self, params):
        try:
            if params.stack_sam_support_schema_migrate:
                Execute(
                    params.bootstrap_storage_run_cmd + ' migrate',
                    user=params.streamline_user)
            else:
                Execute(
                    params.bootstrap_storage_run_cmd + ' create',
                    user=params.streamline_user)
        except:
            show_logs(params.streamline_log_dir, params.streamline_user)
            raise

    def execute_bootstrap_storage_env(self, params):
        from urlparse import urlparse
        try:
            streamline_storage_database_hostname = \
                urlparse(urlparse(params.streamline_storage_connector_connectorURI)[2])[1].split(":")[0]
            database_admin_jdbc_url = params.database_admin_jdbc_url
            if params.streamline_storage_type == 'postgresql':
                database_admin_jdbc_url = database_admin_jdbc_url + '/postgres'
            bootstrap_storage_initevn_db_cmd = database_admin_jdbc_url + ' ' + params.database_admin_user_name + ' ' + PasswordString(
                params.database_admin_password
            ) + ' ' + params.streamline_storage_connector_user + ' ' + PasswordString(
                params.streamline_storage_connector_password
            ) + ' ' + params.streamline_storage_database
            Execute(
                params.bootstrap_storage_initevn_run_cmd + ' ' +
                bootstrap_storage_initevn_db_cmd,
                user='root')
        except:
            show_logs(params.streamline_log_dir, params.streamline_user)

    def install(self, env):
        import params
        install_streamline()
        self.configure(env)
        if params.stack_streamline_support_db_user_creation:
            if params.database_create_db_dbuser == "true":
                self.execute_bootstrap_storage_env(params)
        if not params.stack_sam_support_schema_migrate:
            self.execute_bootstrap(params)

    def configure(self, env):
        import params
        env.set_params(params)
        streamline(env, upgrade_type=None)

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)
        install_streamline()

    def kerberos_server_start(self):
        import params
        if params.security_enabled:
            kinit_cmd = format(
                "{kinit_path_local} -kt {params.streamline_keytab_path} {params.streamline_jaas_principal};"
            )
            return_code, out = shell.checked_call(
                kinit_cmd,
                path='/usr/sbin:/sbin:/usr/local/bin:/bin:/usr/bin',
                user=params.streamline_user)

    def start(self, env):
        import params
        import status_params
        env.set_params(params)
        install_streamline()
        self.configure(env)

        self.kerberos_server_start()

        if params.stack_sam_support_schema_migrate:
            self.execute_bootstrap(params)

        daemon_cmd = format(
            'source {params.conf_dir}/streamline-env.sh ; {params.streamline_bin} start'
        )
        no_op_test = format(
            'ls {status_params.streamline_pid_file} >/dev/null 2>&1 && ps -p `cat {status_params.streamline_pid_file}` >/dev/null 2>&1'
        )

        try:
            Execute(daemon_cmd, user="root", not_if=no_op_test)
        except:
            show_logs(params.streamline_log_dir, params.streamline_user)
            raise

        try:
            wait_until_server_starts()

            # Check to see if bootstrap_done file exists or not.
            if os.path.isfile(params.bootstrap_file):
                if params.stack_sam_support_schema_migrate:
                    File(
                        params.bootstrap_file,
                        owner=params.streamline_user,
                        group=params.user_group,
                        mode=0644)
                    Execute(
                        params.bootstrap_run_cmd + ' migrate',
                        user=params.streamline_user)
            else:
                if params.stack_sam_support_schema_migrate:
                    File(
                        params.bootstrap_file,
                        owner=params.streamline_user,
                        group=params.user_group,
                        mode=0644)
                    Execute(
                        params.bootstrap_run_cmd + ' migrate',
                        user=params.streamline_user)
                else:
                    File(
                        params.bootstrap_file,
                        owner=params.streamline_user,
                        group=params.user_group,
                        mode=0644)
                    Execute(
                        params.bootstrap_run_cmd, user=params.streamline_user)
        except:
            show_logs(params.streamline_log_dir, params.streamline_user)
            raise

    def stop(self, env, upgrade_type=None):
        import params
        import status_params
        env.set_params(params)
        ensure_base_directories()

        daemon_cmd = format(
            'source {params.conf_dir}/streamline-env.sh; {params.streamline_bin} stop'
        )
        try:
            Execute(
                daemon_cmd,
                user=params.streamline_user,
            )
        except:
            show_logs(params.streamline_log_dir, params.streamline_user)
            raise
        File(status_params.streamline_pid_file, action="delete")

    def status(self, env):
        import status_params
        check_process_status(status_params.streamline_pid_file)

    def get_log_folder(self):
        import params
        return params.streamline_log_dir

    def get_user(self):
        import params
        return params.streamline_user

    def get_pid_files(self):
        import status_params
        return [status_params.streamline_pid_file]


if __name__ == "__main__":
    StreamlineServer().execute()
