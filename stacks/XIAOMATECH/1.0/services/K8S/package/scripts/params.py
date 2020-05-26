#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

config = Script.get_config()

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_content = config['configurations']['k8s-env']['install_content']

apiserver_vip = config['configurations']['k8s-env']['apiserver_vip']
apiserver_hosts = default('/clusterHostInfo/kube_apiserver_hosts', [])

kuber_apiserver = "http://" + apiserver_vip + ':8080'

etcd_data_dir = config['configurations']['k8s-env']['etcd_data_dir']
etcd_content = config['configurations']['k8s-env']['etcd_content']
etcd_conf_dir = '/etc/etcd'
etcd_hosts = default('/clusterHostInfo/kube_etcd_hosts', [])
etcd_event_hosts = default('/clusterHostInfo/kube_etcd_event_hosts', [])

etcd_endpoints = 'http://' + ':2379,http://'.join(etcd_hosts) + ':2379'
etcd_event_endpoints = 'http://' + ':2379,http://'.join(
    etcd_event_hosts) + ':2379'

etcd_hosts.sort()
etcd_event_hosts.sort()
etcd_name = 'k8s'
if hostname in etcd_event_hosts:
    etcd_hosts = etcd_event_hosts
    etcd_name = 'k8s_event'

initial_cluster_arr = []
for i, etcd_host in enumerate(etcd_hosts):
    initial_cluster_arr.append(etcd_name + str(i) + '=http://' + etcd_host +
                               ':2380')
initial_cluster = ','.join(initial_cluster_arr)

etcd_systemd_content = '''
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
[Service]
Type=notify
WorkingDirectory=''' + etcd_data_dir + '''
EnvironmentFile=-''' + etcd_conf_dir + '''/etcd.conf
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

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

cluster_cidr = config['configurations']['k8s-env']['cluster_cidr']
service_cidr = config['configurations']['k8s-env']['service_cidr']
node_port_range = config['configurations']['k8s-env']['node_port_range']
cluster_dns_svc_ip = config['configurations']['k8s-env']['cluster_dns_svc_ip']
cluster_dns_domain = config['configurations']['k8s-env']['cluster_dns_domain']

kube_apiserver_install_content = config['configurations']['k8s-env'][
    'apiserver_install_content']
kube_controller_manager_install_content = config['configurations']['k8s-env'][
    'controller_manager_install_content']
kube_scheduler_install_content = config['configurations']['k8s-env'][
    'scheduler_install_content']

node_install_content = config['configurations']['k8s-env'][
    'node_install_content']

ca_init_content = config['configurations']['k8s-env']['ca_init_content']
