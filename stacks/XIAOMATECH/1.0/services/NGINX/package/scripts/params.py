#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default
import os

config = Script.get_config()

nginx_user = config['configurations']['nginx-env']['nginx_user']
log_dir = config['configurations']['nginx-env']['nginx_log_dir']
pid_dir = config['configurations']['nginx-env']['nginx_pid_dir']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['nginx-env']['conf_content']
conf_dir = '/usr/local/openresty/nginx/conf/'

nginx_group = user_group = config['configurations']['cluster-env'][
    'user_group']

agent_cache_dir = config['agentLevelParams']['agentCacheDir']
service_package_folder = config['serviceLevelParams']['service_package_folder']
stack_name = default("/clusterLevelParams/stack_name", None)
agent_resty_dir = os.path.join(agent_cache_dir, service_package_folder,
                               'files')

clickhouse_hosts = default('/clusterHostInfo/clickhouse_server_hosts', [])
clickhouse_host = ''
clicktail_content = config['configurations']['nginx-env']['clicktail_content']
if len(clickhouse_hosts) > 0:
    import random

    clickhouse_host = clickhouse_hosts[random.randint(0, len(clickhouse_hosts) - 1)]
