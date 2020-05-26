from resource_management import *
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script
from client import install_flink, config_flink
from resource_management.libraries.functions.check_process_status import check_process_status


class Jobmanager(Script):
    pid_file = '/var/run/flink-jobmanager.pid'

    def install(self, env):
        install_flink()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        config_flink()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.bin_dir + '/jobmanager.sh stop')

    def start(self, env):
        import params
        install_flink()
        self.configure(env)
        Execute(params.bin_dir + '/jobmanager.sh start')

        Execute(
            "echo `ps aux|grep 'org.apache.flink.runtime.entrypoint' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Jobmanager().execute()
