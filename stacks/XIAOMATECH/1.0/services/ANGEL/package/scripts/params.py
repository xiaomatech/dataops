from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.resources import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/angel'
download_url = config['configurations']['angel-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

hadoop_home = stack_root + '/hadoop'
spark_home = stack_root + '/spark'
angel_home = install_dir

angel_conf_dir = default("/configurations/angel-env/angel_conf_dir",
                         '/etc/angel')
angel_user = config['configurations']['angel-env']['angel_user']

version = default("/commandParams/version", None)

user_group = config['configurations']['cluster-env']['user_group']
proxyuser_group = config['configurations']['hadoop-env']['proxyuser_group']

angel_bin_dir = install_dir + '/bin'

java_home = config['ambariLevelParams']['java_home']
angel_log_dir = config['configurations']['angel-env']['angel_log_dir']
angel_run_dir = config['configurations']['angel-env']['angel_run_dir']
ambari_state_file = format("{angel_run_dir}/ambari-state.txt")

angel_env_sh_template = config['configurations']['angel-env']['content']

hostname = config['agentLevelParams']['hostname']

cluster_name = config["clusterName"]
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
    zookeeper_quorum += ':' + zookeeper_clientPort

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

import functools

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
