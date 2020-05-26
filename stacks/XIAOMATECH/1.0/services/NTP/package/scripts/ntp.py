from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class Master(Script):
    def install(self, env):
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/ntp.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop ntpd')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl start ntpd')

    def status(self, env):
        check_process_status('/var/run/ntpd.pid')


if __name__ == "__main__":
    Master().execute()
