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
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.get_config import get_config
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.resources.template_config import TemplateConfig
from resource_management.core.resources.system import File, Execute, Directory
from resource_management.core.shell import as_user
from resource_management.core.source import Template, InlineTemplate


def install_knox():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.knox_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' mkdir -p ' + params.knox_conf_dir + ' && cp -r ' +
                params.install_dir + '/conf/* ' + params.knox_conf_dir)
        Execute(' cp -rf ' + params.install_dir + '/conf/*  ' +
                params.knox_conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.knox_conf_dir + ' ' + params.install_dir +
                '/conf')

        Execute(' rm -rf ' + params.install_dir + '/pids')
        Execute('ln -s ' + params.knox_pid_dir + ' ' + params.install_dir +
                '/pids')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/knox.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.knox_user, params.knox_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.knox_user, params.knox_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def knox():
    import params
    Directory(
        [
            params.knox_data_dir,params.knox_data_backup_dir, params.knox_logs_dir, params.knox_pid_dir,
            params.knox_conf_dir,
            os.path.join(params.knox_conf_dir, "topologies"),
            params.knox_descriptors_dir, params.knox_shared_providers_dir
        ],
        owner=params.knox_user,
        group=params.knox_group,
        create_parents=True,
        cd_access="a",
        mode=0755,
        recursive_ownership=True,
    )

    XmlConfig(
        "gateway-site.xml",
        conf_dir=params.knox_conf_dir,
        configurations=params.config['configurations']['gateway-site'],
        configuration_attributes=params.config['configurationAttributes']
        ['gateway-site'],
        owner=params.knox_user,
        group=params.knox_group,
    )

    File(
        format("{params.knox_conf_dir}/gateway-log4j.properties"),
        mode=0644,
        group=params.knox_group,
        owner=params.knox_user,
        content=InlineTemplate(params.gateway_log4j))

    File(
        format("{params.knox_conf_dir}/topologies/default.xml"),
        mode=0600,
        group=params.knox_group,
        owner=params.knox_user,
        content=InlineTemplate(params.topology_template))

    if params.admin_topology_template:
        File(
            format("{params.knox_conf_dir}/topologies/admin.xml"),
            mode=0600,
            group=params.knox_group,
            owner=params.knox_user,
            content=InlineTemplate(params.admin_topology_template))

    knoxsso_topology_template_content = get_config("knoxsso-topology")
    if knoxsso_topology_template_content:
        File(
            os.path.join(params.knox_conf_dir, "topologies", "knoxsso.xml"),
            mode=0600,
            group=params.knox_group,
            owner=params.knox_user,
            content=InlineTemplate(params.knoxsso_topology_template))

    if params.security_enabled:
        TemplateConfig(
            format("{knox_conf_dir}/krb5JAASLogin.conf"),
            owner=params.knox_user,
            template_tag=None)

    generate_logfeeder_input_config(
        'knox', Template("input.config-knox.json.j2", extra_imports=[default]))

    cmd = format(
        '{knox_client_bin} create-master --master {knox_master_secret!p}')
    master_secret_exist = as_user(
        format('test -f {knox_master_secret_path}'), params.knox_user)

    Execute(
        cmd,
        user=params.knox_user,
        environment={'JAVA_HOME': params.java_home},
        not_if=master_secret_exist,
    )

    cmd = format(
        '{knox_client_bin} create-cert --hostname {knox_host_name_in_cluster}')
    cert_store_exist = as_user(
        format('test -f {knox_cert_store_path}'), params.knox_user)

    Execute(
        cmd,
        user=params.knox_user,
        environment={'JAVA_HOME': params.java_home},
        not_if=cert_store_exist,
    )


def update_knox_logfolder_permissions():
    """
     Fix for the bug with rpm/deb packages. During installation of the package, they re-apply permissions to the
     folders below; such behaviour will affect installations with non-standard user name/group and will put
     cluster in non-working state
    """
    import params

    Directory(
        params.knox_logs_dir,
        owner=params.knox_user,
        group=params.knox_group,
        create_parents=True,
        cd_access="a",
        mode=0700,
        recursive_ownership=True,
    )
