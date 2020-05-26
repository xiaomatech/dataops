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
# Python Imports
import os

# Local Imports
from resource_management.core.source import InlineTemplate, DownloadSource
from resource_management.libraries.functions import format
from resource_management.libraries.functions.get_config import get_config
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.core.resources.system import File, Link, Directory
from ambari_commons.constants import SERVICE
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script
import os, sys

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/atlas'
sys.path.append(script_path)
from setup_atlas_hook import has_atlas_in_cluster, setup_atlas_hook, setup_atlas_jar_symlinks


def install_sqoop():
    import params
    Directory([params.sqoop_conf_dir, '/var/run/sqoop', '/var/log/sqoop'],
              owner=params.sqoop_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.sqoop_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('ln -s ' + params.sqoop_conf_dir + ' ' + params.install_dir +
                '/etc')
        Execute('chown -R %s:%s %s/%s' % (
        params.sqoop_user, params.user_group, Script.get_stack_root(), params.version_dir))
        Execute('chown -R %s:%s %s' % (params.sqoop_user, params.user_group,
                                       params.install_dir))


def sqoop(type=None):
    import params
    Directory(
        params.sqoop_conf_dir,
        owner=params.sqoop_user,
        group=params.user_group,
        create_parents=True)

    configs = {}
    sqoop_site_config = get_config('sqoop-site')
    if sqoop_site_config:
        configs.update(sqoop_site_config)

        XmlConfig(
            "sqoop-site.xml",
            conf_dir=params.sqoop_conf_dir,
            configurations=configs,
            configuration_attributes=params.config['configurationAttributes']
            ['sqoop-site'],
            owner=params.sqoop_user,
            group=params.user_group)

    # Generate atlas-application.properties.xml file and symlink the hook jars
    if params.enable_atlas_hook:
        atlas_hook_filepath = os.path.join(params.sqoop_conf_dir,
                                           params.atlas_hook_filename)
        setup_atlas_hook(
            SERVICE.SQOOP, params.sqoop_atlas_application_properties,
            atlas_hook_filepath, params.sqoop_user, params.user_group)

    File(
        format("{sqoop_conf_dir}/sqoop-env.sh"),
        owner=params.sqoop_user,
        group=params.user_group,
        content=InlineTemplate(params.sqoop_env_sh_template))
    update_config_permissions(
        ["sqoop-env-template.sh", "sqoop-site-template.xml", "sqoop-site.xml"])


def update_config_permissions(names):
    import params
    for filename in names:
        full_filename = os.path.join(params.sqoop_conf_dir, filename)
        File(
            full_filename,
            owner=params.sqoop_user,
            group=params.user_group,
            only_if=format("test -e {full_filename}"))
