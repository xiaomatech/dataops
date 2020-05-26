from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()
exec_tmp_dir = Script.get_tmp_dir()

hostname = config['agentLevelParams']['hostname']
kafka_user_nofile_limit = default(
    '/configurations/confluent-env/kafka_user_nofile_limit', 1048576)
kafka_user_nproc_limit = default(
    '/configurations/confluent-env/kafka_user_nproc_limit', 65536)

kafka_user = config['configurations']['confluent-env']['kafka_user']
kafka_log_dir = config['configurations']['confluent-env']['kafka_log_dir']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['ambariLevelParams']['java_home']

control_center_dir = config['configurations']['confluent-env'][
    'control_center_dir']

zookeeper_connect = default("/configurations/confluent-env/zookeeper.connect",
                            None)
zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()

kafka_broker_port = default('/configurations/confluent-env/port', '6667')
kafka_host_arr = []

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle
shuffle(kafka_hosts)
for i in range(len(kafka_hosts)):
    kafka_host_arr.append('PLAINTEXT://' + kafka_hosts[i] + ':' +
                          kafka_broker_port)
bootstrap_servers = ",".join(kafka_host_arr)

schema_registry_hosts = default('/clusterHostInfo/schema_registry_hosts',
                                ['localhost'])
schema_registry_arr = []
for i in range(len(schema_registry_hosts)):
    schema_registry_arr.append('http://' + schema_registry_hosts[i] + ':8081')
schema_registry_url = ','.join(schema_registry_arr)

ksql_hosts = default('/clusterHostInfo/ksql_hosts', ['localhost'])
ksql_arr = []
for i in range(len(ksql_hosts)):
    ksql_arr.append('http://' + ksql_hosts[i] + ':8088')
ksql_url = ','.join(ksql_arr)

connect_cluster_hosts = default('/clusterHostInfo/kafkaconnector_hosts',
                                ['localhost'])
connect_cluster_arr = []
for i in range(len(connect_cluster_hosts)):
    connect_cluster_arr.append('http://' + connect_cluster_hosts[i] + ':8083')
connect_cluster_url = ','.join(connect_cluster_arr)

zk_quorum = ""
zookeeper_port = default('/configurations/zoo.cfg/clientPort', 2181)
if 'zookeeper_server_hosts' in config['clusterHostInfo']:
    for host in config['clusterHostInfo']['zookeeper_server_hosts']:
        if zk_quorum:
            zk_quorum += ','
        zk_quorum += host + ":" + str(zookeeper_port)

schema_registry_content = config['configurations']['confluent-env'][
    'schema_registry_content']
kafka_content = config['configurations']['confluent-env']['kafka_content']
kafka_manager_content = config['configurations']['confluent-env'][
    'kafka_manager_content']
kafka_connect_content = config['configurations']['confluent-env'][
    'kafka_connect_content']
kafka_rest_content = config['configurations']['confluent-env'][
    'kafka_rest_content']
ksql_server_content = config['configurations']['confluent-env'][
    'ksql_server_content']
control_center_content = config['configurations']['confluent-env'][
    'control_center_content']
mqtt_proxy_content = config['configurations']['confluent-env'][
    'mqtt_proxy_content']
kafka_connect_plugin_download_url = config['configurations']['confluent-env'][
    'kafka_connect_plugin_download_url']
kafka_connector_content = config['configurations']['confluent-env']['kafka_connector_content']


kafka_connector_hosts = default('/clusterHostInfo/kafkaconnector_hosts', [hostname])
kafka_connector_host = kafka_connector_hosts[0]

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024 ** 3) * 0.8)

kafka_env_content = default(
    '/configurations/confluent-env/kafka_env_content',
    'KAFKA_HEAP_OPTS="-Xms6g -Xmx6g" \nLOG_DIR=/var/log/confluent/kafka \nKAFKA_JVM_PERFORMANCE_OPTS="-XX:MetaspaceSize=96m -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:G1HeapRegionSize=16M -XX:MinMetaspaceFreeRatio=50 -XX:MaxMetaspaceFreeRatio=80" \nJMX_PORT=39999'
)

kafka_rest_env_content = default(
    '/configurations/confluent-env/kafka_rest_env_content',
    'KAFKAREST_HEAP_OPTS="-Xms4g -Xmx4g" \nKAFKAREST_JVM_PERFORMANCE_OPTS="-XX:MetaspaceSize=96m -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:G1HeapRegionSize=16M -XX:MinMetaspaceFreeRatio=50 -XX:MaxMetaspaceFreeRatio=80" \nJMX_PORT=39997 \nLOG_DIR=/var/log/confluent/kafka-rest'
)

kafka_registry_env_content = default(
    '/configurations/confluent-env/kafka_registry_env_content',
    'SCHEMA_REGISTRY_HEAP_OPTS="-Xms1g -Xmx1g" \nJMX_PORT=39998 \nLOG_DIR=/var/log/confluent/schema-registry'
)

with open('/proc/mounts', 'r') as f:
    log_dirs_list = [
        line.split()[1] + '/kafka' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

if len(log_dirs_list) == 0:
    log_dirs_list.append(Script.get_stack_root() + '/kafka')

log_dirs = ','.join(log_dirs_list)

# ranger kafka plugin section start
from resource_management.libraries.functions.is_empty import is_empty
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
import sys
script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

stack_supports_ranger_kerberos = True
retryAble = default("/commandParams/command_retry_enabled", False)

import re


def get_bare_principal(normalized_principal_name):
    """
    :param normalized_principal_name: a string containing the principal name to process
    :return: a string containing the primary component value or None if not valid
    """

    bare_principal = None

    if normalized_principal_name:
        match = re.match(r"([^/@]+)(?:/[^@])?(?:@.*)?",
                         normalized_principal_name)

    if match:
        bare_principal = match.group(1)

    return bare_principal


# Security-related params
kerberos_security_enabled = config['configurations']['cluster-env'][
    'security_enabled']

# server configurations

xa_audit_db_is_enabled = False
xa_audit_db_password = ''
# ranger host
ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

# ranger kafka plugin enabled property
enable_ranger_kafka = default(
    "configurations/ranger-kafka-plugin-properties/ranger-kafka-plugin-enabled",
    "No")
enable_ranger_kafka = True if enable_ranger_kafka.lower() == 'yes' else False

is_supported_kafka_ranger = True

# ranger kafka properties
if enable_ranger_kafka and is_supported_kafka_ranger:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['ranger-kafka-security'][
        'ranger.plugin.kafka.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger kafka service/repository name
    repo_name = str(config['clusterName']) + '_kafka'
    repo_name_value = config['configurations']['ranger-kafka-security'][
        'ranger.plugin.kafka.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_kafka:
        external_admin_username = default(
            '/configurations/ranger-kafka-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-kafka-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-kafka-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-kafka-plugin-properties/external_ranger_admin_password',
            'example!@#')

        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-kafka-plugin-properties']
    ranger_kafka_audit = config['configurations']['ranger-kafka-audit']
    ranger_kafka_audit_attrs = config['configurationAttributes'][
        'ranger-kafka-audit']
    ranger_kafka_security = config['configurations']['ranger-kafka-security']
    ranger_kafka_security_attrs = config['configurationAttributes'][
        'ranger-kafka-security']
    ranger_kafka_policymgr_ssl = config['configurations'][
        'ranger-kafka-policymgr-ssl']
    ranger_kafka_policymgr_ssl_attrs = config['configurationAttributes'][
        'ranger-kafka-policymgr-ssl']

    policy_user = config['configurations']['ranger-kafka-plugin-properties'][
        'policy_user']

    ranger_plugin_config = {
        'username':
            config['configurations']['ranger-kafka-plugin-properties']
            ['REPOSITORY_CONFIG_USERNAME'],
        'password':
            config['configurations']['ranger-kafka-plugin-properties']
            ['REPOSITORY_CONFIG_PASSWORD'],
        'zookeeper.connect':
            config['configurations']['ranger-kafka-plugin-properties']
            ['zookeeper.connect'],
        'commonNameForCertificate':
            config['configurations']['ranger-kafka-plugin-properties']
            ['common.name.for.certificate']
    }

    atlas_server_hosts = default('/clusterHostInfo/atlas_server_hosts', [])
    has_atlas_server = not len(atlas_server_hosts) == 0
    hive_server_hosts = default('/clusterHostInfo/hive_server_hosts', [])
    has_hive_server = not len(hive_server_hosts) == 0
    hbase_master_hosts = default('/clusterHostInfo/hbase_master_hosts', [])
    has_hbase_master = not len(hbase_master_hosts) == 0
    ranger_tagsync_hosts = default('/clusterHostInfo/ranger_tagsync_hosts', [])
    has_ranger_tagsync = not len(ranger_tagsync_hosts) == 0
    storm_nimbus_hosts = default('/clusterHostInfo/nimbus_hosts', [])
    has_storm_nimbus = not len(storm_nimbus_hosts) == 0

    if has_atlas_server:
        atlas_notification_topics = default(
            '/configurations/application-properties/atlas.notification.topics',
            'ATLAS_HOOK,ATLAS_ENTITIES')
        atlas_notification_topics_list = atlas_notification_topics.split(',')
        hive_user = default('/configurations/hive-env/hive_user', 'hive')
        hbase_user = default('/configurations/hbase-env/hbase_user', 'hbase')
        atlas_user = default('/configurations/atlas-env/metadata_user',
                             'atlas')
        rangertagsync_user = default(
            '/configurations/ranger-tagsync-site/ranger.tagsync.dest.ranger.username',
            'rangertagsync')
        if len(atlas_notification_topics_list) == 2:
            atlas_hook = atlas_notification_topics_list[0]
            atlas_entity = atlas_notification_topics_list[1]
            ranger_plugin_config['setup.additional.default.policies'] = 'true'
            ranger_plugin_config['default-policy.1.name'] = atlas_hook
            ranger_plugin_config[
                'default-policy.1.resource.topic'] = atlas_hook
            hook_policy_user = []
            if has_hive_server:
                hook_policy_user.append(hive_user)
            if has_hbase_master:
                hook_policy_user.append(hbase_user)
            if has_storm_nimbus and kerberos_security_enabled:
                storm_principal_name = config['configurations']['storm-env'][
                    'storm_principal_name']
                storm_bare_principal_name = get_bare_principal(
                    storm_principal_name)
                hook_policy_user.append(storm_bare_principal_name)
            if len(hook_policy_user) > 0:
                ranger_plugin_config[
                    'default-policy.1.policyItem.1.users'] = ",".join(
                    hook_policy_user)
                ranger_plugin_config[
                    'default-policy.1.policyItem.1.accessTypes'] = "publish"
            ranger_plugin_config[
                'default-policy.1.policyItem.2.users'] = atlas_user
            ranger_plugin_config[
                'default-policy.1.policyItem.2.accessTypes'] = "consume"
            ranger_plugin_config['default-policy.2.name'] = atlas_entity
            ranger_plugin_config[
                'default-policy.2.resource.topic'] = atlas_entity
            ranger_plugin_config[
                'default-policy.2.policyItem.1.users'] = atlas_user
            ranger_plugin_config[
                'default-policy.2.policyItem.1.accessTypes'] = "publish"
            if has_ranger_tagsync:
                ranger_plugin_config[
                    'default-policy.2.policyItem.2.users'] = rangertagsync_user
                ranger_plugin_config[
                    'default-policy.2.policyItem.2.accessTypes'] = "consume"

    if kerberos_security_enabled:
        ranger_plugin_config['policy.download.auth.users'] = kafka_user
        ranger_plugin_config['tag.download.auth.users'] = kafka_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        ranger_plugin_config.update(custom_ranger_service_config)

    kafka_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': ranger_plugin_config,
        'description': 'kafka repo',
        'name': repo_name,
        'repositoryType': 'kafka',
        'type': 'kafka',
        'assetType': '1'
    }

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-kafka-audit/xasecure.audit.destination.hdfs',
        False)
    ssl_keystore_password = config['configurations']['ranger-kafka-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations'][
        'ranger-kafka-policymgr-ssl'][
        'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

    setup_ranger_env_sh_source = format(
        '{stack_root}/ranger-kafka-plugin/install/conf.templates/enable/kafka-ranger-env.sh'
    )
    setup_ranger_env_sh_target = format("{conf_dir}/kafka-ranger-env.sh")

# need this to capture cluster name from where ranger kafka plugin is enabled
cluster_name = config['clusterName']

# required when Ranger-KMS is SSL enabled
ranger_kms_hosts = default('/clusterHostInfo/ranger_kms_server_hosts', [])
has_ranger_kms = len(ranger_kms_hosts) > 0
is_ranger_kms_ssl_enabled = default(
    'configurations/ranger-kms-site/ranger.service.https.attrib.ssl.enabled',
    False)

conf_dir = '/etc/kafka'


kafka_kerberos_params = ''
kafka_jaas_principal = None
kafka_keytab_path = None

namenode_hosts = default("/clusterHostInfo/namenode_hosts", [])
has_namenode = not len(namenode_hosts) == 0
stack_root = Script.get_stack_root()

hdfs_user = config['configurations']['hadoop-env'][
    'hdfs_user'] if has_namenode else None
hdfs_user_keytab = config['configurations']['hadoop-env'][
    'hdfs_user_keytab'] if has_namenode else None
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name'] if has_namenode else None
hdfs_site = config['configurations']['hdfs-site'] if has_namenode else None
default_fs = config['configurations']['core-site'][
    'fs.defaultFS'] if has_namenode else None
hadoop_bin_dir = stack_root + '/hadoop/bin/' if has_namenode else None
hadoop_conf_dir = '/etc/hadoop' if has_namenode else None
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
dfs_type = default("/clusterLevelParams/dfs_type", "")

mount_table_xml_inclusion_file_full_path = None
mount_table_content = None
if 'viewfs-mount-table' in config['configurations']:
    xml_inclusion_file_name = 'viewfs-mount-table.xml'
    mount_table = config['configurations']['viewfs-mount-table']

    if 'content' in mount_table and mount_table['content'].strip():
        mount_table_xml_inclusion_file_full_path = os.path.join(
            conf_dir, xml_inclusion_file_name)
        mount_table_content = mount_table['content']

import functools

HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file=
    "/var/lib/ambari-agent/data/.hdfs_resource_ignore",
    security_enabled=kerberos_security_enabled,
    keytab=hdfs_user_keytab,
    kinit_path_local=kinit_path_local,
    hadoop_bin_dir=hadoop_bin_dir,
    hadoop_conf_dir=hadoop_conf_dir,
    principal_name=hdfs_principal_name,
    hdfs_site=hdfs_site,
    default_fs=default_fs,
    immutable_paths=get_not_managed_resources(),
    dfs_type=dfs_type,
)

# ranger kafka plugin section end
