from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
import os


class Grafana(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        if params.grafana_plugins:
            for plugin in params.grafana_plugins.split(','):
                Execute('grafana-cli plugins install ' + plugin)

        service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
        Execute('cp -rf ' + service_packagedir +
                '/scripts/files/dashboards/*' +
                ' /etc/grafana/provisioning/dashboards/ ')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/grafana/grafana.ini',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.grafana_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop grafana-server')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start grafana-server')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status grafana-server')


if __name__ == "__main__":
    Grafana().execute()
