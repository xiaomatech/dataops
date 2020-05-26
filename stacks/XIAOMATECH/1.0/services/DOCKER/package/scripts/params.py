#!/usr/bin/env python

from resource_management.libraries.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

disk_dev = config['configurations']['docker-env']['disk_dev']
docker_registry_url = config['configurations']['docker-env'][
    'docker_registry_url']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_content = config['configurations']['docker-env']['install_content']
harbor_cfg_content = config['configurations']['docker-env'][
    'harbor_cfg_content']

install_dir = stack_root + '/dbus'
download_url = config['configurations']['dbus-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '').replace(
    '.tar.bz2', '')
