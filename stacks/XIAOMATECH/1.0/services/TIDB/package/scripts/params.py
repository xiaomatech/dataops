#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default
import os

config = Script.get_config()

tidb_user = config['configurations']['tidb-env']['tidb_user']
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
user_group = config['configurations']['cluster-env']['user_group']
download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

tikv_content = config['configurations']['tidb-env']['tikv_content']
tidb_content = config['configurations']['tidb-env']['tidb_content']
pd_content = config['configurations']['tidb-env']['pd_content']
tikv_import_content = config['configurations']['tidb-env'][
    'tikv_import_content']
syncer_content = config['configurations']['tidb-env']['syncer_content']
drainer_content = config['configurations']['tidb-env']['drainer_content']
pump_content = config['configurations']['tidb-env']['pump_content']

conf_dir = '/etc/tidb'
log_dir = '/var/log/tidb'
data_dir = '/data1/tidb'
raftdb_dir = '/data1/tidb/raft'
wal_dir = '/data2/tidb/wal'

prometheus_pushgateway_hosts = default(
    '/clusterHostInfo/prometheus_pushgateway_hosts', [])
prometheus_pushgateway_addr = ''
if len(prometheus_pushgateway_hosts) > 0:
    prometheus_pushgateway_addr = prometheus_pushgateway_hosts[0] + ':9091'

jaeger_agent_hosts = default('/clusterHostInfo/jaeger_agent_hosts', [])
jaeger_agent_url = ''
jaeger_agent = ''
if len(jaeger_agent_hosts) > 0:
    jaeger_agent_url = 'thrift://' + jaeger_agent_hosts[0] + ':6831'
    jaeger_agent = jaeger_agent_hosts[0] + ':6831'

pd_server_hosts = default('/clusterHostInfo/tidb_pd_hosts', [])
pd_server_urls = []
for id, host in enumerate(pd_server_hosts):
    pd_server_hosts[id] = '"' + host + ':2379"'
    pd_server_urls[id] = 'http://' + host + ':2379'

pd_endpoints = ','.join(pd_server_hosts)
pd_url = ','.join(pd_server_urls)

zk_hosts = []
zookeeper_server_hosts = default("/clusterHostInfo/zookeeper_server_hosts", [])
from random import shuffle
shuffle(zookeeper_server_hosts)
for id, host in enumerate(zookeeper_server_hosts):
    zk_hosts[id] = host + ':2181'
zk_url = ','.join(zk_hosts)


def install_from_file(file_name):
    file_path = '/usr/sbin/' + file_name
    if not os.path.exists(file_path):
        Execute('wget ' + download_url_base + '/tidb/' + file_name + ' -O ' +
                file_path)
        Execute('chmod a+x ' + file_path)


tikv_systemd = '''
[Unit]
Description=TiKV is a distributed transactional key value database powered by Rust and Raft
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/tikv-server --config /etc/tidb/tikv.conf
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

pd_systemd = '''
[Unit]
Description=TiDB PD
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/pd-server --config /etc/tidb/pd.conf
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

tidb_systemd = '''
[Unit]
Description=TiDB 
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/tidb-server --config /etc/tidb/tidb.conf
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

syncer_systemd = '''
[Unit]
Description=TiDB Syncer
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/syncer --config /etc/tidb/syncer.conf -enable-gtid -auto-fix-gtid
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

pump_systemd = '''
[Unit]
Description=TiDB Syncer
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/pump --config /etc/tidb/pump.conf
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''

drainer_systemd = '''
[Unit]
Description=TiDB Syncer
After=network-online.target
Wants=network-online.target

[Service]
User=tikv
Group=tikv
ExecStart=/usr/sbin/drainer --config /etc/tidb/drainer.conf
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
'''
