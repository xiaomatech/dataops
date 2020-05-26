#!/usr/bin/env python

import functools
import os

from ambari_commons.constants import AMBARI_SUDO_BINARY

from resource_management.libraries.functions import format
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.script import Script
from resource_management.libraries.functions import get_user_call_output

from status_params import *

# server configurations
java_home = config['hostLevelParams']['java_home']
ambari_cluster_name = config['clusterName']
java_version = expect("/hostLevelParams/java_version", int)
host_sys_prepped = default("/hostLevelParams/host_sys_prepped", False)

dpprofiler_hosts = default("/clusterHostInfo/dpprofiler_hosts", None)
if type(dpprofiler_hosts) is list:
    dpprofiler_host_name = dpprofiler_hosts[0]
else:
    dpprofiler_host_name = dpprofiler_hosts

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
sudo = AMBARI_SUDO_BINARY

credential_store_enabled = False
if 'credentialStoreEnabled' in config:
    credential_store_enabled = config['credentialStoreEnabled']
jdk_location = config['hostLevelParams']['jdk_location']

stack_root = Script.get_stack_root()
dpprofiler_root = 'profiler_agent'
dpprofiler_home = format('{stack_root}/{dpprofiler_root}')
dpprofiler_env = config['configurations']['dpprofiler-env']
dpprofiler_job_configs = config['configurations']['dpprofiler-job-config']
user_group = config['configurations']['cluster-env']['user_group']
dpprofiler_user = dpprofiler_env['dpprofiler.user']
dpprofiler_group = dpprofiler_env['dpprofiler.group']
dpprofiler_pid_dir = dpprofiler_env['dpprofiler.pid.dir']
dpprofiler_log_dir = dpprofiler_env['dpprofiler.log.dir']
dpprofiler_data_dir = dpprofiler_env['dpprofiler.data.dir']
dpprofiler_conf_dir = dpprofiler_env['dpprofiler.conf.dir']
dpprofiler_hadoop_conf_dir = dpprofiler_env['dpprofiler.hadoop.conf.dir']
logback_content = dpprofiler_env['logback.content']
dpprofiler_kerberos_principal = dpprofiler_env['dpprofiler.kerberos.principal']
dpprofiler_kerberos_keytab = dpprofiler_env['dpprofiler.kerberos.keytab']
dpprofiler_spnego_kerberos_principal = dpprofiler_env['dpprofiler.spnego.kerberos.principal']
dpprofiler_spnego_kerberos_keytab = dpprofiler_env['dpprofiler.spnego.kerberos.keytab']
dpprofiler_http_port = dpprofiler_env['dpprofiler.http.port']
dpprofiler_incremental_changedetector_cron = dpprofiler_env['dpprofiler.incremental.changedetector.cron']
dpprofiler_incremental_changedetector_keeprange = dpprofiler_env['dpprofiler.incremental.changedetector.keeprange']
dpprofiler_incremental_changedetector_purge_oldlogs = "false"
if dpprofiler_env['dpprofiler.incremental.changedetector.purge.oldlogs']:
    dpprofiler_incremental_changedetector_purge_oldlogs = "true"

dpprofiler_credential_provider_path = format("jceks://file{dpprofiler_conf_dir}/dpprofiler-config.jceks")

hiveserver2_interactive_jdbc_url = dpprofiler_env['hiveserver2.interactive.jdbc.url']
security_credentials_hiveserver2_enabled = dpprofiler_env['security.credentials.hiveserver2.enabled']
dpprofiler_extra_jars = dpprofiler_env["dpprofiler.extra.jars"]

dpprofiler_config = config['configurations']['dpprofiler-config']
dpprofiler_db_type = dpprofiler_config["dpprofiler.db.type"]
slick_driver_dict = {
    'h2': 'slick.driver.H2Driver$',
    'mysql': 'slick.driver.MySQLDriver$',
    'postgres': 'slick.driver.PostgresDriver$'
}
db_driver_dict = {
    'mysql': 'com.mysql.jdbc.Driver',
    'h2': 'org.h2.Driver',
    'postgres': 'org.postgresql.Driver'
}
dpprofiler_db_slick_driver = slick_driver_dict.get(dpprofiler_db_type)
dpprofiler_db_driver = db_driver_dict.get(dpprofiler_db_type)
dpprofiler_db_jdbc_url = dpprofiler_config["dpprofiler.db.jdbc.url"]
dpprofiler_db_user = dpprofiler_config["dpprofiler.db.user"]
dpprofiler_db_password = dpprofiler_config["dpprofiler.db.password"]

if credential_store_enabled:
    dpprofiler_db_password = "dpprofiler.db.password"

dpprofiler_spnego_signature_secret = dpprofiler_config["dpprofiler.spnego.signature.secret"]
if credential_store_enabled:
    dpprofiler_spnego_signature_secret = "dpprofiler.spnego.signature.secret"

dpprofiler_spnego_cookie_name = dpprofiler_config["dpprofiler.spnego.cookie.name"]

dpprofiler_profiler_hdfs_dir = dpprofiler_config["dpprofiler.profiler.hdfs.dir"]
dpprofiler_profiler_dwh_dir = dpprofiler_config["dpprofiler.profiler.dwh.dir"]
dpprofiler_profiler_dir = dpprofiler_config["dpprofiler.profiler.dir"]

dpprofiler_credential_provider_path = format("jceks://file{dpprofiler_conf_dir}/dpprofiler-config.jceks")
dpprofiler_credential_provider_tmp_path = format("{dpprofiler_conf_dir}/dpprofiler-config-tmp.jceks")
dpprofiler_credential_provider_crc_path = format("{dpprofiler_conf_dir}/.dpprofiler-config.jceks.crc")
dpprofiler_credential_provider_hdfs_path = format(
    "jceks://hdfs{dpprofiler_profiler_hdfs_dir}/security/dpprofiler-config.jceks")

dpprofiler_kerberos_ticket_refresh_cron = dpprofiler_env["dpprofiler.kerberos.ticket.refresh.cron"]
dpprofiler_kerberos_ticket_refresh_retry_allowed = dpprofiler_env["dpprofiler.kerberos.ticket.refresh.retry.allowed"]

dpprofiler_submitter_batch_size = dpprofiler_config["dpprofiler.submitter.batch.size"]
dpprofiler_submitter_jobs_max = dpprofiler_config["dpprofiler.submitter.jobs.max"]
dpprofiler_submitter_jobs_scan_seconds = dpprofiler_config["dpprofiler.submitter.jobs.scan.seconds"]
dpprofiler_submitter_queue_size = dpprofiler_config["dpprofiler.submitter.queue.size"]

dpprofiler_livy_config = config['configurations']['dpprofiler-livy-config']

livy_session_lifetime_minutes = dpprofiler_livy_config["livy.session.lifetime.minutes"]
livy_session_lifetime_requests = dpprofiler_livy_config["livy.session.lifetime.requests"]
livy_session_max_errors = dpprofiler_livy_config["livy.session.max.errors"]

livy_session_config_read_name = dpprofiler_livy_config["livy.session.config.read.name"]
livy_session_config_read_queue = dpprofiler_livy_config["livy.session.config.read.queue"]
livy_session_config_read_driverMemory = dpprofiler_livy_config["livy.session.config.read.driverMemory"]
livy_session_config_read_driverCores = dpprofiler_livy_config["livy.session.config.read.driverCores"]
livy_session_config_read_executorMemory = dpprofiler_livy_config["livy.session.config.read.executorMemory"]
livy_session_config_read_executorCores = dpprofiler_livy_config["livy.session.config.read.executorCores"]
livy_session_config_read_numExecutors = dpprofiler_livy_config["livy.session.config.read.numExecutors"]
livy_session_config_read_heartbeatTimeoutInSecond = dpprofiler_livy_config[
    "livy.session.config.read.heartbeatTimeoutInSecond"]
livy_session_config_read_timeoutInSeconds = dpprofiler_livy_config["livy.session.config.read.timeoutInSeconds"]

livy_session_config_write_name = dpprofiler_livy_config["livy.session.config.write.name"]
livy_session_config_write_queue = dpprofiler_livy_config["livy.session.config.write.queue"]
livy_session_config_write_driverMemory = dpprofiler_livy_config["livy.session.config.write.driverMemory"]
livy_session_config_write_driverCores = dpprofiler_livy_config["livy.session.config.write.driverCores"]
livy_session_config_write_executorMemory = dpprofiler_livy_config["livy.session.config.write.executorMemory"]
livy_session_config_write_executorCores = dpprofiler_livy_config["livy.session.config.write.executorCores"]
livy_session_config_write_numExecutors = dpprofiler_livy_config["livy.session.config.write.numExecutors"]
livy_session_config_write_heartbeatTimeoutInSecond = dpprofiler_livy_config[
    "livy.session.config.write.heartbeatTimeoutInSecond"]
livy_session_config_write_timeoutInSeconds = dpprofiler_livy_config["livy.session.config.write.timeoutInSeconds"]

profiler_job_executor_memory_min = dpprofiler_job_configs["profiler.job.executor.memory.min"]
profiler_job_executor_memory_max = dpprofiler_job_configs["profiler.job.executor.memory.max"]
profiler_job_executor_cores_min = dpprofiler_job_configs["profiler.job.executor.cores.min"]
profiler_job_executor_cores_max = dpprofiler_job_configs["profiler.job.executor.cores.max"]
profiler_job_executor_count_min = dpprofiler_job_configs["profiler.job.executor.count.min"]
profiler_job_executor_count_max = dpprofiler_job_configs["profiler.job.executor.count.max"]
profiler_job_driver_cores_min = dpprofiler_job_configs["profiler.job.driver.cores.min"]
profiler_job_driver_cores_max = dpprofiler_job_configs["profiler.job.driver.cores.max"]
profiler_job_driver_memory_min = dpprofiler_job_configs["profiler.job.driver.memory.min"]
profiler_job_driver_memory_max = dpprofiler_job_configs["profiler.job.driver.memory.max"]
scheduler_config_cron_frequency_check_enabled = dpprofiler_job_configs["scheduler.config.cron.frequency.check.enabled"]

dpprofiler_sso_knox_enabled = dpprofiler_env["dpprofiler.sso.knox.enabled"]
dpprofiler_sso_knox_public_key = dpprofiler_env["dpprofiler.sso.knox.public.key"]

dpprofiler_custom_config = dpprofiler_config["dpprofiler.custom.config"]

dpprofiler_crypto_secret = \
    get_user_call_output.get_user_call_output(format("date +%s | sha256sum | base64 | head -c 32 "),
                                              user=dpprofiler_user,
                                              is_checked_call=False)[1]

livy_hosts = default("/clusterHostInfo/livy2_server_hosts", [])

livy_url = ""

if len(livy_hosts) > 0:
    livy_livyserver_host = str(livy_hosts[0])
    livy_livyserver_port = config['configurations']['livy2-conf']['livy.server.port']
    livy_url = "http://" + livy_livyserver_host + ":" + livy_livyserver_port

dpprofiler_secured = "false"
if config['configurations']['cluster-env']['security_enabled']:
    dpprofiler_secured = "true"

dpprofiler_cluster_config_keys = dpprofiler_config["dpprofiler.cluster.config.keys"].split(";")
dpprofiler_cluster_configs = "isSecured=\"" + dpprofiler_secured + "\"\n"

dpprofiler_spark_cluster_configs = ""

for config_key in dpprofiler_cluster_config_keys:
    config_name = config_key.split("=")[0]
    config_file = config_key.split("=")[1].split("/")[0]
    config_key = config_key.split("=")[1].split("/")[1]
    if config_file in config['configurations'] and config_key in config['configurations'][config_file]:
        config_string = config_name + "=\"" + config['configurations'][config_file][config_key] + "\"\n"
        if config_key.startswith("hive"):
            dpprofiler_spark_cluster_configs += config_string
        else:
            dpprofiler_cluster_configs += config_string

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
hadoop_bin_dir = stack_root +  '/hadoop/bin'
hadoop_conf_dir = '/etc/hadoop'
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
hdfs_site = config['configurations']['hdfs-site']
default_fs = default("/clusterLevelParams/dfs_type", "")

atlas_rest_address = ""
atlas_username = ""
atlas_password = ""

if 'application-properties' in config['configurations']:
    atlas_rest_address = config['configurations']['application-properties']['atlas.rest.address']

if 'atlas-env' in config['configurations']:
    atlas_username = config['configurations']['atlas-env']["atlas.admin.username"]
    atlas_password = config['configurations']['atlas-env']["atlas.admin.password"]

atlas_password_alias = "dpprofiler.atlas.password"

ranger_username = ""
ranger_password = ""
ranger_audit_hdfs = ""
ranger_audit_hdfs_dir = ""
ranger_url = ""

if 'ranger-env' in config['configurations']:
    ranger_username = config['configurations']['ranger-env']['admin_username']
    ranger_password = config['configurations']['ranger-env']['admin_password']
    ranger_audit_hdfs = config['configurations']['ranger-env']['xasecure.audit.destination.hdfs']
    ranger_audit_hdfs_dir = config['configurations']['ranger-env']['xasecure.audit.destination.hdfs.dir']
    ranger_url = config['configurations']['admin-properties']['policymgr_external_url']

yarn_rm_address = ""

if "yarn-site" in config["configurations"]:
    yarn_rm_address = config["configurations"]["yarn-site"]["yarn.resourcemanager.webapp.address"]

# create partial functions with common arguments for every HdfsResource call
# to create hdfs directory we need to call params.HdfsResource in code
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
    default_fs=default_fs
)

# mysql driver download properties
patch_mysql_driver = dpprofiler_db_driver == "com.mysql.jdbc.Driver"
jdk_location = config['ambariLevelParams']['jdk_location']
jdbc_jar_name = default("/ambariLevelParams/custom_mysql_jdbc_name", None)
driver_source = format("{jdk_location}/{jdbc_jar_name}")
mysql_driver_target = os.path.join(dpprofiler_home, "lib/mysql-connector-java.jar")
