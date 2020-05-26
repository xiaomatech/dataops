from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import Directory
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Mgr(Script):
    pid_file = ''
    conf_file = ''

    def install(self, env):
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/soar.yaml',
            content=InlineTemplate(params.soar_content),
            mode=0755,
            owner='mysql',
            group='mysql')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('service archery start')
        Execute("echo `ps aux|grep '" + self.conf_file +
                "' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + self.pid_file + ' ` ')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Mgr().execute()
