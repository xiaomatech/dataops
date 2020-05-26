# encoding=utf8

from resource_management import *
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import InlineTemplate, Template, StaticFile
from resource_management.libraries.script.script import Script


class Radius(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)
        File(
            '/etc/raddb/sites-enabled/default',
            mode=0755,
            content=StaticFile('default'))
        File(
            '/etc/raddb/sites-enabled/inner-tunnel',
            mode=0755,
            content=StaticFile('inner-tunnel'))
        Execute(
            'ln -s /etc/raddb/mods-available/ldap /etc/raddb/mods-enabled/')
        Execute('systemctl enable radiusd')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("/etc/raddb/mods-enabled/ldap"),
            content=InlineTemplate('radius'),
            owner='root',
            group='root',
            mode=0644)

    def stop(self, env):
        Execute('systemctl stop radiusd')

    def start(self, env):
        self.configure(env)
        Execute('systemctl start radiusd')

    def status(self, env):
        Execute('systemctl status radiusd')


if __name__ == "__main__":
    Radius().execute()
