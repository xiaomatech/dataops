from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Proxy(Script):
    def install(self, env):
        self.install_packages(env)
        Execute('yum install -y proxysql')

    def configure(self, env):
        import params
        env.set_params(params)
        Directory(['/data1/proxysql'],
                  owner='proxysql',
                  group='proxysql',
                  mode=0755,
                  create_parents=True)

        File(
            '/etc/proxysql-admin.cnf',
            content=InlineTemplate(params.proxy_admin_content),
            mode=0755)
        File(
            '/etc/proxysql.cnf',
            content=InlineTemplate(params.proxy_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('service proxysql stop')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('service proxysql start')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('service proxysql status')


if __name__ == "__main__":
    Proxy().execute()
