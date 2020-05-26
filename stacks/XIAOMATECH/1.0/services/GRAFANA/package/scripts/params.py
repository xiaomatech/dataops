#!/usr/bin/env python

from resource_management.libraries.script import Script

config = Script.get_config()

grafana_user = config['configurations']['grafana-env']['grafana_user']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['grafana-env']['content']
grafana_plugins = config['configurations']['grafana-env']['grafana_plugins'].strip()

user_group = config['configurations']['cluster-env']['user_group']
