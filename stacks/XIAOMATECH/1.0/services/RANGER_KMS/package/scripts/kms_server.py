#!/usr/bin/env python
from resource_management.core.exceptions import Fail
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute, File
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core import shell
from resource_management.libraries.functions.default import default
from kms_service import kms_service
import upgrade

import kms


class KmsServer(Script):

    def install(self, env):
        self.install_packages(env)
        import params
        env.set_params(params)

        # taking backup of install.properties file
        Execute(('cp', '-f', format('{kms_home}/install.properties'), format('{kms_home}/install-backup.properties')),
                not_if=format('ls {kms_home}/install-backup.properties'),
                only_if=format('ls {kms_home}/install.properties'),
                sudo=True
                )

        kms.setup_kms_db()
        self.configure(env)
        kms.setup_java_patch()

    def stop(self, env, upgrade_type=None):
        import params

        env.set_params(params)
        kms_service(action='stop', upgrade_type=upgrade_type)
        if params.stack_supports_pid:
            File(params.ranger_kms_pid_file,
                 action="delete"
                 )

    def start(self, env, upgrade_type=None):
        import params

        env.set_params(params)
        self.configure(env)
        kms.enable_kms_plugin()
        kms.setup_kms_jce()
        kms.update_password_configs()
        kms_service(action='start', upgrade_type=upgrade_type)

    def status(self, env):
        import status_params
        env.set_params(status_params)

        if status_params.stack_supports_pid:
            check_process_status(status_params.ranger_kms_pid_file)
            return

        cmd = 'ps -ef | grep proc_rangerkms | grep -v grep'
        code, output = shell.call(cmd, timeout=20)
        if code != 0:
            Logger.debug('KMS process not running')
            raise ComponentIsNotRunning()
        pass

    def configure(self, env):
        import params

        env.set_params(params)
        kms.kms()

    def pre_upgrade_restart(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        upgrade.prestart(env)
        kms.kms(upgrade_type=upgrade_type)
        kms.setup_java_patch()

    def post_upgrade_restart(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        if upgrade_type and params.upgrade_direction == Direction.UPGRADE and not params.stack_supports_multiple_env_sh_files:
            files_name_list = ['ranger-kms-env-piddir.sh', 'ranger-kms-env-logdir.sh']
            for file_name in files_name_list:
                File(format("{kms_conf_dir}/{file_name}"),
                     action="delete"
                     )

    def setup_ranger_kms_database(self, env):
        import params
        env.set_params(params)

        kms.setup_kms_db()

    def get_log_folder(self):
        import params
        return params.kms_log_dir

    def get_user(self):
        import params
        return params.kms_user


if __name__ == "__main__":
    KmsServer().execute()
