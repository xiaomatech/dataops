#!/usr/bin/env python
'''
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
'''
import socket
import tarfile
import os
from contextlib import closing

from resource_management.libraries.functions.copy_tarball import copy_to_hdfs, get_tarball_paths
from resource_management.libraries.functions import format
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.shell import as_sudo


def make_tarfile(output_filename, source_dir):
    try:
        os.remove(output_filename)
    except OSError:
        pass
    parent_dir = os.path.dirname(output_filename)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    os.chmod(parent_dir, 0711)
    with closing(tarfile.open(output_filename, "w:gz")) as tar:
        for file in os.listdir(source_dir):
            tar.add(os.path.join(source_dir, file), arcname=file)
    os.chmod(output_filename, 0644)


def spark_service(name, action=None):
    import params

    if action == 'start':
        if name == 'jobhistoryserver':
            if not params.sysprep_skip_copy_tarballs_hdfs:
                source_dir = params.spark_home + "/jars"
                source_cp_dir = '/tmp/spark_jars'
                Execute('cp -rf %s %s;rm -rf %s/hadoop-*' % (source_dir, source_cp_dir,source_cp_dir))
                tmp_archive_file = get_tarball_paths("spark2")[1]
                make_tarfile(tmp_archive_file, source_cp_dir)
                Execute('rm -rf %s' % source_cp_dir)
                copy_to_hdfs(
                    "spark2",
                    params.user_group,
                    params.hdfs_user,
                    custom_dest_file=params.spark_yarn_archive,
                    skip=params.sysprep_skip_copy_tarballs_hdfs,
                    replace_existing_files=True)

            # create spark history directory
            params.HdfsResource(
                params.spark_history_dir,
                type="directory",
                action="create_on_execute",
                owner=params.spark_user,
                group=params.user_group,
                mode=0777,
                recursive_chmod=True)
            params.HdfsResource(None, action="execute")

        if params.security_enabled:
            spark_kinit_cmd = format(
                "{kinit_path_local} -kt {spark_kerberos_keytab} {spark_principal}; "
            )
            Execute(spark_kinit_cmd, user=params.spark_user)

        if name == 'jobhistoryserver':

            create_catalog_cmd = format(
                "{hive_schematool_bin}/schematool -dbType {hive_metastore_db_type} "
                "-createCatalog {default_metastore_catalog} "
                "-catalogDescription 'Default catalog, for Spark' -ifNotExists "
                "-catalogLocation {default_fs}{spark_warehouse_dir}")

            # Execute(create_catalog_cmd, user=params.hive_user)

            historyserver_no_op_test = as_sudo([
                "test", "-f", params.spark_history_server_pid_file
            ]) + " && " + as_sudo(
                ["pgrep", "-F", params.spark_history_server_pid_file])
            try:
                Execute(
                    ' source /etc/spark/spark-env.sh; ' +
                    params.spark_history_server_start,
                    user=params.spark_user,
                    environment={'JAVA_HOME': params.java_home},
                    not_if=historyserver_no_op_test)
            except:
                show_logs(params.spark_log_dir, user=params.spark_user)
                raise

        elif name == 'sparkthriftserver':
            if params.security_enabled:
                hive_kinit_cmd = format(
                    "{kinit_path_local} -kt {hive_kerberos_keytab} {hive_kerberos_principal}; "
                )
                Execute(hive_kinit_cmd, user=params.spark_user)

            thriftserver_no_op_test = as_sudo([
                "test", "-f", params.spark_thrift_server_pid_file
            ]) + " && " + as_sudo(
                ["pgrep", "-F", params.spark_thrift_server_pid_file])
            try:
                Execute(
                    ' source /etc/spark/spark-env.sh; ' + format(
                        '{spark_thrift_server_start} --properties-file {spark_thrift_server_conf_file} {spark_thrift_cmd_opts_properties}'
                    ),
                    user=params.spark_user,
                    environment={'JAVA_HOME': params.java_home},
                    not_if=thriftserver_no_op_test)
            except:
                show_logs(params.spark_log_dir, user=params.spark_user)
                raise
    elif action == 'stop':
        if name == 'jobhistoryserver':
            try:
                Execute(
                    format('{spark_history_server_stop}'),
                    user=params.spark_user,
                    environment={'JAVA_HOME': params.java_home})
            except:
                show_logs(params.spark_log_dir, user=params.spark_user)
                raise
            File(params.spark_history_server_pid_file, action="delete")

        elif name == 'sparkthriftserver':
            try:
                Execute(
                    format('{spark_thrift_server_stop}'),
                    user=params.spark_user,
                    environment={'JAVA_HOME': params.java_home})
            except:
                show_logs(params.spark_log_dir, user=params.spark_user)
                raise
            File(params.spark_thrift_server_pid_file, action="delete")
