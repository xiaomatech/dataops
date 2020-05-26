from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Directory, Execute, File, Link
from master import install_alluxio, config_alluxio
from resource_management.libraries.functions.check_process_status import check_process_status


class Slave(Script):
    def install(self, env):
        import params

        self.install_packages(env)
        env.set_params(params)
        install_alluxio()

    def configure(self, env):
        import params
        env.set_params(params)
        config_alluxio()

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        #Mount ramfs
        Execute(params.start_script + ' worker ' + ' Mount')

        cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep AlluxioWorker | awk '{print $1}'`> " + params.pid_dir + "/AlluxioWorker.pid"
        Execute(cmd)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.stop_script + ' worker')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_dir + "/AlluxioWorker.pid")


if __name__ == "__main__":
    Slave().execute()
