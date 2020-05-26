from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class Mqtt(Script):
    pid_file = '/var/run/kafka-mqtt.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Package(['confluent-kafka-mqtt'])

        systemd_content = '''
[Unit]
Description=A MQTT proxy for Apache Kafka
Documentation=http://docs.confluent.io/
After=network.target confluent-kafka.target

[Service]
Type=simple
User=cp-kafka-rest
Group=confluent
Environment="LOG_DIR=/var/log/confluent/kafka-mqtt"
ExecStart=/usr/bin/kafka-mqtt-start /etc/confluent-kafka-mqtt/kafka-mqtt-production.properties
TimeoutStopSec=180
Restart=no

[Install]
WantedBy=multi-user.target
        '''
        File(
            '/usr/lib/systemd/system/confluent-kafka-mqtt.service',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(systemd_content))
        Execute('systemctl enable confluent-kafka-mqtt')

    def configure(self, env):
        import params
        env.set_params(params)
        Directory([
            params.control_center_dir, params.kafka_log_dir,
            '/etc/confluent-kafka-mqtt'
        ],
                  owner=params.kafka_user,
                  group=params.user_group,
                  mode=0775,
                  create_parents=True)
        File(
            '/etc/confluent-kafka-mqtt/kafka-mqtt-production.properties',
            owner=params.kafka_user,
            group=params.user_group,
            mode=0644,
            content=InlineTemplate(params.mqtt_proxy_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start confluent-kafka-mqtt")
        Execute(
            "echo `ps aux|grep '/etc/confluent-kafka-mqtt/kafka-mqtt-production.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-kafka-mqtt")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/confluent-kafka-mqtt/kafka-mqtt-production.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Mqtt().execute()
