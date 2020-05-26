#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default
import os

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

config = Script.get_config()

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

master_content = config['configurations']['containerfs-env']['master_content']
metanode_content = config['configurations']['containerfs-env'][
    'metanode_content']
datanode_content = config['configurations']['containerfs-env'][
    'datanode_content']
client_content = config['configurations']['containerfs-env']['client_content']
conf_dir = '/etc/containerfs'

containerfs_master_hosts = default('/clusterHostInfo/containerfs_master_hosts',
                                   [])
containerfs_master_host = ','.join(containerfs_master_hosts)
master_host = '"' + '","'.join(containerfs_master_hosts) + '"'


def install_from_file(file_name):
    file_path = '/usr/sbin/' + file_name
    if not os.path.exists(file_path):
        Execute('wget ' + download_url_base + '/' + file_name + ' -O ' + file_path)
        Execute('chmod a+x ' + file_path)
