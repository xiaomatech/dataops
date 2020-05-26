from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.libraries.script.script import Script

from angel import angel, install_angel


class Angel(Script):
    def configure(self, env):
        import params
        env.set_params(params)
        angel()

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def install(self, env):
        install_angel()
        self.configure(env)


if __name__ == "__main__":
    Angel().execute()
