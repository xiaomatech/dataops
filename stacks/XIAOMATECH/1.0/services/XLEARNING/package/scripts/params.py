#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default
import functools
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.resources import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/xlearning'
download_url = config['configurations']['xlearning-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

xlearning_user = config['configurations']['xlearning-env']['xlearning_user']
xlearning_group = user_group = config['configurations']['cluster-env'][
    'user_group']
log_dir = config['configurations']['xlearning-env']['xlearning_log_dir']
xlearning_pid_file = install_dir + '/bin/xlearning.pid'

env_content = config['configurations']['xlearning-env']['env_content']
log_content = config['configurations']['xlearning-env']['log_content']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
hadoop_conf_dir = '/etc/hadoop'
conf_dir = '/etc/xlearning'

security_enabled = config['configurations']['cluster-env']['security_enabled']
hadoop_home = stack_root + '/hadoop'

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
