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

from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute, Directory, File, Link
from resource_management.core.resources import Package
from resource_management.core.source import Template
from resource_management.core.resources.service import ServiceConfig
from resource_management.libraries.resources.xml_config import XmlConfig

from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format
import os
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def install_hadoop_share_lib():
    import params
    share_dir = '/usr/share/java/hadoop/'
    Directory(
        share_dir,
        owner=params.hdfs_user,
        group=params.user_group,
        create_parents=True,
        mode=0755)

    hadoop_native_so_file = share_dir + '/native/libgplcompression.a'
    if not os.path.exists(hadoop_native_so_file):
        Execute('mkdir -p ' + share_dir + '/native/')
        Execute(
            'wget ' + download_url_base + '/share/hadoop/hadoopnative.tar.gz -O /tmp/hadoopnative.tar.gz',
            user=params.hdfs_user)
        Execute('tar -zxvf /tmp/hadoopnative.tar.gz -C ' + share_dir +
                '/native/')

    share_jar_files_conf = default("/configurations/hadoop-env/share_jars", '').strip()
    if share_jar_files_conf != '':
        share_jar_files = share_jar_files_conf.split(',')
        for jar_file in share_jar_files:
            jar_file_path = share_dir + jar_file.strip()
            if not os.path.exists(jar_file_path):
                Execute('wget ' + download_url_base + '/share/hadoop/' + jar_file + ' -O ' + jar_file_path,
                        user=params.hdfs_user)


def install_hadoop():
    import params
    Directory(
        params.hdfs_log_dir,
        owner=params.hdfs_user,
        group=params.user_group,
        create_parents=True,
        mode=0755)

    Directory(
        params.limits_conf_dir,
        create_parents=True,
        owner='root',
        group='root')

    Directory(
        params.hadoop_conf_dir,
        create_parents=True,
        owner='root',
        group='root')

    install_hadoop_share_lib()

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.hdfs_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/etc/hadoop')
        Execute('ln -s ' + params.hadoop_conf_dir + ' ' + params.install_dir +
                '/etc/hadoop')
        Execute('mkdir ' + params.install_dir + '/logs && chmod 777 ' +
                params.install_dir + '/logs')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/hadoop.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.hdfs_user, params.user_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.hdfs_user, params.user_group,
                                       params.install_dir))
        Execute('chmod -R 755 %s/%s' % (params.stack_root, params.version_dir))
        Execute('chown root:%s %s/bin/container-executor' %
                (params.user_group, params.install_dir))

        Execute('/bin/rm -f /tmp/' + params.filename)


def hdfs(name=None):
    import params

    # On some OS this folder could be not exists, so we will create it before pushing there files
    Directory(
        params.limits_conf_dir,
        create_parents=True,
        owner='root',
        group='root')

    File(
        os.path.join(params.limits_conf_dir, 'hdfs.conf'),
        owner='root',
        group='root',
        mode=0644,
        content=Template("hdfs.conf.j2"))

    if params.security_enabled:
        File(
            os.path.join(params.hadoop_conf_dir, 'hdfs_dn_jaas.conf'),
            owner=params.hdfs_user,
            group=params.user_group,
            content=Template("hdfs_dn_jaas.conf.j2"))
        File(
            os.path.join(params.hadoop_conf_dir, 'hdfs_nn_jaas.conf'),
            owner=params.hdfs_user,
            group=params.user_group,
            content=Template("hdfs_nn_jaas.conf.j2"))
        if params.dfs_ha_enabled:
            File(
                os.path.join(params.hadoop_conf_dir, 'hdfs_jn_jaas.conf'),
                owner=params.hdfs_user,
                group=params.user_group,
                content=Template("hdfs_jn_jaas.conf.j2"))

        tc_mode = 0644
        tc_owner = "root"
    else:
        tc_mode = None
        tc_owner = params.hdfs_user

    if "hadoop-policy" in params.config['configurations']:
        XmlConfig(
            "hadoop-policy.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['hadoop-policy'],
            configuration_attributes=params.config['configurationAttributes']
            ['hadoop-policy'],
            owner=params.hdfs_user,
            group=params.user_group)

    if "ssl-client" in params.config['configurations']:
        XmlConfig(
            "ssl-client.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['ssl-client'],
            configuration_attributes=params.config['configurationAttributes']
            ['ssl-client'],
            owner=params.hdfs_user,
            group=params.user_group)

        Directory(
            params.hadoop_conf_secure_dir,
            create_parents=True,
            owner='root',
            group=params.user_group,
            cd_access='a',
        )

        XmlConfig(
            "ssl-client.xml",
            conf_dir=params.hadoop_conf_secure_dir,
            configurations=params.config['configurations']['ssl-client'],
            configuration_attributes=params.config['configurationAttributes']
            ['ssl-client'],
            owner=params.hdfs_user,
            group=params.user_group)

    if "ssl-server" in params.config['configurations']:
        XmlConfig(
            "ssl-server.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['ssl-server'],
            configuration_attributes=params.config['configurationAttributes']
            ['ssl-server'],
            owner=params.hdfs_user,
            group=params.user_group)

    XmlConfig(
        "hdfs-site.xml",
        conf_dir=params.hadoop_conf_dir,
        configurations=params.config['configurations']['hdfs-site'],
        configuration_attributes=params.config['configurationAttributes']
        ['hdfs-site'],
        owner=params.hdfs_user,
        group=params.user_group)

    XmlConfig(
        "core-site.xml",
        conf_dir=params.hadoop_conf_dir,
        configurations=params.config['configurations']['core-site'],
        configuration_attributes=params.config['configurationAttributes']
        ['core-site'],
        owner=params.hdfs_user,
        group=params.user_group,
        mode=0644,
        xml_include_file=params.mount_table_xml_inclusion_file_full_path)

    if params.mount_table_content:
        File(
            params.mount_table_xml_inclusion_file_full_path,
            owner=params.hdfs_user,
            group=params.user_group,
            content=params.mount_table_content,
            mode=0644)

    File(
        os.path.join(params.hadoop_conf_dir, 'slaves'),
        owner=tc_owner,
        content=Template("slaves.j2"))


class ConfigStatusParser():
    def __init__(self):
        self.reconfig_successful = False

    def handle_new_line(self, line, is_stderr):
        if is_stderr:
            return

        if line.startswith('SUCCESS: Changed property'):
            self.reconfig_successful = True

        Logger.info('[reconfig] %s' % (line))


def reconfig(componentName, componentAddress):
    import params

    if params.security_enabled:
        Execute(params.nn_kinit_cmd, user=params.hdfs_user)

    nn_reconfig_cmd = format(
        params.hadoop_bin_dir + '/hdfs --config {hadoop_conf_dir} dfsadmin -reconfig {componentName} {componentAddress} start'
    )

    Execute(
        nn_reconfig_cmd,
        user=params.hdfs_user,
        logoutput=True,
        path=params.hadoop_bin_dir)

    nn_reconfig_cmd = format(
        params.hadoop_bin_dir + '/hdfs --config {hadoop_conf_dir} dfsadmin -reconfig {componentName} {componentAddress} status'
    )
    config_status_parser = ConfigStatusParser()
    Execute(
        nn_reconfig_cmd,
        user=params.hdfs_user,
        logoutput=False,
        path=params.hadoop_bin_dir,
        on_new_line=config_status_parser.handle_new_line)

    if not config_status_parser.reconfig_successful:
        Logger.info('Reconfiguration failed')
        raise Fail('Reconfiguration failed!')

    Logger.info('Reconfiguration successfully completed.')
