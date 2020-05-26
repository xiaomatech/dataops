#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

config = Script.get_config()

etcd_user = config['configurations']['etcd-env']['etcd_user']
data_dir = config['configurations']['etcd-env']['data_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['etcd-env']['conf_content']
conf_dir = '/etc/etcd'

etcd_hosts = default('/clusterHostInfo/etcd_hosts', [])

etcd_hosts.sort()
initial_cluster_arr = []
for i, etcd_host in enumerate(etcd_hosts):
    initial_cluster_arr.append('default' + str(i) + '=http://' + etcd_host +
                               ':2380')
initial_cluster = ','.join(initial_cluster_arr)

user_group = config['configurations']['cluster-env']['user_group']

systemd_content = '''
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
[Service]
Type=notify
WorkingDirectory=''' + data_dir + '''
EnvironmentFile=-''' + conf_dir + '''/etcd.conf
User=etcd
ExecStart=/usr/bin/etcd \
    --name ${ETCD_NAME} \
    --data-dir ${ETCD_DATA_DIR} \
    --initial-advertise-peer-urls ${ETCD_INITIAL_ADVERTISE_PEER_URLS} \
    --listen-peer-urls ${ETCD_LISTEN_PEER_URLS} \
    --listen-client-urls ${ETCD_LISTEN_CLIENT_URLS},http://127.0.0.1:2379 \
    --advertise-client-urls ${ETCD_ADVERTISE_CLIENT_URLS} \
    --initial-cluster-token ${ETCD_INITIAL_CLUSTER_TOKEN} \
    --initial-cluster ${ETCD_INITIAL_CLUSTER} \
    --initial-cluster-state ${ETCD_INITIAL_CLUSTER_STATE}
Restart=on-failure
RestartSec=5
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
'''
