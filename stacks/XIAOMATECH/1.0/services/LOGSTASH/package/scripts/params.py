#!/usr/bin/env python

from resource_management.libraries.functions import format
from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()

conf_dir = "/etc/logstash"
logstash_user = 'logstash'
logstash_group = 'logstash'
log_dir = config['configurations']['logstash-env']['logstash_log_dir']
pid_dir = '/var/run/logstash'
pid_file = format("{pid_dir}/logstash.pid")
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
patterns_dir = '/etc/logstash/patterns'

indexer_content = config['configurations']['logstash-env']['indexer_content']
jvm_content = config['configurations']['logstash-env']['jvm_content']
logstash_content = config['configurations']['logstash-env']['logstash_content']
init_content = config['configurations']['logstash-env']['init_content']
patterns_content = config['configurations']['logstash-env']['patterns_content']

cluster_zookeeper_quorum_hosts = default(
    '/clusterHostInfo/zookeeper_server_hosts', [])
from random import shuffle
shuffle(cluster_zookeeper_quorum_hosts)
zk_url = ':2181,'.join(cluster_zookeeper_quorum_hosts) + ':2181'

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_url = ''
if len(kafka_hosts) > 0:
    kafka_url = ':6667,'.join(kafka_hosts) + ':6667'

es_hosts = default('/clusterHostInfo/es_client_hosts', [])
from random import shuffle
shuffle(es_hosts)
es_host = es_hosts[0]
es_hosts_url = '"' + ':9200","'.join(es_hosts) + ':9200"'

kibana_hosts = default('/clusterHostInfo/kibana_hosts', [])
kibana_host = kibana_hosts[0]

import os
import multiprocessing
cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024**3))
men_mib = int(mem_bytes / (1024**2))
