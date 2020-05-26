#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default
import functools
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.resources import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['filebeat-env']['conf_content']
metricbeat_content = config['configurations']['filebeat-env']['metricbeat_content']
heartbeat_content = config['configurations']['filebeat-env']['heartbeat_content']

apm_server_content = config['configurations']['filebeat-env'][
    'apm_server_content']

user_group = config['configurations']['cluster-env']['user_group']

cluster_zookeeper_quorum_hosts = default(
    '/clusterHostInfo/zookeeper_server_hosts', [])
from random import shuffle
shuffle(cluster_zookeeper_quorum_hosts)
zk_url = ':2181,'.join(cluster_zookeeper_quorum_hosts) + ':2181'

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_broker_url = kafka_url = ''
if len(kafka_hosts) > 0:
    kafka_broker_url = ':6667,'.join(kafka_hosts) + ':6667'
    kafka_url = '"' + ':6667","'.join(kafka_hosts) + ':6667"'

kibana_hosts = default('/clusterHostInfo/kibana_hosts', [])
kibana_host = kibana_hosts[0]

es_hosts = default('/clusterHostInfo/es_client_hosts', [])
from random import shuffle
shuffle(es_hosts)
es_url = '"http://' + ':9200","http://'.join(es_hosts) + ':9200"'
es_host = '"' + ':9200","'.join(es_hosts) + ':9200"'

hadoop_home = stack_root + '/hadoop'

security_enabled = config['configurations']['cluster-env']['security_enabled']
if security_enabled:
    _hostname_lowercase = config['agentLevelParams']['hostname'].lower()

# smokeuser
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']

hadoop_bin_dir = hadoop_home + '/bin'
hadoop_conf_dir = hadoop_home + '/etc/hadoop'
hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']
dfs_type = default("/commandParams/dfs_type", "")
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']

HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file=
    "/var/lib/ambari-agent/data/.hdfs_resource_ignore",
    security_enabled=security_enabled,
    keytab=hdfs_user_keytab,
    kinit_path_local=kinit_path_local,
    hadoop_bin_dir=hadoop_bin_dir,
    hadoop_conf_dir=hadoop_conf_dir,
    principal_name=hdfs_principal_name,
    hdfs_site=hdfs_site,
    default_fs=default_fs,
    immutable_paths=get_not_managed_resources(),
    dfs_type=dfs_type)
