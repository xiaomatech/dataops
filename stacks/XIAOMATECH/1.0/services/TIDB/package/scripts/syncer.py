from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from tidb import install_tidb


class Syncer(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('syncer')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/syncer.conf',
            content=InlineTemplate(params.syncer_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/syncer.service',
            content=InlineTemplate(params.syncer_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop syncer')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('syncer')
        self.configure(env)
        Execute('systemctl start syncer')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status syncer')


if __name__ == "__main__":
    Syncer().execute()
