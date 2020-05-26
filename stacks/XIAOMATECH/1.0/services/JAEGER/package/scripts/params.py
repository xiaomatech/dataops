#!/usr/bin/env python

from resource_management.libraries.script import Script

config = Script.get_config()

jaeger_user = config['configurations']['jaeger-env']['jaeger_user']
data_dir = config['configurations']['jaeger-env']['data_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['jaeger-env']['conf_content']
conf_dir = '/etc/jaeger'

user_group = config['configurations']['cluster-env']['user_group']

collector_hosts = config['clusterHostInfo']['jaeger_collector_hosts']
collector_hosts_arr = []
for i, host in enumerate(collector_hosts):
    collector_hosts_arr.append(host + ':14267')
collector_host_url = ','.join(collector_hosts_arr)

es_hosts = config['clusterHostInfo']['es_client_hosts']
es_hosts_arr = []
for i, host in enumerate(es_hosts):
    es_hosts_arr.append('http://' + host + ':9200')
es_url = ','.join(es_hosts_arr)
