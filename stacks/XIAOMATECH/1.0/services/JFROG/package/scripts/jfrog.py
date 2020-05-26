from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Artifactory(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/jfrog/artifactory/artifactory.system.properties',
            content=InlineTemplate(params.conf_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop artifactory')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start artifactory')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status artifactory')


if __name__ == "__main__":
    Artifactory().execute()
