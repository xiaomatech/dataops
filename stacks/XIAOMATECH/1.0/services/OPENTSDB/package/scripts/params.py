#!/usr/bin/env python

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/opentsdb'
download_url = config['configurations']['opentsdb-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

conf_dir = '/etc/opentsdb'
opentsdb_user = opentsdb_group = config['configurations']['opentsdb-env'][
    'opentsdb_user']
opentsdb_log_dir = config['configurations']['opentsdb-env']['opentsdb_log_dir']

opentsdb_principal = default('configurations/opentsdb-env/opentsdb_principal',
                             'opentsdb')
opentsdb_keytab = default('configurations/opentsdb-env/opentsdb_keytab', '')

opentsdb_pid_dir = config['configurations']['opentsdb-env']['opentsdb_pid_dir']
opentsdb_pid_file = format("{opentsdb_pid_dir}/opentsdb.pid")

conf_content = config['configurations']['opentsdb-env']['content']
init_content = config['configurations']['opentsdb-env']['init_content']
log_content = config['configurations']['opentsdb-env']['log_content']
jaas_content = config['configurations']['opentsdb-env']['jaas_content']

zk_basedir = config['configurations']['hbase-site']['zookeeper.znode.parent']
zk_quorum = config['configurations']['hbase-site']['hbase.zookeeper.quorum']

security_enabled = config['configurations']['cluster-env']['security_enabled']

kerberos_params = ''

opentsdb_hosts = default('clusterHostInfo/opentsdb_master_hosts', [])
opentsdb_hosts = sorted(opentsdb_hosts)
opentsdb_hosts_dict = {}
hostname = config['agentLevelParams']['hostname']

if security_enabled:
    _hostname_lowercase = config['agentLevelParams']['hostname'].lower()
    opentsdb_principal = opentsdb_principal.replace('_HOST',
                                                    _hostname_lowercase)
    kerberos_params = " -Djava.security.auth.login.config=" + conf_dir + "/opentsdb_jaas.conf"
