#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default
from random import shuffle

config = Script.get_config()
stack_root = Script.get_stack_root()

rocketmq_user = config['configurations']['rocketmq-env']['rocketmq_user']
user_group = config['configurations']['cluster-env']['user_group']
log_dir = config['configurations']['rocketmq-env']['log_dir']
pid_dir = config['configurations']['rocketmq-env']['pid_dir']
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

broker_id = 0
broker_role = 'ASYNC_MASTER'
store_commitlog = '/data1/rocketmq/commitlog'
store_queue = '/data1/rocketmq/consumequeue'

install_dir = stack_root + '/rocketmq'
download_url = config['configurations']['rocketmq-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '').replace('.tar.bz2', '')
conf_dir = '/etc/rocketmq'

broker_content = config['configurations']['rocketmq-env']['broker_content']
logback_broker_content = config['configurations']['rocketmq-env']['logback_broker_content']
logback_namesrv_content = config['configurations']['rocketmq-env']['logback_namesrv_content']
logback_tools_content = config['configurations']['rocketmq-env']['logback_tools_content']
acl_content = config['configurations']['rocketmq-env']['acl_content']

namesrv_hosts = default("/clusterHostInfo/rocketmq_namesrv_hosts", [])
shuffle(namesrv_hosts)
namesrv_addr = ''
if len(namesrv_hosts) > 0:
    namesrv_host = namesrv_hosts.pop()
    namesrv_addr = namesrv_host + ':9876'
