from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from tidb import install_tidb


class Drainer(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('drainer')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/drainer.conf',
            content=InlineTemplate(params.drainer_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/drainer.service',
            content=InlineTemplate(params.drainer_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop drainer')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('drainer')
        self.configure(env)
        Execute('systemctl start drainer')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status drainer')


if __name__ == "__main__":
    Drainer().execute()
