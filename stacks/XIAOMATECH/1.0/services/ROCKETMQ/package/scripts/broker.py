from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.libraries.functions.check_process_status import check_process_status
from namesrv import install_rocketmq, config_rocketmq


class Rocketmq(Script):
    pid_file = '/var/run/mqbroker.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_rocketmq()

    def configure(self, env):
        import params
        env.set_params(params)
        config_rocketmq()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + '/bin/mqshutdown broker')

    def start(self, env):
        import params
        env.set_params(params)
        install_rocketmq()
        self.configure(env)
        Execute(
            'nohup ' + params.install_dir + '/bin/runbroker.sh org.apache.rocketmq.broker.BrokerStartup &')
        Execute(
            "echo `ps ax | grep -i 'org.apache.rocketmq.broker.BrokerStartup' |grep java | grep -v grep | awk '{print $1}'` > " + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Rocketmq().execute()
