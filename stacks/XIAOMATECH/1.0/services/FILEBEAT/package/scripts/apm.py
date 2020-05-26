from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class APM(Script):
    pid_file = '/var/run/apm-server.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        self.configure(env)
        Execute('apm-server setup --dashboards;apm-server setup --template')
        Execute('systemctl enable apm-server')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/apm-server/apm-server.yml',
            content=InlineTemplate(params.apm_server_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop apm-server")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start apm-server")
        Execute(
            "echo `ps aux|grep '/etc/apm-server' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    APM().execute()
