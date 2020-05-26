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

import nodemanager_upgrade

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.security_commons import build_expectations, \
    cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
    FILE_TYPE_XML
from resource_management.core.logger import Logger
from yarn import yarn, install_yarn
from service import service
from resource_management.core.resources.system import Execute


class Nodemanager(Script):
    def install(self, env):
        self.install_packages(env)
        install_yarn()

    def stop(self, env):
        import params
        env.set_params(params)
        service('nodemanager', action='stop')

    def start(self, env):
        import params
        env.set_params(params)
        install_yarn()
        Execute(
            'chown -R ' + params.yarn_user + ':' + params.user_group + ' /sys/fs/cgroup/cpu/yarn /sys/fs/cgroup/memory/yarn /sys/fs/cgroup/blkio/yarn /sys/fs/cgroup/net_cls/yarn')
        Execute('chown root:hadoop ' + params.install_dir +
                '/bin/container-executor')
        self.configure(env)  # FOR SECURITY
        service('nodemanager', action='start')

    def configure(self, env):
        import params
        env.set_params(params)
        yarn(name="nodemanager")

    def pre_upgrade_restart(self, env):
        Logger.info("Executing NodeManager Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def post_upgrade_restart(self, env):
        Logger.info("Executing NodeManager Stack Upgrade post-restart")
        import params
        env.set_params(params)
        nodemanager_upgrade.post_upgrade_check()

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.nodemanager_pid_file)

    def get_log_folder(self):
        import params
        return params.yarn_log_dir

    def get_user(self):
        import params
        return params.yarn_user

    def get_pid_files(self):
        import status_params
        return [status_params.nodemanager_pid_file]


if __name__ == "__main__":
    Nodemanager().execute()
