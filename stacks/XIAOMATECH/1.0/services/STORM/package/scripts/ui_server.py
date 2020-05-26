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
from storm import storm, install_storm
from service import service
from resource_management.libraries.functions import check_process_status
from resource_management.libraries.script import Script
from resource_management.libraries.functions import format
from resource_management.core.resources.system import Link
from resource_management.core.resources.system import Execute
from setup_ranger_storm import setup_ranger_storm


class UiServer(Script):
    def install(self, env):
        install_storm()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        storm("ui")

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

    def link_metrics_sink_jar(self):
        import params
        # Add storm metrics reporter JAR to storm-ui-server classpath.
        sink_jar = params.metric_collector_sink_jar

        Execute(
            format(
                "{sudo} ln -s {sink_jar} {storm_lib_dir}/ambari-metrics-storm-sink.jar"
            ),
            not_if=format("ls {storm_lib_dir}/ambari-metrics-storm-sink.jar"),
            only_if=format("ls {sink_jar}"))

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        install_storm()
        self.configure(env)
        self.link_metrics_sink_jar()
        setup_ranger_storm(upgrade_type=upgrade_type)
        service("ui", action="start")

    def stop(self, env):
        import params
        env.set_params(params)
        service("ui", action="stop")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.pid_ui)

    def get_log_folder(self):
        import params
        return params.log_dir

    def get_user(self):
        import params
        return params.storm_user

    def get_pid_files(self):
        import status_params
        return [status_params.pid_ui]


if __name__ == "__main__":
    UiServer().execute()
