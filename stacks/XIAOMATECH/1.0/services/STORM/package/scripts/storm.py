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

from resource_management.core.exceptions import Fail
from resource_management.core.resources.service import ServiceConfig
from resource_management.core.resources.system import Directory, Execute, File, Link
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.resources.template_config import TemplateConfig
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.core.source import Template
from storm_yaml_utils import yaml_config_template, yaml_config
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from ambari_commons.constants import SERVICE

import os, sys
script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/atlas'
sys.path.append(script_path)
from setup_atlas_hook import has_atlas_in_cluster, setup_atlas_hook, setup_atlas_jar_symlinks


def install_storm():
    import params
    Directory([params.conf_dir],
              owner=params.storm_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.storm_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/storm.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.storm_user, params.user_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.storm_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def storm(name=None):
    import params
    import os

    Directory(
        params.log_dir,
        owner=params.storm_user,
        group=params.user_group,
        mode=0777,
        create_parents=True,
        cd_access="a",
    )

    Directory(
        [params.pid_dir, params.local_dir],
        owner=params.storm_user,
        group=params.user_group,
        create_parents=True,
        cd_access="a",
        mode=0755,
    )

    Directory(
        params.conf_dir,
        group=params.user_group,
        create_parents=True,
        cd_access="a",
    )

    File(
        format("{limits_conf_dir}/storm.conf"),
        owner='root',
        group='root',
        mode=0644,
        content=Template("storm.conf.j2"))

    File(
        format("{conf_dir}/config.yaml"),
        content=Template("config.yaml.j2"),
        owner=params.storm_user,
        group=params.user_group)

    configurations = params.config['configurations']['storm-site']

    File(
        format("{conf_dir}/storm.yaml"),
        content=yaml_config_template(configurations),
        owner=params.storm_user,
        group=params.user_group)

    File(
        format("{conf_dir}/storm-env.sh"),
        owner=params.storm_user,
        content=InlineTemplate(params.storm_env_sh_template))

    generate_logfeeder_input_config(
        'storm', Template(
            "input.config-storm.json.j2", extra_imports=[default]))

    # Generate atlas-application.properties.xml file and symlink the hook jars
    if params.enable_atlas_hook:
        atlas_hook_filepath = os.path.join(params.conf_dir,
                                           params.atlas_hook_filename)
        setup_atlas_hook(
            SERVICE.STORM, params.storm_atlas_application_properties,
            atlas_hook_filepath, params.storm_user, params.user_group)

    if params.storm_logs_supported:
        Directory(
            params.log4j_dir,
            owner=params.storm_user,
            group=params.user_group,
            mode=0755,
            create_parents=True)

        File(
            format("{log4j_dir}/cluster.xml"),
            owner=params.storm_user,
            content=InlineTemplate(params.storm_cluster_log4j_content))
        File(
            format("{log4j_dir}/worker.xml"),
            owner=params.storm_user,
            content=InlineTemplate(params.storm_worker_log4j_content))

    if params.security_enabled:
        TemplateConfig(
            format("{conf_dir}/storm_jaas.conf"),
            owner=params.storm_user,
            mode=0644)
        TemplateConfig(
            format("{conf_dir}/client_jaas.conf"),
            owner=params.storm_user,
            mode=0644)
        minRuid = configurations['_storm.min.ruid'] if configurations.has_key(
            '_storm.min.ruid') else ''

        min_user_ruid = int(
            minRuid) if minRuid.isdigit() else _find_real_user_min_uid()

        File(
            format("{conf_dir}/worker-launcher.cfg"),
            content=Template(
                "worker-launcher.cfg.j2", min_user_ruid=min_user_ruid),
            owner='root',
            group=params.user_group)
    else:
        File(format("{conf_dir}/storm_jaas.conf"), action="delete")
        File(format("{conf_dir}/client_jaas.conf"), action="delete")


def _find_real_user_min_uid():
    """
    Finds minimal real user UID
    """
    with open('/etc/login.defs') as f:
        for line in f:
            if line.strip().startswith('UID_MIN') and len(
                    line.split()) == 2 and line.split()[1].isdigit():
                return int(line.split()[1])
    raise Fail(
        "Unable to find UID_MIN in file /etc/login.defs. Expecting format e.g.: 'UID_MIN    500'"
    )
