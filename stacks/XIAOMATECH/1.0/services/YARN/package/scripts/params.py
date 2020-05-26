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

Ambari Agent

"""
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.copy_tarball import get_sysprep_skip_copy_tarballs_hdfs
import os

from resource_management.core import sudo
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import component_version
from resource_management.libraries.functions import format
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.expect import expect
from resource_management.libraries import functions
from resource_management.libraries.functions import is_empty
from resource_management.libraries.functions.get_architecture import get_architecture
import status_params
from functions import calc_heap_memory, ensure_unit_for_memory

import sys, os

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

import os
import multiprocessing

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes * 0.9 / (1024 ** 3))
mem_mib = int(mem_bytes * 0.9 / (1024 ** 2))

with open('/proc/mounts', 'r') as f:
    local_mounts = [
        line.split()[1] + '/yarn/nm-local-dir' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]
with open('/proc/mounts', 'r') as f:
    log_mounts = [
        line.split()[1] + '/yarn/log' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

nm_local_dirs = ','.join(local_mounts)
nm_log_dirs = ','.join(log_mounts)

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/hadoop'
download_url = config['configurations']['yarn-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

architecture = get_architecture()

stack_name = status_params.stack_name
stack_root = Script.get_stack_root()
tarball_map = default("/configurations/cluster-env/tarball_map", None)

config_path = status_params.hadoop_conf_dir
config_dir = os.path.realpath(config_path)

stack_supports_ru = True
stack_supports_timeline_state_store = True

# New Cluster Stack Version that is defined during the RESTART of a Stack Upgrade.
# It cannot be used during the initial Cluser Install because the version is not yet known.
version = default("/commandParams/version", None)

stack_supports_ranger_kerberos = True
stack_supports_ranger_audit_db = False

hostname = config['agentLevelParams']['hostname']

# hadoop default parameters
hadoop_home = status_params.hadoop_home
hadoop_libexec_dir = hadoop_home + "/libexec"
hadoop_bin = hadoop_home + "/sbin"
hadoop_bin_dir = hadoop_home + "/bin"
hadoop_lib_home = hadoop_home + "/lib"
hadoop_conf_dir = status_params.hadoop_conf_dir
hadoop_java_io_tmpdir = os.path.join(tmp_dir, "hadoop_java_io_tmpdir")

# MapR directory root
mapred_role_root = "mapreduce"
command_role = default("/role", "")

# YARN directory root
yarn_role_root = "yarn"

# defaults set to current based on role
hadoop_mapr_home = hadoop_home
hadoop_yarn_home = hadoop_home

# try to render the specific version
version = component_version.get_component_repository_version()
if version is None:
    version = default("/commandParams/version", None)

hadoop_mapred2_jar_location = hadoop_home + '/share/hadoop/mapreduce/'
mapred_bin = format("{hadoop_mapr_home}/bin")
yarn_bin = format("{hadoop_yarn_home}/bin")

if stack_supports_timeline_state_store:
    # Timeline Service property that was added timeline_state_store stack feature
    ats_leveldb_state_store_dir = default(
        '/configurations/yarn-site/yarn.timeline-service.leveldb-state-store.path',
        '/data1/hadoop/yarn/timeline')

# ats 1.5 properties
entity_groupfs_active_dir = config['configurations']['yarn-site'][
    'yarn.timeline-service.entity-group-fs-store.active-dir']
entity_groupfs_active_dir_mode = 01777
entity_groupfs_store_dir = config['configurations']['yarn-site'][
    'yarn.timeline-service.entity-group-fs-store.done-dir']
entity_groupfs_store_dir_mode = 0700

sharedcache_dir = default('/configurations/yarn-site/yarn.sharedcache.root-dir', '/sharedcache')

hadoop_conf_secure_dir = os.path.join(hadoop_conf_dir, "secure")

limits_conf_dir = "/etc/security/limits.d"
yarn_user_nofile_limit = default(
    "/configurations/yarn-env/yarn_user_nofile_limit", "1048576")
yarn_user_nproc_limit = default(
    "/configurations/yarn-env/yarn_user_nproc_limit", "65536")

mapred_user_nofile_limit = default(
    "/configurations/mapred-env/mapred_user_nofile_limit", "1048576")
mapred_user_nproc_limit = default(
    "/configurations/mapred-env/mapred_user_nproc_limit", "65536")

execute_path = os.environ[
                   'PATH'] + os.pathsep + hadoop_bin_dir + os.pathsep + yarn_bin

ulimit_cmd = "ulimit -c unlimited;"

mapred_user = status_params.mapred_user
yarn_user = status_params.yarn_user
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_tmp_dir = default("/configurations/hadoop-env/hdfs_tmp_dir", "/tmp")

smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_hdfs_user_mode = 0770
security_enabled = config['configurations']['cluster-env']['security_enabled']
nm_security_marker_dir = "/var/lib/hadoop-yarn"
nm_security_marker = format('{nm_security_marker_dir}/nm_security_enabled')
current_nm_security_state = os.path.isfile(nm_security_marker)
toggle_nm_security = (current_nm_security_state and not security_enabled) or (
        not current_nm_security_state and security_enabled)
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']

mapred2_service_check_test_file = format('{tmp_dir}/mapred2-service-check')

yarn_executor_container_group = config['configurations']['yarn-site'][
    'yarn.nodemanager.linux-container-executor.group']
yarn_nodemanager_container_executor_class = config['configurations'][
    'yarn-site']['yarn.nodemanager.container-executor.class']
is_linux_container_executor = (
        yarn_nodemanager_container_executor_class ==
        'org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor')
container_executor_mode = 06050 if is_linux_container_executor else 02050
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
yarn_http_policy = config['configurations']['yarn-site']['yarn.http.policy']
yarn_https_on = (yarn_http_policy.upper() == 'HTTPS_ONLY')
rm_hosts = config['clusterHostInfo']['resourcemanager_hosts']
rm_host = rm_hosts[0]
rm_port = config['configurations']['yarn-site'][
    'yarn.resourcemanager.webapp.address'].split(':')[-1]
rm_https_port = default(
    '/configurations/yarn-site/yarn.resourcemanager.webapp.https.address',
    ":8090").split(':')[-1]

java64_home = config['ambariLevelParams']['java_home']
java_exec = format("{java64_home}/bin/java")
hadoop_ssl_enabled = default("/configurations/core-site/hadoop.ssl.enabled",
                             False)
java_version = expect("/ambariLevelParams/java_version", int)

yarn_heapsize = config['configurations']['yarn-env']['yarn_heapsize']
resourcemanager_heapsize = config['configurations']['yarn-env'][
    'resourcemanager_heapsize']
nodemanager_heapsize = config['configurations']['yarn-env'][
    'nodemanager_heapsize']
apptimelineserver_heapsize = default(
    "/configurations/yarn-env/apptimelineserver_heapsize", 1024)
ats_leveldb_dir = config['configurations']['yarn-site'][
    'yarn.timeline-service.leveldb-timeline-store.path']
ats_leveldb_lock_file = os.path.join(ats_leveldb_dir,
                                     "leveldb-timeline-store.ldb", "LOCK")
yarn_log_dir_prefix = config['configurations']['yarn-env'][
    'yarn_log_dir_prefix']
yarn_pid_dir_prefix = status_params.yarn_pid_dir_prefix
mapred_pid_dir_prefix = status_params.mapred_pid_dir_prefix
mapred_log_dir_prefix = config['configurations']['mapred-env'][
    'mapred_log_dir_prefix']
mapred_env_sh_template = config['configurations']['mapred-env']['content']
yarn_env_sh_template = config['configurations']['yarn-env']['content']
container_executor_cfg_template = config['configurations'][
    'container-executor']['content']
yarn_nodemanager_recovery_dir = default(
    '/configurations/yarn-site/yarn.nodemanager.recovery.dir', None)
service_check_queue_name = default(
    '/configurations/yarn-env/service_check.queue.name', 'default')

if len(rm_hosts) > 1:
    additional_rm_host = rm_hosts[1]
    rm_webui_address = format(
        "{rm_host}:{rm_port},{additional_rm_host}:{rm_port}")
    rm_webui_https_address = format(
        "{rm_host}:{rm_https_port},{additional_rm_host}:{rm_https_port}")
else:
    rm_webui_address = format("{rm_host}:{rm_port}")
    rm_webui_https_address = format("{rm_host}:{rm_https_port}")

if security_enabled:
    tc_mode = 0644
    tc_owner = "root"
else:
    tc_mode = None
    tc_owner = hdfs_user

nm_webui_address = config['configurations']['yarn-site'][
    'yarn.nodemanager.webapp.address']
hs_webui_address = config['configurations']['mapred-site'][
    'mapreduce.jobhistory.webapp.address']
nm_address = config['configurations']['yarn-site'][
    'yarn.nodemanager.address']  # still contains 0.0.0.0
if hostname and nm_address and nm_address.startswith("0.0.0.0:"):
    nm_address = nm_address.replace("0.0.0.0", hostname)

nm_local_dirs_list = nm_local_dirs.split(',')
nm_log_dirs_list = nm_log_dirs.split(',')

nm_log_dir_to_mount_file = "/var/lib/ambari-agent/data/yarn/yarn_log_dir_mount.hist"
nm_local_dir_to_mount_file = "/var/lib/ambari-agent/data/yarn/yarn_local_dir_mount.hist"

distrAppJarName = "hadoop-yarn-applications-distributedshell-3.*.jar"
hadoopMapredExamplesJarName = "hadoop-mapreduce-examples-3.*.jar"

entity_file_history_directory = "/tmp/entity-file-history/active"

yarn_pid_dir = status_params.yarn_pid_dir
mapred_pid_dir = status_params.mapred_pid_dir

mapred_log_dir = format("{mapred_log_dir_prefix}/{mapred_user}")
yarn_log_dir = format("{yarn_log_dir_prefix}/{yarn_user}")
mapred_job_summary_log = format(
    "{mapred_log_dir_prefix}/{mapred_user}/hadoop-mapreduce.jobsummary.log")
yarn_job_summary_log = format(
    "{yarn_log_dir_prefix}/{yarn_user}/hadoop-mapreduce.jobsummary.log")

user_group = config['configurations']['cluster-env']['user_group']

# exclude file
if 'all_decommissioned_hosts' in config['commandParams']:
    exclude_hosts = config['commandParams']['all_decommissioned_hosts'].split(
        ",")
else:
    exclude_hosts = []
exclude_file_path = default(
    "/configurations/yarn-site/yarn.resourcemanager.nodes.exclude-path",
    "/etc/hadoop/yarn.exclude")
rm_nodes_exclude_dir = os.path.dirname(exclude_file_path)

nm_hosts = default("/clusterHostInfo/nodemanager_hosts", [])
# incude file
include_file_path = default(
    "/configurations/yarn-site/yarn.resourcemanager.nodes.include-path", None)
include_hosts = None
manage_include_files = default(
    "/configurations/yarn-site/manage.include.files", False)
if include_file_path and manage_include_files:
    rm_nodes_include_dir = os.path.dirname(include_file_path)
    include_hosts = list(set(nm_hosts) - set(exclude_hosts))

ats_host = default("/clusterHostInfo/app_timeline_server_hosts", [])
has_ats = not len(ats_host) == 0

atsv2_host = default("/clusterHostInfo/timeline_reader_hosts", [])
has_atsv2 = not len(atsv2_host) == 0

timeline_reader_address_http = format(
    "{atsv2_host[0]}:8198"
) if has_atsv2 else ""  # after stack_upgrade, timeline_reader can be absent
timeline_reader_address_https = format(
    "{atsv2_host[0]}:8199"
) if has_atsv2 else ""  # after stack_upgrade, timeline_reader can be absent

registry_dns_host = default("/clusterHostInfo/yarn_registry_dns_hosts", [])
has_registry_dns = not len(registry_dns_host) == 0

# don't using len(nm_hosts) here, because check can take too much time on large clusters
number_of_nm = 1

hs_host = default("/clusterHostInfo/historyserver_hosts", [])
has_hs = not len(hs_host) == 0

# default kinit commands
rm_kinit_cmd = ""
yarn_timelineservice_kinit_cmd = ""
nodemanager_kinit_cmd = ""

rm_zk_address = config['configurations']['yarn-site'][
    'yarn.resourcemanager.zk-address']
rm_zk_znode = config['configurations']['yarn-site'][
    'yarn.resourcemanager.zk-state-store.parent-path']
rm_zk_store_class = config['configurations']['yarn-site'][
    'yarn.resourcemanager.store.class']
rm_zk_failover_znode = default(
    '/configurations/yarn-site/yarn.resourcemanager.ha.automatic-failover.zk-base-path',
    '/yarn-leader-election')
hadoop_registry_zk_root = default(
    '/configurations/yarn-site/hadoop.registry.zk.root', '/registry')

if security_enabled:
    rm_principal_name = config['configurations']['yarn-site'][
        'yarn.resourcemanager.principal']
    rm_principal_name = rm_principal_name.replace('_HOST', hostname.lower())
    rm_keytab = config['configurations']['yarn-site'][
        'yarn.resourcemanager.keytab']
    rm_kinit_cmd = format(
        "{kinit_path_local} -kt {rm_keytab} {rm_principal_name};")
    yarn_jaas_file = os.path.join(config_dir, 'yarn_jaas.conf')
    rm_security_opts = format(
        '-Dzookeeper.sasl.client=true -Dzookeeper.sasl.client.username=zookeeper -Djava.security.auth.login.config={yarn_jaas_file} -Dzookeeper.sasl.clientconfig=Client'
    )

    # YARN timeline security options
    if has_ats or has_atsv2:
        yarn_timelineservice_principal_name = config['configurations'][
            'yarn-site']['yarn.timeline-service.principal']
        yarn_timelineservice_principal_name = yarn_timelineservice_principal_name.replace(
            '_HOST', hostname.lower())
        yarn_timelineservice_keytab = config['configurations']['yarn-site'][
            'yarn.timeline-service.keytab']
        yarn_timelineservice_kinit_cmd = format(
            "{kinit_path_local} -kt {yarn_timelineservice_keytab} {yarn_timelineservice_principal_name};"
        )
        yarn_ats_jaas_file = os.path.join(config_dir, 'yarn_ats_jaas.conf')

    if has_registry_dns:
        yarn_registry_dns_principal_name = config['configurations'][
            'yarn-env']['yarn.registry-dns.principal']
        yarn_registry_dns_principal_name = yarn_registry_dns_principal_name.replace(
            '_HOST', hostname.lower())
        yarn_registry_dns_keytab = config['configurations']['yarn-env'][
            'yarn.registry-dns.keytab']
        yarn_registry_dns_jaas_file = os.path.join(
            config_dir, 'yarn_registry_dns_jaas.conf')

    if 'yarn.nodemanager.principal' in config['configurations']['yarn-site']:
        nodemanager_principal_name = default(
            '/configurations/yarn-site/yarn.nodemanager.principal', None)
        if nodemanager_principal_name:
            nodemanager_principal_name = nodemanager_principal_name.replace(
                '_HOST', hostname.lower())

        nodemanager_keytab = config['configurations']['yarn-site'][
            'yarn.nodemanager.keytab']
        nodemanager_kinit_cmd = format(
            "{kinit_path_local} -kt {nodemanager_keytab} {nodemanager_principal_name};"
        )
        yarn_nm_jaas_file = os.path.join(config_dir, 'yarn_nm_jaas.conf')

    if has_hs:
        mapred_jhs_principal_name = config['configurations']['mapred-site'][
            'mapreduce.jobhistory.principal']
        mapred_jhs_principal_name = mapred_jhs_principal_name.replace(
            '_HOST', hostname.lower())
        mapred_jhs_keytab = config['configurations']['mapred-site'][
            'mapreduce.jobhistory.keytab']
        mapred_jaas_file = os.path.join(config_dir, 'mapred_jaas.conf')

yarn_log_aggregation_enabled = config['configurations']['yarn-site'][
    'yarn.log-aggregation-enable']
yarn_nm_app_log_dir = config['configurations']['yarn-site'][
    'yarn.nodemanager.remote-app-log-dir']
mapreduce_jobhistory_intermediate_done_dir = config['configurations'][
    'mapred-site']['mapreduce.jobhistory.intermediate-done-dir']
mapreduce_jobhistory_done_dir = config['configurations']['mapred-site'][
    'mapreduce.jobhistory.done-dir']
jobhistory_heapsize = default("/configurations/mapred-env/jobhistory_heapsize",
                              "900")
jhs_leveldb_state_store_dir = default(
    '/configurations/mapred-site/mapreduce.jobhistory.recovery.store.leveldb.path',
    "/data1/hadoop/mapreduce/jhs")


# for create_hdfs_directory
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name']
hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']
is_webhdfs_enabled = hdfs_site['dfs.webhdfs.enabled']

# Path to file that contains list of HDFS resources to be skipped during processing
hdfs_resource_ignore_file = "/var/lib/ambari-agent/data/.hdfs_resource_ignore"

dfs_type = default("/clusterLevelParams/dfs_type", "")

import functools

# create partial functions with common arguments for every HdfsResource call
# to create/delete hdfs directory/file/copyfromlocal we need to call params.HdfsResource in code
HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file=hdfs_resource_ignore_file,
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
update_files_only = default("/commandParams/update_files_only", False)

mapred_tt_group = default(
    "/configurations/mapred-site/mapreduce.tasktracker.group", user_group)

# taskcontroller.cfg

mapred_local_dir = "/tmp/hadoop-mapred/mapred/local"
hdfs_log_dir_prefix = config['configurations']['hadoop-env'][
    'hdfs_log_dir_prefix']

# Node labels
node_labels_dir = default(
    "/configurations/yarn-site/yarn.node-labels.fs-store.root-dir", None)
node_label_enable = config['configurations']['yarn-site'][
    'yarn.node-labels.enabled']

cgroups_dir = "/cgroups_test/cpu"

ranger_admin_log_dir = default(
    "/configurations/ranger-env/ranger_admin_log_dir", "/var/log/ranger/admin")

scheme = 'http' if not yarn_https_on else 'https'
yarn_rm_address = config['configurations']['yarn-site'][
    'yarn.resourcemanager.webapp.address'] if not yarn_https_on else config[
    'configurations']['yarn-site'][
    'yarn.resourcemanager.webapp.https.address']
rm_active_port = rm_https_port if yarn_https_on else rm_port

rm_ha_enabled = False
rm_ha_id = None
rm_ha_ids_list = []
rm_webapp_addresses_list = [yarn_rm_address]
rm_ha_ids = default("/configurations/yarn-site/yarn.resourcemanager.ha.rm-ids",
                    None)

if rm_ha_ids:
    rm_ha_ids_list = rm_ha_ids.split(",")
    if len(rm_ha_ids_list) > 1:
        rm_ha_enabled = True

if rm_ha_enabled:
    rm_webapp_addresses_list = []
    for rm_id in rm_ha_ids_list:
        rm_webapp_address_property = format(
            'yarn.resourcemanager.webapp.address.{rm_id}'
        ) if not yarn_https_on else format(
            'yarn.resourcemanager.webapp.https.address.{rm_id}')
        rm_webapp_address = config['configurations']['yarn-site'][
            rm_webapp_address_property]
        rm_webapp_addresses_list.append(rm_webapp_address)
        rm_host_name = config['configurations']['yarn-site'][format(
            'yarn.resourcemanager.hostname.{rm_id}')]
        if rm_host_name == hostname.lower():
            rm_ha_id = rm_id
# for curl command in ranger plugin to get db connector
jdk_location = config['ambariLevelParams']['jdk_location']

# ranger yarn plugin section start
xa_audit_db_is_enabled = False
xa_audit_db_password = ''
# ranger host
ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0

xml_configurations_supported = True

# ranger yarn plugin enabled property
enable_ranger_yarn = default(
    "/configurations/ranger-yarn-plugin-properties/ranger-yarn-plugin-enabled",
    "No")
enable_ranger_yarn = True if enable_ranger_yarn.lower() == 'yes' else False

# ranger yarn-plugin supported flag, instead of using is_supported_yarn_ranger/yarn-env, using stack feature
is_supported_yarn_ranger = True

# get ranger yarn properties if enable_ranger_yarn is True
if enable_ranger_yarn and is_supported_yarn_ranger:
    # get ranger policy url
    policymgr_mgr_url = config['configurations']['ranger-yarn-security'][
        'ranger.plugin.yarn.policy.rest.url']

    if not is_empty(policymgr_mgr_url) and policymgr_mgr_url.endswith('/'):
        policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

    # ranger yarn service/repository name
    repo_name = str(config['clusterName']) + '_yarn'
    repo_name_value = config['configurations']['ranger-yarn-security'][
        'ranger.plugin.yarn.service.name']
    if not is_empty(repo_name_value) and repo_name_value != "{{repo_name}}":
        repo_name = repo_name_value

    # ranger-env config
    ranger_env = config['configurations']['ranger-env']

    # create ranger-env config having external ranger credential properties
    if not has_ranger_admin and enable_ranger_yarn:
        external_admin_username = default(
            '/configurations/ranger-yarn-plugin-properties/external_admin_username',
            'admin')
        external_admin_password = default(
            '/configurations/ranger-yarn-plugin-properties/external_admin_password',
            'admin')
        external_ranger_admin_username = default(
            '/configurations/ranger-yarn-plugin-properties/external_ranger_admin_username',
            'ranger_admin')
        external_ranger_admin_password = default(
            '/configurations/ranger-yarn-plugin-properties/external_ranger_admin_password',
            'example!@#')

        ranger_env = {}
        ranger_env['admin_username'] = external_admin_username
        ranger_env['admin_password'] = external_admin_password
        ranger_env['ranger_admin_username'] = external_ranger_admin_username
        ranger_env['ranger_admin_password'] = external_ranger_admin_password

    ranger_plugin_properties = config['configurations'][
        'ranger-yarn-plugin-properties']
    policy_user = config['configurations']['ranger-yarn-plugin-properties'][
        'policy_user']
    yarn_rest_url = config['configurations']['yarn-site'][
        'yarn.resourcemanager.webapp.address']

    ranger_plugin_config = {
        'username':
            config['configurations']['ranger-yarn-plugin-properties']
            ['REPOSITORY_CONFIG_USERNAME'],
        'password':
            unicode(config['configurations']['ranger-yarn-plugin-properties']
                    ['REPOSITORY_CONFIG_PASSWORD']),
        'yarn.url':
            format('{scheme}://{yarn_rest_url}'),
        'commonNameForCertificate':
            config['configurations']['ranger-yarn-plugin-properties']
            ['common.name.for.certificate'],
        'hadoop.security.authentication':
            'kerberos' if security_enabled else 'simple'
    }

    if security_enabled:
        ranger_plugin_config['policy.download.auth.users'] = yarn_user
        ranger_plugin_config['tag.download.auth.users'] = yarn_user

    ranger_plugin_config['setup.additional.default.policies'] = "true"
    ranger_plugin_config[
        'default-policy.1.name'] = "Service Check User Policy for Yarn"
    ranger_plugin_config[
        'default-policy.1.resource.queue'] = service_check_queue_name
    ranger_plugin_config['default-policy.1.policyItem.1.users'] = policy_user
    ranger_plugin_config[
        'default-policy.1.policyItem.1.accessTypes'] = "submit-app"

    custom_ranger_service_config = generate_ranger_service_config(
        ranger_plugin_properties)
    if len(custom_ranger_service_config) > 0:
        ranger_plugin_config.update(custom_ranger_service_config)

    yarn_ranger_plugin_repo = {
        'isEnabled': 'true',
        'configs': ranger_plugin_config,
        'description': 'yarn repo',
        'name': repo_name,
        'repositoryType': 'yarn',
        'type': 'yarn',
        'assetType': '1'
    }

    xa_audit_hdfs_is_enabled = config['configurations']['ranger-yarn-audit'][
        'xasecure.audit.destination.hdfs'] if xml_configurations_supported else False
    ssl_keystore_password = config['configurations']['ranger-yarn-policymgr-ssl'][
        'xasecure.policymgr.clientssl.keystore.password'] if xml_configurations_supported else None
    ssl_truststore_password = config['configurations']['ranger-yarn-policymgr-ssl'][
        'xasecure.policymgr.clientssl.truststore.password'] if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks')

# need this to capture cluster name from where ranger yarn plugin is enabled
cluster_name = config['clusterName']

# ranger yarn plugin end section

# container-executor properties
min_user_id = config['configurations']['container-executor']['min_user_id']
docker_module_enabled = str(config['configurations']['container-executor']
                            ['docker_module_enabled']).lower()
docker_binary = config['configurations']['container-executor']['docker_binary']
docker_allowed_capabilities = config['configurations']['yarn-site'][
    'yarn.nodemanager.runtime.linux.docker.capabilities']
if docker_allowed_capabilities:
    docker_allowed_capabilities = ','.join(
        x.strip() for x in docker_allowed_capabilities.split(','))
else:
    docker_allowed_capabilities = ""
docker_allowed_devices = config['configurations']['container-executor'][
    'docker_allowed_devices']
docker_allowed_networks = config['configurations']['yarn-site'][
    'yarn.nodemanager.runtime.linux.docker.allowed-container-networks']
if docker_allowed_networks:
    docker_allowed_networks = ','.join(
        x.strip() for x in docker_allowed_networks.split(','))
else:
    docker_allowed_networks = ""
docker_allowed_ro_mounts = config['configurations']['container-executor'][
    'docker_allowed_ro-mounts']
docker_allowed_rw_mounts = config['configurations']['container-executor'][
    'docker_allowed_rw-mounts']
docker_privileged_containers_enabled = str(
    config['configurations']['container-executor']
    ['docker_privileged-containers_enabled']).lower()
docker_trusted_registries = config['configurations']['container-executor'][
    'docker_trusted_registries']
docker_allowed_volume_drivers = config['configurations']['container-executor'][
    'docker_allowed_volume-drivers']

# ATSv2 integration properties started.
yarn_timelinereader_pid_file = status_params.yarn_timelinereader_pid_file

cluster_zookeeper_quorum_hosts = ",".join(
    config['clusterHostInfo']['zookeeper_server_hosts'])
if 'zoo.cfg' in config['configurations'] and 'clientPort' in config[
    'configurations']['zoo.cfg']:
    cluster_zookeeper_clientPort = config['configurations']['zoo.cfg'][
        'clientPort']
else:
    cluster_zookeeper_clientPort = '2181'

zookeeper_quorum_hosts = cluster_zookeeper_quorum_hosts
zookeeper_clientPort = cluster_zookeeper_clientPort
yarn_service_app_hdfs_path = format("/apps/yarn")
if rm_ha_id is not None:
    yarn_service_app_hdfs_path = format(
        "{yarn_service_app_hdfs_path}/{rm_ha_id}")
yarn_service_dep_source_path = format("{hadoop_home}/lib/service-dep.tar.gz")

timeline_collector = ""
yarn_timeline_service_version = config['configurations']['yarn-site'][
    'yarn.timeline-service.version']
yarn_timeline_service_versions = config['configurations']['yarn-site'][
    'yarn.timeline-service.versions']
yarn_timeline_service_enabled = config['configurations']['yarn-site'][
    'yarn.timeline-service.enabled']

if yarn_timeline_service_enabled:
    if is_empty(yarn_timeline_service_versions):
        if yarn_timeline_service_version == '2.0' or yarn_timeline_service_version == '2':
            timeline_collector = "timeline_collector"
    else:
        ts_version_list = yarn_timeline_service_versions.split(',')
        for ts_version in ts_version_list:
            if '2.0' in ts_version or ts_version == '2':
                timeline_collector = "timeline_collector"
                break

yarn_user_hbase_permissions = "RWXCA"

if security_enabled and has_atsv2:
    yarn_ats_principal_name = config['configurations']['yarn-env'][
        'yarn_ats_principal_name']
    yarn_ats_user_keytab = config['configurations']['yarn-env'][
        'yarn_ats_user_keytab']

# System service configuration as part of ATSv2.
yarn_system_service_dir = config['configurations']['yarn-site'][
    'yarn.service.system-service.dir']

# ATSv2 integration properties ended

gpu_module_enabled = str(config['configurations']['container-executor']
                         ['gpu_module_enabled']).lower()
cgroup_root = config['configurations']['container-executor']['cgroup_root']
yarn_hierarchy = config['configurations']['container-executor'][
    'yarn_hierarchy']

# registry dns service
registry_dns_needs_privileged_access = status_params.registry_dns_needs_privileged_access

mount_table_content = None
if 'viewfs-mount-table' in config['configurations']:
    xml_inclusion_file_name = 'viewfs-mount-table.xml'
    mount_table = config['configurations']['viewfs-mount-table']

    if 'content' in mount_table and mount_table['content'].strip():
        mount_table_content = mount_table['content']

rm_cross_origin_enabled = config['configurations']['yarn-site'][
    'yarn.resourcemanager.webapp.cross-origin.enabled']

cross_origins = '*'
if rm_cross_origin_enabled:
    host_suffix = rm_host.rsplit('.', 2)[1:]
    if len(host_suffix) == 2:
        cross_origins = 'regex:.*[.]' + '[.]'.join(host_suffix) + "(:\d*)?"

ams_collector_hosts = ",".join(
    default("/clusterHostInfo/metrics_collector_hosts", []))
has_metric_collector = not len(ams_collector_hosts) == 0
if has_metric_collector:
    if 'cluster-env' in config[
        'configurations'] and 'metrics_collector_external_port' in config[
        'configurations']['cluster-env']:
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
    host_in_memory_aggregation = default(
        "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation",
        True)
    host_in_memory_aggregation_port = default(
        "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation.port",
        61888)

metrics_report_interval = default(
    "/configurations/ams-site/timeline.metrics.sink.report.interval", 60)
metrics_collection_period = default(
    "/configurations/ams-site/timeline.metrics.sink.collection.period", 10)

is_aggregation_https_enabled = False
if default(
        "/configurations/ams-site/timeline.metrics.host.inmemory.aggregation.http.policy",
        "HTTP_ONLY") == "HTTPS_ONLY":
    host_in_memory_aggregation_protocol = 'https'
    is_aggregation_https_enabled = True
else:
    host_in_memory_aggregation_protocol = 'http'

sysprep_skip_copy_tarballs_hdfs = get_sysprep_skip_copy_tarballs_hdfs()
retryAble = default("/commandParams/command_retry_enabled", False)

spark_home = Script.get_stack_root() + '/spark'
