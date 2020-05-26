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

import ambari_simplejson as json
from ambari_jinja2 import Environment as JinjaEnvironment
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Directory, File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.libraries.script import Script


def setup_config():
    import params
    stackversion = params.stack_version_unformatted
    Logger.info("FS Type: {0}".format(params.dfs_type))

    is_hadoop_conf_dir_present = False
    if hasattr(params, "hadoop_conf_dir"
               ) and params.hadoop_conf_dir is not None and os.path.exists(
                   params.hadoop_conf_dir):
        is_hadoop_conf_dir_present = True
    else:
        Logger.warning(
            "Parameter hadoop_conf_dir is missing or directory does not exist. This is expected if this host does not have any Hadoop components."
        )

    if is_hadoop_conf_dir_present and params.has_namenode:
        # create core-site only if the hadoop config diretory exists
        XmlConfig(
            "core-site.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['core-site'],
            configuration_attributes=params.config['configurationAttributes']
            ['core-site'],
            owner=params.hdfs_user,
            group=params.user_group,
            only_if=format("ls {hadoop_conf_dir}"),
            xml_include_file=params.mount_table_xml_inclusion_file_full_path)

        if params.mount_table_content:
            File(
                os.path.join(params.hadoop_conf_dir,
                             params.xml_inclusion_file_name),
                owner=params.hdfs_user,
                group=params.user_group,
                content=params.mount_table_content)

    Directory(
        params.logsearch_logfeeder_conf,
        mode=0755,
        cd_access='a',
        create_parents=True)

    if params.logsearch_config_file_exists:
        File(
            format("{logsearch_logfeeder_conf}/" +
                   params.logsearch_config_file_name),
            content=Template(
                params.logsearch_config_file_path, extra_imports=[default]))
    else:
        Logger.warning('No logsearch configuration exists at ' +
                       params.logsearch_config_file_path)
