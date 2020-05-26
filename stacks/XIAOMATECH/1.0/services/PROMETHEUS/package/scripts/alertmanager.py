from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Alertmanager(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Directory([
            params.conf_dir, params.alertmanager_data_dir,
            params.prometheus_data_dir
        ],
                  owner=params.prometheus_user,
                  group=params.user_group,
                  mode=0775,
                  create_parents=True)
        params.install_from_file('alertmanager')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/alertmanager.yml',
            content=InlineTemplate(params.alertmanager_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)

        File(
            '/usr/lib/systemd/system/alertmanager.service',
            content=InlineTemplate(params.alertmanager_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop alertmanager')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start alertmanager')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status alertmanager')


if __name__ == "__main__":
    Alertmanager().execute()
