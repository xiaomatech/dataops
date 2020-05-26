#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default
import os

config = Script.get_config()

prometheus_user = config['configurations']['prometheus-env']['prometheus_user']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

alertmanager_content = config['configurations']['prometheus-env'][
    'alertmanager_content']
prometheus_content = config['configurations']['prometheus-env'][
    'prometheus_content']
prometheus_rules_content = config['configurations']['prometheus-env'][
    'prometheus_rules_content']
alert_rules_content = config['configurations']['prometheus-env'][
    'alert_rules_content']

statsd_content = config['configurations']['prometheus-env']['statsd_content']
blackbox_content = config['configurations']['prometheus-env'][
    'blackbox_content']

conf_dir = '/etc/prometheus'

user_group = config['configurations']['cluster-env']['user_group']

exporter_lists = config['configurations']['prometheus-env'][
    'exporter_lists'].strip().split(',')

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

prometheus_alertmanager_hosts = default(
    '/clusterHostInfo/prometheus_alertmanager_hosts', [])
prometheus_pushgateway_hosts = default(
    '/clusterHostInfo/prometheus_pushgateway_hosts', [])
prometheus_pushgateway_addr = ''
if len(prometheus_pushgateway_hosts) > 0:
    prometheus_pushgateway_addr = prometheus_pushgateway_hosts[0] + ':9091'


def install_from_file(file_name):
    file_path = '/usr/sbin/' + file_name
    if not os.path.exists(file_path):
        Execute('wget ' + download_url_base + '/' + file_name + ' -O ' + file_path)
        Execute('chmod a+x ' + file_path)


alertmanager_data_dir = '/data1/prometheus/alertmanager'
prometheus_data_dir = '/data1/prometheus'

alertmanager_systemd = '''
[Unit]
Description=Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/alertmanager -config.file ''' + conf_dir + '''/alertmanager.yml -storage.path ''' + alertmanager_data_dir + '''  --data.retention 120h
ExecStop=/bin/kill -WINCH ${MAINPID}

[Install]
WantedBy=multi-user.target
'''

prometheus_systemd = '''
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/prometheus -config.file ''' + conf_dir + '''/prometheus.yml -storage.local.path ''' + prometheus_data_dir + '''
ExecStop=/bin/kill -WINCH ${MAINPID}

[Install]
WantedBy=multi-user.target
'''

node_exporter_systemd = '''
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/node_exporter --collector.systemd --collector.tcpstat --collector.processes --collector.ntp --collector.meminfo_numa --collector.interrupts
ExecStop=/bin/kill -WINCH $MAINPID

[Install]
WantedBy=multi-user.target
'''

graphite_systemd = '''
[Unit]
Description=Prometheus Graphite
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/graphite_exporter
ExecStop=/bin/kill -WINCH $MAINPID

[Install]
WantedBy=multi-user.target
'''

snmp_systemd = '''
[Unit]
Description=Prometheus SNMP
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/snmp_exporter --config.file="''' + conf_dir + '''/snmp.yml"
ExecStop=/bin/kill -WINCH $MAINPID

[Install]
WantedBy=multi-user.target
'''

blackbox_systemd = '''
[Unit]
Description=Prometheus BlackBox
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/blackbox_exporter --config.file="''' + conf_dir + '''/blackbox.yml"
ExecStop=/bin/kill -WINCH $MAINPID

[Install]
WantedBy=multi-user.target
'''

statsd_systemd = '''
[Unit]
Description=Prometheus Statsd exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=always
RestartSec=3
ExecStart=/usr/sbin/statsd_exporter --statsd.mapping-config ''' + conf_dir + '''/statsd.yml
ExecStop=/bin/kill -WINCH ${MAINPID}

[Install]
WantedBy=multi-user.target
'''

pushgateway_systemd = '''
[Unit]
Description=Prometheus Pushgateway
Documentation=https://github.com/prometheus/pushgateway
After=network.target

[Service]
EnvironmentFile=-''' + conf_dir + '''/pushgateway
User=prometheus
Group=prometheus
Type=simple
Restart=always
ExecStart=/usr/sbin/pushgateway
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
'''
