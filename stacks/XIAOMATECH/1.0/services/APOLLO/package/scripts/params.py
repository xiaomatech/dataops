#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default
# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

apollo_user = config['configurations']['apollo-env']['apollo_user']
log_dir = config['configurations']['apollo-env']['log_dir']
pid_dir = config['configurations']['apollo-env']['pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir_configservice = stack_root + '/apollo-configservice'
download_url_configservice = config['configurations']['apollo-env'][
    'download_url']
filename_configservice = download_url_configservice.split('/')[-1]
version_dir_configservice = filename_configservice.replace(
    '.tar.gz', '').replace('.tgz', '').replace('.zip', '')

install_dir_adminservice = stack_root + '/apollo-adminservice'
download_url_adminservice = config['configurations']['apollo-env'][
    'download_url_adminservice']
filename_adminservice = download_url_adminservice.split('/')[-1]
version_dir_adminservice = filename_adminservice.replace(
    '.tar.gz', '').replace('.tgz', '').replace('.zip', '')

install_dir_portal = stack_root + '/apollo-portal'
download_url_portal = config['configurations']['apollo-env'][
    'download_url_portal']
filename_portal = download_url_portal.split('/')[-1]
version_dir_portal = filename_portal.replace('.tar.gz', '').replace(
    '.tgz', '').replace('.zip', '')

configservice_conf_content = config['configurations']['apollo-env'][
    'configservice_conf_content']
adminservice_conf_content = config['configurations']['apollo-env'][
    'adminservice_conf_content']
portal_conf_content = config['configurations']['apollo-env'][
    'portal_conf_content']
env_conf_content = config['configurations']['apollo-env']['env_conf_content']

portaldb_url = config['configurations']['apollo-env']['portaldb_url']

db_host = config['configurations']['apollo-env']['db_host']
db_user = config['configurations']['apollo-env']['db_user']
db_password = config['configurations']['apollo-env']['db_password']

cluster_name = config['clusterName']

conf_dir = '/etc/apollo'

user_group = config['configurations']['cluster-env']['user_group']

dev_configdb_url = config['configurations']['apollo-env']['dev_configdb_url']
uat_configdb_url = config['configurations']['apollo-env']['uat_configdb_url']
pro_configdb_url = config['configurations']['apollo-env']['pro_configdb_url']

apollo_configservice_hosts = sorted(
    default('/clusterHostInfo/apollo_configservice_hosts', []))

dev_meta_host = uat_meta_host = pro_meta_host = ''

if apollo_configservice_hosts.index(hostname) == 0:
    configdb_url = dev_configdb_url
    dev_meta_host = hostname
elif apollo_configservice_hosts.index(hostname) == 1:
    configdb_url = uat_configdb_url
    uat_meta_host = hostname
elif apollo_configservice_hosts.index(hostname) == 2:
    configdb_url = pro_configdb_url
    pro_meta_host = hostname
