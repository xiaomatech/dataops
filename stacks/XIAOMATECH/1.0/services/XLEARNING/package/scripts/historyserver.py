from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.libraries.functions.check_process_status import check_process_status

from xlearning import install_xlearning, config_xlearning


class xlearning(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_xlearning()

    def configure(self, env):
        import params
        env.set_params(params)
        config_xlearning()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat /var/run/xlearning_historyserver.pid` ')

    def start(self, env):
        import params
        env.set_params(params)
        install_xlearning()
        self.configure(env)
        Execute('source ' + params.conf_dir + '/xlearning-env.sh;' +
                params.install_dir + "/sbin/start-history-server.sh")
        Execute(
            " echo `jps -l|grep net.qihoo.xlearning.jobhistory.JobHistoryServer|awk '{print $1}'`  > /var/run/xlearning_historyserver.pid"
        )

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status('/var/run/xlearning_historyserver.pid')


if __name__ == "__main__":
    xlearning().execute()
