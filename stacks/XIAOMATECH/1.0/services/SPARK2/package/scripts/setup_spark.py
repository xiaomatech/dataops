#!/usr/bin/python
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
import socket

from urlparse import urlparse
from resource_management.core.source import Template, InlineTemplate
from resource_management.core.resources.system import Directory, File
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.resources.properties_file import PropertiesFile
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def install_spark_share_lib():
    import params
    share_dir = params.spark_home + "/jars/"
    Directory(
        share_dir,
        owner=params.spark_user,
        group=params.user_group,
        create_parents=True,
        mode=0755)

    share_jar_files_conf = default("/configurations/spark2-env/share_jars", '').strip()
    if share_jar_files_conf.strip() != '':
        share_jar_files = share_jar_files_conf.split(',')
        for jar_file in share_jar_files:
            jar_file_path = share_dir + jar_file.strip()
            if not os.path.exists(jar_file_path):
                Execute('wget ' + download_url_base + '/share/spark/' + jar_file + ' -O ' + jar_file_path,
                        user=params.spark_user)


def install_spark():
    import params
    Directory([params.spark_conf],
              owner=params.spark_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)

    install_spark_share_lib()

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.spark_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.spark_conf + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/spark.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (
            params.spark_user, params.user_group, Script.get_stack_root(), params.version_dir))
        Execute('chown -R %s:%s %s' % (params.spark_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def setup_spark(env, type, action=None):
    import params

    # ensure that matching LZO libraries are installed for Spark

    Directory([params.spark_pid_dir, params.spark_log_dir],
              owner=params.spark_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if type == 'server' and action == 'config':
        params.HdfsResource(
            params.spark_hdfs_user_dir,
            type="directory",
            action="create_on_execute",
            owner=params.spark_user,
            mode=0775)
        params.HdfsResource(
            '/carbon',
            type="directory",
            action="create_on_execute",
            owner=params.spark_user,
            mode=0775)

        if not params.whs_dir_protocol or params.whs_dir_protocol == urlparse(
                params.default_fs).scheme:
            # Create Spark Warehouse Dir
            params.HdfsResource(
                params.spark_warehouse_dir,
                type="directory",
                action="create_on_execute",
                owner=params.spark_user,
                mode=0777)

        params.HdfsResource(None, action="execute")

        generate_logfeeder_input_config(
            'spark2',
            Template("input.config-spark2.json.j2", extra_imports=[default]))

    spark2_defaults = dict(params.config['configurations']['spark2-defaults'])

    if params.security_enabled:
        spark2_defaults.pop("history.server.spnego.kerberos.principal")
        spark2_defaults.pop("history.server.spnego.keytab.file")
        spark2_defaults['spark.history.kerberos.principal'] = spark2_defaults[
            'spark.history.kerberos.principal'].replace(
            '_HOST',
            socket.getfqdn().lower())

    PropertiesFile(
        format("{spark_conf}/spark-defaults.conf"),
        properties=spark2_defaults,
        key_value_delimiter=" ",
        owner=params.spark_user,
        group=params.spark_group,
        mode=0644)

    File(
        os.path.join(params.spark_conf, 'carbon.properties'),
        owner=params.spark_user,
        group=params.spark_group,
        content=InlineTemplate(params.carbondata_content),
        mode=0644,
    )

    # create spark-env.sh in etc/conf dir
    File(
        os.path.join(params.spark_conf, 'spark-env.sh'),
        owner=params.spark_user,
        group=params.spark_group,
        content=InlineTemplate(params.spark_env_sh),
        mode=0644,
    )

    # create log4j.properties in etc/conf dir
    File(
        os.path.join(params.spark_conf, 'log4j.properties'),
        owner=params.spark_user,
        group=params.spark_group,
        content=params.spark_log4j_properties,
        mode=0644,
    )

    # create metrics.properties in etc/conf dir
    File(
        os.path.join(params.spark_conf, 'metrics.properties'),
        owner=params.spark_user,
        group=params.spark_group,
        content=InlineTemplate(params.spark_metrics_properties),
        mode=0644)

    if params.is_hive_installed:
        XmlConfig(
            "hive-site.xml",
            conf_dir=params.spark_conf,
            configurations=params.spark_hive_properties,
            owner=params.spark_user,
            group=params.spark_group,
            mode=0644)

    if params.has_spark_thriftserver:
        spark2_thrift_sparkconf = dict(
            params.config['configurations']['spark2-thrift-sparkconf'])

        if params.security_enabled and 'spark.yarn.principal' in spark2_thrift_sparkconf:
            spark2_thrift_sparkconf[
                'spark.yarn.principal'] = spark2_thrift_sparkconf[
                'spark.yarn.principal'].replace('_HOST',
                                                socket.getfqdn().lower())

        PropertiesFile(
            params.spark_thrift_server_conf_file,
            properties=spark2_thrift_sparkconf,
            owner=params.hive_user,
            group=params.user_group,
            key_value_delimiter=" ",
            mode=0644)

    if params.spark_thrift_fairscheduler_content:
        # create spark-thrift-fairscheduler.xml
        File(
            os.path.join(params.spark_conf, "spark-thrift-fairscheduler.xml"),
            owner=params.spark_user,
            group=params.spark_group,
            mode=0755,
            content=InlineTemplate(params.spark_thrift_fairscheduler_content))

    # Generate atlas-application.properties.xml file
    if params.enable_atlas_hook:
        PropertiesFile(
            params.spark_conf + params.atlas_hook_filename,
            properties=params.atlas_application_content,
            owner=params.spark_user,
            group=params.user_group,
            key_value_delimiter=" ",
            mode=0644)
