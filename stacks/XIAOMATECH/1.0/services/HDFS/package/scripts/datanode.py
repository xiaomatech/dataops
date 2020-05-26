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
import datanode_upgrade
from hdfs_datanode import datanode
from resource_management.libraries.script.script import Script
from resource_management.core.logger import Logger
from hdfs import hdfs, reconfig, install_hadoop
from utils import get_hdfs_binary

from resource_management.core.resources.system import Directory, Execute, File


class DataNode(Script):
    def get_hdfs_binary(self):
        return get_hdfs_binary("hadoop-hdfs-datanode")

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_hadoop()

    def configure(self, env):
        import params
        env.set_params(params)
        hdfs("datanode")
        datanode(action="configure")

    def save_configs(self, env):
        import params
        env.set_params(params)
        hdfs("datanode")

    def reload_configs(self, env):
        import params
        env.set_params(params)
        Logger.info("RELOAD CONFIGS")
        reconfig("datanode", params.dfs_dn_ipc_address)

    def start(self, env):
        import params
        env.set_params(params)
        install_hadoop()
        self.configure(env)
        Directory(params.ramdisk + '/hdfs/data',
                  create_parents=True,
                  mode=0751,
                  owner=params.hdfs_user,
                  group=params.user_group)
        datanode(action="start")

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        hdfs_binary = self.get_hdfs_binary()
        if upgrade_type == "rolling":
            stopped = datanode_upgrade.pre_rolling_upgrade_shutdown(
                hdfs_binary)
            if not stopped:
                datanode(action="stop")
        else:
            datanode(action="stop")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        datanode(action="status")

    def pre_upgrade_restart(self, env):
        Logger.info("Executing DataNode Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def post_upgrade_restart(self, env):
        Logger.info("Executing DataNode Stack Upgrade post-restart")
        import params
        env.set_params(params)
        hdfs_binary = self.get_hdfs_binary()
        # ensure the DataNode has started and rejoined the cluster
        datanode_upgrade.post_upgrade_check(hdfs_binary)

    def get_log_folder(self):
        import params
        return params.hdfs_log_dir

    def get_user(self):
        import params
        return params.hdfs_user

    def get_pid_files(self):
        import params
        return [params.datanode_pid_file]


if __name__ == "__main__":
    DataNode().execute()
