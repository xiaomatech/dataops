# encoding=utf8

from resource_management import *
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import InlineTemplate, Template, StaticFile
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format


class Tac(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)
        File(
            '/etc/tac_plus.conf',
            mode=0755,
            content=StaticFile('tac_plus.conf'))

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        Execute('systemctl stop tac_plus')

    def start(self, env):
        self.configure(env)
        Execute('systemctl start tac_plus')

    def status(self, env):
        Execute('systemctl status tac_plus')


if __name__ == "__main__":
    Tac().execute()
