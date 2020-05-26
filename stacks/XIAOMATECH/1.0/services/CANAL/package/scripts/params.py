#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/canal'
download_url = config['configurations']['canal-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

canal_user = config['configurations']['canal-env']['canal_user']
user_group = config['configurations']['cluster-env']['user_group']

log_dir = config['configurations']['canal-env']['canal_log_dir']
canal_pid_file = install_dir + '/bin/canal.pid'

canal_properties_content = config['configurations']['canal-env'][
    'canal_properties_content']
instance_content = config['configurations']['canal-env']['instance_content']
kafka_content = config['configurations']['canal-env']['kafka_content']
instance_name = 'default'

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_dir = '/etc/canal'

canal_kafka_hosts = default("/clusterHostInfo/canal_kafka_hosts", [])

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_broker_url = ''
if len(kafka_hosts) > 0:
    kafka_broker_url = ':6667,'.join(kafka_hosts) + ':6667'

zookeeper_hosts = default('/clusterHostInfo/zookeeper_server_hosts', [])
zk_url = ':2181,'.join(zookeeper_hosts) + ':2181'