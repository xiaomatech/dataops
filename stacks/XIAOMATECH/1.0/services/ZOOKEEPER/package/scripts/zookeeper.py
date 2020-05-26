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
import os
import sys

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.core.resources.system import Directory, File
from resource_management.core.resources.service import ServiceConfig
from resource_management.core.source import InlineTemplate, Template
from resource_management.core.resources.system import Execute


def install_zookeeper():
    import params
    Directory([params.config_dir],
              owner=params.zk_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.zk_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.config_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/zookeeper.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.zk_user, params.user_group,params.stack_root,params.version_dir))
        Execute('chown -R %s:%s %s' % (params.zk_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def zookeeper(type=None):
    import params

    Directory(
        params.config_dir,
        owner=params.zk_user,
        create_parents=True,
        group=params.user_group)

    File(
        os.path.join(params.config_dir, "zookeeper-env.sh"),
        content=InlineTemplate(params.zk_env_sh_template),
        owner=params.zk_user,
        group=params.user_group)

    configFile("zoo.cfg", template_name="zoo.cfg.j2")
    configFile("configuration.xsl", template_name="configuration.xsl.j2")

    Directory(
        params.zk_pid_dir,
        owner=params.zk_user,
        create_parents=True,
        group=params.user_group,
        mode=0755,
    )

    Directory(
        params.zk_log_dir,
        owner=params.zk_user,
        create_parents=True,
        group=params.user_group,
        mode=0755,
    )

    Directory(
        params.zk_data_dir,
        owner=params.zk_user,
        create_parents=True,
        cd_access="a",
        group=params.user_group,
        mode=0755,
    )

    if type == 'server':
        myid = str(sorted(params.zookeeper_hosts).index(params.hostname) + 1)

        File(os.path.join(params.zk_data_dir, "myid"), mode=0644, content=myid)

        generate_logfeeder_input_config(
            'zookeeper',
            Template(
                "input.config-zookeeper.json.j2", extra_imports=[default]))

    if (params.log4j_props != None):
        File(
            os.path.join(params.config_dir, "log4j.properties"),
            mode=0644,
            group=params.user_group,
            owner=params.zk_user,
            content=InlineTemplate(params.log4j_props))
    elif (os.path.exists(os.path.join(params.config_dir, "log4j.properties"))):
        File(
            os.path.join(params.config_dir, "log4j.properties"),
            mode=0644,
            group=params.user_group,
            owner=params.zk_user)

    if params.security_enabled:
        if type == "server":
            configFile(
                "zookeeper_jaas.conf", template_name="zookeeper_jaas.conf.j2")
            configFile(
                "zookeeper_client_jaas.conf",
                template_name="zookeeper_client_jaas.conf.j2")
        else:
            configFile(
                "zookeeper_client_jaas.conf",
                template_name="zookeeper_client_jaas.conf.j2")

    File(
        os.path.join(params.config_dir, "zoo_sample.cfg"),
        owner=params.zk_user,
        group=params.user_group)


def configFile(name, template_name=None, mode=None):
    import params

    File(
        os.path.join(params.config_dir, name),
        content=Template(template_name),
        owner=params.zk_user,
        group=params.user_group,
        mode=mode)
