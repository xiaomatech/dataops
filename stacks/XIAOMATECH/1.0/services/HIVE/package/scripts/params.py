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

# Python Imports
import os
from urlparse import urlparse

# Local Imports
import status_params

# Ambari Commons & Resource Management Imports
from ambari_commons.constants import AMBARI_SUDO_BINARY
from ambari_commons.credential_store_helper import get_password_from_credential_store
import ambari_simplejson as json
from resource_management.core.exceptions import Fail
from resource_management.core.shell import checked_call
from resource_management.core.utils import PasswordString
from resource_management.libraries import functions
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import upgrade_summary
from resource_management.libraries.functions.copy_tarball import get_sysprep_skip_copy_tarballs_hdfs
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.get_architecture import get_architecture
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions.get_port_from_url import get_port_from_url
from resource_management.libraries.functions.is_empty import is_empty
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.script.script import Script

import sys, os

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

sysprep_skip_copy_tarballs_hdfs = get_sysprep_skip_copy_tarballs_hdfs()
retryAble = default("/commandParams/command_retry_enabled", False)

# log4j version is 2 for hive3; put config files under /etc/hive
log4j_version = '2'

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

architecture = get_architecture()
sudo = AMBARI_SUDO_BINARY

install_dir = stack_root + '/hive'
download_url = config['configurations']['hive-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

credential_store_enabled = False
if 'credentialStoreEnabled' in config:
    credential_store_enabled = config['credentialStoreEnabled']

stack_root = Script.get_stack_root()
stack_name = status_params.stack_name
stack_name_uppercase = stack_name.upper()
agent_stack_retry_on_unavailability = config['ambariLevelParams'][
    'agent_stack_retry_on_unavailability']
agent_stack_retry_count = expect("/ambariLevelParams/agent_stack_retry_count",
                                 int)

# Needed since this is an Atlas Hook service.
cluster_name = config['clusterName']

# node hostname
hostname = config['agentLevelParams']['hostname']

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade.
# It cannot be used during the initial Cluser Install because the version is not yet known.
version = default("/commandParams/version", None)

# When downgrading the 'version' is pointing to the downgrade-target version
# downgrade_from_version provides the source-version the downgrade is happening from
downgrade_from_version = upgrade_summary.get_downgrade_from_version("HIVE")

# Upgrade direction
upgrade_direction = default("/commandParams/upgrade_direction", None)
stack_supports_ranger_kerberos = True
stack_supports_ranger_audit_db = False
stack_supports_ranger_hive_jdbc_url_change = True
stack_supports_atlas_hook_for_hive_interactive = True

hadoop_home = Script.get_stack_root() + '/hadoop/'
hive_bin = format('{install_dir}/bin/')
hive_schematool_ver_bin = format('{install_dir}/bin/')
hive_schematool_bin = format('{install_dir}/bin/')
hive_lib = format('{install_dir}/lib/')
hive_version_lib = format('{install_dir}/lib/')
hive_var_lib = hive_lib
hive_user_home_dir = "/home/hive"
zk_bin = stack_root + '/zookeeper/bin/'

# starting on stacks where HSI is supported, we need to begin using the 'hive2' schematool
hive_server2_hive_dir = install_dir
hive_server2_hive_version_lib = hive_server2_hive_lib = hive_lib

hive_interactive_bin = hive_bin
hive_interactive_lib = hive_lib

# Heap dump related
heap_dump_enabled = default('/configurations/hive-env/enable_heap_dump', None)
heap_dump_opts = ""  # Empty if 'heap_dump_enabled' is False.
if heap_dump_enabled:
    heap_dump_path = default('/configurations/hive-env/heap_dump_location',
                             "/tmp")
    heap_dump_opts = " -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=" + heap_dump_path

# Hive Interactive related paths
hive_interactive_var_lib = hive_lib

# These tar folders were used in previous stack versions, e.g., HDP 2.1
hadoop_streaming_jars = hadoop_home + '/mapreduce/hadoop-streaming-*.jar'

limits_conf_dir = "/etc/security/limits.d"

hive_user_nofile_limit = default(
    "/configurations/hive-env/hive_user_nofile_limit", "1048576")
hive_user_nproc_limit = default(
    "/configurations/hive-env/hive_user_nproc_limit", "16000")

# use the directories from status_params as they are already calculated for
# the correct stack version
hadoop_conf_dir = status_params.hadoop_conf_dir
hadoop_bin_dir = status_params.hadoop_bin_dir
hive_conf_dir = status_params.hive_conf_dir
hive_home_dir = status_params.hive_home_dir
hive_config_dir = status_params.hive_config_dir
hive_client_conf_dir = status_params.hive_client_conf_dir
hive_server_conf_dir = status_params.hive_server_conf_dir
tez_conf_dir = status_params.tez_conf_dir

tarballs_mode = 0444

purge_tables = 'true'

hive_metastore_site_supported = True

execute_path = os.environ[
                   'PATH'] + os.pathsep + hive_bin + os.pathsep + hadoop_bin_dir

hive_metastore_user_name = config['configurations']['hive-site'][
    'javax.jdo.option.ConnectionUserName']
hive_jdbc_connection_url = config['configurations']['hive-site'][
    'javax.jdo.option.ConnectionURL']

jdk_location = config['ambariLevelParams']['jdk_location']

if credential_store_enabled:
    if 'hadoop.security.credential.provider.path' in config['configurations'][
        'hive-site']:
        cs_lib_path = config['configurations']['hive-site'][
            'credentialStoreClassPath']
        java_home = config['ambariLevelParams']['java_home']
        alias = 'javax.jdo.option.ConnectionPassword'
        provider_path = config['configurations']['hive-site'][
            'hadoop.security.credential.provider.path']
        hive_metastore_user_passwd = PasswordString(
            get_password_from_credential_store(
                alias, provider_path, cs_lib_path, java_home, jdk_location))
    else:
        raise Exception(
            "hadoop.security.credential.provider.path property should be set")
else:
    hive_metastore_user_passwd = config['configurations']['hive-site'][
        'javax.jdo.option.ConnectionPassword']
hive_metastore_user_passwd = unicode(
    hive_metastore_user_passwd
) if not is_empty(hive_metastore_user_passwd) else hive_metastore_user_passwd
hive_metastore_db_type = config['configurations']['hive-env'][
    'hive_database_type']
hive_db_schma_name = config['configurations']['hive-site'][
    'ambari.hive.db.schema.name']

# users
hive_user = config['configurations']['hive-env']['hive_user']

# is it a restart command
is_restart_command = False
if 'roleCommand' in config and 'CUSTOM_COMMAND' == config['roleCommand']:
    if 'custom_command' in config['commandParams'] and 'RESTART' == config[
        'commandParams']['custom_command']:
        is_restart_command = True

# JDBC driver jar name
hive_jdbc_driver = config['configurations']['hive-site'][
    'javax.jdo.option.ConnectionDriverName']
java_share_dir = '/usr/share/java'
hive_database_name = config['configurations']['hive-env']['hive_database_name']
hive_database = config['configurations']['hive-env']['hive_database']
hive_use_existing_db = hive_database.startswith('Existing')

default_connectors_map = {
    "com.microsoft.sqlserver.jdbc.SQLServerDriver": "sqljdbc4.jar",
    "com.mysql.jdbc.Driver": "mysql-connector-java.jar",
    "org.postgresql.Driver": "postgresql-jdbc.jar",
    "oracle.jdbc.driver.OracleDriver": "ojdbc.jar",
    "sap.jdbc4.sqlanywhere.IDriver": "sajdbc4.jar"
}

# NOT SURE THAT IT'S A GOOD IDEA TO USE PATH TO CLASS IN DRIVER, MAYBE IT WILL BE BETTER TO USE DB TYPE.
# BECAUSE PATH TO CLASSES COULD BE CHANGED
sqla_db_used = False
hive_previous_jdbc_jar_name = None
if hive_jdbc_driver == "com.microsoft.sqlserver.jdbc.SQLServerDriver":
    jdbc_jar_name = default("/ambariLevelParams/custom_mssql_jdbc_name", None)
    hive_previous_jdbc_jar_name = default(
        "/ambariLevelParams/previous_custom_mssql_jdbc_name", None)
elif hive_jdbc_driver == "com.mysql.jdbc.Driver":
    jdbc_jar_name = default("/ambariLevelParams/custom_mysql_jdbc_name", None)
    hive_previous_jdbc_jar_name = default(
        "/ambariLevelParams/previous_custom_mysql_jdbc_name", None)
elif hive_jdbc_driver == "org.postgresql.Driver":
    jdbc_jar_name = default("/ambariLevelParams/custom_postgres_jdbc_name",
                            None)
    hive_previous_jdbc_jar_name = default(
        "/ambariLevelParams/previous_custom_postgres_jdbc_name", None)
elif hive_jdbc_driver == "oracle.jdbc.driver.OracleDriver":
    jdbc_jar_name = default("/ambariLevelParams/custom_oracle_jdbc_name", None)
    hive_previous_jdbc_jar_name = default(
        "/ambariLevelParams/previous_custom_oracle_jdbc_name", None)
elif hive_jdbc_driver == "sap.jdbc4.sqlanywhere.IDriver":
    jdbc_jar_name = default("/ambariLevelParams/custom_sqlanywhere_jdbc_name",
                            None)
    hive_previous_jdbc_jar_name = default(
        "/ambariLevelParams/previous_custom_sqlanywhere_jdbc_name", None)
    sqla_db_used = True
else:
    raise Fail(format("JDBC driver '{hive_jdbc_driver}' not supported."))

default_mysql_jar_name = "mysql-connector-java.jar"
default_mysql_target = format("{hive_lib}/{default_mysql_jar_name}")
hive_previous_jdbc_jar = format("{hive_lib}/{hive_previous_jdbc_jar_name}")
if not hive_use_existing_db:
    jdbc_jar_name = default_mysql_jar_name

downloaded_custom_connector = format("{tmp_dir}/{jdbc_jar_name}")

hive_jdbc_target = format("{hive_lib}/{jdbc_jar_name}")

# during upgrade / downgrade, use the specific version to copy the JDBC JAR to
if upgrade_direction:
    hive_jdbc_target = format("{hive_version_lib}/{jdbc_jar_name}")

driver_curl_source = format("{jdk_location}/{jdbc_jar_name}")

# normally, the JDBC driver would be referenced by <stack-root>/current/.../foo.jar
source_jdbc_file = format("{stack_root}/hive/lib/{jdbc_jar_name}")

check_db_connection_jar_name = "DBConnectionVerification.jar"
check_db_connection_jar = format(
    "/usr/lib/ambari-agent/{check_db_connection_jar_name}")
hive_jdbc_drivers_list = [
    "com.microsoft.sqlserver.jdbc.SQLServerDriver", "com.mysql.jdbc.Driver",
    "org.postgresql.Driver", "oracle.jdbc.driver.OracleDriver",
    "sap.jdbc4.sqlanywhere.IDriver"
]

prepackaged_jdbc_name = "ojdbc6.jar"
prepackaged_ojdbc_symlink = format("{hive_lib}/{prepackaged_jdbc_name}")

# constants for type2 jdbc
jdbc_libs_dir = format("{hive_lib}/native/lib64")
lib_dir_available = os.path.exists(jdbc_libs_dir)

if sqla_db_used:
    jars_path_in_archive = format("{tmp_dir}/sqla-client-jdbc/java/*")
    libs_path_in_archive = format("{tmp_dir}/sqla-client-jdbc/native/lib64/*")
    downloaded_custom_connector = format("{tmp_dir}/{jdbc_jar_name}")
    libs_in_hive_lib = format("{jdbc_libs_dir}/*")

# Start, Common Hosts and Ports
ambari_server_hostname = config['ambariLevelParams']['ambari_server_host']

hive_metastore_hosts = default('/clusterHostInfo/hive_metastore_hosts', [])
hive_metastore_host = hive_metastore_hosts[0] if len(
    hive_metastore_hosts) > 0 else None
hive_metastore_port = get_port_from_url(
    config['configurations']['hive-site']['hive.metastore.uris'])

hive_server_hosts = default("/clusterHostInfo/hive_server_hosts", [])
hive_server_host = hive_server_hosts[0] if len(hive_server_hosts) > 0 else None

hive_server_interactive_hosts = default(
    '/clusterHostInfo/hive_server_interactive_hosts', [])
hive_server_interactive_host = hive_server_interactive_hosts[0] if len(
    hive_server_interactive_hosts) > 0 else None
hive_server_interactive_ha = True if len(
    hive_server_interactive_hosts) > 1 else False
hive_server_interactive_webui_port = default(
    "/configurations/hive-interactive-site/hive.server2.webui.port", 10502)
hive_server_interactive_webui_use_ssl = default(
    "/configurations/hive-interactive-site/hive.server2.webui.use.ssl", False)
hive_server_interactive_webui_protocol = "https" if hive_server_interactive_webui_use_ssl else "http"
# End, Common Hosts and Ports

hive_transport_mode = config['configurations']['hive-site'][
    'hive.server2.transport.mode']

if hive_transport_mode.lower() == "http":
    hive_server_port = config['configurations']['hive-site'][
        'hive.server2.thrift.http.port']
else:
    hive_server_port = default(
        '/configurations/hive-site/hive.server2.thrift.port', "10000")

hive_url = format("jdbc:hive2://{hive_server_host}:{hive_server_port}")
hive_http_endpoint = default(
    '/configurations/hive-site/hive.server2.thrift.http.path', "cliservice")
hive_server_principal = config['configurations']['hive-site'][
    'hive.server2.authentication.kerberos.principal']
hive_server2_authentication = config['configurations']['hive-site'][
    'hive.server2.authentication']

# ssl options
hive_ssl = default('/configurations/hive-site/hive.server2.use.SSL', False)
hive_ssl_keystore_path = default(
    '/configurations/hive-site/hive.server2.keystore.path', None)
hive_ssl_keystore_password = default(
    '/configurations/hive-site/hive.server2.keystore.password', None)
hive_interactive_ssl_keystore_path = default(
    '/configurations/hive-interactive-site/hive.server2.keystore.path', None)
hive_interactive_ssl_keystore_password = default(
    '/configurations/hive-interactive-site/hive.server2.keystore.password',
    None)

smokeuser = config['configurations']['cluster-env']['smokeuser']
smoke_test_sql = format("{tmp_dir}/hiveserver2.sql")
smoke_test_path = format("{tmp_dir}/hiveserver2Smoke.sh")
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']

fs_root = config['configurations']['core-site']['fs.defaultFS']
security_enabled = config['configurations']['cluster-env']['security_enabled']

kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
hive_metastore_keytab_path = config['configurations']['hive-site'][
    'hive.metastore.kerberos.keytab.file']
hive_metastore_principal = config['configurations']['hive-site'][
    'hive.metastore.kerberos.principal']

hive_server2_keytab = config['configurations']['hive-site'][
    'hive.server2.authentication.kerberos.keytab']

# hive_env
hive_log_dir = config['configurations']['hive-env']['hive_log_dir']
hive_pid_dir = status_params.hive_pid_dir
hive_pid = status_params.hive_pid
hive_interactive_pid = status_params.hive_interactive_pid

# Default conf dir for client
hive_conf_dirs_list = [hive_client_conf_dir]

# These are the folders to which the configs will be written to.
ranger_hive_ssl_config_file = os.path.join(hive_server_conf_dir,
                                           "ranger-policymgr-ssl.xml")
if status_params.role == "HIVE_METASTORE" and hive_metastore_hosts is not None and hostname in hive_metastore_hosts:
    hive_conf_dirs_list.append(hive_server_conf_dir)
elif status_params.role == "HIVE_SERVER" and hive_server_hosts is not None and hostname in hive_server_hosts:
    hive_conf_dirs_list.append(hive_server_conf_dir)
elif status_params.role == "HIVE_SERVER_INTERACTIVE" and hive_server_interactive_hosts is not None and hostname in hive_server_interactive_hosts:
    hive_conf_dirs_list.append(status_params.hive_server_interactive_conf_dir)
    ranger_hive_ssl_config_file = os.path.join(
        status_params.hive_server_interactive_conf_dir,
        "ranger-policymgr-ssl.xml")
# log4j version is 2 for hive2; put config files under /etc/hive_llap/conf
if status_params.role == "HIVE_SERVER_INTERACTIVE":
    log4j_version = '2'

# Starting hiveserver2
start_hiveserver2_script = 'startHiveserver2.sh.j2'

##Starting metastore
start_metastore_script = 'startMetastore.sh'
hive_metastore_pid = status_params.hive_metastore_pid

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
yarn_user = config['configurations']['yarn-env']['yarn_user']
user_group = config['configurations']['cluster-env']['user_group']
artifact_dir = format("{tmp_dir}/AMBARI-artifacts/")
# Need this for yarn.nodemanager.recovery.dir in yarn-site
yarn_log_dir_prefix = config['configurations']['yarn-env'][
    'yarn_log_dir_prefix']

target_hive_interactive = format("{hive_interactive_lib}/{jdbc_jar_name}")
hive_intaractive_previous_jdbc_jar = format(
    "{hive_interactive_lib}/{hive_previous_jdbc_jar_name}")
jars_in_hive_lib = format("{hive_lib}/*.jar")

start_hiveserver2_path = format("{tmp_dir}/start_hiveserver2_script")
start_metastore_path = format("{tmp_dir}/start_metastore_script")

hadoop_heapsize = config['configurations']['hadoop-env']['hadoop_heapsize']

hive_heapsize = config['configurations']['hive-env']['hive.heapsize']

hive_metastore_heapsize = config['configurations']['hive-env'][
    'hive.metastore.heapsize']

java64_home = config['ambariLevelParams']['java_home']
java_exec = format("{java64_home}/bin/java")
java_version = expect("/ambariLevelParams/java_version", int)

##### MYSQL
db_name = config['configurations']['hive-env']['hive_database_name']
mysql_group = 'mysql'

mysql_adduser_path = format("{tmp_dir}/addMysqlUser.sh")
mysql_deluser_path = format("{tmp_dir}/removeMysqlUser.sh")

#### Metastore
# initialize the schema only if not in an upgrade/downgrade
init_metastore_schema = upgrade_direction is None

# Hive log4j properties
hive_log_level = default("/configurations/hive-env/hive.log.level", "INFO")

# parquet-logging.properties
parquet_logging_properties = None
if 'parquet-logging' in config['configurations']:
    parquet_logging_properties = config['configurations']['parquet-logging'][
        'content']

process_name = status_params.process_name
hive_env_sh_template = config['configurations']['hive-env']['content']

hive_hdfs_user_dir = format("/user/{hive_user}")
hive_hdfs_user_mode = 0755
hive_metastore_warehouse_dir = config['configurations']['hive-site'][
    "hive.metastore.warehouse.dir"]
hive_metastore_warehouse_external_dir = config['configurations']['hive-site'][
    "hive.metastore.warehouse.external.dir"]
whs_dir_protocol = urlparse(hive_metastore_warehouse_dir).scheme
hive_exec_scratchdir = config['configurations']['hive-site'][
    "hive.exec.scratchdir"]

# Hive and Tez hook directories
hive_hook_proto_base_directory = format(
    config['configurations']['hive-site']["hive.hook.proto.base-directory"])
tez_hook_proto_base_directory = format(
    "{hive_metastore_warehouse_external_dir}/sys.db/")

# for create_hdfs_directory
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
hdfs_principal_name = default('/configurations/hadoop-env/hdfs_principal_name',
                              'missing_principal').replace("_HOST", hostname)

# Tez-related properties
tez_user = config['configurations']['tez-env']['tez_user']

# Tez jars
tez_local_api_jars = stack_root + '/tez/tez*.jar'
tez_local_lib_jars = stack_root + '/tez/lib/*.jar'

# Tez libraries
tez_lib_uris = default("/configurations/tez-site/tez.lib.uris", None)

mysql_configname = '/etc/my.cnf'

mysql_user = 'mysql'

# Hive security
hive_authorization_enabled = config['configurations']['hive-site'][
    'hive.security.authorization.enabled']

mysql_jdbc_driver_jar = "/usr/share/java/mysql-connector-java.jar"

hive_site_config = dict(config['configurations']['hive-site'])
hive_site_config["hive.metastore.db.type"] = hive_metastore_db_type.upper()
hive_site_config[
    "hive.hook.proto.base-directory"] = hive_hook_proto_base_directory

########################################################
############# AMS related params #####################
########################################################
set_instanceId = "false"

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
    metric_truststore_path = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.location", "")
    metric_truststore_type = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.type", "")
    metric_truststore_password = default(
        "/configurations/ams-ssl-client/ssl.client.truststore.password", "")

metrics_report_interval = default(
    "/configurations/ams-site/timeline.metrics.sink.report.interval", 60)
metrics_collection_period = default(
    "/configurations/ams-site/timeline.metrics.sink.collection.period", 10)

host_in_memory_aggregation = default(
    "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation",
    True)
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
########################################################
############# Atlas related params #####################
########################################################
# region Atlas Hooks
hive_atlas_application_properties = default(
    '/configurations/hive-atlas-application.properties', {})
enable_atlas_hook = default('/configurations/hive-env/hive.atlas.hook', False)
atlas_hook_filename = default('/configurations/atlas-env/metadata_conf_file',
                              'atlas-application.properties')
metastore_event_listener = ''
if enable_atlas_hook:
    metastore_event_listener = 'AtlasMhook'
# endregion

# for create_hdfs_directory
security_param = "true" if security_enabled else "false"

hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']

dfs_type = default("/clusterLevelParams/dfs_type", "")

import functools

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

# Hive Interactive related
hive_interactive_hosts = default(
    '/clusterHostInfo/hive_server_interactive_hosts', [])
has_hive_interactive = len(hive_interactive_hosts) > 0

# llap log4j properties
hive_llap_log_maxfilesize = default(
    '/configurations/llap-daemon-log4j/hive_llap_log_maxfilesize', 256)
hive_llap_log_maxbackupindex = default(
    '/configurations/llap-daemon-log4j/hive_llap_log_maxbackupindex', 240)

# hive log4j2 properties
hive2_log_maxfilesize = default(
    '/configurations/hive-log4j2/hive2_log_maxfilesize', 256)
hive2_log_maxbackupindex = default(
    '/configurations/hive-log4j2/hive2_log_maxbackupindex', 30)

# llap cli log4j2 properties
llap_cli_log_maxfilesize = default(
    '/configurations/llap-cli-log4j2/llap_cli_log_maxfilesize', 256)
llap_cli_log_maxbackupindex = default(
    '/configurations/llap-cli-log4j2/llap_cli_log_maxbackupindex', 30)

llap_daemon_log4j = config['configurations']['llap-daemon-log4j']['content']
llap_cli_log4j2 = config['configurations']['llap-cli-log4j2']['content']
hive_log4j2 = config['configurations']['hive-log4j2']['content']
hive_exec_log4j2 = config['configurations']['hive-exec-log4j2']['content']
beeline_log4j2 = config['configurations']['beeline-log4j2']['content']

hive_server2_zookeeper_namespace = config['configurations']['hive-site'][
    'hive.server2.zookeeper.namespace']
hive_zookeeper_quorum = config['configurations']['hive-site'][
    'hive.zookeeper.quorum']
hive_jdbc_url = format(
    "jdbc:hive2://{hive_zookeeper_quorum}/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace={hive_server2_zookeeper_namespace}"
)

if has_hive_interactive:
    if hive_server_interactive_ha:
        hsi_zookeeper_namespace = config['configurations'][
            'hive-interactive-site'][
            'hive.server2.active.passive.ha.registry.namespace']
        hsi_jdbc_url = format(
            "jdbc:hive2://{hive_zookeeper_quorum}/;serviceDiscoveryMode=zooKeeperHA;zooKeeperNamespace={hsi_zookeeper_namespace}"
        )
    else:
        hsi_zookeeper_namespace = config['configurations'][
            'hive-interactive-site']['hive.server2.zookeeper.namespace']
        hsi_jdbc_url = format(
            "jdbc:hive2://{hive_zookeeper_quorum}/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace={hsi_zookeeper_namespace}"
        )
    hive_server_interactive_conf_dir = status_params.hive_server_interactive_conf_dir
    execute_path_hive_interactive = os.path.join(
        os.environ['PATH'], hive_interactive_bin, hadoop_bin_dir)
    start_hiveserver2_interactive_script = 'startHiveserver2Interactive.sh.j2'
    start_hiveserver2_interactive_path = format(
        "{tmp_dir}/start_hiveserver2_interactive_script")
    hive_interactive_env_sh_template = config['configurations'][
        'hive-interactive-env']['content']
    hive_interactive_enabled = default(
        '/configurations/hive-interactive-env/enable_hive_interactive', False)
    llap_app_java_opts = default(
        '/configurations/hive-interactive-env/llap_java_opts',
        '-XX:+AlwaysPreTouch -XX:+UseG1GC -XX:TLABSize=8m -XX:+ResizeTLAB -XX:+UseNUMA -XX:+AggressiveOpts -XX:InitiatingHeapOccupancyPercent=70 -XX:+UnlockExperimentalVMOptions -XX:G1MaxNewSizePercent=40  -XX:MaxGCPauseMillis=200'
    )
    hive_interactive_heapsize = hive_heapsize
    llap_app_name = config['configurations']['hive-interactive-env'][
        'llap_app_name']
    # Ambari upgrade may not add this config as it will force restart of HSI (stack upgrade should)
    if 'hive_heapsize' in config['configurations']['hive-interactive-env']:
        hive_interactive_heapsize = config['configurations'][
            'hive-interactive-env']['hive_heapsize']

    # Service check related
    if hive_transport_mode.lower() == "http":
        hive_server_interactive_port = config['configurations'][
            'hive-interactive-site']['hive.server2.thrift.http.port']
    else:
        hive_server_interactive_port = default(
            '/configurations/hive-interactive-site/hive.server2.thrift.port',
            "10500")
    # Tez for Hive interactive related
    tez_interactive_conf_dir = status_params.tez_interactive_conf_dir
    tez_interactive_user = config['configurations']['tez-env']['tez_user']
    num_retries_for_checking_llap_status = config['configurations'][
        'hive-interactive-env']['num_retries_for_checking_llap_status']
    # Used in LLAP YARN Service package creation
    yarn_nm_mem = config['configurations']['yarn-site'][
        'yarn.nodemanager.resource.memory-mb']
    num_llap_daemon_running_nodes = config['configurations'][
        'hive-interactive-env']['num_llap_nodes_for_llap_daemons']
    num_llap_nodes = config['configurations']['hive-interactive-env'][
        'num_llap_nodes']
    llap_daemon_container_size = config['configurations'][
        'hive-interactive-site']['hive.llap.daemon.yarn.container.mb']
    llap_log_level = config['configurations']['hive-interactive-env'][
        'llap_log_level']
    llap_logger = default(
        '/configurations/hive-interactive-site/hive.llap.daemon.logger',
        'query-routing')
    hive_aux_jars = default(
        '/configurations/hive-interactive-env/hive_aux_jars', '')
    hive_llap_io_mem_size = config['configurations']['hive-interactive-site'][
        'hive.llap.io.memory.size']
    llap_heap_size = config['configurations']['hive-interactive-env'][
        'llap_heap_size']
    llap_app_name = config['configurations']['hive-interactive-env'][
        'llap_app_name']
    hive_llap_daemon_num_executors = config['configurations'][
        'hive-interactive-site']['hive.llap.daemon.num.executors']
    hive_llap_principal = None
    if security_enabled:
        hive_llap_keytab_file = config['configurations'][
            'hive-interactive-site']['hive.llap.daemon.keytab.file']
        hive_llap_principal = (
            config['configurations']['hive-interactive-site']
            ['hive.llap.daemon.service.principal']).replace(
            '_HOST', hostname.lower())
    pass

if security_enabled:
    hive_principal = hive_server_principal.replace('_HOST', hostname.lower())
    hive_keytab = config['configurations']['hive-site'][
        'hive.server2.authentication.kerberos.keytab']

    yarn_principal_name = config['configurations']['yarn-site'][
        'yarn.timeline-service.principal']
    yarn_principal_name = yarn_principal_name.replace('_HOST',
                                                      hostname.lower())
    yarn_keytab = config['configurations']['yarn-site'][
        'yarn.timeline-service.keytab']
    yarn_kinit_cmd = format(
        "{kinit_path_local} -kt {yarn_keytab} {yarn_principal_name};")

hive_cluster_token_zkstore = default(
    "/configurations/hive-site/hive.cluster.delegation.token.store.zookeeper.znode",
    None)
jaas_file = os.path.join(hive_config_dir, 'zkmigrator_jaas.conf')
hive_zk_namespace = default(
    "/configurations/hive-site/hive.zookeeper.namespace", None)

# ranger hive plugin section start

# ranger host
ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

# ranger hive plugin enabled property
enable_ranger_hive = config['configurations']['hive-env'][
                         'hive_security_authorization'].lower() == 'ranger'
doAs = config["configurations"]["hive-site"]["hive.server2.enable.doAs"]

xml_configurations_supported = True

xa_audit_db_is_enabled = False
xa_audit_db_password = ''

# get ranger hive properties if enable_ranger_hive is True
if enable_ranger_hive:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['admin-properties'][
        'policymgr_external_url']
    if xml_configurations_supported:
        policymgr_mgr_url = config['configurations']['ranger-hive-security'][
            'ranger.plugin.hive.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger hive service name
    repo_name = str(config['clusterName']) + '_hive'
    repo_name_value = config['configurations']['ranger-hive-security'][
        'ranger.plugin.hive.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    jdbc_driver_class_name = config['configurations'][
        'ranger-hive-plugin-properties']['jdbc.driverClassName']
    common_name_for_certificate = config['configurations'][
        'ranger-hive-plugin-properties']['common.name.for.certificate']
    repo_config_username = config['configurations'][
        'ranger-hive-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_hive:
        external_admin_username = default(
            '/configurations/ranger-hive-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-hive-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-hive-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-hive-plugin-properties/external_ranger_admin_password',
            'example!@#')

        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-hive-plugin-properties']
    policy_user = config['configurations']['ranger-hive-plugin-properties'][
        'policy_user']
    repo_config_password = config['configurations'][
        'ranger-hive-plugin-properties']['REPOSITORY_CONFIG_PASSWORD']

    ranger_hive_url = format("{hive_url}/default;principal={hive_principal}"
                             ) if security_enabled else hive_url
    if stack_supports_ranger_hive_jdbc_url_change:
        ranger_hive_url = hive_jdbc_url

    hive_ranger_plugin_config = {
        'username': repo_config_username,
        'password': repo_config_password,
        'jdbc.driverClassName': jdbc_driver_class_name,
        'jdbc.url': ranger_hive_url,
        'commonNameForCertificate': common_name_for_certificate
    }

    if security_enabled:
        hive_ranger_plugin_config['policy.download.auth.users'] = hive_user
        hive_ranger_plugin_config['tag.download.auth.users'] = hive_user
        hive_ranger_plugin_config['policy.grantrevoke.auth.users'] = hive_user

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        hive_ranger_plugin_config.update(custom_ranger_service_config)

    hive_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': hive_ranger_plugin_config,
        'description': 'hive repo',
        'name': repo_name,
        'type': 'hive'
    }

    xa_audit_hdfs_is_enabled = config['configurations']['ranger-hive-audit'][
        'xasecure.audit.destination.hdfs'] if xml_configurations_supported else False
    ssl_keystore_password = config['configurations']['ranger-hive-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations']['ranger-hive-policymgr-ssl'][
        'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# ranger hive plugin section end

# below property is used for cluster deployed in cloud env to create ranger hive service in ranger admin
# need to add it as custom property
ranger_hive_metastore_lookup = default(
    '/configurations/ranger-hive-plugin-properties/ranger.service.config.param.enable.hive.metastore.lookup',
    False)

if security_enabled:
    hive_metastore_principal_with_host = hive_metastore_principal.replace(
        '_HOST', hostname.lower())

# replication directories
hive_repl_cmrootdir = default('/configurations/hive-site/hive.repl.cmrootdir',
                              None)
hive_repl_rootdir = default('/configurations/hive-site/hive.repl.rootdir',
                            None)

# zookeeper
zk_quorum = ""
zookeeper_port = default('/configurations/zoo.cfg/clientPort', None)
if 'zookeeper_server_hosts' in config['clusterHostInfo']:
    for host in config['clusterHostInfo']['zookeeper_server_hosts']:
        if zk_quorum:
            zk_quorum += ','
        zk_quorum += host + ":" + str(zookeeper_port)

# For druid metadata password
druid_metadata_password = ""
if 'druid-common' in config['configurations'] \
        and 'druid.metadata.storage.connector.password' in config['configurations']['druid-common']:
    druid_metadata_password = config['configurations']['druid-common'][
        'druid.metadata.storage.connector.password']

# For druid storage directory, hive will write segments here
druid_storage_dir = ""
if 'druid-common' in config['configurations'] \
        and 'druid.storage.storageDirectory' in config['configurations']['druid-common']:
    druid_storage_dir = config['configurations']['druid-common'][
        'druid.storage.storageDirectory']

# beeline-site config

beeline_site_config = {
    'beeline.hs2.jdbc.url.container': hive_jdbc_url,
    'beeline.hs2.jdbc.url.default': 'container'
}

if has_hive_interactive:
    beeline_site_config['beeline.hs2.jdbc.url.llap'] = hsi_jdbc_url

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024 ** 3) * 0.8)

with open('/proc/mounts', 'r') as f:
    mounts = [
        line.split()[1] + '/hive' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

disk_partion = ','.join(mounts)

webhcat_bin_dir = install_dir + '/hcatalog/sbin/webhcat_server.sh'
webhcat_user = config['configurations']['hive-env']['webhcat_user']
webhcat_hdfs_user_dir = format("/user/{webhcat_user}")
hcat_hdfs_user_dir = format("/user/{webhcat_user}")
templeton_port = config['configurations']['webhcat-site']['templeton.port']
hcat_pid_dir = status_params.hcat_pid_dir
hcat_log_dir = config['configurations']['hive-env']['hcat_log_dir']
hcat_env_sh_template = config['configurations']['hcat-env']['content']
webhcat_log_maxfilesize = default("/configurations/webhcat-log4j/webhcat_log_maxfilesize", 256)
webhcat_log_maxbackupindex = default("/configurations/webhcat-log4j/webhcat_log_maxbackupindex", 20)
# webhcat-log4j.properties.template
if (('webhcat-log4j' in config['configurations']) and ('content' in config['configurations']['webhcat-log4j'])):
    log4j_webhcat_props = config['configurations']['webhcat-log4j']['content']
else:
    log4j_webhcat_props = None
webhcat_env_sh_template = config['configurations']['webhcat-env']['content']
templeton_log_dir = config['configurations']['hive-env']['hcat_log_dir']
templeton_pid_dir = status_params.hcat_pid_dir

webhcat_pid_file = status_params.webhcat_pid_file

templeton_jar = config['configurations']['webhcat-site']['templeton.jar']
webhcat_conf_dir = '/etc/hive'  # '/etc/hive/webhcat'
hcat_conf_dir = '/etc/hive'  # '/etc/hive/hcatalog'

hcat_lib = install_dir + '/hcatalog/share/hcatalog/'
webhcat_bin_dir = install_dir + '/hcatalog/sbin/'
webhcat_apps_dir = "/apps/webhcat"
hcat_dbroot = hcat_lib

webhcat_server_host = default("/clusterHostInfo/webhcat_server_hosts", [])

hcat_hdfs_user_dir = format("/user/{webhcat_user}")
hcat_hdfs_user_mode = 0755
webhcat_hdfs_user_dir = format("/user/{webhcat_user}")
webhcat_hdfs_user_mode = 0755

waggle_dance_federation_content = config['configurations']['hive-env']['waggle_dance_federation_content']
waggle_dance_server_content = config['configurations']['hive-env']['waggle_dance_server_content']