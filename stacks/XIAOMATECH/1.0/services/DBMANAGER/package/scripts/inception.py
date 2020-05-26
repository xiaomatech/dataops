from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

config_file = '/etc/inception.cnf'


def conf_inception():
    import params
    File(
        config_file,
        content=InlineTemplate(params.inception_content),
        mode=0755,
        owner='mysql',
        group='mysql')


class Backup(Script):
    pid_file = '/var/run/inception.pid'

    def install(self, env):
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        conf_inception()

    def start(self, env):
        import params
        env.set_params(params)
        Execute('/usr/local/inception/bin/Inception --defaults-file=' +
                config_file)
        Execute("echo `ps aux|grep '" + config_file +
                "' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + self.pid_file + '`')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Backup().execute()
