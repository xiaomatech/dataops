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
from resource_management.core.resources.system import Directory
from resource_management.libraries.resources.xml_config import XmlConfig


class ResourceEstimator(Script):
    yarn_pid_dir = '/var/run/hadoop/yarn'

    def install(self, env):
        self.install_packages(env)
        install_yarn()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(
            'cd ' + params.install_dir +
            '/share/hadoop/tools/resourceestimator; ./bin/stop-estimator.sh; echo sucess',
            user=params.yarn_user)

    def start(self, env):
        import params
        env.set_params(params)
        install_yarn()
        self.configure(env)
        Execute(
            'cd ' + params.install_dir +
            '/share/hadoop/tools/resourceestimator; ./bin/start-estimator.sh; echo sucess',
            user=params.yarn_user)

    def configure(self, env):
        import params
        env.set_params(params)
        Directory(
            self.yarn_pid_dir,
            owner=params.yarn_user,
            group=params.user_group,
            create_parents=True,
            mode=0755)

        yarn(name="nodemanager")
        XmlConfig(
            "resourceestimator-config.xml",
            conf_dir=params.install_dir +
            '/share/hadoop/tools/resourceestimator/conf',
            configurations=params.config['configurations']
            ['resourceestimator-config'],
            configuration_attributes=params.config['configurationAttributes']
            ['resourceestimator-config'],
            owner=params.hdfs_user,
            group=params.user_group,
            mode=0644)

    def status(self, env):
        import params
        env.set_params(params)
        pid_file = self.yarn_pid_dir + '/hadoop-' + params.yarn_user + '-resourceestimator.pid'
        check_process_status(pid_file)


if __name__ == "__main__":
    ResourceEstimator().execute()
