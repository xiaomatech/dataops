from resource_management.libraries.script.script import Script

from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.default import default

config = Script.get_config()

redis_hosts = config['clusterHostInfo']['redis_hosts']
redis_hosts_str = ','.join(redis_hosts)
hostname = config['agentLevelParams']['hostname']

master_host = default("/configurations/redis-env/master_host", hostname)
redis_content = default("/configurations/redis-env/redis_content", "")
