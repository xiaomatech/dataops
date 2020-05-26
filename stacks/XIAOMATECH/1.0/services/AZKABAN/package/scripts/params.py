# -*- coding: utf-8 -*-

from resource_management.libraries.script.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

azkaban_web_properties = config['configurations']['azkaban-env'][
    'azkaban_web_content']
azkaban_executor_properties = config['configurations']['azkaban-env'][
    'azkaban_executor_content']
azkaban_users = config['configurations']['azkaban-env']['azkaban_user_content']
global_properties = config['configurations']['azkaban-env']['global_content']
log4j_properties = config['configurations']['azkaban-env']['log4j_content']

java_home = config['ambariLevelParams']['java_home']
java_exec = format("{java_home}/bin/java")

install_dir = stack_root + '/azkaban-web-server'

download_url = config['configurations']['azkaban-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

install_dir_executor = stack_root + '/azkaban-exec-server'
download_url_executor = config['configurations']['azkaban-env'][
    'download_url_executor']
filename_executor = download_url_executor.split('/')[-1]
version_dir_executor = filename_executor.replace('.tar.gz', '').replace(
    '.tgz', '')

azkaban_user = config['configurations']['azkaban-env']['azkaban_user']
user_group = config['configurations']['cluster-env']['user_group']
hostname = config['agentLevelParams']['hostname']

conf_dir = '/etc/azkaban'
log_dir = '/var/log/azkaban'

db_host = config['configurations']['apollo-env']['db_host']
db_user = config['configurations']['apollo-env']['db_user']
db_password = config['configurations']['apollo-env']['db_password']
