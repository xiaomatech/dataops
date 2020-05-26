from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

systemd = '''
[Unit]
Description=A REST proxy for Apache Kafka
Documentation=http://docs.confluent.io/
After=network.target confluent-kafka.target

[Service]
EnvironmentFile=-/etc/sysconfig/kafka-rest
Type=simple
User=cp-kafka-rest
Group=confluent
ExecStart=/usr/bin/kafka-rest-start /etc/kafka-rest/kafka-rest.properties
TimeoutStopSec=180
LimitNOFILE = 1048576
Restart=no

[Install]
WantedBy=multi-user.target
'''


class Rest(Script):
    pid_file = '/var/run/kafka-rest.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('rm -rf /usr/lib/systemd/system/confluent-kafka-rest.service')
        File(
            '/usr/lib/systemd/system/confluent-kafka-rest.service',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(systemd))
        Execute("systemctl daemon-reload")

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/kafka-rest/kafka-rest.properties',
            owner=params.kafka_user,
            group=params.user_group,
            mode=0644,
            content=InlineTemplate(params.kafka_rest_content))
        File(
            '/etc/sysconfig/kafka-rest',
            owner='cp-kafka-rest',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_rest_env_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start confluent-kafka-rest")
        Execute(
            "echo `ps aux|grep '/etc/kafka-rest/kafka-rest.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-kafka-rest")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/kafka-rest/kafka-rest.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Rest().execute()
