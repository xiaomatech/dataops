from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

systemd = '''
[Unit]
Description=RESTful Avro schema registry for Apache Kafka
Documentation=http://docs.confluent.io/
After=network.target confluent-kafka.target

[Service]
EnvironmentFile=-/etc/sysconfig/kafka-schema-registry
Type=simple
User=cp-schema-registry
Group=confluent
ExecStart=/usr/bin/schema-registry-start /etc/schema-registry/schema-registry.properties
ExecStop=/usr/bin/schema-registry-stop
TimeoutStopSec=180
Restart=no
LimitNOFILE = 1048576
SuccessExitStatus=143
[Install]
WantedBy=multi-user.target
'''


class SchemaRegistry(Script):
    pid_file = '/var/run/kafka-schema-registry.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute(
            'rm -rf /usr/lib/systemd/system/confluent-schema-registry.service')
        File(
            '/usr/lib/systemd/system/confluent-schema-registry.service',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(systemd))
        Execute("systemctl daemon-reload")

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/schema-registry/schema-registry.properties',
            owner='cp-schema-registry',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.schema_registry_content))
        File(
            '/etc/sysconfig/kafka-schema-registry',
            owner='cp-schema-registry',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_registry_env_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start confluent-schema-registry")
        Execute(
            "echo `ps aux|grep '/etc/schema-registry/schema-registry.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-schema-registry")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/schema-registry/schema-registry.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    SchemaRegistry().execute()
