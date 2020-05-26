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
from resource_management.libraries.functions.check_process_status import check_process_status
from yarn import yarn, install_yarn
from resource_management.core.resources.system import Execute


class SharedCacheManager(Script):
    def install(self, env):
        self.install_packages(env)
        install_yarn()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(
            params.hadoop_bin_dir + '/yarn --daemon stop sharedcachemanager',
            user=params.yarn_user)

    def start(self, env):
        import params
        env.set_params(params)
        install_yarn()
        self.configure(env)
        Execute(
            params.hadoop_bin_dir + '/yarn --daemon start sharedcachemanager',
            user=params.yarn_user)

    def configure(self, env):
        import params
        env.set_params(params)
        yarn(name="nodemanager")
        params.HdfsResource(
            params.sharedcache_dir,
            action="create_on_execute",
            type="directory",
            owner=params.yarn_user,
            group=params.user_group)
        params.HdfsResource(None, action="execute")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.yarn_pid_dir + '/hadoop-' +
                             params.yarn_user + '-sharedcachemanager.pid')


if __name__ == "__main__":
    SharedCacheManager().execute()
