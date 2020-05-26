from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class Metricbeat(Script):
    pid_file = '/var/run/metricbeat.pid'

    def install(self, env):
        import params
        env.set_params(params)
        Execute('yum install -y metricbeat')
        self.configure(env)

        Execute(
            'metricbeat setup --dashboards; metricbeat setup --machine-learning; metricbeat setup --template'
        )
        Execute('systemctl enable metricbeat')
        Execute("metricbeat enroll http://" + params.kibana_host + ':5601')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/metricbeat/metricbeat.yml',
            content=InlineTemplate(params.metricbeat_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop metricbeat")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start metricbeat")
        Execute(
            "echo `ps aux|grep '/etc/metricbeat' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Metricbeat().execute()
