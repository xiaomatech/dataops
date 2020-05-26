#!/usr/bin/python
from resource_management.libraries.script.script import Script

config = Script.get_config()
kylin_user = config['configurations']['kylin-env']['kylin_user']
kylin_pid_dir = config['configurations']['kylin-env']['kylin_pid_dir']
kylin_pid_file = kylin_pid_dir + '/kylin-' + kylin_user + '.pid'