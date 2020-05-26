#!/usr/bin/env python
from resource_management import *

config = Script.get_config()

opentsdb_pid_dir = config['configurations']['opentsdb-env']['opentsdb_pid_dir']
opentsdb_pid_file = format("{opentsdb_pid_dir}/opentsdb.pid")