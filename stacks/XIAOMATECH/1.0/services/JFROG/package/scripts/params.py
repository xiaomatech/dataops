#!/usr/bin/env python

from resource_management.libraries.script import Script

config = Script.get_config()

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['jfrog-env']['conf_content']