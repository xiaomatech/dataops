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

Ambari Agent

"""
import status_params
import ambari_simplejson as json
from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.get_port_from_url import get_port_from_url
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script
from status_params import *
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions import is_empty
import sys, os

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/knox-server'
download_url = config['configurations']['knox-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

tmp_dir = Script.get_tmp_dir()
stack_name = status_params.stack_name
upgrade_direction = default("/commandParams/upgrade_direction", None)
version = default("/commandParams/version", None)

stack_supports_ranger_kerberos = True
stack_supports_ranger_audit_db = False
stack_supports_core_site_for_ranger_plugin = True

knox_data_dir = '/data1/knox'
knox_data_backup_dir = '/data1/backup/knox'

knox_master_secret_path = format('{knox_data_dir}/security/master')
knox_cert_store_path = format('{knox_data_dir}/security/keystores/gateway.jks')
knox_user = default("/configurations/knox-env/knox_user", "knox")
knox_logs_dir = '/var/log/knox'

# default parameters
knox_bin = install_dir + '/bin/gateway.sh'
knox_conf_dir = '/etc/knox'
ldap_bin = install_dir + '/bin/ldap.sh'
knox_client_bin = install_dir + '/bin/knoxcli.sh'

knox_group = default("/configurations/knox-env/knox_group", "knox")
mode = 0644

namenode_hosts = default("/clusterHostInfo/namenode_hosts", None)
has_namenode = bool(namenode_hosts)

dfs_ha_enabled = False
dfs_ha_nameservices = default(
    '/configurations/hdfs-site/dfs.internal.nameservices', None)
if dfs_ha_nameservices is None:
    dfs_ha_nameservices = default('/configurations/hdfs-site/dfs.nameservices',
                                  None)

if dfs_ha_nameservices is not None:
    dfs_ha_nameservices = dfs_ha_nameservices.split(
        ','
    )[0]  # for now knox topology.xml supports working with only one nameservice

dfs_ha_namenode_ids = default(
    format("/configurations/hdfs-site/dfs.ha.namenodes.{dfs_ha_nameservices}"),
    None)

namenode_rpc = None

dfs_type = default("/clusterLevelParams/dfs_type", "").lower()

namenode_http_port = "9870"
namenode_https_port = "9871"
namenode_rpc_port = "8020"
namenode_address = ""

if has_namenode:
    if 'dfs.namenode.http-address' in config['configurations']['hdfs-site']:
        namenode_http_port = get_port_from_url(
            config['configurations']['hdfs-site']['dfs.namenode.http-address'])
    if 'dfs.namenode.https-address' in config['configurations']['hdfs-site']:
        namenode_https_port = get_port_from_url(
            config['configurations']['hdfs-site']
            ['dfs.namenode.https-address'])
    if dfs_ha_enabled and namenode_rpc:
        namenode_rpc_port = get_port_from_url(namenode_rpc)
    else:
        if 'dfs.namenode.rpc-address' in config['configurations']['hdfs-site']:
            namenode_rpc_port = get_port_from_url(
                config['configurations']['hdfs-site']
                ['dfs.namenode.rpc-address'])

    namenode_address = format(
        "{dfs_type}://{namenode_hosts[0]}:{namenode_rpc_port}")

if dfs_ha_namenode_ids:
    dfs_ha_namemodes_ids_list = dfs_ha_namenode_ids.split(",")
    dfs_ha_namenode_ids_array_len = len(dfs_ha_namemodes_ids_list)
    if dfs_ha_namenode_ids_array_len > 1:
        dfs_ha_enabled = True

if dfs_ha_enabled:
    for nn_id in dfs_ha_namemodes_ids_list:
        nn_host = config['configurations']['hdfs-site'][format(
            'dfs.namenode.rpc-address.{dfs_ha_nameservices}.{nn_id}')]
        if hostname.lower() in nn_host.lower():
            namenode_id = nn_id
            namenode_rpc = nn_host
        # With HA enabled namenode_address is recomputed
    namenode_address = format('{dfs_type}://{dfs_ha_nameservices}')

namenode_port_map = {}
if dfs_ha_enabled:
    for nn_id in dfs_ha_namemodes_ids_list:
        nn_host = config['configurations']['hdfs-site'][format(
            'dfs.namenode.http-address.{dfs_ha_nameservices}.{nn_id}')]
        nn_host_parts = nn_host.split(':')
        namenode_port_map[nn_host_parts[0]] = nn_host_parts[1]

dfs_http_policy = default('/configurations/hdfs-site/dfs.http.policy', None)

hdfs_https_on = False
hdfs_scheme = 'http'
if dfs_http_policy != None:
    hdfs_https_on = (dfs_http_policy.upper() == 'HTTPS_ONLY')
    hdfs_scheme = 'http' if not hdfs_https_on else 'https'
    hdfs_port = str(namenode_http_port) if not hdfs_https_on else str(
        namenode_https_port)
    namenode_http_port = hdfs_port


def buildUrlElement(protocol, hdfs_host, port, servicePath):
    openTag = "<url>"
    closeTag = "</url>"
    proto = protocol + "://"
    newLine = "\n"
    if hdfs_host is None or port is None:
        return ""
    else:
        return openTag + proto + hdfs_host + ":" + port + servicePath + closeTag + newLine


namenode_host_keys = namenode_port_map.keys()
webhdfs_service_urls = ""
if len(namenode_host_keys) > 0:
    for host in namenode_host_keys:
        webhdfs_service_urls += buildUrlElement(
            "http", host, namenode_port_map[host], "/webhdfs")
elif has_namenode:
    webhdfs_service_urls = buildUrlElement("http", namenode_hosts[0],
                                           namenode_http_port, "/webhdfs")

yarn_http_policy = default('/configurations/yarn-site/yarn.http.policy', None)
yarn_https_on = False
yarn_scheme = 'http'
if yarn_http_policy != None:
    yarn_https_on = (yarn_http_policy.upper() == 'HTTPS_ONLY')
    yarn_scheme = 'http' if not yarn_https_on else 'https'

rm_hosts = default("/clusterHostInfo/resourcemanager_hosts", None)
if type(rm_hosts) is list:
    rm_host = rm_hosts[0]
else:
    rm_host = rm_hosts
has_rm = not rm_host == None

jt_rpc_port = "8050"
rm_port = "8080"

if has_rm:
    if 'yarn.resourcemanager.address' in config['configurations']['yarn-site']:
        jt_rpc_port = get_port_from_url(config['configurations']['yarn-site']
                                        ['yarn.resourcemanager.address'])

    if 'yarn.resourcemanager.webapp.address' in config['configurations'][
            'yarn-site']:
        rm_port = get_port_from_url(config['configurations']['yarn-site']
                                    ['yarn.resourcemanager.webapp.address'])

hive_http_port = default(
    '/configurations/hive-site/hive.server2.thrift.http.port', "10001")
hive_http_path = default(
    '/configurations/hive-site/hive.server2.thrift.http.path', "cliservice")
hive_server_hosts = default("/clusterHostInfo/hive_server_hosts", None)
if type(hive_server_hosts) is list:
    hive_server_host = hive_server_hosts[0] if len(
        hive_server_hosts) > 0 else None
else:
    hive_server_host = hive_server_hosts

templeton_port = default('/configurations/webhcat-site/templeton.port',
                         "50111")
webhcat_server_hosts = default("/clusterHostInfo/webhcat_server_hosts", None)
if type(webhcat_server_hosts) is list:
    webhcat_server_host = webhcat_server_hosts[0]
else:
    webhcat_server_host = webhcat_server_hosts

hive_scheme = 'http'
webhcat_scheme = 'http'

hbase_master_scheme = 'http'
hbase_master_ui_port = default(
    '/configurations/hbase-site/hbase.master.info.port', "16010")
hbase_master_port = default('/configurations/hbase-site/hbase.rest.port',
                            "8080")
hbase_master_hosts = default("/clusterHostInfo/hbase_master_hosts", None)
if type(hbase_master_hosts) is list:
    hbase_master_host = hbase_master_hosts[0]
else:
    hbase_master_host = hbase_master_hosts

#
# Oozie
#
oozie_https_port = None
oozie_scheme = 'http'
oozie_server_port = "11000"
oozie_server_hosts = default("/clusterHostInfo/oozie_server_hosts", None)

if type(oozie_server_hosts) is list:
    oozie_server_host = oozie_server_hosts[0]
else:
    oozie_server_host = oozie_server_hosts

has_oozie = not oozie_server_host == None

if has_oozie:
    oozie_server_port = get_port_from_url(
        config['configurations']['oozie-site']['oozie.base.url'])
    oozie_https_port = default("/configurations/oozie-site/oozie.https.port",
                               None)

if oozie_https_port is not None:
    oozie_scheme = 'https'
    oozie_server_port = oozie_https_port

#
# Falcon
#
falcon_server_hosts = default("/clusterHostInfo/falcon_server_hosts", None)
if type(falcon_server_hosts) is list:
    falcon_server_host = falcon_server_hosts[0]
else:
    falcon_server_host = falcon_server_hosts

falcon_scheme = 'http'
has_falcon = not falcon_server_host == None
falcon_server_port = "15000"

if has_falcon:
    falcon_server_port = config['configurations']['falcon-env']['falcon_port']

#
# Solr
#
solr_scheme = 'http'
solr_server_hosts = default("/clusterHostInfo/solr_hosts", None)
if type(solr_server_hosts) is list:
    solr_host = solr_server_hosts[0]
else:
    solr_host = solr_server_hosts
solr_port = default("/configuration/solr/solr-env/solr_port", "8983")

#
# Spark
#
spark_scheme = 'http'
spark_historyserver_hosts = default(
    "/clusterHostInfo/spark_jobhistoryserver_hosts", None)
if type(spark_historyserver_hosts) is list:
    spark_historyserver_host = spark_historyserver_hosts[0]
else:
    spark_historyserver_host = spark_historyserver_hosts
spark_historyserver_ui_port = default(
    "/configurations/spark-defaults/spark.history.ui.port", "18080")

#
# JobHistory mapreduce
#
mr_scheme = 'http'
mr_historyserver_address = default(
    "/configurations/mapred-site/mapreduce.jobhistory.webapp.address", None)

#
# Yarn nodemanager
#
nodeui_scheme = 'http'
nodeui_port = "8042"
nm_hosts = default("/clusterHostInfo/nodemanager_hosts", None)
if type(nm_hosts) is list:
    nm_host = nm_hosts[0]
else:
    nm_host = nm_hosts

has_yarn = default("/configurations/yarn-site", None)
if has_yarn and 'yarn.nodemanager.webapp.address' in config['configurations'][
        'yarn-site']:
    nodeui_port = get_port_from_url(config['configurations']['yarn-site']
                                    ['yarn.nodemanager.webapp.address'])

#
# Spark Thrift UI
#
spark_thriftserver_scheme = 'http'
spark_thriftserver_ui_port = 4039
spark_thriftserver_hosts = default("/clusterHostInfo/spark_thriftserver_hosts",
                                   None)
if type(spark_thriftserver_hosts) is list:
    spark_thriftserver_host = spark_thriftserver_hosts[0]
else:
    spark_thriftserver_host = spark_thriftserver_hosts

# Knox managed properties
knox_managed_pid_symlink = format('{stack_root}/knox-server/pids')

# knox log4j
knox_gateway_log_maxfilesize = default(
    '/configurations/gateway-log4j/knox_gateway_log_maxfilesize', 256)
knox_gateway_log_maxbackupindex = default(
    '/configurations/gateway-log4j/knox_gateway_log_maxbackupindex', 20)
knox_ldap_log_maxfilesize = default(
    '/configurations/ldap-log4j/knox_ldap_log_maxfilesize', 256)
knox_ldap_log_maxbackupindex = default(
    '/configurations/ldap-log4j/knox_ldap_log_maxbackupindex', 20)

# server configurations
knox_master_secret = config['configurations']['knox-env']['knox_master_secret']
knox_host_name = config['clusterHostInfo']['knox_gateway_hosts'][0]
knox_host_name_in_cluster = config['agentLevelParams']['hostname']
knox_host_port = config['configurations']['gateway-site']['gateway.port']
topology_template = config['configurations']['topology']['content']
admin_topology_template = default('/configurations/admin-topology/content',
                                  None)
knoxsso_topology_template = config['configurations']['knoxsso-topology'][
    'content']
gateway_log4j = config['configurations']['gateway-log4j']['content']
ldap_log4j = config['configurations']['ldap-log4j']['content']
users_ldif = config['configurations']['users-ldif']['content']
java_home = config['ambariLevelParams']['java_home']
security_enabled = config['configurations']['cluster-env']['security_enabled']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
if security_enabled:
    knox_keytab_path = config['configurations']['knox-env']['knox_keytab_path']
    _hostname_lowercase = config['agentLevelParams']['hostname'].lower()
    knox_principal_name = config['configurations']['knox-env'][
        'knox_principal_name'].replace('_HOST', _hostname_lowercase)

# for curl command in ranger plugin to get db connector
jdk_location = config['ambariLevelParams']['jdk_location']

# ranger knox plugin start section

xa_audit_db_is_enabled = False
xa_audit_db_password = ''

# ranger host
ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

# ranger knox plugin enabled property
enable_ranger_knox = default(
    "/configurations/ranger-knox-plugin-properties/ranger-knox-plugin-enabled",
    "No")
enable_ranger_knox = True if enable_ranger_knox.lower() == 'yes' else False

# get ranger knox properties if enable_ranger_knox is True
if enable_ranger_knox:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations']['ranger-knox-security'][
            'ranger.plugin.knox.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger knox service/repositry name
    repo_name = str(config['clusterName']) + '_knox'
    repo_name_value = config['configurations']['ranger-knox-security'][
        'ranger.plugin.knox.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    knox_home = install_dir
    common_name_for_certificate = config['configurations'][
        'ranger-knox-plugin-properties']['common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-knox-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_knox:
        external_admin_username = default(
            '/configurations/ranger-knox-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-knox-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-knox-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-knox-plugin-properties/external_ranger_admin_password',
            'example!@#')
        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-knox-plugin-properties']
    policy_user = config['configurations']['ranger-knox-plugin-properties'][
        'policy_user']
    repo_config_password = config['configurations'][
        'ranger-knox-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    knox_ranger_plugin_config = {
        'username':
        repo_config_username,
        'password':
        repo_config_password,
        'knox.url':
        format(
            "https://{knox_host_name}:{knox_host_port}/gateway/admin/api/v1/topologies"
        ),
        'commonNameForCertificate':
        common_name_for_certificate
    }

    if security_enabled:
        knox_ranger_plugin_config['policy.download.auth.users'] = knox_user
        knox_ranger_plugin_config['tag.download.auth.users'] = knox_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        knox_ranger_plugin_config.update(custom_ranger_service_config)

    knox_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': knox_ranger_plugin_config,
        'description': 'knox repo',
        'name': repo_name,
        'type': 'knox'
    }

    xa_audit_hdfs_is_enabled = config['configurations']['ranger-knox-audit'][
        'xasecure.audit.destination.hdfs'] if xml_configurations_supported else False
    ssl_keystore_password = config['configurations']['ranger-knox-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations']['ranger-knox-policymgr-ssl'][
        'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# need this to capture cluster name from where ranger knox plugin is enabled
cluster_name = config['clusterName']

# ranger knox plugin end section

hdfs_user = config['configurations']['hadoop-env'][
    'hdfs_user'] if has_namenode else None
hdfs_user_keytab = config['configurations']['hadoop-env'][
    'hdfs_user_keytab'] if has_namenode else None
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name'] if has_namenode else None
hdfs_site = config['configurations']['hdfs-site'] if has_namenode else None
default_fs = config['configurations']['core-site'][
    'fs.defaultFS'] if has_namenode else None
hadoop_bin_dir = Script.get_stack_root() + '/hadoop/bin/' if has_namenode else None
hadoop_conf_dir = '/etc/hadoop' if has_namenode else None

import functools

# create partial functions with common arguments for every HdfsResource call
# to create/delete hdfs directory/file/copyfromlocal we need to call params.HdfsResource in code
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

druid_coordinator_urls = ""
if "druid-coordinator" in config['configurations']:
    port = config['configurations']['druid-coordinator']['druid.port']
    for host in config['clusterHostInfo']['druid_coordinator_hosts']:
        druid_coordinator_urls += buildUrlElement("http", host, port, "")

druid_overlord_urls = ""
if "druid-overlord" in config['configurations']:
    port = config['configurations']['druid-overlord']['druid.port']
    for host in config['clusterHostInfo']['druid_overlord_hosts']:
        druid_overlord_urls += buildUrlElement("http", host, port, "")

druid_broker_urls = ""
if "druid-broker" in config['configurations']:
    port = config['configurations']['druid-broker']['druid.port']
    for host in config['clusterHostInfo']['druid_broker_hosts']:
        druid_broker_urls += buildUrlElement("http", host, port, "")

druid_router_urls = ""
if "druid-router" in config['configurations']:
    port = config['configurations']['druid-router']['druid.port']
    for host in config['clusterHostInfo']['druid_router_hosts']:
        druid_router_urls += buildUrlElement("http", host, port, "")

zeppelin_ui_urls = ""
zeppelin_ws_urls = ""
websocket_support = "false"
if "zeppelin-site" in config['configurations']:
    port = config['configurations']['zeppelin-site']['zeppelin.server.port']
    protocol = "https" if config['configurations']['zeppelin-site'][
        'zeppelin.ssl'] else "http"
    host = config['clusterHostInfo']['zeppelin_master_hosts'][0]
    zeppelin_ui_urls += buildUrlElement(protocol, host, port, "")
    zeppelin_ws_urls += buildUrlElement("ws", host, port, "/ws")
    websocket_support = "true"

if "topology" in config['configurations']:
    if 'ws://' in config['configurations']['topology'][
            'content'] or 'wss://' in config['configurations']['topology'][
                'content']:
        websocket_support = "true"

# for stack 3.0 +
knox_descriptors_dir = format('{knox_conf_dir}/descriptors')
knox_shared_providers_dir = format('{knox_conf_dir}/shared-providers')

mount_table_xml_inclusion_file_full_path = None
mount_table_content = None
if 'viewfs-mount-table' in config['configurations']:
    xml_inclusion_file_name = 'viewfs-mount-table.xml'
    mount_table = config['configurations']['viewfs-mount-table']

    if 'content' in mount_table and mount_table['content'].strip():
        mount_table_xml_inclusion_file_full_path = os.path.join(
            knox_conf_dir, xml_inclusion_file_name)
        mount_table_content = mount_table['content']
retryAble = default("/commandParams/command_retry_enabled", False)
