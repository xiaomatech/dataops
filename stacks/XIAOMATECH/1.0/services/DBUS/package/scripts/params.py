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

dbus_user = config['configurations']['dbus-env']['dbus_user']
log_dir = config['configurations']['dbus-env']['log_dir']
pid_dir = config['configurations']['dbus-env']['pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/dbus'
download_url = config['configurations']['dbus-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '').replace(
    '.tar.bz2', '')

conf_content = config['configurations']['dbus-env']['conf_content']
cluster_id = config['configurations']['dbus-env']['cluster_id']
db_url = config['configurations']['dbus-env']['db_url']
db_user = config['configurations']['dbus-env']['db_user']
db_password = config['configurations']['dbus-env']['db_password']

cluster_name = config['clusterName']
flink_home = stack_root + '/flink'
spark_home = stack_root + '/spark'
hadoop_home = stack_root + '/hadoop'

cluster_zookeeper_quorum_hosts = default(
    '/clusterHostInfo/zookeeper_server_hosts', [])

from random import shuffle
shuffle(cluster_zookeeper_quorum_hosts)

zk_url = ':2181,'.join(cluster_zookeeper_quorum_hosts) + ':2181'

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_broker_url = ''
if len(kafka_hosts) > 0:
    kafka_broker_url = ':6667,'.join(kafka_hosts) + ':6667'

conf_dir = '/etc/dbus'

pid_file = pid_dir + '/dbus.pid'

dbus_group = user_group = config['configurations']['cluster-env']['user_group']

influxdb_hosts = default('/clusterHostInfo/influxdb_hosts', [])
influxdb_server = influxdb_hosts[0]

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
