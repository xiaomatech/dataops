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

Ambari Agent

"""
import status_params
import os

from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.expect import expect

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/zookeeper'
download_url = config['configurations']['zookeeper-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')


stack_name = status_params.stack_name

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)

# default parameters
zk_home = install_dir
zk_bin = zk_home + "/bin"
zk_cli_shell = zk_home + "/bin/zkCli.sh"
config_dir = "/etc/zookeeper"
zk_smoke_out = os.path.join(tmp_dir, "zkSmoke.out")

zk_user = config['configurations']['zookeeper-env']['zk_user']
hostname = config['agentLevelParams']['hostname']
user_group = config['configurations']['cluster-env']['user_group']
zk_env_sh_template = config['configurations']['zookeeper-env']['content']

zk_log_dir = config['configurations']['zookeeper-env']['zk_log_dir']
zk_data_dir = config['configurations']['zoo.cfg']['dataDir']
zk_pid_dir = status_params.zk_pid_dir
zk_pid_file = status_params.zk_pid_file
zk_server_heapsize_value = str(
    default('configurations/zookeeper-env/zk_server_heapsize', "1024"))
zk_server_heapsize_value = zk_server_heapsize_value.strip()
if len(zk_server_heapsize_value) > 0 and zk_server_heapsize_value[-1].isdigit(
):
    zk_server_heapsize_value = zk_server_heapsize_value + "m"
zk_server_heapsize = format("-Xmx{zk_server_heapsize_value}")

client_port = default('/configurations/zoo.cfg/clientPort', None)

if 'zoo.cfg' in config['configurations']:
    zoo_cfg_properties_map = config['configurations']['zoo.cfg']
else:
    zoo_cfg_properties_map = {}
zoo_cfg_properties_map_length = len(zoo_cfg_properties_map)

zk_principal_name = default(
    "/configurations/zookeeper-env/zookeeper_principal_name",
    "zookeeper@EXAMPLE.COM")
zk_principal = zk_principal_name.replace('_HOST', hostname.lower())

java64_home = config['ambariLevelParams']['java_home']
java_version = expect("/ambariLevelParams/java_version", int)

zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()

zk_keytab_path = config['configurations']['zookeeper-env'][
    'zookeeper_keytab_path']
zk_server_jaas_file = format("{config_dir}/zookeeper_jaas.conf")
zk_client_jaas_file = format("{config_dir}/zookeeper_client_jaas.conf")
security_enabled = config['configurations']['cluster-env']['security_enabled']

smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))

# Zookeeper log4j settings
zookeeper_log_max_backup_size = default(
    'configurations/zookeeper-log4j/zookeeper_log_max_backup_size', 10)
zookeeper_log_number_of_backup_files = default(
    'configurations/zookeeper-log4j/zookeeper_log_number_of_backup_files', 10)

#log4j.properties
if ('zookeeper-log4j' in config['configurations']) and (
        'content' in config['configurations']['zookeeper-log4j']):
    log4j_props = config['configurations']['zookeeper-log4j']['content']
else:
    log4j_props = None

zookeeper_port = default('/configurations/zoo.cfg/clientPort', None)
zookeeper_hosts = default("/clusterHostInfo/zookeeper_server_hosts", [])
index = 0
zookeeper_quorum = ""
for host in zookeeper_hosts:
    zookeeper_quorum += host + ":" + str(zookeeper_port)
    index += 1
    if index < len(zookeeper_hosts):
        zookeeper_quorum += ","

zkui_script_content = config['configurations']['zookeeper-env'][
    'zkui_script_content']
zkui_content = config['configurations']['zookeeper-env']['zkui_content']
