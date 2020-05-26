from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from dbus import install_dbus


class Hearbeat(Script):
    pid_file = '/var/run/dbus_hearbeat.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_dbus()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/application.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.dbus_user,
            group=params.dbus_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + params.pid_file + '`')

    def start(self, env):
        import params
        env.set_params(params)
        install_dbus()
        self.configure(env)
        Execute('')
        Execute(
            "echo `ps aux|grep 'edp.rider.RiderStarter' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(params.pid_file):
            Execute(
                "echo `ps aux|grep 'edp.rider.RiderStarter' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    Hearbeat().execute()
