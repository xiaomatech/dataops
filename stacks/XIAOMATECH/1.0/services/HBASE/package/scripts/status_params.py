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

from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

log_dir = config['configurations']['hbase-env']['hbase_log_dir']
pid_dir = config['configurations']['hbase-env']['hbase_pid_dir']
hbase_user = config['configurations']['hbase-env']['hbase_user']

hbase_master_pid_file = format("{pid_dir}/hbase-{hbase_user}-master.pid")
regionserver_pid_file = format("{pid_dir}/hbase-{hbase_user}-regionserver.pid")
phoenix_pid_file = format("{pid_dir}/phoenix-{hbase_user}-queryserver.pid")
rest_pid_file = format("{pid_dir}/hbase-{hbase_user}-rest.pid")
thrift_pid_file = format("{pid_dir}/hbase-{hbase_user}-thrift.pid")
zookeeper_pid_file = format("{pid_dir}/hbase-{hbase_user}-zookeeper.pid")

# Security related/required params
hostname = config['agentLevelParams']['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()

hbase_conf_dir = "/etc/hbase"
limits_conf_dir = "/etc/security/limits.d"

stack_name = default("/clusterLevelParams/stack_name", None)
