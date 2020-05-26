from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Router(Script):
    def install(self, env):
        self.install_packages(env)
        Execute('yum install -y percona-mysql-shell percona-mysql-router')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/mysqlrouter/mysqlrouter.conf',
            content=InlineTemplate(params.router_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop mysqlrouter')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl start mysqlrouter')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status mysqlrouter')


if __name__ == "__main__":
    Router().execute()
