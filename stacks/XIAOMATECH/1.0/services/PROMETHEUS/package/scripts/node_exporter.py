from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Exporter(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        for exporter in params.exporter_lists:
            if exporter != '':
                params.install_from_file(file_name=exporter)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/usr/lib/systemd/system/node_exporter.service',
            content=InlineTemplate(params.node_exporter_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop node_exporter')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start node_exporter')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status node_exporter')


if __name__ == "__main__":
    Exporter().execute()
