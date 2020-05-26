from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class Filebeat(Script):
    pid_file = '/var/run/filebeat.pid'

    def install(self, env):
        import params
        env.set_params(params)
        Execute('yum install -y filebeat')
        self.configure(env)
        Execute(
            'filebeat setup --dashboards; filebeat setup --machine-learning;filebeat setup --template'
        )
        Execute('systemctl enable filebeat')
        Execute("filebeat enroll http://" + params.kibana_host + ':5601')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/filebeat/filebeat.yml',
            content=InlineTemplate(params.conf_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop filebeat")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start filebeat")
        Execute(
            "echo `ps aux|grep '/etc/filebeat' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Filebeat().execute()
