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

elastic_home = config['configurations']['elastic-sysconfig']['elastic_home']
work_dir = config['configurations']['elastic-sysconfig']['work_dir']
conf_dir = config['configurations']['elastic-sysconfig']['conf_dir']
heap_size = config['configurations']['elastic-sysconfig']['heap_size']
max_open_files = config['configurations']['elastic-sysconfig'][
    'max_open_files']
max_map_count = config['configurations']['elastic-sysconfig']['max_map_count']

elastic_user = config['configurations']['elastic-env']['elastic_user']
elastic_group = config['configurations']['elastic-env']['elastic_group']
log_dir = config['configurations']['elastic-env']['elastic_log_dir']
pid_dir = config['configurations']['elastic-env']['elastic_pid_dir']

elastic_pid_file = pid_dir + '/elasticsearch.pid'

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
elastic_env_sh_template = config['configurations']['elastic-env']['content']
sysconfig_template = config['configurations']['elastic-sysconfig']['content']

master_content = config['configurations']['elastic-env']['master_content']
policy_content = config['configurations']['elastic-env']['policy_content']

jvm_content = config['configurations']['elastic-env']['jvm_content']
index_template_content = config['configurations']['elastic-env'][
    'index_template_content']

cluster_name = config['configurations']['elastic-env']['cluster_name']

data_hosts = default("/clusterHostInfo/es_data_hosts", [])
master_hosts = default("/clusterHostInfo/es_master_hosts", [])
client_hosts = default("/clusterHostInfo/es_client_hosts", [])
ingest_hosts = default("/clusterHostInfo/es_ingest_hosts", [])
coordinating_hosts = default("/clusterHostInfo/es_coordinating_hosts", [])
ml_hosts = default("/clusterHostInfo/es_ml_hosts", [])

unicast_hosts = ','.join(master_hosts)
minimum_master_nodes = len(master_hosts) - 1

if hostname in data_hosts:
    node_mode = '''
node.master: false
node.data: true
node.ingest: true
node.ml: false
xpack.ml.enabled: true
'''
elif hostname in master_hosts:
    node_mode = '''
node.master: true
node.data: false
node.ingest: false
node.ml: false
'''
elif hostname in client_hosts:
    node_mode = '''
node.data: false
node.master: false
node.ingest: false
node.ml: false 
'''
elif hostname in ingest_hosts:
    node_mode = '''
node.master: false
node.data: true
node.ingest: true
search.remote.connect: false
node.ml: false
'''
elif hostname in coordinating_hosts:
    node_mode = '''
node.master: false
node.data: false
node.ingest: false
search.remote.connect: false
node.ml: false
'''
elif hostname in ml_hosts:
    node_mode = '''
node.master: false
node.data: true
node.ingest: true
search.remote.connect: false
node.ml: true
xpack.ml.enabled: true
'''


# detect server role
# https://www.elastic.co/guide/en/elasticsearch/reference/6.6/index-lifecycle-management.html
def detect_host_role(hostname):
    hot_servers = []
    cold_servers = []
    warm_servers = []
    if hostname in hot_servers:
        return 'hot'
    elif hostname in cold_servers:
        return 'cold'
    elif hostname in warm_servers:
        return 'warm'
    else:
        return 'normal'


role_type = detect_host_role(hostname=hostname)

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = min(32, int(mem_bytes / (1024 ** 3) * 0.6))

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/es' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

data_dir = ','.join(mounts)

cluster_name = config["clusterName"]
hdfs_backup_dir = '/es/backup'
hdfs_backup_content = config['configurations']['elastic-env'][
    'hdfs_backup_content']

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

# ranger plugin start section
script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config
from resource_management.libraries.functions import is_empty

ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

stack_supports_ranger_kerberos = True
retryAble = default("/commandParams/command_retry_enabled", False)

# ambari-server hostname
ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']

# ranger elasticsearch plugin enabled property
enable_ranger_elasticsearch = default(
    "/configurations/ranger-elasticsearch-plugin-properties/ranger-elasticsearch-plugin-enabled",
    "No")
enable_ranger_elasticsearch = True if enable_ranger_elasticsearch.lower(
) == 'yes' else False

xa_audit_db_is_enabled = False
xa_audit_db_password = ''

# ranger elasticsearch properties
if enable_ranger_elasticsearch:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations'][
            'ranger-elasticsearch-security'][
            'ranger.plugin.elasticsearch.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger elasticsearch service name
    repo_name = str(config['clusterName']) + '_elasticsearch'
    repo_name_value = config['configurations'][
        'ranger-elasticsearch-security'][
        'ranger.plugin.elasticsearch.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    common_name_for_certificate = config['configurations'][
        'ranger-elasticsearch-plugin-properties'][
        'common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-elasticsearch-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_elasticsearch:
        external_admin_username = default(
            '/configurations/ranger-elasticsearch-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-elasticsearch-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-elasticsearch-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-elasticsearch-plugin-properties/external_ranger_admin_password',
            'example!@#')
        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-elasticsearch-plugin-properties']
    policy_user = elastic_user
    repo_config_password = config['configurations'][
        'ranger-elasticsearch-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    elasticsearch_ranger_plugin_config = {
        'username': repo_config_username,
        'password': repo_config_password,
        'commonNameForCertificate': common_name_for_certificate
    }

    if security_enabled:
        policy_user = format(
            '{elasticsearch_user},{elasticsearch_bare_jaas_principal}')
        elasticsearch_ranger_plugin_config[
            'policy.download.auth.users'] = policy_user
        elasticsearch_ranger_plugin_config[
            'tag.download.auth.users'] = policy_user
        elasticsearch_ranger_plugin_config[
            'ambari.service.check.user'] = policy_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        elasticsearch_ranger_plugin_config.update(custom_ranger_service_config)

    elasticsearch_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': elasticsearch_ranger_plugin_config,
        'description': 'elasticsearch repo',
        'name': repo_name,
        'type': 'elasticsearch'
    }

    ranger_elasticsearch_principal = None
    ranger_elasticsearch_keytab = None

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-elasticsearch-audit/xasecure.audit.destination.hdfs',
        False)
    ssl_keystore_password = config['configurations'][
        'ranger-elasticsearch-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations'][
        'ranger-elasticsearch-policymgr-ssl'][
        'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# required when Ranger-KMS is SSL enabled
ranger_kms_hosts = default('/clusterHostInfo/ranger_kms_server_hosts', [])
has_ranger_kms = len(ranger_kms_hosts) > 0
is_ranger_kms_ssl_enabled = default(
    'configurations/ranger-kms-site/ranger.service.https.attrib.ssl.enabled',
    False)
# ranger plugin end section
