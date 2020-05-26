#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

pika_user = config['configurations']['pika-env']['pika_user']
log_dir = config['configurations']['pika-env']['pika_log_dir']
pid_dir = config['configurations']['pika-env']['pika_pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/pika'
download_url = config['configurations']['pika-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '').replace(
    '.tar.bz2', '')

conf_content = config['configurations']['pika-env']['conf_content']

dump_dir = '/data1/pika_dump'
db_dir = '/data1/pika'
conf_dir = '/etc/pika'

pid_file = pid_dir + '/pika.pid'

pika_group = user_group = config['configurations']['cluster-env']['user_group']
