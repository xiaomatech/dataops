from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Prometheus(Script):
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
        params.install_from_file('prometheus')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/prometheus.yml',
            content=InlineTemplate(params.prometheus_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            params.conf_dir + '/alert.rules',
            content=InlineTemplate(params.alert_rules_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            params.conf_dir + '/prometheus.rules',
            content=InlineTemplate(params.prometheus_rules_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/prometheus.service',
            content=InlineTemplate(params.prometheus_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop prometheus')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start prometheus')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status prometheus')


if __name__ == "__main__":
    Prometheus().execute()
