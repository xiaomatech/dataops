#!/usr/bin/env python

import functools
import os

from ambari_commons.credential_store_helper import get_password_from_credential_store
from resource_management.libraries.functions import format
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from status_params import *
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions.is_empty import is_empty
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.script import Script

config = Script.get_config()

# server configurations
java_home = config['ambariLevelParams']['java_home']
jdk_location = config['ambariLevelParams']['jdk_location']
dfs_type = default("/clusterLevelParams/dfs_type", "")
jdbc_jar_name = default("/ambariLevelParams/custom_mysql_jdbc_name", None)
hostname = config['agentLevelParams']['hostname']
ambari_cluster_name = config['clusterName']
java_version = expect("/hostLevelParams/java_version", int)
host_sys_prepped = default("/hostLevelParams/host_sys_prepped", False)

beacon_hosts = default("/clusterHostInfo/beacon_server_hosts", None)
if type(beacon_hosts) is list:
    beacon_host_name = beacon_hosts[0]
else:
    beacon_host_name = beacon_hosts

tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()


install_dir = stack_root + '/canal'
download_url = config['configurations']['beacon-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')
beacon_user = config['configurations']['beacon-env']['canal_user']

beacon_home_dir = stack_root + '/beacon'
beacon_root = beacon_home_dir
beacon_webapp_dir = beacon_home_dir + '/webapp'
beacon_home = beacon_home_dir
beacon_cluster_name = format('{ambari_cluster_name}')
credential_store_enabled = False
if 'credentialStoreEnabled' in config:
    credential_store_enabled = config['credentialStoreEnabled']
beacon_env = config['configurations']['beacon-env']
user_group = config['configurations']['cluster-env']['user_group']

beacon_cloud_cred_provider_dir = beacon_env['beacon_cloud_cred_provider_path']
beacon_plugin_staging_dir = beacon_env['beacon_plugin_staging_dir']
beacon_user = beacon_env['beacon_user']
beacon_pid_dir = beacon_env['beacon_pid_dir']
beacon_data_dir = beacon_env['beacon_data_dir']
beacon_log_dir = beacon_env['beacon_log_dir']
beacon_port = beacon_env['beacon_port']
beacon_knox_proxy_enabled = beacon_env['beacon_knox_proxy_enabled']
beacon_knox_preauth_topology = beacon_env['beacon_knox_preauth_topology']
beacon_knox_proxy_topology = beacon_env['beacon_knox_proxy_topology']
beacon_knox_proxy_token_threshold = beacon_env['beacon_knox_proxy_token_threshold']
beacon_principal = beacon_env['beacon_principal']
beacon_tls_port = beacon_env['beacon_tls_port']
beacon_tls_enabled = beacon_env['beacon_tls_enabled']
beacon_key_store = beacon_env['beacon_key_store']
beacon_trust_store = beacon_env['beacon_trust_store']
beacon_results_per_page = beacon_env['beacon_results_per_page']
beacon_max_results_per_page = beacon_env['beacon_max_results_per_page']
beacon_max_instance_count = beacon_env['beacon_max_instance_count']
beacon_app_path = format('{beacon_webapp_dir}/beacon')
beacon_socket_buffer_size = beacon_env['beacon_socket_buffer_size']
beacon_services = beacon_env['beacon_services']
beacon_hadoop_job_lookup_retries = beacon_env['beacon_hadoop_job_lookup_retries']
beacon_hadoop_job_lookup_delay = beacon_env['beacon_hadoop_job_lookup_delay']

beacon_store_driver = beacon_env['beacon_store_driver']
beacon_store_url = format(beacon_env['beacon_store_url'])
beacon_store_user = beacon_env['beacon_store_user']
beacon_store_alias = beacon_env['beacon_store_alias']
beacon_credential_provider_path = format("jceks://file{beacon_conf_dir}/beacon-env.jceks")
if not credential_store_enabled:
    beacon_store_password = beacon_env['beacon_store_password']
    beacon_key_store_password = beacon_env['beacon_key_store_password']
    beacon_trust_store_password = beacon_env['beacon_trust_store_password']
    beacon_key_password = beacon_env['beacon_key_password']
if credential_store_enabled:
    beacon_key_store_password_alias = 'beacon_key_store_password'
    beacon_trust_store_password_alias = 'beacon_trust_store_password'
    beacon_key_password_alias = 'beacon_key_password'
    beacon_store_alias = 'beacon_store_password'
beacon_store_schema_dir = format(beacon_env['beacon_store_schema_dir'])

beacon_quartz_prefix = beacon_env['beacon_quartz_prefix']
beacon_quartz_thread_pool = beacon_env['beacon_quartz_thread_pool']
beacon_retired_policy_older_than = beacon_env['beacon_retired_policy_older_than']
beacon_cleanup_service_frequency = beacon_env['beacon_cleanup_service_frequency']
beacon_house_keeping_threads = beacon_env['beacon_house_keeping_threads']
beacon_house_keeping_sync_frequency = beacon_env['beacon_house_keeping_sync_frequency']
beacon_house_keeping_sync_max_retry = beacon_env['beacon_house_keeping_sync_max_retry']
beacon_min_replication_frequency = beacon_env['beacon_min_replication_frequency']
beacon_replication_metrics_interval = beacon_env['beacon_replication_metrics_interval']
beacon_policy_check_frequency = beacon_env['beacon_policy_check_frequency']
beacon_auth_relogin_seconds = beacon_env['beacon_auth_relogin_seconds']
beacon_exclude_file_regex = beacon_env['beacon_exclude_file_regex']
beacon_store_max_connections = beacon_env['beacon_store_max_connections']
beacon_store_max_idle_connections = beacon_env['beacon_store_max_idle_connections']
beacon_store_min_idle_connections = beacon_env['beacon_store_min_idle_connections']
beacon_store_waittime_msecs = beacon_env['beacon_store_waittime_msecs']
beacon_store_connect_timeout_msecs = beacon_env['beacon_store_connect_timeout_msecs']
beacon_encryption_zones_refresh_frequency = beacon_env['beacon_encryption_zones_refresh_frequency']
beacon_snapshot_dirs_refresh_frequency = beacon_env['beacon_snapshot_dirs_refresh_frequency']
beacon_snapshot_retention_number = beacon_env['beacon_snapshot_retention_number']

beacon_bind_host = beacon_env['beacon_bind_host']
beacon_cloud_cred_provider_path = beacon_env['beacon_cloud_cred_provider_path']
beacon_preserve_meta = beacon_env['beacon_preserve_meta']
hive_bootstrap_job_retry_attempts = beacon_env['hive_bootstrap_job_retry_attempts']

ranger_client_connect_timeout = beacon_env['ranger_client_connect_timeout']
ranger_client_read_timeout = beacon_env['ranger_client_read_timeout']

atlas_client_connect_timeout = beacon_env['atlas_client_connect_timeout']
atlas_client_read_timeout = beacon_env['atlas_client_read_timeout']

beacon_max_file_list_per_page = beacon_env['beacon_max_file_list_per_page']

etc_prefix_dir = "/etc/beacon"

security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))

hadoop_home_dir = Script.get_stack_root() + '/hadoop'
hadoop_bin_dir = hadoop_home_dir + "/bin"
hadoop_conf_dir = '/etc/hadoop'
hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']

beacon_dbsetup_tool = 'com.hortonworks.beacon.tools.BeaconDBSetup'

hive_server_hosts = default('/clusterHostInfo/hive_server_host', [])
is_hive_installed = not len(hive_server_hosts) == 0

hdfs_namenode_hosts = default("/clusterHostInfo/namenode_host", [])
is_hdfs_installed = not len(hdfs_namenode_hosts) == 0

hive_site = config['configurations']['hive-site']
if 'hive-env' in config['configurations']:
    hive_user = config['configurations']['hive-env']['hive_user']
else:
    hive_user = "hive"
hive_repl_cmrootdir = hive_site['hive.repl.cmrootdir']
hive_repl_rootdir = hive_site['hive.repl.rootdir']

HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file="/var/lib/ambari-agent/data/.hdfs_resource_ignore",
    security_enabled=security_enabled,
    keytab=hdfs_user_keytab,
    kinit_path_local=kinit_path_local,
    hadoop_bin_dir=hadoop_bin_dir,
    hadoop_conf_dir=hadoop_conf_dir,
    principal_name=hdfs_principal_name,
    hdfs_site=hdfs_site,
    default_fs=default_fs,
    immutable_paths=get_not_managed_resources(),
    dfs_type=dfs_type
)

beacon_security_site = dict(config['configurations']['beacon-security-site'])
beacon_ranger_user = beacon_security_site['beacon.ranger.user']
beacon_atlas_password = ""
if credential_store_enabled:
    if 'hadoop.security.credential.provider.path' in beacon_security_site:
        cs_lib_path = beacon_security_site['credentialStoreClassPath']
        alias = 'beacon.ranger.password'
        provider_path = beacon_security_site['hadoop.security.credential.provider.path']
        beacon_ranger_password = get_password_from_credential_store(alias, provider_path, cs_lib_path, java_home,
                                                                    jdk_location)
        beacon_atlas_password_alias = 'beacon.atlas.password'
        beacon_atlas_password = get_password_from_credential_store(beacon_atlas_password_alias, provider_path,
                                                                   cs_lib_path, java_home, jdk_location)
    else:
        raise Exception(
            "hadoop.security.credential.provider.path property not found in beacon-security-site config-type")
else:
    beacon_ranger_password = beacon_security_site['beacon.ranger.password']
    beacon_atlas_password = default("/configurations/beacon-security-site/beacon.atlas.password", "")

ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

ranger_hive_plugin_enabled = False
if not is_empty(config['configurations']['hive-env']['hive_security_authorization']):
    ranger_hive_plugin_enabled = config['configurations']['hive-env']['hive_security_authorization'].lower() == 'ranger'

service_name = str(config['clusterName']) + '_hive'
service_name_value = config['configurations']['ranger-hive-security']['ranger.plugin.hive.service.name']
if not is_empty(service_name_value) and service_name_value != "{{repo_name}}":
    service_name = service_name_value

# mysql driver download properties
download_mysql_driver = beacon_store_driver == "com.mysql.jdbc.Driver"
driver_source = format("{jdk_location}/{jdbc_jar_name}")
mysql_driver_target = os.path.join(beacon_webapp_dir, "beacon/WEB-INF/lib/mysql-connector-java.jar")

ranger_atlas_plugin_enabled = False
if not is_empty(config['configurations']['ranger-atlas-plugin-properties']['ranger-atlas-plugin-enabled']):
    ranger_atlas_plugin_enabled = config['configurations']['ranger-atlas-plugin-properties'][
                                      'ranger-atlas-plugin-enabled'].lower() == 'yes'

beacon_atlas_user = default("/configurations/beacon-security-site/beacon.atlas.user", "beacon_atlas")
ranger_atlas_service_name = str(config['clusterName']) + '_atlas'
ranger_atlas_service_value = config['configurations']['ranger-atlas-security']['ranger.plugin.atlas.service.name']
if not is_empty(ranger_atlas_service_value) and ranger_atlas_service_value != "{{repo_name}}":
    ranger_atlas_service_name = ranger_atlas_service_value

is_stack_3_0_or_further = True
