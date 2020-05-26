from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.check_process_status import check_process_status

import os
download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def install_kafka_share_lib():
    share_dir = '/usr/share/java/kafka/'
    Directory(
        share_dir,
        owner='cp-kafka',
        group='confluent',
        create_parents=True,
        mode=0755)

    share_jar_files_conf = default("/configurations/confluent-env/share_jars", '').strip()
    if share_jar_files_conf != '':
        share_jar_files = share_jar_files_conf.split(',')
        for jar_file in share_jar_files:
            jar_file_path = share_dir + jar_file.strip()
            if not os.path.exists(jar_file_path):
                Execute('wget ' + download_url_base + '/share/kafka/' + jar_file + ' -O ' + jar_file_path,
                        user='cp-kafka')


systemd = '''
[Unit]
Description=Apache Kafka - broker
Documentation=http://docs.confluent.io/
After=network.target confluent-zookeeper.target

[Service]
EnvironmentFile=-/etc/sysconfig/kafka
Type=simple
User=cp-kafka
Group=confluent
ExecStart=/usr/bin/kafka-server-start /etc/kafka/server.properties
ExecStop=/usr/bin/kafka-server-stop
TimeoutStopSec=180
Restart=on-failure
LimitNOFILE=1048576
SuccessExitStatus=143
[Install]
WantedBy=multi-user.target
'''

log4j_content = '''
kafka.logs.dir=logs

log4j.rootLogger=INFO, stdout

log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n

log4j.appender.kafkaAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.kafkaAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.kafkaAppender.File=${kafka.logs.dir}/server.log
log4j.appender.kafkaAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.kafkaAppender.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n
log4j.appender.kafkaAppender.MaxFileSize = 256MB
log4j.appender.kafkaAppender.MaxBackupIndex = 10

log4j.appender.stateChangeAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.stateChangeAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.stateChangeAppender.File=${kafka.logs.dir}/state-change.log
log4j.appender.stateChangeAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.stateChangeAppender.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n

log4j.appender.requestAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.requestAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.requestAppender.File=${kafka.logs.dir}/kafka-request.log
log4j.appender.requestAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.requestAppender.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n

log4j.appender.cleanerAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.cleanerAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.cleanerAppender.File=${kafka.logs.dir}/log-cleaner.log
log4j.appender.cleanerAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.cleanerAppender.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n

log4j.appender.controllerAppender=org.apache.log4j.DailyRollingFileAppender
log4j.appender.controllerAppender.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.controllerAppender.File=${kafka.logs.dir}/controller.log
log4j.appender.controllerAppender.layout=org.apache.log4j.PatternLayout
log4j.appender.controllerAppender.layout.ConversionPattern=[%d{ISO8601}] %p %m (%c)%n
log4j.appender.controllerAppender.MaxFileSize = 256MB
log4j.appender.controllerAppender.MaxBackupIndex = 10

# Turn on all our debugging info
#log4j.logger.kafka.producer.async.DefaultEventHandler=DEBUG, kafkaAppender
#log4j.logger.kafka.client.ClientUtils=DEBUG, kafkaAppender
#log4j.logger.kafka.perf=DEBUG, kafkaAppender
#log4j.logger.kafka.perf.ProducerPerformance$ProducerThread=DEBUG, kafkaAppender
#log4j.logger.org.I0Itec.zkclient.ZkClient=DEBUG
log4j.logger.kafka=INFO, kafkaAppender
log4j.logger.kafka.network.RequestChannel$=WARN, requestAppender
log4j.additivity.kafka.network.RequestChannel$=false

#log4j.logger.kafka.network.Processor=TRACE, requestAppender
#log4j.logger.kafka.server.KafkaApis=TRACE, requestAppender
#log4j.additivity.kafka.server.KafkaApis=false
log4j.logger.kafka.request.logger=WARN, requestAppender
log4j.additivity.kafka.request.logger=false

log4j.logger.kafka.controller=TRACE, controllerAppender
log4j.additivity.kafka.controller=false

log4j.logger.kafka.log.LogCleaner=INFO, cleanerAppender
log4j.additivity.kafka.log.LogCleaner=false

log4j.logger.state.change.logger=TRACE, stateChangeAppender
log4j.additivity.state.change.logger=false

'''


class Kafka(Script):
    pid_file = '/var/run/kafka.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_kafka_share_lib()

        Execute('rm -rf /usr/lib/systemd/system/confluent-kafka.service')
        File(
            '/usr/lib/systemd/system/confluent-kafka.service',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(systemd))
        Execute("systemctl daemon-reload")

    def configure(self, env):
        import params
        env.set_params(params)
        Directory(
            [params.log_dirs_list, '/etc/kafka', '/var/log/kafka', '/var/log/confluent/kafka'],
            owner='cp-kafka',
            group='confluent',
            mode=0775,
            create_parents=True)
        Directory([params.control_center_dir, params.kafka_log_dir],
                  owner='cp-kafka',
                  group='confluent',
                  mode=0777,
                  create_parents=True)
        File(
            '/etc/kafka/server.properties',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_content))
        File(
            '/etc/kafka/log4j.properties',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=log4j_content)
        File(
            '/etc/sysconfig/kafka',
            owner='cp-kafka',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_env_content))
        generate_logfeeder_input_config(
            'kafka',
            Template("input.config-kafka.json.j2", extra_imports=[default]))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("systemctl start confluent-kafka")
        Execute(
            "echo `ps aux|grep '/etc/kafka/server.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-kafka")
        Execute('rm -rf ' + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/kafka/server.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Kafka().execute()
