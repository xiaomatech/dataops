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
# Python Imports

from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import File, Execute, Directory
from resource_management.core.source import InlineTemplate
from resource_management.libraries.script import Script


class HiveMetastore(Script):
    def install(self, env):
        import params
        env.set_params(params)
        packages = ['waggle-dance-rpm']
        Package(packages)

    def start(self, env):
        import params
        env.set_params(params)
        Execute('/etc/init.d/waggle-dance start')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('/etc/init.d/waggle-dance stop')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("/opt/waggle-dance/conf/waggle-dance-federation.yml"),
            owner=params.hive_user,
            group=params.user_group,
            content=InlineTemplate(params.waggle_dance_federation_content),
            mode=0755)
        File(
            format("/opt/waggle-dance/conf/waggle-dance-server.yml"),
            owner=params.hive_user,
            group=params.user_group,
            content=InlineTemplate(params.waggle_dance_server_content),
            mode=0755)

    def status(self, env):
        import params
        env.set_params(params)
        Execute('/etc/init.d/waggle-dance status')


if __name__ == "__main__":
    HiveMetastore().execute()
