#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default
import os

config = Script.get_config()

download_url = config['configurations']['pulsar-env']['download_url']

pulsar_user = config['configurations']['pulsar-env']['pulsar_user']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

pulsar_content = config['configurations']['pulsar-env'][
    'pulsar_content']


conf_dir = '/etc/pulsar'

user_group = config['configurations']['cluster-env']['user_group']

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

