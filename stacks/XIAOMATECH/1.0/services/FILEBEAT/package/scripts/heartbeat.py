from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class Heartbeat(Script):
    pid_file = '/var/run/heartbeat.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        self.configure(env)
        Execute(
            'heartbeat setup --dashboards; heartbeat setup --machine-learning;heartbeat setup --template'
        )
        Execute('systemctl enable heartbeat-elastic')
        Execute("heartbeat enroll http://" + params.kibana_host + ':5601')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/heartbeat/heartbeat.yml',
            content=InlineTemplate(params.heartbeat_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop heartbeat-elastic")
        # Execute('kill -9 `cat ' + self.pid_file + '`')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start heartbeat-elastic")
        Execute(
            "echo `ps aux|grep '/etc/heartbeat' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Heartbeat().execute()
