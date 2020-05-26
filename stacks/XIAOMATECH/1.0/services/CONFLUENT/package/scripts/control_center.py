from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class ControlCenter(Script):
    pid_file = '/var/run/kafka-control_center.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Package(['confluent-control-center'])

    def configure(self, env):
        import params
        env.set_params(params)
        Directory([params.control_center_dir],
                  owner='cp-kafka',
                  group='confluent',
                  mode=0775,
                  create_parents=True)
        File(
            '/etc/confluent-control-center/control-center-production.properties',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.control_center_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        Execute("systemctl start confluent-control-center")
        Execute(
            "echo `ps aux|grep '/etc/confluent-control-center/control-center-production.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-control-center")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/confluent-control-center/control-center-production.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    ControlCenter().execute()
