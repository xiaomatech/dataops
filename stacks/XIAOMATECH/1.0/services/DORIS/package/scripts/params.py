#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

doris_user = config['configurations']['doris-env']['doris_user']
doris_group = user_group = config['configurations']['cluster-env']['user_group']
log_dir = config['configurations']['doris-env']['doris_log_dir']
pid_dir = config['configurations']['doris-env']['doris_pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/doris'
download_url = config['configurations']['doris-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

fe_conf = config['configurations']['doris-env']['fe_conf']
be_conf = config['configurations']['doris-env']['be_conf']
apache_hdfs_broker_conf = config['configurations']['doris-env'][
    'apache_hdfs_broker_conf']
doris_env_content = config['configurations']['doris-env']['doris_env_content']

dorisfe_hosts = default("/clusterHostInfo/dorisfe_hosts", [])
dorisbe_hosts = default("/clusterHostInfo/dorisbe_hosts", [])
dorishdfsrouter_hosts = default("/clusterHostInfo/dorishdfsrouter_hosts", [])

if hostname in dorisbe_hosts:
    doris_home = install_dir + '/be'
elif hostname in dorisfe_hosts:
    doris_home = install_dir + '/fe'
else:
    doris_home = install_dir + '/apache_hdfs_broker'

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/doris' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

data_dir = ';'.join(mounts)
