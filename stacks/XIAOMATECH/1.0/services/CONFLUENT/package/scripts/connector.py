from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

connect_log4j = '''
log4j.rootLogger=INFO, stdout


log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=[%d] %p %m (%c:%L)%n

log4j.logger.org.apache.zookeeper=ERROR
log4j.logger.org.I0Itec.zkclient=ERROR
log4j.logger.org.reflections=ERROR
'''

'''

https://downloads.datastax.com/kafka/kafka-connect-dse.tar.gz

confluent-hub install confluentinc/kafka-connect-hdfs3-source:latest
confluent-hub install confluentinc/kafka-connect-hdfs3:latest
confluent-hub install confluentinc/kafka-connect-hbase:latest
confluent-hub install mongodb/kafka-connect-mongodb:latest
confluent-hub install confluentinc/kafka-connect-elasticsearch:latest
confluent-hub install confluentinc/kafka-connect-hdfs:latest
confluent-hub install confluentinc/kafka-connect-jms-sink:latest
confluent-hub install confluentinc/kafka-connect-jdbc:latest
confluent-hub install confluentinc/kafka-connect-mqtt:latest
confluent-hub install confluentinc/kafka-connect-s3:latest
confluent-hub install confluentinc/kafka-connect-rabbitmq:latest
confluent-hub install jcustenborder/kafka-connect-redis:latest
confluent-hub install jcustenborder/kafka-connect-spooldir:latest
confluent-hub install debezium/debezium-connector-mysql:latest
confluent-hub install debezium/debezium-connector-mongodb::latest
confluent-hub install debezium/debezium-connector-sqlserver::latest
confluent-hub install debezium/debezium-connector-postgresql::latest

'''

class Connector(Script):
    pid_file = '/var/run/kafka-connector.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        plugin_download_urls = params.kafka_connect_plugin_download_url.strip().split(',')
        Execute('mkdir -p /usr/share/confluent-hub-components')
        for plugin_url in plugin_download_urls:
            Execute('wget ' + plugin_url + ' -O  /tmp/plugin.tar.gz')
            Execute(
                'tar -zxvf /tmp/plugin.tar.gz -C /usr/share/confluent-hub-components'
            )

    def configure(self, env):
        import params
        env.set_params(params)
        Execute('rm -rf /etc/kafka-connect-*/*')
        File(
            '/etc/kafka/connect-log4j.properties',
            owner='cp-kafka-connect',
            group='confluent',
            mode=0644,
            content=connect_log4j)
        File(
            '/etc/kafka/connect-distributed.properties',
            owner='cp-kafka-connect',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.kafka_connect_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        Execute("systemctl start confluent-kafka-connect")
        Execute(
            "echo `ps aux|grep '/etc/kafka/connect-distributed.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-kafka-connect")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/kafka/connect-distributed.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)

    def deployconnector(self):
        import params
        File(
            '/tmp/connector.json', mode=0755, content=params.kafka_connector_content)
        Execute(
            "curl -XPOST -H 'Content-Type: application/json' 'http://" + params.kafka_connector_host + ":8083/connectors' -d @/tmp/connector.json")


if __name__ == "__main__":
    Connector().execute()
