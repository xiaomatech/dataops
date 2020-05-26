#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

config = Script.get_config()
stack_root = Script.get_stack_root()

presto_coordinator_host = default('clusterHostInfo/presto_coordinator_hosts',
                                  [])
presto_coordinator_host_one = presto_coordinator_host[0]

discovery_uri = 'http://' + presto_coordinator_host_one + ':8000'

env_sh_template = config['configurations']['presto-env']['content']

daemon_control_script = '/etc/init.d/presto'
conf_dir = '/etc/presto'
pid_dir = '/var/run/presto'
log_dir = '/var/log/presto'
data_dir = '/data1/presto'

host_info = config['clusterHostInfo']

host_level_params = config['hostLevelParams']
java_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/presto-server'
download_url = config['configurations']['presto-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

download_url_cli = config['configurations']['presto-env']['download_url_cli']

presto_user = config['configurations']['presto-env']['presto_user']
user_group = config['configurations']['cluster-env']['user_group']
security_enabled = config['configurations']['cluster-env']['security_enabled']
hive_metastore_uri = config['configurations']['hive-site'][
    'hive.metastore.uris']

hostname = config['agentLevelParams']['hostname'].lower()

hive_metastore_keytab_path = config['configurations']['hive-site'][
    'hive.metastore.kerberos.keytab.file']
hive_metastore_principal = config['configurations']['hive-site'][
    'hive.metastore.kerberos.principal']
presto_principal = default('configurations/presto-env/presto_principal_name',
                           'presto/' + hostname + '@example.com')
presto_keytab = default('configurations/presto-env/presto_keytab_path',
                        '/etc/security/keytabs/presto.service.keytab')

kafka_broker_hosts = default('clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_broker_hosts)
hadoop_conf_dir = '/etc/hadoop'

kafka_server_hosts = kafka_broker_hosts
kafka_broker_port = 6667
kafka_host_arr = []
for i in range(len(kafka_server_hosts)):
    kafka_host_arr.append(kafka_server_hosts[i] + ':' + str(kafka_broker_port))
kafka_hosts = ",".join(kafka_host_arr)

config_content = config['configurations']['presto-env']['config_content']
jvm_content = config['configurations']['presto-env']['jvm_content']
node_content = config['configurations']['presto-env']['node_content']
event_listener_content = config['configurations']['presto-env'][
    'event_listener_content']
password_authenticator_content = config['configurations']['presto-env'][
    'password_authenticator_content']
resource_groups_content = config['configurations']['presto-env'][
    'resource_groups_content']
resource_groups_json_content = config['configurations']['presto-env'][
    'resource_groups_json_content']
rules_content = config['configurations']['presto-env']['rules_content']
catalog_hive_content = config['configurations']['presto-env'][
    'catalog_hive_content']
catalog_kafka_content = config['configurations']['presto-env'][
    'catalog_kafka_content']
catalog_jmx_content = config['configurations']['presto-env'][
    'catalog_jmx_content']
catalog_pulsar_content = config['configurations']['presto-env']['catalog_pulsar_content']
catalog_phoenix_content = config['configurations']['presto-env'][
    'catalog_phoenix_content']

session_content = config['configurations']['presto-env']['session_content']
session_property_content = config['configurations']['presto-env'][
    'session_property_content']

coordinator = 'false'
if hostname in presto_coordinator_host:
    coordinator = 'true'

zookeeper_znode_parent = None
hbase_zookeeper_quorum = None
if 'hbase-site' in config['configurations']:
    zookeeper_znode_parent = config['configurations']['hbase-site'][
        'zookeeper.znode.parent']
    hbase_zookeeper_quorum = config['configurations']['hbase-site'][
        'hbase.zookeeper.quorum']
phoenix_url = "jdbc:phoenix:" + hbase_zookeeper_quorum + ':' + zookeeper_znode_parent

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024**3) * 0.8)
mem_mib = int(mem_bytes / (1024**2) * 0.8)

# ranger plugin start section
script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config
from resource_management.libraries.functions import is_empty

stack_supports_ranger_kerberos = True
retryAble = default("/commandParams/command_retry_enabled", False)
java64_home = config['ambariLevelParams']['java_home']

ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

# ambari-server hostname
ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']

# ranger presto plugin enabled property
enable_ranger_presto = default(
    "/configurations/ranger-presto-plugin-properties/ranger-presto-plugin-enabled",
    "No")
enable_ranger_presto = True if enable_ranger_presto.lower() == 'yes' else False

xa_audit_db_is_enabled = False
xa_audit_db_password = ''

# ranger presto properties
if enable_ranger_presto:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations']['ranger-presto-security'][
            'ranger.plugin.presto.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger presto service name
    repo_name = str(config['clusterName']) + '_presto'
    repo_name_value = config['configurations']['ranger-presto-security'][
        'ranger.plugin.presto.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    common_name_for_certificate = config['configurations'][
        'ranger-presto-plugin-properties']['common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-presto-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_presto:
        external_admin_username = default(
            '/configurations/ranger-presto-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-presto-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-presto-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-presto-plugin-properties/external_ranger_admin_password',
            'example!@#')
        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-presto-plugin-properties']
    policy_user = presto_user
    repo_config_password = config['configurations'][
        'ranger-presto-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    presto_ranger_plugin_config = {
        'username': repo_config_username,
        'password': repo_config_password,
        'commonNameForCertificate': common_name_for_certificate
    }

    if security_enabled:
        policy_user = format('{presto_user},{presto_bare_jaas_principal}')
        presto_ranger_plugin_config['policy.download.auth.users'] = policy_user
        presto_ranger_plugin_config['tag.download.auth.users'] = policy_user
        presto_ranger_plugin_config['ambari.service.check.user'] = policy_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        presto_ranger_plugin_config.update(custom_ranger_service_config)

    presto_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': presto_ranger_plugin_config,
        'description': 'presto repo',
        'name': repo_name,
        'type': 'presto'
    }

    ranger_presto_principal = None
    ranger_presto_keytab = None

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-presto-audit/xasecure.audit.destination.hdfs',
        False)
    ssl_keystore_password = config['configurations']['ranger-presto-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations'][
        'ranger-presto-policymgr-ssl'][
            'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# required when Ranger-KMS is SSL enabled
ranger_kms_hosts = default('/clusterHostInfo/ranger_kms_server_hosts', [])
has_ranger_kms = len(ranger_kms_hosts) > 0
is_ranger_kms_ssl_enabled = default(
    'configurations/ranger-kms-site/ranger.service.https.attrib.ssl.enabled',
    False)
# ranger plugin end section
