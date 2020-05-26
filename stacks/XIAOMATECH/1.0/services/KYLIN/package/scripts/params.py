#!/usr/bin/env python

import functools
import os
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.script.script import Script

from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

install_dir = stack_root + '/kylin'
download_url = config['configurations']['kylin-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

spark_home = stack_root +  '/spark'

# params from kylin-env
kylin_user = config['configurations']['kylin-env']['kylin_user']
kylin_group = config['configurations']['cluster-env']['user_group']
kylin_log_dir = config['configurations']['kylin-env']['kylin_log_dir']
kylin_pid_dir = config['configurations']['kylin-env']['kylin_pid_dir']
kylin_hdfs_user_dir = format("/user/{kylin_user}")
kylin_log_file = os.path.join(kylin_log_dir, 'setup.log')
kylin_cluster_server_hosts = default(
    "/clusterHostInfo/kylin_query_hosts", []) + default(
        "/clusterHostInfo/kylin_job_hosts", [])
kylin_cluster_servers = ':7000'.join(kylin_cluster_server_hosts) + ':7000'
kylin_dir = install_dir
conf_dir = "/etc/kylin"
kylin_pid_file = kylin_pid_dir + '/kylin-' + kylin_user + '.pid'
server_mode = 'job'

hostname = config['agentLevelParams']['hostname'].lower()
if hostname in default("/clusterHostInfo/kylin_query_hosts", []):
    server_mode = 'query'

kylin_properties_template = config['configurations']['kylin-env']['content']
kylin_env_template = config['configurations']['kylin-env']['kylin_env_content']

log4j_server_props = config['configurations']['kylin-env'][
    'kylin-server-log4j']
log4j_tool_props = config['configurations']['kylin-env']['kylin-tools-log4j']
log4j_kafka_props = config['configurations']['kylin-env']['kylin-kafka-log4j']
kylin_kerberos_keytab = config['configurations']['kylin-env'][
    'kylin.server.kerberos.keytab']
kylin_kerberos_principal = config['configurations']['kylin-env'][
    'kylin.server.kerberos.principal']

# detect configs
master_configs = config['clusterHostInfo']
java64_home = config['ambariLevelParams']['java_home']

hbase_master_hosts = default("/clusterHostInfo/hbase_master_hosts", [])

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
hadoop_bin_dir = stack_root +  '/hadoop/bin'
hadoop_conf_dir = '/etc/hadoop'
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name']
hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']
dfs_type = default("/clusterLevelParams/dfs_type", "")
# create partial functions with common arguments for every HdfsResource call
# to create hdfs directory we need to call params.HdfsResource in code
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

thriftserver_hosts = default("/clusterHostInfo/hive_server_hosts", [])

hive_thriftserver = thriftserver_hosts[0]

# ranger plugin start section
script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config
from resource_management.libraries.functions import is_empty

ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

# ambari-server hostname
ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']

# ranger kylin plugin enabled property
enable_ranger_kylin = default(
    "/configurations/ranger-kylin-plugin-properties/ranger-kylin-plugin-enabled",
    "No")
enable_ranger_kylin = True if enable_ranger_kylin.lower() == 'yes' else False

xa_audit_db_is_enabled = False
xa_audit_db_password = ''
stack_supports_ranger_kerberos = True
retryAble = default("/commandParams/command_retry_enabled", False)

# ranger kylin properties
if enable_ranger_kylin:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations']['ranger-kylin-security'][
            'ranger.plugin.kylin.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger kylin service name
    repo_name = str(config['clusterName']) + '_kylin'
    repo_name_value = config['configurations']['ranger-kylin-security'][
        'ranger.plugin.kylin.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    common_name_for_certificate = config['configurations'][
        'ranger-kylin-plugin-properties']['common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-kylin-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_kylin:
        external_admin_username = default(
            '/configurations/ranger-kylin-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-kylin-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-kylin-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-kylin-plugin-properties/external_ranger_admin_password',
            'example!@#')
        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-kylin-plugin-properties']
    policy_user = kylin_user
    repo_config_password = config['configurations'][
        'ranger-kylin-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    kylin_ranger_plugin_config = {
        'username': repo_config_username,
        'password': repo_config_password,
        'commonNameForCertificate': common_name_for_certificate
    }

    if security_enabled:
        policy_user = format('{kylin_user},{kylin_bare_jaas_principal}')
        kylin_ranger_plugin_config['policy.download.auth.users'] = policy_user
        kylin_ranger_plugin_config['tag.download.auth.users'] = policy_user
        kylin_ranger_plugin_config['ambari.service.check.user'] = policy_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        kylin_ranger_plugin_config.update(custom_ranger_service_config)

    kylin_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': kylin_ranger_plugin_config,
        'description': 'kylin repo',
        'name': repo_name,
        'type': 'kylin'
    }

    ranger_kylin_principal = None
    ranger_kylin_keytab = None

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-kylin-audit/xasecure.audit.destination.hdfs',
        False)
    ssl_keystore_password = config['configurations']['ranger-kylin-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations'][
        'ranger-kylin-policymgr-ssl'][
            'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# required when Ranger-KMS is SSL enabled
ranger_kms_hosts = default('/clusterHostInfo/ranger_kms_server_hosts', [])
has_ranger_kms = len(ranger_kms_hosts) > 0
is_ranger_kms_ssl_enabled = default(
    'configurations/ranger-kms-site/ranger.service.https.attrib.ssl.enabled',
    False)
# ranger plugin end section
