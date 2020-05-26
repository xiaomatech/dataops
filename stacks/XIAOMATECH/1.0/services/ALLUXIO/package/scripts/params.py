from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/alluxio'
download_url = config['configurations']['alluxio-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')
conf_dir = install_dir + '/conf/'
libexec_dir = install_dir + '/libexec/'

alluxio_masters = default('clusterHostInfo/alluxio_master_hosts', [])
alluxio_masters_str = '\n'.join(alluxio_masters)

alluxio_workers = default('clusterHostInfo/alluxio_worker_hosts', [])
alluxio_workers_str = '\n'.join(alluxio_workers)

underfs_addr = config['configurations']['alluxio-env'][
    'alluxio.underfs.address']

worker_mem = config['configurations']['alluxio-env']['alluxio.worker.memory']

namenode_address = None
if 'dfs.namenode.rpc-address' in config['configurations']['hdfs-site']:
    namenode_rpcaddress = config['configurations']['hdfs-site'][
        'dfs.namenode.rpc-address']
    namenode_address = format("hdfs://{namenode_rpcaddress}")
else:
    namenode_address = config['configurations']['core-site']['fs.defaultFS']

# HA
enabled_ha = 'alluxio.zookeeper.enabled=false'
zk_addr = '#alluxio.zookeeper.address=' + config['configurations'][
    'alluxio-env']['alluxio.zookeeper.address']
journal_folder = 'alluxio.master.journal.folder=' + config['configurations'][
    'alluxio-env']['alluxio.master.journal.folder']
worker_timeout = 'alluxio.worker.block.heartbeat.timeout.ms=120000'
if len(alluxio_masters) > 1:
    enabled_ha = 'alluxio.zookeeper.enabled=true'
    zk_addr = 'alluxio.zookeeper.address=' + config['configurations'][
        'alluxio-env']['alluxio.zookeeper.address']
    journal_folder = 'alluxio.master.journal.folder=' + config[
        'configurations']['alluxio-env']['alluxio.master.journal.folder']
    worker_timeout = 'alluxio.worker.block.heartbeat.timeout.ms=120000'

host_name = config['hostname']

alluxio_master = '#alluxio.master.hostname=' + host_name
alluxio_master_web_port = '#alluxio.master.web.port=' + config[
    'configurations']['alluxio-env']['alluxio.master.web.port']
for master in config['clusterHostInfo']['alluxio_master_hosts']:
    if master == host_name:
        alluxio_master = 'alluxio.master.hostname=' + host_name
        alluxio_master_web_port = 'alluxio.master.web.port=' + config[
            'configurations']['alluxio-env']['alluxio.master.web.port']
        break

alluxio_user = config['configurations']['alluxio-env']['alluxio_user']
user_group = config['configurations']['cluster-env']['user_group']

log_dir = config['configurations']['alluxio-env']['alluxio.log.dir']
journal_dir = config['configurations']['alluxio-env'][
    'alluxio.master.journal.folder']

hdd_dirs = config['configurations']['alluxio-env']['alluxio.hdd.dirs']
hdd_quota = config['configurations']['alluxio-env']['alluxio.hdd.quota']
pid_dir = config['configurations']['alluxio-env']['alluxio.pid.dir']

start_script = install_dir + 'bin/alluxio-start.sh '
stop_script = install_dir + 'bin/alluxio-stop.sh '

hadoop_conf_dir = '/etc/hadoop/'

env_content = config['configurations']['alluxio-env']['env_content']
alluxio_site_content = config['configurations']['alluxio-env'][
    'alluxio_site_content']

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024**3) * 0.8)

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/alluxio' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

disk_partion = ','.join(mounts)
