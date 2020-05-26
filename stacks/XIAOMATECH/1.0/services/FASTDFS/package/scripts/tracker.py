from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import Directory
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.packaging import Package


class Tracker(Script):
    pid_file = '/var/run/fdfs_tracker.pid'
    conf_file = '/etc/fdfs/tracker.conf'

    def install(self, env):
        self.install_packages(env)
        Package('libfdfsclient')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            self.conf_file,
            content=InlineTemplate(params.storage_content),
            mode=0755)

    def start(self, env):
        import params
        env.set_params(params)
        Execute('service fdfs_trackerd start')
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
    Tracker().execute()
