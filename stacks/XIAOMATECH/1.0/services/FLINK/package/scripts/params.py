from resource_management import *
from resource_management.libraries.script.script import Script
import os
from resource_management.libraries.functions.default import default
from resource_management.libraries.resources.hdfs_resource import HdfsResource
import functools
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
stack_root = Script.get_stack_root()

# params from flink-config
flink_numcontainers = config['configurations']['flink-yarn'][
    'flink_numcontainers']
flink_numberoftaskslots = config['configurations']['flink-yarn'][
    'flink_numberoftaskslots']
flink_jobmanager_memory = config['configurations']['flink-yarn'][
    'flink_jobmanager_memory']
flink_container_memory = config['configurations']['flink-yarn'][
    'flink_container_memory']
flink_appname = config['configurations']['flink-yarn']['flink_appname']
flink_queue = config['configurations']['flink-yarn']['flink_queue']
flink_streaming = config['configurations']['flink-yarn']['flink_streaming']

install_dir = stack_root + '/flink'
download_url = config['configurations']['flink-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

conf_dir = '/etc/flink'
bin_dir = install_dir + '/bin'

# params from flink-conf.yaml
flink_yaml_content = config['configurations']['flink-env']['content']
flink_user = config['configurations']['flink-env']['flink_user']
flink_group = config['configurations']['cluster-env']['user_group']
flink_log_dir = config['configurations']['flink-env']['flink_log_dir']
flink_log_file = os.path.join(flink_log_dir, 'flink-setup.log')
flink_dir = config['configurations']['flink-env']['flink_hdfs_dir']
flink_checkpoints_dir = config['configurations']['flink-env'][
    'flink_checkpoints_dir']
flink_recovery_dir = config['configurations']['flink-env'][
    'flink_recovery_dir']
flink_savepoint_dir = config['configurations']['flink-env'][
    'flink_savepoint_dir']
flink_kerberos_keytab = config['configurations']['flink-env']['flink.keytab']
hostname = config['agentLevelParams']['hostname']
flink_kerberos_principal = config['configurations']['flink-env'][
    'flink.principal'].replace('_HOST', hostname.lower())

zk_url = []
for item in config['clusterHostInfo']['zookeeper_hosts']:
    zk_url.append(item + ':2181')
zookeeper_quorum = ",".join(zk_url)
zk_jaas_file = '/etc/zookeeper/zookeeper_client_jaas.conf'

hostname = config['agentLevelParams']['hostname']
hdfs_user = default("/configurations/hadoop-env/hdfs_user", 'hdfs')
hdfs_user_keytab = default("/configurations/hadoop-env/hdfs_user_keytab", None)
hdfs_principal_name = default('/configurations/hadoop-env/hdfs_principal_name',
                              'missing_principal').replace("_HOST", hostname)
security_enabled = default("/configurations/cluster-env/security_enabled",
                           False)
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
hdfs_site = default("/configurations/hdfs-site", [])
default_fs = default("/configurations/core-site/fs.defaultFS", 'XMcluster')
dfs_type = default("/commandParams/dfs_type", "")
hadoop_bin_dir = stack_root + '/hadoop/bin'
flink_pid_dir = config['configurations']['flink-env']['flink_pid_dir']
flink_pid_file = flink_pid_dir + '/flink.pid'
hadoop_conf_dir = '/etc/hadoop'
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

flink_jobmanager_hosts = default('/clusterHostInfo/flink_jobmanager_hosts', [])
flink_taskmanager_hosts = default('/clusterHostInfo/flink_taskmanager_hosts',
                                  [])

flink_master_hosts_str = ':8081\n'.join(flink_jobmanager_hosts)
flink_slave_hosts_str = '\n'.join(flink_taskmanager_hosts)

streamsql_install_dir = stack_root + '/flinkstreamsql'
streamsql_download_url = config['configurations']['flink-env'][
    'streamsql_download_url']
streamsql_filename = streamsql_download_url.split('/')[-1]
streamsql_version_dir = streamsql_filename.replace('.tar.gz', '').replace(
    '.tgz', '')
streamsql_conf_dir = '/etc/flinksql'

cluster_name = config["clusterName"]

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024**3))
men_mib = int(mem_bytes / (1024**2))

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/flink/tmp' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

tmp_dir = ':'.join(mounts)

task_slot_num = int(cpu_count / 8)
tm_heap_size = int(mem_gib * 0.2)
jm_heapsize = int(mem_gib * 0.6)
