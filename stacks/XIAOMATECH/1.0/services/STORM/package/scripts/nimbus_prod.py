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

import sys
from resource_management.libraries.script import Script
from storm import storm, install_storm
from supervisord_service import supervisord_service, supervisord_check_status
from resource_management.libraries.functions import format
from resource_management.core.resources.system import Execute


class Nimbus(Script):
    def install(self, env):
        install_storm()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)

        storm()

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        install_storm()
        self.configure(env)

        supervisord_service("nimbus", action="start")

    def stop(self, env):
        import params
        env.set_params(params)

        supervisord_service("nimbus", action="stop")

    def status(self, env):
        supervisord_check_status("nimbus")

    def get_log_folder(self):
        import params
        return params.log_dir

    def get_user(self):
        import params
        return params.storm_user


if __name__ == "__main__":
    Nimbus().execute()
