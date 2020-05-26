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

import os
import pwd

from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script

config = Script.get_config()

hadoop_pid_dir_prefix = config['configurations']['hadoop-env'][
    'hadoop_pid_dir_prefix']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
root_user = "root"
hadoop_pid_dir = format("{hadoop_pid_dir_prefix}/{hdfs_user}")
namenode_pid_file = format("{hadoop_pid_dir}/hadoop-{hdfs_user}-namenode.pid")
snamenode_pid_file = format(
    "{hadoop_pid_dir}/hadoop-{hdfs_user}-secondarynamenode.pid")
journalnode_pid_file = format(
    "{hadoop_pid_dir}/hadoop-{hdfs_user}-journalnode.pid")
zkfc_pid_file = format("{hadoop_pid_dir}/hadoop-{hdfs_user}-zkfc.pid")
nfsgateway_pid_file = format(
    "{hadoop_pid_dir_prefix}/root/privileged-root-nfs3.pid")
unprivileged_nfsgateway_pid_file = format(
    "{hadoop_pid_dir_prefix}/root/hadoop-{hdfs_user}-root-nfs3.pid")

dfsrouter_pid_file = format("{hadoop_pid_dir}/hadoop-{hdfs_user}-dfsrouter.pid")
kms_pid_file = format("{hadoop_pid_dir}/hadoop-{hdfs_user}-kms.pid")

observer_namenode_pid_file = format("{hadoop_pid_dir}/hadoop-{hdfs_user}-observernamenode.pid")

# Security related/required params
hostname = config['agentLevelParams']['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_principal = config['configurations']['hadoop-env'][
    'hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']

hadoop_conf_dir = '/etc/hadoop'

kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()

stack_name = default("/clusterLevelParams/stack_name", None)
