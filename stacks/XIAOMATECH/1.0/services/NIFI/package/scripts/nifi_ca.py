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

import nifi_toolkit_util_common, os

from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.resources.system import Directory, Execute
from resource_management.core.sudo import kill, read_file, path_isfile, unlink
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.script.script import Script
from resource_management.core.resources import File
from resource_management.core.source import Template
from nifi import install_nifi_toolkit, install_nifi


class CertificateAuthority(Script):
    def install(self, env):
        import params
        import status_params

        self.install_packages(env)
        install_nifi()
        install_nifi_toolkit()
        # Be sure ca script is in cache
        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_user,
            params.nifi_group,
            upgrade_type=None,
            service=nifi_toolkit_util_common.NIFI)

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        # create the log, pid, conf dirs if not already present
        Directory([
            status_params.nifi_pid_dir, params.nifi_node_log_dir,
            params.nifi_config_dir
        ],
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True)

        ca_json = os.path.join(params.nifi_config_dir,
                               'nifi-certificate-authority.json')
        ca_dict = nifi_toolkit_util_common.load(ca_json)
        nifi_toolkit_util_common.overlay(ca_dict, params.nifi_ca_config)
        nifi_toolkit_util_common.dump(ca_json, ca_dict, params.nifi_user,
                                      params.nifi_group)

        generate_logfeeder_input_config(
            'nifi',
            Template("input.config-nifi.json.j2", extra_imports=[default]))

        Directory([params.nifi_config_dir],
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True,
                  recursive_ownership=True)

    def invalidate_ca_server(self, env):
        import params
        ca_json = os.path.join(params.nifi_config_dir,
                               'nifi-certificate-authority.json')
        nifi_toolkit_util_common.move_store(
            nifi_toolkit_util_common.load(ca_json), 'keyStore')
        unlink(ca_json)

    def status(self, env):
        import status_params
        check_process_status(status_params.nifi_ca_pid_file)

    def start(self, env, upgrade_type=None):
        import params
        import status_params
        install_nifi()
        install_nifi_toolkit()
        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_user,
            params.nifi_group,
            upgrade_type,
            service=nifi_toolkit_util_common.NIFI)

        self.configure(env)
        ca_server_script = nifi_toolkit_util_common.get_toolkit_script(
            'tls-toolkit.sh', params.toolkit_tmp_dir,
            params.stack_version_buildnum)
        run_ca_script = os.path.join(params.toolkit_tmp_dir, 'run_ca.sh')
        Directory([params.nifi_config_dir],
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True,
                  recursive_ownership=True)

        File(ca_server_script, mode=0755)
        File(run_ca_script, mode=0755)
        Execute(
            (run_ca_script, "start", params.jdk64_home, ca_server_script,
             params.nifi_config_dir + '/nifi-certificate-authority.json',
             params.nifi_ca_log_file_stdout, params.nifi_ca_log_file_stderr,
             status_params.nifi_ca_pid_file, params.toolkit_ca_check_url),
            user=params.nifi_user,
            logoutput=True)
        if not os.path.isfile(status_params.nifi_ca_pid_file):
            raise Exception('Expected pid file to exist')

    def stop(self, env, upgrade_type=None):
        import params
        import status_params

        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_user,
            params.nifi_group,
            upgrade_type,
            service=nifi_toolkit_util_common.NIFI)
        run_ca_script = os.path.join(params.toolkit_tmp_dir, 'run_ca.sh')
        ca_server_script = nifi_toolkit_util_common.get_toolkit_script(
            'tls-toolkit.sh', params.toolkit_tmp_dir,
            params.stack_version_buildnum)
        File(ca_server_script, mode=0755)
        File(run_ca_script, mode=0755)

        if path_isfile(status_params.nifi_ca_pid_file):
            Execute(
                (run_ca_script, "stop", params.jdk64_home, ca_server_script,
                 params.nifi_config_dir + '/nifi-certificate-authority.json',
                 params.nifi_ca_log_file_stdout,
                 params.nifi_ca_log_file_stderr,
                 status_params.nifi_ca_pid_file, params.toolkit_ca_check_url),
                user=params.nifi_user,
                logoutput=True)
            try:
                self.status(env)
            except ComponentIsNotRunning:
                unlink(status_params.nifi_ca_pid_file)


if __name__ == "__main__":
    CertificateAuthority().execute()
