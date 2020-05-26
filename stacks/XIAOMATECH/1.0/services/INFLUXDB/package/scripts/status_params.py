from resource_management import *
from resource_management.libraries.script import Script

config = Script.get_config()

influxdb_pid_file = "/var/run/influxdb/influxd.pid"
