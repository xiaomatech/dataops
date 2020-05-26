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
from resource_management.libraries.functions import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute

from resource_management.libraries.functions.copy_tarball import copy_to_hdfs

import glob

from yarn import yarn, install_yarn
from service import service


class ApplicationTimelineServer(Script):
    def install(self, env):
        self.install_packages(env)
        install_yarn()

    def start(self, env):
        import params
        env.set_params(params)
        install_yarn()
        self.configure(env)  # FOR SECURITY
        service('timelineserver', action='start')
        # create hbase table to timeline collector
        Execute('source ' + params.config_dir + '/hadoop-env.sh;' +
                params.install_dir + '/bin/hadoop org.apache.hadoop.yarn.server.timelineservice.storage.TimelineSchemaCreator -Dhbase.client.retries.number=35 -create -skipExistingTable')

    def stop(self, env):
        import params
        env.set_params(params)
        service('timelineserver', action='stop')

    def configure(self, env):
        import params
        env.set_params(params)

        params.HdfsResource('/apps/hbase/coprocessor',
                            type="directory",
                            action="create_on_execute",
                            owner=params.hdfs_user,
                            group=params.user_group,
                            change_permissions_for_parents=True,
                            mode=0777)
        coprocessor_path = params.install_dir + '/share/hadoop/yarn/timelineservice/hadoop-yarn-server-timelineservice-hbase-coprocessor*.jar'
        coprocessor_path_arr = glob.glob(coprocessor_path)
        if len(coprocessor_path) > 0:
            coprocessor_path = coprocessor_path_arr.pop()
            copy_to_hdfs(
                "yarn",
                params.user_group,
                params.hdfs_user,
                custom_source_file=coprocessor_path,
                custom_dest_file='/apps/hbase/coprocessor/hadoop-yarn-server-timelineservice.jar')
            params.HdfsResource(None, action="execute")

        yarn(name='apptimelineserver')

    def pre_upgrade_restart(self, env):
        Logger.info("Executing Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.yarn_historyserver_pid_file)

    def get_log_folder(self):
        import params
        return params.yarn_log_dir

    def get_user(self):
        import params
        return params.yarn_user

    def get_pid_files(self):
        import status_params
        Execute(
            format(
                "mv {status_params.yarn_historyserver_pid_file_old} {status_params.yarn_historyserver_pid_file}"
            ),
            only_if=format(
                "test -e {status_params.yarn_historyserver_pid_file_old}",
                user=status_params.yarn_user))
        return [status_params.yarn_historyserver_pid_file]


if __name__ == "__main__":
    ApplicationTimelineServer().execute()
