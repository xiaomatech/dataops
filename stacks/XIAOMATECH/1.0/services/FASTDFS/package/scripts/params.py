#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

config = Script.get_config()

client_content = config['configurations']['fastdfs-env']['client_content']
storage_content = config['configurations']['fastdfs-env']['storage_content']
tracker_content = config['configurations']['fastdfs-env']['tracker_content']

tracker_hosts = config['clusterHostInfo']['fastdfs_tracker_hosts']
tracker_host = ':22122,'.join(tracker_hosts) + ':22122'

storage_hosts = config['clusterHostInfo']['fastdfs_storage_hosts']

base_path = '/data1/fastdfs'

data_paths = []
with open('/proc/mounts', 'r') as f:
    data_paths = [
        line.split()[1] + '/dfs' for line in f.readlines()
        if line.split()[0].startswith('/dev')
        and line.split()[1] not in ['/boot', '/var/log', '/']
    ]

data_path_count = len(data_paths)
