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
from resource_management.libraries.functions.copy_tarball import get_sysprep_skip_copy_tarballs_hdfs
import os

from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

hostname = config['agentLevelParams']['hostname']

install_dir = stack_root + '/tez'

download_url = config['configurations']['tez-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

install_dir_tomcat = stack_root + '/tomcat'
download_url_tomcat = config['configurations']['tez-env']['download_url_tomcat']
filename_tomcat = download_url_tomcat.split('/')[-1]
version_dir_tomcat = filename_tomcat.replace('.tar.gz', '').replace('.tgz', '')

stack_name = default("/clusterLevelParams/stack_name", None)


# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)

# default hadoop parameters
hadoop_home = stack_root + '/hadoop'
hadoop_bin_dir = hadoop_home + "/bin"
hadoop_conf_dir = '/etc/hadoop'
tez_etc_dir = config_dir = "/etc/tez"
tez_examples_jar = install_dir + "/tez-examples-*.jar"

# Heap dump related
heap_dump_enabled = default('/configurations/tez-env/enable_heap_dump', None)
heap_dump_opts = ""  # Empty if 'heap_dump_enabled' is False.
if heap_dump_enabled:
    heap_dump_path = default('/configurations/tez-env/heap_dump_location',
                             "/tmp")
    heap_dump_opts = " -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=" + heap_dump_path

kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
security_enabled = config['configurations']['cluster-env']['security_enabled']
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env'][
    'hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']

java64_home = config['ambariLevelParams']['java_home']

tez_user = config['configurations']['tez-env']['tez_user']
user_group = config['configurations']['cluster-env']['user_group']
tez_env_sh_template = config['configurations']['tez-env']['content']

hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']

dfs_type = default("/clusterLevelParams/dfs_type", "")

import functools

# create partial functions with common arguments for every HdfsResource call
# to create/delete/copyfromlocal hdfs directories/files we need to call params.HdfsResource in code
HdfsResource = functools.partial(
    HdfsResource,
    user=hdfs_user,
    hdfs_resource_ignore_file=
    "/var/lib/ambari-agent/data/.hdfs_resource_ignore",
    security_enabled=security_enabled,
    keytab=hdfs_user_keytab,
    kinit_path_local=kinit_path_local,
    hadoop_bin_dir=hadoop_bin_dir,
    hadoop_conf_dir=hadoop_conf_dir,
    principal_name=hdfs_principal_name,
    hdfs_site=hdfs_site,
    default_fs=default_fs,
    immutable_paths=get_not_managed_resources(),
    dfs_type=dfs_type)

tez_site_config = dict(config['configurations']['tez-site'])

sysprep_skip_copy_tarballs_hdfs = get_sysprep_skip_copy_tarballs_hdfs()
