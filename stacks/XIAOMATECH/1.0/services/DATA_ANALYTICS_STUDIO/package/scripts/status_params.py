#!/usr/bin/env python

from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script

config = Script.get_config()

data_analytics_studio_pid_dir = default("/configurations/data_analytics_studio-env/data_analytics_studio_pid_dir",
                                        "/var/run/das")
data_analytics_studio_webapp_pid_file = format("{data_analytics_studio_pid_dir}/das-webapp.pid")
data_analytics_studio_event_processor_pid_file = format("{data_analytics_studio_pid_dir}/das-event-processor.pid")

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
