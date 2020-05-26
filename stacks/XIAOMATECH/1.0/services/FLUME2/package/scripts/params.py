"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import get_kinit_path
from ambari_commons.ambari_metrics_helper import select_metric_collector_hosts_from_hostnames
from resource_management.libraries.functions.constants import Direction

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/flume'
download_url = config['configurations']['flume-env']['download_url']
filename = download_url.split('/')[-1]

version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

flume_conf_dir = default("/configurations/flume-env/flume_conf_dir",
                         '/etc/flume')

flume_user = config['configurations']['flume-env']['flume_user']

flume_group = user_group = config['configurations']['cluster-env']['user_group']
proxyuser_group = config['configurations']['hadoop-env']['proxyuser_group']

security_enabled = config['configurations']['cluster-env']['security_enabled']

flume_jaas_conf_template = default("/configurations/flume-env/jaas_content",
                                   None)

if security_enabled:
    _hostname_lowercase = config['agentLevelParams']['hostname'].lower()
    flume_jaas_princ = config['configurations']['flume-env'][
        'flume_principal_name'].replace('_HOST', _hostname_lowercase)
    flume_keytab_path = config['configurations']['flume-env'][
        'flume_keytab_path']

# hadoop default parameters
flume_bin = install_dir + '/bin/flume-ng'
flume_hive_home = stack_root + '/hive'
flume_hcat_home = stack_root + '/hive/hcatalog/share/webhcat/svr/lib/'

java_home = config['ambariLevelParams']['java_home']
flume_log_dir = config['configurations']['flume-env']['flume_log_dir']
flume_run_dir = config['configurations']['flume-env']['flume_run_dir']
flume_pid_file = flume_run_dir + '/flume.pid'

flume_conf_content = config['configurations']['flume-env']['conf_content']

flume_env_sh_template = config['configurations']['flume-env']['content']

hostname = config['agentLevelParams']['hostname']

cluster_name = config["clusterName"]

if 'cluster-env' in config['configurations'] and \
        'metrics_collector_external_hosts' in config['configurations']['cluster-env']:
    ams_collector_hosts = config['configurations']['cluster-env'][
        'metrics_collector_external_hosts']
else:
    ams_collector_hosts = ",".join(
        default("/clusterHostInfo/metrics_collector_hosts", []))

has_metric_collector = not len(ams_collector_hosts) == 0
metric_collector_port = None
if has_metric_collector:
    metric_collector_host = select_metric_collector_hosts_from_hostnames(
        ams_collector_hosts)
    if 'cluster-env' in config['configurations'] and \
            'metrics_collector_external_port' in config['configurations']['cluster-env']:
        metric_collector_port = config['configurations']['cluster-env'][
            'metrics_collector_external_port']
    else:
        metric_collector_web_address = default(
            "/configurations/ams-site/timeline.metrics.service.webapp.address",
            "0.0.0.0:6188")
        if metric_collector_web_address.find(':') != -1:
            metric_collector_port = metric_collector_web_address.split(':')[1]
        else:
            metric_collector_port = '6188'
    if default("/configurations/ams-site/timeline.metrics.service.http.policy",
               "HTTP_ONLY") == "HTTPS_ONLY":
        metric_collector_protocol = 'https'
    else:
        metric_collector_protocol = 'http'
    metric_truststore_path = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.location", "")
    metric_truststore_type = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.type", "")
    metric_truststore_password = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.password", "")
    pass
metrics_report_interval = default(
    "/configurations/ams-site/timeline.metrics.sink.report.interval", 60)
metrics_collection_period = default(
    "/configurations/ams-site/timeline.metrics.sink.collection.period", 10)

host_in_memory_aggregation = default(
    "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation",
    True)
host_in_memory_aggregation_port = default(
    "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation.port",
    61888)

# Cluster Zookeeper quorum
zookeeper_quorum = None
if not len(default("/clusterHostInfo/zookeeper_server_hosts", [])) == 0:
    if 'zoo.cfg' in config['configurations'] and 'clientPort' in config[
        'configurations']['zoo.cfg']:
        zookeeper_clientPort = config['configurations']['zoo.cfg'][
            'clientPort']
    else:
        zookeeper_clientPort = '2181'
    zookeeper_quorum = (':' + zookeeper_clientPort + ',').join(
        config['clusterHostInfo']['zookeeper_server_hosts'])
    # last port config
    zookeeper_quorum += ':' + zookeeper_clientPort

# smokeuser
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']

data_dirs = []
with open('/proc/mounts', 'r') as f:
    data_dirs = [
        line.split()[1] + '/flume/data' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

datadirs = ','.join(data_dirs)

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_url = ''
if len(kafka_hosts) > 0:
    kafka_url = ':6667,'.join(kafka_hosts) + ':6667'
