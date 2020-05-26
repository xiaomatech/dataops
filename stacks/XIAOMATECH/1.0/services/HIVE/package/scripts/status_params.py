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

# Ambari Commons & Resource Management Imports
from resource_management.libraries.functions import format
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script

# Either HIVE_METASTORE, HIVE_SERVER, HIVE_CLIENT
role = default("/role", None)

config = Script.get_config()

stack_root = Script.get_stack_root()

hive_pid_dir = config['configurations']['hive-env']['hive_pid_dir']
hive_pid = format("{hive_pid_dir}/hive-server.pid")
hive_interactive_pid = format("{hive_pid_dir}/hive-interactive.pid")
hive_metastore_pid = format("{hive_pid_dir}/hive.pid")

process_name = 'mysqld'

SERVICE_FILE_TEMPLATES = [
    '/etc/init.d/{0}', '/usr/lib/systemd/system/{0}.service'
]
POSSIBLE_DAEMON_NAMES = ['mysql', 'mysqld', 'mariadb']

# Security related/required params
hostname = config['agentLevelParams']['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hive_user = config['configurations']['hive-env']['hive_user']

# default configuration directories
hadoop_home = Script.get_stack_root() + '/hadoop/'
hadoop_conf_dir = hadoop_home + '/etc/hadoop'
hadoop_bin_dir = hadoop_home + '/bin'

hive_server_conf_dir = "/etc/hive"
hive_server_interactive_conf_dir = "/etc/hive_llap"
tez_conf_dir = "/etc/tez"
tez_interactive_conf_dir = "/etc/tez_llap"

hive_home_dir = stack_root + '/hive'
hive_conf_dir = hive_server_conf_dir
hive_client_conf_dir = hive_conf_dir

hive_config_dir = hive_client_conf_dir

if 'role' in config and config['role'] in [
        "HIVE_SERVER", "HIVE_METASTORE", "HIVE_SERVER_INTERACTIVE"
]:
    hive_config_dir = hive_server_conf_dir

stack_name = default("/clusterLevelParams/stack_name", None)


hcat_pid_dir = config['configurations']['hive-env']['hcat_pid_dir'] #hcat_pid_dir
webhcat_pid_file = format('{hcat_pid_dir}/webhcat.pid')