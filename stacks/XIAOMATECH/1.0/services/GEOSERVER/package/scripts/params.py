#!/usr/bin/env python

from resource_management.libraries.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()
install_dir = stack_root + '/geoserver'
download_url = config['configurations']['geoserver-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')


hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
geoserver_user = config['configurations']['geoserver-env']['geoserver_user']
geoserver_group = config['configurations']['cluster-env']['user_group']

geoserver_content = config['configurations']['geoserver-env']['geoserver_content']
env_content = config['configurations']['geoserver-env']['env_content']
pid_dir = config['configurations']['geoserver-env']['run_dir']
conf_dir = config['configurations']['geoserver-env']['conf_dir']
log_dir = config['configurations']['geoserver-env']['log_dir']
data_dir = config['configurations']['geoserver-env']['data_dir']

