from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_doris():
    import params
    Directory([params.pid_dir, params.log_dir],
              owner=params.doris_user,
              group=params.doris_group,
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.doris_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('mkdir ' + params.install_dir + '/log && chmod 777 ' +
                params.install_dir + '/log')
        Execute('chown -R %s:%s %s/%s' %
                (params.doris_user, params.doris_group,Script.get_stack_root(), params.version_dir))
        Execute('chown -R %s:%s %s' % (params.doris_user, params.doris_group,
                                       params.install_dir))


class dorisBe(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_doris()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("{install_dir}/be/bin/doris-env.sh"),
            content=InlineTemplate(params.doris_env_content),
            mode=0755,
            owner=params.doris_user,
            group=params.doris_group)
        File(
            format("{install_dir}/be/conf/be.conf"),
            content=InlineTemplate(params.be_conf),
            mode=0755,
            owner=params.doris_user,
            group=params.doris_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + "/be/bin/stop_be.sh")

    def start(self, env):
        import params
        env.set_params(params)
        install_doris()
        self.configure(env)
        Execute(params.install_dir + "/be/bin/start_be.sh --daemon")

    def status(self, env):
        import params
        check_process_status(params.pid_dir + '/be.pid')


if __name__ == "__main__":
    dorisBe().execute()
