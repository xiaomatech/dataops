from resource_management.core.logger import Logger
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.script import Script

from resource_management.libraries.functions.default import default
download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


class Kibana(Script):
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info("Install Kibana Master")
        self.install_packages(env)
        Execute('systemctl enable kibana')

    def configure(self, env):
        import params
        env.set_params(params)

        Logger.info("Configure Kibana for Metron")

        directories = [params.log_dir, params.pid_dir, params.conf_dir]
        Directory(
            directories,
            # recursive=True,
            mode=0755,
            owner=params.kibana_user,
            group=params.kibana_user)

        File(
            "{0}/kibana.yml".format(params.conf_dir),
            owner=params.kibana_user,
            content=InlineTemplate(params.kibana_yml_template))

    def stop(self, env):
        import params
        env.set_params(params)

        Logger.info("Stop Kibana Master")

        Execute("service kibana stop")

    def start(self, env):
        import params
        env.set_params(params)

        self.configure(env)

        Logger.info("Start the Master")

        Execute("service kibana start")

    def restart(self, env):
        import params
        env.set_params(params)

        self.configure(env)

        Logger.info("Restarting the Master")

        Execute("service kibana restart")

    def status(self, env):
        import params
        env.set_params(params)

        Logger.info("Status of the Master")

        Execute("service kibana status")


if __name__ == "__main__":
    Kibana().execute()
