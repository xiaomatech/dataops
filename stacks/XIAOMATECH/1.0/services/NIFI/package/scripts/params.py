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

from resource_management import *
from resource_management import get_bare_principal
from resource_management.libraries.script.script import Script
import os, socket, re
from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.version_select_util import *
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions.get_port_from_url import get_port_from_url
import ambari_simplejson as json
import config_utils

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()
zk_root = Script.get_stack_root()
tmp_dir = Script.get_tmp_dir()

stack_name = default("/clusterLevelParams/stack_name", None)
stack_version_buildnum = default("/commandParams/version", None)
zk_stack_version_buildnum = default("/commandParams/version", None)

install_dir = stack_root + '/nifi'
download_url = config['configurations']['nifi-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

toolkit_install_dir = stack_root + '/nifi-toolkit'
toolkit_download_url = config['configurations']['nifi-toolkit-env'][
    'download_url']
toolkit_filename = toolkit_download_url.split('/')[-1]
toolkit_version_dir = toolkit_filename.replace('.tar.gz', '').replace(
    '.tgz', '')

service_name = 'nifi'

script_dir = os.path.dirname(__file__)
toolkit_files_dir = os.path.realpath(
    os.path.join(os.path.dirname(script_dir), 'files'))
toolkit_tmp_dir = tmp_dir

# Version being upgraded/downgraded to
version = default("/commandParams/version", None)
# upgrade direction
upgrade_direction = default("/commandParams/upgrade_direction", None)

nifi_install_dir = install_dir
# nifi registry properties
if 'nifi-registry-ambari-config' in config['configurations']:
    nifi_registry_port = config['configurations'][
        'nifi-registry-ambari-config']['nifi.registry.port']
    nifi_registry_ssl_port = config['configurations'][
        'nifi-registry-ambari-config']['nifi.registry.port.ssl']
    nifi_registry_ssl_enabled = config['configurations'][
        'nifi-registry-ambari-ssl-config']['nifi.registry.ssl.isenabled']
    nifi_registry_url_port = nifi_registry_ssl_port if nifi_registry_ssl_enabled else nifi_registry_port
    nifi_registry_master_hosts = default(
        "/clusterHostInfo/nifi_registry_master_hosts", [])
    nifi_registry_host = None if len(
        nifi_registry_master_hosts) == 0 else nifi_registry_master_hosts[0]
    nifi_registry_protocol = "https" if nifi_registry_ssl_enabled else "http"
    nifi_registry_url = format(
        "{nifi_registry_protocol}://{nifi_registry_host}:{nifi_registry_url_port}"
    )
else:
    nifi_registry_url = None

# params from nifi-ambari-config
nifi_initial_mem = config['configurations']['nifi-ambari-config'][
    'nifi.initial_mem']
nifi_max_mem = config['configurations']['nifi-ambari-config']['nifi.max_mem']
nifi_ambari_reporting_frequency = config['configurations'][
    'nifi-ambari-config']['nifi.ambari_reporting_frequency']
nifi_ambari_reporting_enabled = config['configurations']['nifi-ambari-config'][
    'nifi.ambari_reporting_enabled']

nifi_ssl_enabled = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.node.ssl.isenabled']
nifi_host_name = config['agentLevelParams']['hostname']
# note: nifi.node.port and nifi.node.ssl.port must be defined in same xml file for quicklinks to work
nifi_node_port = config['configurations']['nifi-ambari-config'][
    'nifi.node.port']
nifi_node_ssl_port = config['configurations']['nifi-ambari-config'][
    'nifi.node.ssl.port']
nifi_node_protocol_port = config['configurations']['nifi-ambari-config'][
    'nifi.node.protocol.port']
nifi_url = format("https://{nifi_host_name}:{nifi_node_ssl_port}"
                  ) if nifi_ssl_enabled else format(
                      "http://{nifi_host_name}:{nifi_node_port}")

# zookeeper node path
nifi_znode = config['configurations']['nifi-ambari-config']['nifi.nifi_znode']

nifi_internal_dir = config['configurations']['nifi-ambari-config'][
    'nifi.internal.dir']
nifi_state_dir = config['configurations']['nifi-ambari-config'][
    'nifi.state.dir']
nifi_database_dir = config['configurations']['nifi-ambari-config'][
    'nifi.database.dir']
nifi_flowfile_repo_dir = config['configurations']['nifi-ambari-config'][
    'nifi.flowfile.repository.dir']
nifi_provenance_repo_dir_default = config['configurations'][
    'nifi-ambari-config']['nifi.provenance.repository.dir.default']
nifi_config_dir = config['configurations']['nifi-ambari-config'][
    'nifi.config.dir']
nifi_flow_config_dir = config['configurations']['nifi-ambari-config'][
    'nifi.flow.config.dir']
nifi_sensitive_props_key = config['configurations']['nifi-ambari-config'][
    'nifi.sensitive.props.key']
nifi_security_encrypt_configuration_password = config['configurations'][
    'nifi-ambari-config']['nifi.security.encrypt.configuration.password']

# param for nifi explicit key tab
nifi_allow_explicit_keytab = str(config['configurations']['nifi-ambari-config'][
                                     'nifi.allow.explicit.keytab']).lower() if 'nifi.allow.explicit.keytab' in \
                                                                               config['configurations'][
                                                                                   'nifi-ambari-config'] else 'true'

# multiple content repository directories may be defined so search for all values
nifi_content_repo_dir_default = None

# check if default property is available in configurations
if 'nifi.content.repository.dir.default' in config['configurations'][
        'nifi-ambari-config']:
    nifi_content_repo_dir_default = config['configurations'][
        'nifi-ambari-config']['nifi.content.repository.dir.default']

nifi_content_repo_dirs = [
    v.replace('{{nifi_content_repo_dir_default}}',
              nifi_content_repo_dir_default)
    for k, v in config['configurations']['nifi-properties'].items()
    if k.startswith('nifi.content.repository.dir')
]

if nifi_content_repo_dir_default is not None:
    nifi_content_repo_dirs.append(nifi_content_repo_dir_default)

nifi_flow_config_dir = nifi_flow_config_dir.replace('{nifi_internal_dir}',
                                                    nifi_internal_dir)
nifi_state_dir = nifi_state_dir.replace('{nifi_internal_dir}',
                                        nifi_internal_dir)
nifi_config_dir = '/etc/nifi'

master_configs = config['clusterHostInfo']
nifi_master_hosts = master_configs['nifi_master_hosts']

# nifi bootstrap file location
nifi_bootstrap_file = nifi_config_dir + '/bootstrap.conf'

# detect if running in single (sandbox) box
nifi_num_nodes = len(master_configs['nifi_master_hosts'])

# In sandbox scenario, Ambari should still setup nifi in clustered mode for now
nifi_is_node = 'true'

# is node joining an existing cluster
is_additional_node = False

nifi_node_dir = nifi_install_dir
bin_dir = os.path.join(*[nifi_node_dir, 'bin'])
lib_dir = os.path.join(*[nifi_node_dir, 'lib'])

nifi_ca_host = None
if 'nifi_ca_hosts' in master_configs:
    nifi_ca_hosts = master_configs['nifi_ca_hosts']
    if len(nifi_ca_hosts) > 0:
        nifi_ca_host = nifi_ca_hosts[0]

# params from nifi-ambari-ssl-config
nifi_keystore = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.keystore']
nifi_keystoreType = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.keystoreType']
nifi_keystorePasswd = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.keystorePasswd']
nifi_keyPasswd = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.keyPasswd']
nifi_truststore = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.truststore']
nifi_truststoreType = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.truststoreType']
nifi_truststorePasswd = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.security.truststorePasswd']
nifi_initial_admin_id = config['configurations']['nifi-ambari-ssl-config'][
    'nifi.initial.admin.identity']
nifi_ssl_config_content = config['configurations']['nifi-ambari-ssl-config'][
    'content']

if 'nifi.security.needClientAuth' in config['configurations'][
        'nifi-ambari-ssl-config']:
    nifi_needClientAuth = config['configurations']['nifi-ambari-ssl-config'][
        'nifi.security.needClientAuth']
else:
    nifi_needClientAuth = ""

# default keystore/truststore type if empty
nifi_keystoreType = 'jks' if len(nifi_keystoreType) == 0 else nifi_keystoreType
nifi_truststoreType = 'jks' if len(
    nifi_truststoreType) == 0 else nifi_truststoreType

# property that is set to hostname regardless of whether SSL enabled
nifi_node_host = socket.getfqdn()

nifi_truststore = nifi_truststore.replace('{nifi_node_ssl_host}',
                                          nifi_node_host)
nifi_keystore = nifi_keystore.replace('{nifi_node_ssl_host}', nifi_node_host)

# populate properties whose values depend on whether SSL enabled
nifi_keystore = nifi_keystore.replace('{{nifi_config_dir}}', nifi_config_dir)
nifi_truststore = nifi_truststore.replace('{{nifi_config_dir}}',
                                          nifi_config_dir)

if nifi_ssl_enabled:
    nifi_node_ssl_host = nifi_node_host
    nifi_node_port = ""
else:
    nifi_node_nonssl_host = nifi_node_host
    nifi_node_ssl_port = ""

nifi_ca_parent_config = config['configurations']['nifi-ambari-ssl-config']
nifi_use_ca = nifi_ca_parent_config['nifi.toolkit.tls.token']
nifi_toolkit_dn_prefix = nifi_ca_parent_config['nifi.toolkit.dn.prefix']
nifi_toolkit_dn_suffix = nifi_ca_parent_config['nifi.toolkit.dn.suffix']
nifi_toolkit_tls_regenerate = nifi_ca_parent_config[
    'nifi.toolkit.tls.regenerate']
nifi_ca_log_file_stdout = config['configurations']['nifi-env'][
    'nifi_node_log_dir'] + '/nifi-ca.stdout'
nifi_ca_log_file_stderr = config['configurations']['nifi-env'][
    'nifi_node_log_dir'] + '/nifi-ca.stderr'

nifi_ca_config = {
    "days": int(nifi_ca_parent_config['nifi.toolkit.tls.helper.days']),
    "keyStore": nifi_config_dir + '/nifi-certificate-authority-keystore.jks',
    "token": nifi_ca_parent_config['nifi.toolkit.tls.token'],
    "caHostname": nifi_ca_host,
    "port": int(nifi_ca_parent_config['nifi.toolkit.tls.port'])
}

toolkit_ca_api_port = int(nifi_ca_parent_config['nifi.toolkit.tls.port'])
toolkit_ca_check_url = format(
    "https://{nifi_ca_host}:{toolkit_ca_api_port}/v1/api")

if nifi_ca_host:
    nifi_ca_config[
        'dn'] = nifi_toolkit_dn_prefix + nifi_ca_host + nifi_toolkit_dn_suffix

stack_support_tls_toolkit_san = True

nifi_ca_client_config = {
    "days": int(nifi_ca_parent_config['nifi.toolkit.tls.helper.days']),
    "keyStore": nifi_keystore,
    "keyStoreType": nifi_keystoreType,
    "keyStorePassword": nifi_keystorePasswd,
    "keyPassword": nifi_keyPasswd,
    "token": nifi_ca_parent_config['nifi.toolkit.tls.token'],
    "dn": nifi_toolkit_dn_prefix + nifi_node_host + nifi_toolkit_dn_suffix,
    "port": int(nifi_ca_parent_config['nifi.toolkit.tls.port']),
    "caHostname": nifi_ca_host,
    "trustStore": nifi_truststore,
    "trustStoreType": nifi_truststoreType,
    "trustStorePassword": nifi_truststorePasswd
}

if stack_support_tls_toolkit_san:
    nifi_ca_client_config["domainAlternativeNames"] = nifi_node_host

# params from nifi-env
nifi_user = config['configurations']['nifi-env']['nifi_user']
nifi_group = config['configurations']['cluster-env']['user_group']

nifi_node_log_dir = config['configurations']['nifi-env']['nifi_node_log_dir']
nifi_node_log_file = os.path.join(nifi_node_log_dir, 'nifi-setup.log')

# limits related params
limits_conf_dir = '/etc/security/limits.d'
nifi_user_nofile_limit = config['configurations']['nifi-env'][
    'nifi_user_nofile_limit']
nifi_user_nproc_limit = config['configurations']['nifi-env'][
    'nifi_user_nproc_limit']

# params from nifi-boostrap
nifi_env_content = config_utils.merge_env(config['configurations']['nifi-env'])

# params from nifi-logback
nifi_master_logback_content = config['configurations'][
    'nifi-master-logback-env']['content']
nifi_node_logback_content = config['configurations']['nifi-node-logback-env'][
    'content']

# params from nifi-properties-env
nifi_master_properties_content = config['configurations'][
    'nifi-master-properties-env']['content']
nifi_properties = config['configurations']['nifi-properties'].copy()

# kerberos params
nifi_kerberos_authentication_expiration = config['configurations'][
    'nifi-properties']['nifi.kerberos.spnego.authentication.expiration']
nifi_kerberos_realm = default("/configurations/kerberos-env/realm", None)

# params from nifi-flow
nifi_flow_content = config['configurations']['nifi-flow-env']['content']

# params from nifi-state-management-env
nifi_state_management_content = config['configurations'][
    'nifi-state-management-env']['content']

# params from nifi-authorizers-env
nifi_authorizers_content = config['configurations']['nifi-authorizers-env'][
    'content']
nifi_authorizers_dict = config['configurations']['nifi-authorizers-env']
# params from nifi-login-identity-providers-env
nifi_login_identity_providers_content = config['configurations'][
    'nifi-login-identity-providers-env']['content']
nifi_login_identity_providers_dict = config['configurations'][
    'nifi-login-identity-providers-env']
# params from nifi-boostrap
nifi_boostrap_content = config_utils.merge_env(
    config['configurations']['nifi-bootstrap-env'])

# params from nifi-bootstrap-notification-services-env
nifi_boostrap_notification_content = config['configurations'][
    'nifi-bootstrap-notification-services-env']['content']
nifi_boostrap_notification_dict = config['configurations'][
    'nifi-bootstrap-notification-services-env']
# params from nifi-toolkit-env
nifi_toolkit_java_options = config['configurations']['nifi-toolkit-env'][
    'nifi_toolkit_java_options'] if 'nifi-toolkit-env' in config[
        'configurations'] else '-Xms128m -Xmx256m'

nifi_toolkit_conf_dir = '/etc/nifi-toolkit'

# autodetect jdk home
jdk64_home = config['ambariLevelParams']['java_home']

# autodetect ambari server for metrics
if 'metrics_collector_hosts' in config['clusterHostInfo']:
    metrics_collector_host = str(
        config['clusterHostInfo']['metrics_collector_hosts'][0])
    metrics_collector_port = str(
        get_port_from_url(config['configurations']['ams-site']
                          ['timeline.metrics.service.webapp.address']))
else:
    metrics_collector_host = ''
    metrics_collector_port = ''

# detect zookeeper_quorum
zookeeper_port = default('/configurations/zoo.cfg/clientPort', None)
# get comma separated list of zookeeper hosts from clusterHostInfo
index = 0
zookeeper_quorum = ""
zk_hosts_property = 'zookeeper_hosts' if 'zookeeper_hosts' in config[
    'clusterHostInfo'] else "zookeeper_server_hosts"
for host in config['clusterHostInfo'][zk_hosts_property]:
    zookeeper_quorum += host + ":" + str(zookeeper_port)
    index += 1
    if index < len(config['clusterHostInfo'][zk_hosts_property]):
        zookeeper_quorum += ","

# setup ranger configuration

retryAble = default("/commandParams/command_retry_enabled", False)
version = default("/commandParams/version", None)
namenode_hosts = default("/clusterHostInfo/namenode_host", None)

if type(namenode_hosts) is list:
    namenode_host = namenode_hosts[0]
else:
    namenode_host = namenode_hosts

has_namenode = not namenode_host == None

nifi_authorizer = 'file-provider'

nifi_host_port = config['configurations']['nifi-ambari-config'][
    'nifi.node.port']
java_home = config['ambariLevelParams']['java_home']
security_enabled = config['configurations']['cluster-env']['security_enabled']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
stack_support_nifi_toolkit_package = True
stack_support_encrypt_config = True
stack_support_toolkit_update = True
stack_support_admin_toolkit = True
stack_support_nifi_jaas = True
stack_support_encrypt_authorizers = True
stack_support_nifi_auto_client_registration = True

if security_enabled:
    _hostname_lowercase = nifi_host_name.lower()
    nifi_properties['nifi.kerberos.service.principal'] = nifi_properties[
        'nifi.kerberos.service.principal'].replace('_HOST',
                                                   _hostname_lowercase)
    nifi_properties['nifi.kerberos.spnego.principal'] = nifi_properties[
        'nifi.kerberos.spnego.principal'].replace('_HOST', _hostname_lowercase)

    if stack_support_nifi_jaas:
        nifi_service_principal = nifi_properties[
            'nifi.kerberos.service.principal']
        nifi_service_keytab = nifi_properties[
            'nifi.kerberos.service.keytab.location']
        nifi_jaas_conf_template = config['configurations']['nifi-jaas-conf'][
            'content']
        nifi_jaas_conf = nifi_config_dir + "/nifi_jaas.conf"

    zookeeper_principal = default(
        "/configurations/zookeeper-env/zookeeper_principal_name",
        "zookeeper/_HOST@EXAMPLE.COM")
    zookeeper_principal_primary = get_bare_principal(zookeeper_principal)

# ranger host
stack_supports_ranger_kerberos = True
stack_supports_ranger_audit_db = False
xa_audit_db_is_enabled = False
xa_audit_db_password = ''

ranger_admin_hosts = default("/clusterHostInfo/ranger_admin_hosts", [])
has_ranger_admin = not len(ranger_admin_hosts) == 0
xml_configurations_supported = config['configurations']['ranger-env'][
    'xml_configurations_supported']

ambari_server_hostname = config['clusterHostInfo']['ambari_server_host'][0]

# ranger nifi properties
policymgr_mgr_url = config['configurations']['admin-properties'][
    'policymgr_external_url']

if 'admin-properties' in config[
        'configurations'] and 'policymgr_external_url' in config[
            'configurations'][
                'admin-properties'] and policymgr_mgr_url.endswith('/'):
    policymgr_mgr_url = policymgr_mgr_url.rstrip('/')

xa_audit_db_name = config['configurations']['admin-properties'][
    'audit_db_name']
xa_audit_db_user = config['configurations']['admin-properties'][
    'audit_db_user']
xa_db_host = config['configurations']['admin-properties']['db_host']
repo_name = str(config['clusterName']) + '_nifi'

repo_config_username = config['configurations'][
    'ranger-nifi-plugin-properties']['REPOSITORY_CONFIG_USERNAME']

ranger_env = config['configurations']['ranger-env']
ranger_plugin_properties = config['configurations'][
    'ranger-nifi-plugin-properties']
policy_user = config['configurations']['ranger-nifi-plugin-properties'][
    'policy_user']

# For curl command in ranger plugin to get db connector
jdk_location = config['ambariLevelParams']['jdk_location']
java_share_dir = '/usr/share/java'

if has_ranger_admin:
    enable_ranger_nifi = (
        config['configurations']['ranger-nifi-plugin-properties']
        ['ranger-nifi-plugin-enabled'].lower() == 'yes')
    repo_config_password = unicode(
        config['configurations']['ranger-nifi-plugin-properties']
        ['REPOSITORY_CONFIG_PASSWORD'])
    sql_connector_jar = ''

    ssl_keystore_password = unicode(
        config['configurations']['ranger-nifi-policymgr-ssl']
        ['xasecure.policymgr.clientssl.keystore.password']
    ) if xml_configurations_supported else None
    ssl_truststore_password = unicode(
        config['configurations']['ranger-nifi-policymgr-ssl']
        ['xasecure.policymgr.clientssl.truststore.password']
    ) if xml_configurations_supported else None
    credential_file = format('/etc/ranger/{repo_name}/cred.jceks'
                             ) if xml_configurations_supported else None
    credential_file_type = 'jceks'
    ranger_admin_username = config['configurations']['ranger-env'][
        'ranger_admin_username']
    ranger_admin_password = config['configurations']['ranger-env'][
        'ranger_admin_password']

    # create ranger service's nifi client properties
    nifi_authentication = config['configurations'][
        'ranger-nifi-plugin-properties']['nifi.authentication']
    ranger_id_owner_for_certificate = config['configurations'][
        'ranger-nifi-plugin-properties']['owner.for.certificate']
    nifi_id_owner_for_certificate = config['configurations'][
        'ranger-nifi-policymgr-ssl']['owner.for.certificate']
    regex = r"(CN)=([a-zA-Z0-9\.\-\*\[\]\|\:]*)"
    match = re.search(regex, nifi_id_owner_for_certificate)
    common_name_for_certificate = match.group(2) if match else 'NONE'

    if nifi_authentication == 'SSL':

        nifi_ranger_plugin_config = {
            'nifi.authentication':
            nifi_authentication,
            'nifi.url':
            format(
                "https://{nifi_host_name}:{nifi_node_ssl_port}/nifi-api/resources"
            ),
            'nifi.ssl.keystore':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.keystore'],
            'nifi.ssl.keystoreType':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.keystoreType'],
            'nifi.ssl.keystorePassword':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.keystorePassword'],
            'nifi.ssl.truststore':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.truststore'],
            'nifi.ssl.truststoreType':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.truststoreType'],
            'nifi.ssl.truststorePassword':
            config['configurations']['ranger-nifi-plugin-properties']
            ['nifi.ssl.truststorePassword'],
            'commonNameForCertificate':
            common_name_for_certificate
        }
    else:
        nifi_ranger_plugin_config = {
            'nifi.authentication':
            nifi_authentication,
            'nifi.url':
            format(
                "https://{nifi_host_name}:{nifi_host_port}/nifi-api/resources"
            ),
            'commonNameForCertificate':
            common_name_for_certificate
        }

    nifi_ranger_plugin_repo = {
        'isActive': 'true',
        'config': json.dumps(nifi_ranger_plugin_config),
        'description': 'nifi repo',
        'name': repo_name,
        'repositoryType': 'nifi',
        'assetType': '5'
    }

    # used in nifi authorizers
    ranger_admin_identity = ranger_id_owner_for_certificate

    if stack_supports_ranger_kerberos and security_enabled:
        nifi_ranger_plugin_config['policy.download.auth.users'] = nifi_user
        nifi_ranger_plugin_config['tag.download.auth.users'] = nifi_user
        ranger_nifi_principal = config['configurations'][
            'nifi-properties']['nifi.kerberos.service.principal'].replace(
                '_HOST', _hostname_lowercase)
        ranger_nifi_keytab = config['configurations']['nifi-properties'][
            'nifi.kerberos.service.keytab.location']

    if stack_supports_ranger_kerberos:
        nifi_ranger_plugin_config['ambari.service.check.user'] = policy_user

        nifi_ranger_plugin_repo = {
            'isEnabled': 'true',
            'configs': nifi_ranger_plugin_config,
            'description': 'nifi repo',
            'name': repo_name,
            'type': 'nifi'
        }

    ranger_audit_solr_urls = config['configurations']['ranger-admin-site'][
        'ranger.audit.solr.urls']

    xa_audit_hdfs_is_enabled = default(
        '/configurations/ranger-nifi-audit/xasecure.audit.destination.hdfs',
        True)

    nifi_authorizer = 'ranger-provider'

hdfs_user = config['configurations']['hadoop-env'][
    'hdfs_user'] if has_namenode else None
hdfs_user_keytab = config['configurations']['hadoop-env'][
    'hdfs_user_keytab'] if has_namenode else None
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name'] if has_namenode else None
hdfs_site = config['configurations']['hdfs-site'] if has_namenode else None
default_fs = config['configurations']['core-site'][
    'fs.defaultFS'] if has_namenode else None
hadoop_bin_dir = Script.get_stack_root() + '/hadoop/bin' if has_namenode else None
hadoop_conf_dir = '/etc/hadoop' if has_namenode else None
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))

local_component_list = default("/localComponents", [])
has_hdfs_client_on_node = 'HDFS_CLIENT' in local_component_list

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
    immutable_paths=get_not_managed_resources())

registry_install_dir = stack_root + '/nifi-registry'
registry_download_url = config['configurations']['nifi-registry-env'][
    'download_url']
registry_filename = registry_download_url.split('/')[-1]
registry_version_dir = registry_filename.replace('.tar.gz', '').replace(
    '.tgz', '')

nifi_registry_install_dir = registry_install_dir

# params from nifi-registry-ambari-config
nifi_registry_initial_mem = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.initial_mem']
nifi_registry_max_mem = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.max_mem']

# note: nifi.registry.port and nifi.registry.port.ssl must be defined in same xml file for quicklinks to work
nifi_registry_port = config['configurations']['nifi-registry-ambari-config'][
    'nifi.registry.port']
nifi_registry_ssl_port = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.port.ssl']

nifi_registry_internal_dir = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.internal.dir']
nifi_registry_internal_config_dir = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.internal.config.dir']
nifi_registry_internal_config_dir = nifi_registry_internal_config_dir.replace(
    '{nifi_registry_internal_dir}', nifi_registry_internal_dir)

nifi_registry_config_dir = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.config.dir']
nifi_registry_config_dir = nifi_registry_config_dir.replace(
    '{nifi_registry_install_dir}', nifi_registry_install_dir)

nifi_registry_database_dir = config['configurations'][
    'nifi-registry-ambari-config']['nifi.registry.database.dir']
nifi_registry_database_dir = nifi_registry_database_dir.replace(
    '{nifi_registry_internal_dir}', nifi_registry_internal_dir)

# password for encrypted config
nifi_registry_security_encrypt_configuration_password = config[
    'configurations']['nifi-registry-ambari-config'][
        'nifi.registry.security.encrypt.configuration.password']

# nifi registry bootstrap file location
nifi_registry_bootstrap_file = nifi_registry_config_dir + '/bootstrap.conf'

nifi_registry_dir = nifi_registry_install_dir
nifi_registry_bin_dir = os.path.join(*[nifi_registry_dir, 'bin'])
nifi_registry_lib_dir = os.path.join(*[nifi_registry_dir, 'lib'])
nifi_registry_docs_dir = os.path.join(*[nifi_registry_dir, 'docs'])

# params from nifi-registry-ambari-ssl-config
nifi_registry_ssl_enabled = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.ssl.isenabled']
nifi_registry_keystore = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.keystore']
nifi_registry_keystoreType = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.keystoreType']
nifi_registry_keystorePasswd = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.keystorePasswd']
nifi_registry_keyPasswd = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.keyPasswd']
nifi_registry_truststore = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.truststore']
nifi_registry_truststoreType = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.truststoreType']
nifi_registry_truststorePasswd = config['configurations'][
    'nifi-registry-ambari-ssl-config'][
        'nifi.registry.security.truststorePasswd']
nifi_registry_needClientAuth = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.security.needClientAuth']
nifi_registry_initial_admin_id = config['configurations'][
    'nifi-registry-ambari-ssl-config']['nifi.registry.initial.admin.identity']
nifi_registry_ssl_config_content = config['configurations'][
    'nifi-registry-ambari-ssl-config']['content']

# default keystore/truststore type if empty
nifi_registry_keystoreType = 'jks' if len(
    nifi_registry_keystoreType) == 0 else nifi_registry_keystoreType
nifi_registry_truststoreType = 'jks' if len(
    nifi_registry_truststoreType) == 0 else nifi_registry_truststoreType

# property that is set to hostname regardless of whether SSL enabled
nifi_registry_host = socket.getfqdn()

nifi_registry_truststore = nifi_registry_truststore.replace(
    '{nifi_registry_ssl_host}', nifi_registry_host)
nifi_registry_keystore = nifi_registry_keystore.replace(
    '{nifi_registry_ssl_host}', nifi_registry_host)

# populate properties whose values depend on whether SSL enabled
nifi_registry_keystore = nifi_registry_keystore.replace(
    '{{nifi_registry_config_dir}}', nifi_registry_config_dir)
nifi_registry_truststore = nifi_registry_truststore.replace(
    '{{nifi_registry_config_dir}}', nifi_registry_config_dir)

if nifi_registry_ssl_enabled:
    nifi_registry_ssl_host = nifi_registry_host
    nifi_registry_port = ""
else:
    nifi_registry_nonssl_host = nifi_registry_host
    nifi_registry_ssl_port = ""

# params from nifi-registry-env
nifi_registry_user = config['configurations']['nifi-registry-env'][
    'nifi_registry_user']
nifi_registry_group = config['configurations']['cluster-env']['user_group']

nifi_registry_log_dir = config['configurations']['nifi-registry-env'][
    'nifi_registry_log_dir']
nifi_registry_log_file = os.path.join(nifi_registry_log_dir,
                                      'nifi-registry-setup.log')

# params from nifi-registry-boostrap
nifi_registry_env_content = config_utils.merge_env(
    config['configurations']['nifi-registry-env'])

# params from nifi-registry-logback
nifi_registry_logback_content = config['configurations'][
    'nifi-registry-logback-env']['content']

# params from nifi-registry-properties-env
nifi_registry_master_properties_content = config['configurations'][
    'nifi-registry-master-properties-env']['content']
nifi_registry_properties = config['configurations'][
    'nifi-registry-properties'].copy()

# kerberos params
nifi_registry_kerberos_authentication_expiration = config['configurations'][
    'nifi-registry-properties'][
        'nifi.registry.kerberos.spnego.authentication.expiration']
nifi_registry_kerberos_realm = default("/configurations/kerberos-env/realm",
                                       None)

# params from nifi-registry-authorizers-env
nifi_registry_authorizers_content = config['configurations'][
    'nifi-registry-authorizers-env']['content']
nifi_registry_authorizers_dict = config['configurations'][
    'nifi-registry-authorizers-env']
# params from nifi-registry-identity-providers-env
nifi_registry_identity_providers_content = config['configurations'][
    'nifi-registry-identity-providers-env']['content']
nifi_registry_identity_providers_dict = config['configurations'][
    'nifi-registry-identity-providers-env']
# params from nifi-registry-providers-env
nifi_registry_providers_content = config['configurations'][
    'nifi-registry-providers-env']['content']
nifi_registry_providers_dict = config['configurations'][
    'nifi-registry-providers-env']
# params from nifi-registry-boostrap
nifi_registry_boostrap_content = config_utils.merge_env(
    config['configurations']['nifi-registry-bootstrap-env'])

nifi_registry_authorizer = 'managed-authorizer'
