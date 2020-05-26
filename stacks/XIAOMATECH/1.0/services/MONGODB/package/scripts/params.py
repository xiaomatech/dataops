from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
import os

# server configurations
config = Script.get_config()

bind_ip = default('configurations/mongodb/bind_ip', '0.0.0.0')
tcp_port = default('configurations/mongodb/tcp_port', '27017')
mongos_tcp_port = default('configurations/mongodb/mongos_tcp_port', '30000')
db_path = default('configurations/mongodb/db_path', '/var/lib/mongo')
db_name = default('configurations/mongodb/db_name', '')
db_user = default('configurations/mongodb/db_user', 'anadmin')
db_pass = default('configurations/mongodb/db_pass', '')
mongo_host = default('/clusterHostInfo/mongodb_master_hosts', ['unknown'])[0]
db_ports = ["27017", "27018", "27019"]
arbiter_port = '27016'
log_path = '/var/log/mongodb'
shard_prefix = 'shard'
pid_db_path = '/var/run/mongodb'
node_group = default('configurations/mongodb/node_group', '')
mongod_db_content = default('configurations/mongodb/mongod_db_content', '')
mongod_config_content = default('configurations/mongodb/mongod_config_content',
                                '')
auth = default('configurations/mongodb/auth', 'false')
# auth=False
auth_pattern = ' --auth ' if auth else ''
# auth_pattern = ''
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
mongodb_admin = default('configurations/mongodb/mongodb_admin', 'admin')
mongodb_password = default('configurations/mongodb/mongodb_password', '123456')

clickhouse_hosts = default('/clusterHostInfo/clickhouse_server_hosts', [])
clickhouse_host = ''
clicktail_content = config['configurations']['mongodb']['clicktail_content']
if len(clickhouse_hosts) > 0:
    import random

    clickhouse_host = clickhouse_hosts[random.randint(0, len(clickhouse_hosts) - 1)]
