#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

config = Script.get_config()

rabbitmq_user = config['configurations']['rabbitmq-env']['rabbitmq_user']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

conf_content = config['configurations']['rabbitmq-env']['conf_content']

conf_dir = '/etc/rabbitmq'

rabbitmq_group = user_group = config['configurations']['cluster-env'][
    'user_group']
