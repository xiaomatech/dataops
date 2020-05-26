#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

config = Script.get_config()

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

download_url_jira = config['configurations']['jira-env']['download_url_jira']
download_url_confluence = config['configurations']['jira-env'][
    'download_url_confluence']
conf_dir = '/etc/jira'

user_group = config['configurations']['cluster-env']['user_group']

jira_systemd = '''
[Unit] 
Description=Jira Issue & Project Tracking Software
After=network.target

[Service] 
Type=forking
User=jira
PIDFile=/opt/atlassian/jira/work/jira.pid
ExecStart=/opt/atlassian/jira/bin/start-jira.sh
ExecStop=/opt/atlassian/jira/bin/stop-jira.sh
TimeoutSec=200
LimitNOFILE=1048576
LimitNPROC=204800
[Install] 
WantedBy=multi-user.target
'''

confluence_systemd = '''
[Unit]
Description=Confluence
After=network.target

[Service]
Type=forking
User=confluence
PIDFile=/opt/atlassian/confluence/work/confluence.pid
ExecStart=/opt/atlassian/confluence/bin/start-confluence.sh
ExecStop=/opt/atlassian/confluence/bin/stop-confluence.sh
TimeoutSec=200
LimitNOFILE=1048576
LimitNPROC=204800

[Install]
WantedBy=multi-user.target
'''
