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
import sys
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.get_kinit_path import get_kinit_path
from resource_management.libraries.script import Script
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.expect import expect
from resource_management.core.exceptions import Fail

config = Script.get_config()
stack_root = Script.get_stack_root()
install_dir = stack_root + '/sqoop'
download_url = config['configurations']['sqoop-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

# Needed since this is an Atlas Hook service.
cluster_name = config['clusterName']

ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']

stack_name = default("/clusterLevelParams/stack_name", None)

agent_stack_retry_on_unavailability = config['ambariLevelParams'][
    'agent_stack_retry_on_unavailability']
agent_stack_retry_count = expect("/ambariLevelParams/agent_stack_retry_count",
                                 int)

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)

# default hadoop params
sqoop_conf_dir = '/etc/sqoop'
sqoop_lib = install_dir + "/lib"
hadoop_home = Script.get_stack_root()+'/hadoop'
hbase_home = Script.get_stack_root() + '/hbase'
hive_home = Script.get_stack_root() + '/hive'
sqoop_bin_dir = install_dir + "/bin"
zoo_conf_dir = "/etc/zookeeper"

security_enabled = config['configurations']['cluster-env']['security_enabled']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
user_group = config['configurations']['cluster-env']['user_group']
sqoop_env_sh_template = config['configurations']['sqoop-env']['content']

sqoop_user = config['configurations']['sqoop-env']['sqoop_user']

smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
# JDBC driver jar name
sqoop_jdbc_drivers_dict = []
sqoop_jdbc_drivers_name_dict = {}
sqoop_jdbc_drivers_to_remove = {}
if "jdbc_drivers" in config['configurations']['sqoop-env']:
    sqoop_jdbc_drivers = config['configurations']['sqoop-env'][
        'jdbc_drivers'].split(',')

    for driver_name in sqoop_jdbc_drivers:
        previous_jdbc_jar_name = None
        driver_name = driver_name.strip()
        if driver_name and not driver_name == '':
            if driver_name == "com.microsoft.sqlserver.jdbc.SQLServerDriver":
                jdbc_name = default(
                    "/ambariLevelParams/custom_mssql_jdbc_name", None)
                previous_jdbc_jar_name = default(
                    "/ambariLevelParams/previous_custom_mssql_jdbc_name", None)
                jdbc_driver_name = "mssql"
            elif driver_name == "com.mysql.jdbc.Driver":
                jdbc_name = default(
                    "/ambariLevelParams/custom_mysql_jdbc_name", None)
                previous_jdbc_jar_name = default(
                    "/ambariLevelParams/previous_custom_mysql_jdbc_name", None)
                jdbc_driver_name = "mysql"
            elif driver_name == "org.postgresql.Driver":
                jdbc_name = default(
                    "/ambariLevelParams/custom_postgres_jdbc_name", None)
                previous_jdbc_jar_name = default(
                    "/ambariLevelParams/previous_custom_postgres_jdbc_name",
                    None)
                jdbc_driver_name = "postgres"
            elif driver_name == "oracle.jdbc.driver.OracleDriver":
                jdbc_name = default(
                    "/ambariLevelParams/custom_oracle_jdbc_name", None)
                previous_jdbc_jar_name = default(
                    "/ambariLevelParams/previous_custom_oracle_jdbc_name",
                    None)
                jdbc_driver_name = "oracle"
            elif driver_name == "org.hsqldb.jdbc.JDBCDriver":
                jdbc_name = default(
                    "/ambariLevelParams/custom_hsqldb_jdbc_name", None)
                previous_jdbc_jar_name = default(
                    "/ambariLevelParams/previous_custom_hsqldb_jdbc_name",
                    None)
                jdbc_driver_name = "hsqldb"
            else:
                raise Fail(
                    format("JDBC driver '{driver_name}' not supported."))
        else:
            continue
        sqoop_jdbc_drivers_dict.append(jdbc_name)
        sqoop_jdbc_drivers_to_remove[jdbc_name] = previous_jdbc_jar_name
        sqoop_jdbc_drivers_name_dict[jdbc_name] = jdbc_driver_name
jdk_location = config['ambariLevelParams']['jdk_location']

########################################################
############# Atlas related params #####################
########################################################
# region Atlas Hooks
sqoop_atlas_application_properties = default(
    '/configurations/sqoop-atlas-application.properties', {})
enable_atlas_hook = default('/configurations/sqoop-env/sqoop.atlas.hook',
                            False)
atlas_hook_filename = default('/configurations/atlas-env/metadata_conf_file',
                              'atlas-application.properties')
# endregion

import functools
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.resources import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources

security_enabled = config['configurations']['cluster-env']['security_enabled']
hadoop_home = stack_root +  '/hadoop'

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

java64_home = config['ambariLevelParams']['java_home']
stack_supports_ranger_kerberos = True
retryAble = default("/commandParams/command_retry_enabled", False)
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

# ranger sqoop plugin enabled property
enable_ranger_sqoop = default(
    "/configurations/ranger-sqoop-plugin-properties/ranger-sqoop-plugin-enabled",
    "No")
enable_ranger_sqoop = True if enable_ranger_sqoop.lower() == 'yes' else False

xa_audit_db_is_enabled = False
xa_audit_db_password = ''

# ranger sqoop properties
if enable_ranger_sqoop:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations']['ranger-sqoop-security'][
            'ranger.plugin.sqoop.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger sqoop service name
    repo_name = str(config['clusterName']) + '_sqoop'
    repo_name_value = config['configurations']['ranger-sqoop-security'][
        'ranger.plugin.sqoop.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    common_name_for_certificate = config['configurations'][
        'ranger-sqoop-plugin-properties']['common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-sqoop-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_sqoop:
        external_admin_username = default(
            '/configurations/ranger-sqoop-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-sqoop-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-sqoop-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-sqoop-plugin-properties/external_ranger_admin_password',
            'example!@#')
        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-sqoop-plugin-properties']
    policy_user = sqoop_user
    repo_config_password = config['configurations'][
        'ranger-sqoop-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    sqoop_ranger_plugin_config = {
        'username': repo_config_username,
        'password': repo_config_password,
        'commonNameForCertificate': common_name_for_certificate
    }

    if security_enabled:
        policy_user = format('{sqoop_user},{sqoop_bare_jaas_principal}')
        sqoop_ranger_plugin_config['policy.download.auth.users'] = policy_user
        sqoop_ranger_plugin_config['tag.download.auth.users'] = policy_user
        sqoop_ranger_plugin_config['ambari.service.check.user'] = policy_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        sqoop_ranger_plugin_config.update(custom_ranger_service_config)

    sqoop_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': sqoop_ranger_plugin_config,
        'description': 'sqoop repo',
        'name': repo_name,
        'type': 'sqoop'
    }

    ranger_sqoop_principal = None
    ranger_sqoop_keytab = None

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-sqoop-audit/xasecure.audit.destination.hdfs',
        False)
    ssl_keystore_password = config['configurations']['ranger-sqoop-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations'][
        'ranger-sqoop-policymgr-ssl'][
            'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# required when Ranger-KMS is SSL enabled
ranger_kms_hosts = default('/clusterHostInfo/ranger_kms_server_hosts', [])
has_ranger_kms = len(ranger_kms_hosts) > 0
is_ranger_kms_ssl_enabled = default(
    'configurations/ranger-kms-site/ranger.service.https.attrib.ssl.enabled',
    False)
# ranger plugin end section
