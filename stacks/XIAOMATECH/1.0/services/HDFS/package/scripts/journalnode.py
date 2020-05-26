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
from ambari_commons.constants import UPGRADE_TYPE_NON_ROLLING

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_XML
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Directory
from resource_management.core.source import Template
from utils import service
from hdfs import hdfs, install_hadoop
import journalnode_upgrade


class JournalNode(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_hadoop()

    def pre_upgrade_restart(self, env):
        Logger.info("Executing Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def start(self, env):
        import params
        install_hadoop()
        env.set_params(params)
        self.configure(env)
        service(
            action="start",
            name="journalnode",
            user=params.hdfs_user,
            create_pid_dir=True,
            create_log_dir=True)

    def post_upgrade_restart(self, env, upgrade_type=None):
        # express upgrade cannot determine if the JN quorum is established
        if upgrade_type == UPGRADE_TYPE_NON_ROLLING:
            return

        Logger.info("Executing Stack Upgrade post-restart")
        import params
        env.set_params(params)
        journalnode_upgrade.post_upgrade_check()

    def stop(self, env):
        import params

        env.set_params(params)
        service(
            action="stop",
            name="journalnode",
            user=params.hdfs_user,
            create_pid_dir=True,
            create_log_dir=True)

    def configure(self, env):
        import params

        Directory(
            params.jn_edits_dirs,
            create_parents=True,
            cd_access="a",
            owner=params.hdfs_user,
            group=params.user_group)
        env.set_params(params)
        generate_logfeeder_input_config(
            'hdfs',
            Template("input.config-hdfs.json.j2", extra_imports=[default]))
        hdfs()
        pass

    def status(self, env):
        import status_params

        env.set_params(status_params)
        check_process_status(status_params.journalnode_pid_file)

    def get_log_folder(self):
        import params
        return params.hdfs_log_dir

    def get_user(self):
        import params
        return params.hdfs_user

    def get_pid_files(self):
        import status_params
        return [status_params.journalnode_pid_file]


if __name__ == "__main__":
    JournalNode().execute()