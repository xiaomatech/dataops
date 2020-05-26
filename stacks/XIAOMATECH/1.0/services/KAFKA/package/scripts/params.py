#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os
from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
from utils import get_bare_principal
from resource_management.libraries.functions.is_empty import is_empty
import status_params
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

import sys, os

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()
stack_name = default("/clusterLevelParams/stack_name", None)
retryAble = default("/commandParams/command_retry_enabled", False)

install_dir = stack_root + '/kafka'
download_url = config['configurations']['kafka-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

# Version being upgraded/downgraded to
version = default("/commandParams/version", None)

upgrade_direction = default("/commandParams/upgrade_direction", None)

stack_supports_ranger_kerberos = True
stack_supports_ranger_audit_db = False
stack_supports_core_site_for_ranger_plugin = True

hostname = config['agentLevelParams']['hostname']

# default kafka parameters
kafka_home = install_dir
kafka_bin = kafka_home + '/bin/kafka'
conf_dir = "/etc/kafka"
limits_conf_dir = "/etc/security/limits.d"

# Used while upgrading the stack in a kerberized cluster and running kafka-acls.sh
zookeeper_connect = default("/configurations/kafka-broker/zookeeper.connect",
                            None)

kafka_user_nofile_limit = default(
    '/configurations/kafka-env/kafka_user_nofile_limit', 1048576)
kafka_user_nproc_limit = default(
    '/configurations/kafka-env/kafka_user_nproc_limit', 65536)

kafka_delete_topic_enable = default(
    '/configurations/kafka-broker/delete.topic.enable', True)

kafka_user = config['configurations']['kafka-env']['kafka_user']
kafka_log_dir = config['configurations']['kafka-env']['kafka_log_dir']
kafka_pid_dir = status_params.kafka_pid_dir
kafka_pid_file = kafka_pid_dir + "/kafka.pid"
# This is hardcoded on the kafka bash process lifecycle on which we have no control over
kafka_managed_pid_dir = "/var/run/kafka"
kafka_managed_log_dir = "/var/log/kafka"
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['ambariLevelParams']['java_home']
kafka_env_sh_template = config['configurations']['kafka-env']['content']
kafka_jaas_conf_template = default("/configurations/kafka_jaas_conf/content",
                                   None)
kafka_client_jaas_conf_template = default(
    "/configurations/kafka_client_jaas_conf/content", None)
kafka_hosts = config['clusterHostInfo']['kafka_broker_hosts']
kafka_hosts.sort()

zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()
secure_acls = default("/configurations/kafka-broker/zookeeper.set.acl", False)
kafka_security_migrator = os.path.join(kafka_home, "bin",
                                       "zookeeper-security-migration.sh")

all_hosts = default("/clusterHostInfo/all_hosts", [])
all_racks = default("/clusterHostInfo/all_racks", [])

# Kafka log4j
kafka_log_maxfilesize = default(
    '/configurations/kafka-log4j/kafka_log_maxfilesize', 256)
kafka_log_maxbackupindex = default(
    '/configurations/kafka-log4j/kafka_log_maxbackupindex', 20)
controller_log_maxfilesize = default(
    '/configurations/kafka-log4j/controller_log_maxfilesize', 256)
controller_log_maxbackupindex = default(
    '/configurations/kafka-log4j/controller_log_maxbackupindex', 20)

if (('kafka-log4j' in config['configurations'])
        and ('content' in config['configurations']['kafka-log4j'])):
    log4j_props = config['configurations']['kafka-log4j']['content']
else:
    log4j_props = None

if 'ganglia_server_hosts' in config['clusterHostInfo'] and \
        len(config['clusterHostInfo']['ganglia_server_hosts']) > 0:
    ganglia_installed = True
    ganglia_server = config['clusterHostInfo']['ganglia_server_hosts'][0]
    ganglia_report_interval = 60
else:
    ganglia_installed = False

metric_collector_port = ""
metric_collector_protocol = ""
metric_truststore_path = default(
    "/configurations/ams-ssl-client/ssl.client.truststore.location", "")
metric_truststore_type = default(
    "/configurations/ams-ssl-client/ssl.client.truststore.type", "")
metric_truststore_password = default(
    "/configurations/ams-ssl-client/ssl.client.truststore.password", "")

set_instanceId = "false"
cluster_name = config["clusterName"]

if 'cluster-env' in config['configurations'] and \
        'metrics_collector_external_hosts' in config['configurations']['cluster-env']:
    ams_collector_hosts = config['configurations']['cluster-env'][
        'metrics_collector_external_hosts']
    set_instanceId = "true"
else:
    ams_collector_hosts = ",".join(
        default("/clusterHostInfo/metrics_collector_hosts", []))

has_metric_collector = not len(ams_collector_hosts) == 0

if has_metric_collector:
    if 'cluster-env' in config['configurations'] and \
            'metrics_collector_external_port' in config['configurations']['cluster-env']:
        metric_collector_port = config['configurations']['cluster-env'][
            'metrics_collector_external_port']
    else:
        metric_collector_web_address = default(
            "/configurations/ams-site/timeline.metrics.service.webapp.address",
            "0.0.0.0:6188")
        if metric_collector_web_address.find(':') != -1:
            metric_collector_port = metric_collector_web_address.split(':')[1]
        else:
            metric_collector_port = '6188'
    if default("/configurations/ams-site/timeline.metrics.service.http.policy",
               "HTTP_ONLY") == "HTTPS_ONLY":
        metric_collector_protocol = 'https'
    else:
        metric_collector_protocol = 'http'

    host_in_memory_aggregation = str(
        default(
            "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation",
            True)).lower()
    host_in_memory_aggregation_port = default(
        "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation.port",
        61888)
    is_aggregation_https_enabled = False
    if default(
            "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation.http.policy",
            "HTTP_ONLY") == "HTTPS_ONLY":
        host_in_memory_aggregation_protocol = 'https'
        is_aggregation_https_enabled = True
    else:
        host_in_memory_aggregation_protocol = 'http'
    pass

# Security-related params
kerberos_security_enabled = config['configurations']['cluster-env'][
    'security_enabled']

kafka_kerberos_enabled = (
    ('security.inter.broker.protocol' in config['configurations']
     ['kafka-broker']) and
    (config['configurations']['kafka-broker']['security.inter.broker.protocol']
     in ("PLAINTEXTSASL", "SASL_PLAINTEXT", "SASL_SSL")))

kafka_other_sasl_enabled = not kerberos_security_enabled and \
                           (("SASL_PLAINTEXT" in config['configurations']['kafka-broker']['listeners']) or
                            ("PLAINTEXTSASL" in config['configurations']['kafka-broker']['listeners']) or
                            ("SASL_SSL" in config['configurations']['kafka-broker']['listeners']))

if kerberos_security_enabled and 'kafka_principal_name' in config[
        'configurations']['kafka-env']:
    _hostname_lowercase = config['agentLevelParams']['hostname'].lower()
    _kafka_principal_name = config['configurations']['kafka-env'][
        'kafka_principal_name']
    kafka_jaas_principal = _kafka_principal_name.replace(
        '_HOST', _hostname_lowercase)
    kafka_keytab_path = config['configurations']['kafka-env']['kafka_keytab']
    kafka_bare_jaas_principal = get_bare_principal(_kafka_principal_name)
    kafka_kerberos_params = "-Djava.security.auth.login.config=" + conf_dir + "/kafka_jaas.conf"
elif kafka_other_sasl_enabled:
    kafka_kerberos_params = "-Djava.security.auth.login.config=" + conf_dir + "/kafka_jaas.conf"
else:
    kafka_kerberos_params = ''
    kafka_jaas_principal = None
    kafka_keytab_path = None

# for curl command in ranger plugin to get db connector
jdk_location = config['ambariLevelParams']['jdk_location']

# ranger kafka plugin section start
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

# ranger kafka plugin section end

namenode_hosts = default("/clusterHostInfo/namenode_hosts", [])
has_namenode = not len(namenode_hosts) == 0

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

# create partial functions with common arguments for every HdfsResource call
# to create/delete hdfs directory/file/copyfromlocal we need to call params.HdfsResource in code
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

kafka_init_content = config['configurations']['kafka-env'][
    'kafka-init-content']

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024**3) * 0.8)

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/kafka' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

data_dir = ','.join(mounts)
kafka_data_dirs = filter(None, data_dir.split(","))
