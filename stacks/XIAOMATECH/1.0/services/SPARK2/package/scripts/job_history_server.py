#!/usr/bin/python
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
import os

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from setup_spark import *
from spark_service import spark_service


class JobHistoryServer(Script):
    def install(self, env):
        import params
        env.set_params(params)

        self.install_packages(env)
        install_spark()

    def configure(self, env):
        import params
        env.set_params(params)

        setup_spark(env, 'server', action='config')

    def start(self, env):
        import params
        env.set_params(params)
        install_spark()
        self.configure(env)
        spark_service('jobhistoryserver', action='start')

    def stop(self, env):
        import params
        env.set_params(params)

        spark_service('jobhistoryserver', action='stop')

    def status(self, env):
        import status_params
        env.set_params(status_params)

        check_process_status(status_params.spark_history_server_pid_file)

    def pre_upgrade_restart(self, env):
        import params

        env.set_params(params)

    def get_log_folder(self):
        import params
        return params.spark_log_dir

    def get_user(self):
        import params
        return params.spark_user

    def get_pid_files(self):
        import status_params
        return [status_params.spark_history_server_pid_file]


if __name__ == "__main__":
    JobHistoryServer().execute()
