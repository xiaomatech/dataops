from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from tidb import install_tidb


class Tikv(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('tikv-server')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/tikv.conf',
            content=InlineTemplate(params.tikv_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/tikv.service',
            content=InlineTemplate(params.tikv_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop tikv')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('tikv-server')
        self.configure(env)
        Execute('systemctl start tikv')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status tikv')


if __name__ == "__main__":
    Tikv().execute()
