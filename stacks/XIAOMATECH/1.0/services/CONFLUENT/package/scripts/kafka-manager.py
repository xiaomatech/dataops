from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.check_process_status import check_process_status


class Manager(Script):
    pid_file = '/var/run/kafka-manager/kafka-manager.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Package(['kafka-manager'])

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/kafka-manager/application.conf',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_manager_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('rm -rf ' + self.pid_file)
        Execute("systemctl start kafka-manager")

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop kafka-manager")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Manager().execute()
