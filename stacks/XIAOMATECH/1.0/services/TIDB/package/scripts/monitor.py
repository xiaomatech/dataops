from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from tidb import install_tidb


class TiMonitor(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('pd-server')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/pd.conf',
            content=InlineTemplate(params.pd_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/pd.service',
            content=InlineTemplate(params.pd_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop pd')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('pd-server')
        self.configure(env)
        Execute('systemctl start pd')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status pd')


if __name__ == "__main__":
    TiMonitor().execute()
