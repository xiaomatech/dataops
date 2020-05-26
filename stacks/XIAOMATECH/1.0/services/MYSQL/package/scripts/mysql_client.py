from resource_management.libraries.script.script import Script
from resource_management.core.resources.packaging import Package


class Client(Script):
    def install(self, env):
        packages = ['percona-server-client']
        Package(packages)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)

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
