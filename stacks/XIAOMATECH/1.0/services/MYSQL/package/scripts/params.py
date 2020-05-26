from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
import os
import multiprocessing

config = Script.get_config()

stack_root = Script.get_stack_root()

tmp_dir = Script.get_tmp_dir()

conf_dir = '/etc/mysql-tools'
log_dir = '/var/log/mysql-tools'

hostname = config['agentLevelParams']['hostname']

conf_file = '/etc/my.cnf'

mysql_host = config['clusterHostInfo']['mysql_server_hosts']
privileges = config['configurations']['mysql-env']['privileges']
conf_content = config['configurations']['mysql-env']['conf_content']

cpu_count = multiprocessing.cpu_count()
mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
mem_gib = int(mem_bytes / (1024 ** 3))

innodb_buffer_pool_size = int(mem_gib * 0.8 / 4)
innodb_log_file_size = int(mem_gib * 0.4 / 4)
innodb_buffer_pool_instances = cpu_limit = int(cpu_count / 4)

mem_limit = innodb_buffer_pool_size * 1024 ** 3
cpus = range(cpu_count)

cpu_g1 = ','.join(cpus[0:cpu_limit])
cpu_g2 = ','.join(cpus[cpu_limit:cpu_limit * 2])
cpu_g3 = ','.join(cpus[cpu_limit * 2:cpu_limit * 3])
cpu_g4 = ','.join(cpus[cpu_limit * 3:])

import binascii

unique_id = int(binascii.crc32(b'' + hostname))

mysql_server_hosts = default('/clusterHostInfo/mysql_server_hosts', [])

group_name = 'idc-business'
group_seeds = hostname + ':3306' + ',' + hostname + ':3307' + ',' + hostname + ':3308' + ',' + hostname + ':3309'

clickhouse_hosts = default('/clusterHostInfo/clickhouse_server_hosts', [])
clickhouse_host = ''
clicktail_slow_content = config['configurations']['mysql-env']['clicktail_slow_content']
clicktail_audit_content = config['configurations']['mysql-env']['clicktail_audit_content']
if len(clickhouse_hosts) > 0:
    import random

    clickhouse_host = clickhouse_hosts[random.randint(0, len(clickhouse_hosts) - 1)]
