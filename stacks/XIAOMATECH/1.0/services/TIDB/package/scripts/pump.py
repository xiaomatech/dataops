from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate

from tidb import install_tidb


class Pump(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('pump')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/pump.conf',
            content=InlineTemplate(params.pump_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/pump.service',
            content=InlineTemplate(params.pump_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop pump')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('pump')
        self.configure(env)
        Execute('systemctl start pump')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status pump')


if __name__ == "__main__":
    Pump().execute()
