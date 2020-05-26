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

wormhole_user = config['configurations']['wormhole-env']['wormhole_user']
log_dir = config['configurations']['wormhole-env']['log_dir']
pid_dir = config['configurations']['wormhole-env']['pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/wormhole'
download_url = config['configurations']['wormhole-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '').replace(
    '.tar.bz2', '')

conf_content = config['configurations']['wormhole-env']['conf_content']
cluster_id = config['configurations']['wormhole-env']['cluster_id']
db_url = config['configurations']['wormhole-env']['db_url']
cluster_name = config['clusterName']
flink_home = stack_root + '/flink'
spark_home = stack_root + '/spark'
hadoop_home = stack_root + '/hadoop'

yarn_http_policy = config['configurations']['yarn-site']['yarn.http.policy']
yarn_https_on = (yarn_http_policy.upper() == 'HTTPS_ONLY')

yarn_rm_address = config['configurations']['yarn-site'][
    'yarn.resourcemanager.webapp.address'] if not yarn_https_on else config[
        'configurations']['yarn-site'][
            'yarn.resourcemanager.webapp.https.address']

rm_ha_enabled = False
rm_ha_id = None
rm_ha_ids_list = []
rm_webapp_addresses_list = [yarn_rm_address]
rm_ha_ids = default("/configurations/yarn-site/yarn.resourcemanager.ha.rm-ids",
                    None)

if rm_ha_ids:
    rm_ha_ids_list = rm_ha_ids.split(",")
    if len(rm_ha_ids_list) > 1:
        rm_ha_enabled = True

if rm_ha_enabled:
    rm_webapp_addresses_list = []
    for rm_id in rm_ha_ids_list:
        rm_webapp_address_property = format(
            'yarn.resourcemanager.webapp.address.{rm_id}'
        ) if not yarn_https_on else format(
            'yarn.resourcemanager.webapp.https.address.{rm_id}')
        rm_webapp_address = config['configurations']['yarn-site'][
            rm_webapp_address_property]
        rm_webapp_addresses_list.append(rm_webapp_address)
        rm_host_name = config['configurations']['yarn-site'][format(
            'yarn.resourcemanager.hostname.{rm_id}')]
        if rm_host_name == hostname.lower():
            rm_ha_id = rm_id

rm2_url = rm_webapp_addresses_list.pop()
rm1_url = rm_webapp_addresses_list.pop()

ldap_hosts = default('clusterHostInfo/openldap_master_hosts', [])
ldap_user = config['configurations']['openldap-config']['ldap.adminuser']
ldap_pwd = config['configurations']['openldap-config']['ldap.password']
ldap_url = ''
if len(ldap_hosts) > 0:
    ldap_url = 'ldap://' + ldap_hosts[0] + ':389'
ldap_dc = config['configurations']['openldap-config']['ldap.domain']

cluster_zookeeper_quorum_hosts = default(
    '/clusterHostInfo/zookeeper_server_hosts', [])
from random import shuffle
shuffle(cluster_zookeeper_quorum_hosts)
zk_url = cluster_zookeeper_quorum_hosts[0] + ':2181'

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
kafka_broker_url = ''
if len(kafka_hosts) > 0:
    kafka_broker_url = ':6667,'.join(kafka_hosts) + ':6667'

es_hosts = default('/clusterHostInfo/es_client_hosts', [])
from random import shuffle
shuffle(es_hosts)
es_url = ''
if len(es_hosts) > 0:
    es_url = 'http://' + es_hosts[0] + ':9200'

grafana_hosts = default('/clusterHostInfo/grafana_hosts', [])
grafana_url = ''
if len(grafana_hosts) > 0:
    grafana_url = 'http://' + grafana_hosts[0] + ':80'

dbus_web_hosts = default('/clusterHostInfo/dbus_web_hosts', [])
dbus_host = ''
if len(dbus_web_hosts) > 0:
    dbus_host = dbus_web_hosts[0]

conf_dir = '/etc/wormhole'

pid_file = pid_dir + '/wormhole.pid'

wormhole_group = user_group = config['configurations']['cluster-env'][
    'user_group']

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
