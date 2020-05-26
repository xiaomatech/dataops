from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.packaging import Package


class Client(Script):
    def install(self, env):
        self.install_packages(env)
        Package('libfdfsclient')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/fdfs/client.conf',
            content=InlineTemplate(params.client_content),
            mode=0755)

    def start(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)

    def status(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    Client().execute()
