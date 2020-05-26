from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_wherehows():
    import params
    Directory([
        params.log_dir, params.conf_dir + '/backend',
        params.conf_dir + '/jobs', '/var/run/wherehows'
    ],
              owner=params.wherehows_user,
              group=params.user_group,
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir_backend
                          ) or not os.path.exists(params.install_dir_backend):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_backend)
        Execute('rm -rf %s' % params.install_dir_backend)
        Execute('/bin/rm -f /tmp/' + params.filename_backend)
        Execute(
            'wget ' + params.download_url_backend + ' -O /tmp/' + params.filename_backend,
            user=params.wherehows_user)
        Execute('tar -zxf /tmp/' + params.filename_backend + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_backend + ' ' +
                params.install_dir_backend)
        Execute('rm -rf %s/logs && ln -s %s %s/logs ' %
                (params.install_dir_backend, params.log_dir,
                 params.install_dir_backend))
        Execute('rm -rf %s/conf && ln -s %s %s/conf ' %
                (params.install_dir_backend, params.conf_dir,
                 params.install_dir_backend))
        Execute('chown -R %s:%s %s/%s' %
                (params.wherehows_user, params.user_group,
                 params.stack_root,params.version_dir_backend))
        Execute(
            'chown -R %s:%s %s' % (params.wherehows_user, params.user_group,
                                   params.install_dir_backend))


class Backend(Script):
    pid_file = '/var/run/wherehows/backend.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_wherehows()
        File(
            "/usr/lib/systemd/system/wherehows-backend.service",
            content=InlineTemplate(params.backend_systemd),
            mode=0755,
            owner=params.wherehows_user,
            group=params.user_group)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + "/wherehows-env.sh",
            content=InlineTemplate(params.wherehows_env_content),
            mode=0755,
            owner=params.wherehows_user,
            group=params.user_group)
        File(
            params.conf_dir + "/backend/application.conf",
            content=InlineTemplate(params.backend_conf),
            mode=0755,
            owner=params.wherehows_user,
            group=params.user_group)
        File(
            '/etc/sysconfig/wherehows_backend',
            content=InlineTemplate(params.backend_env),
            mode=0755,
            owner=params.wherehows_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop wherehows-backend')

    def start(self, env):
        import params
        env.set_params(params)
        install_wherehows()
        self.configure(env)
        Execute('systemctl start wherehows-backend')
        Execute(
            "echo `ps aux|grep 'wherehows-backend' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep 'wherehows-backend' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Backend().execute()
