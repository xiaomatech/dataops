#!/usr/bin/env python

from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
import hashlib

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()
stack_name = default("/hostLevelParams/stack_name", None)

# Version being upgraded/downgraded to
version = default("/commandParams/version", None)

hostname = config['agentLevelParams']['hostname']

# default clickhouse parameters
conf_dir = "/etc/clickhouse-server"

clickhouse_user_nofile_soft = config['configurations']['clickhouse-env'][
    'clickhouse_user_nofile_soft']
clickhouse_user_nofile_hard = config['configurations']['clickhouse-env'][
    'clickhouse_user_nofile_hard']
clickhouse_user = config['configurations']['clickhouse-env']['clickhouse_user']
clickhouse_group = config['configurations']['clickhouse-env']['clickhouse_group']

clickhouse_data_path = config['configurations']['clickhouse-env']['clickhouse_data_path']
clickhouse_pid_dir = config['configurations']['clickhouse-env']['clickhouse_pid_dir']
clickhouse_pid_file = clickhouse_pid_dir + '/clickhouse-server.pid'

# clickhouse log configuratioins
clickhouse_log_dir = config['configurations']['clickhouse-env']['clickhouse_log_dir']
clickhouse_log_level = default('/configurations/clickhouse-env/clickhouse_log_level', 'trace')

clickhouse_log_file = default('/configurations/clickhouse-env/clickhouse_log_file', clickhouse_log_dir + '/server.log')
clickhouse_errorlog_file = default('/configurations/clickhouse-env/clickhouse_errorlog_file',
                                   clickhouse_log_dir + '/error.log')

clickhouse_log_size = default('/configurations/clickhouse-env/clickhouse_log_size', '1000M')
clickhouse_log_count = default('/configurations/clickhouse-env/clickhouse_log_count', 10)

# Java Home and clickhouse_hosts
java64_home = config['ambariLevelParams']['java_home']


def sha256_checksum(password):
    sha256 = hashlib.sha256(password)
    return sha256.hexdigest()


user_admin_password = config['configurations']['clickhouse-env']['user_admin_password']
user_admin_password_sha256 = sha256_checksum(user_admin_password)

user_ck_password = config['configurations']['clickhouse-env']['user_ck_password']
user_ck_password_sha256 = sha256_checksum(user_ck_password)

# zookeeper cluster configuratioins
zookeeper_hosts = default('/clusterHostInfo/zookeeper_server_hosts', [])
from random import shuffle
shuffle(zookeeper_hosts)
zookeeper_hosts.sort()
zookeeper_servers = ''
for index, zk_host in enumerate(zookeeper_hosts):
    zookeeper_servers += '<node index="' + str(index + 1) + '"><host>' + zk_host + '</host><port>2181</port></node>'

clickhouse_hosts = default('/clusterHostInfo/clickhouse_hosts', [])
clickhouse_hosts.sort()
remote_cluster = ''
for host in clickhouse_hosts:
    remote_cluster += '<shard><internal_replication>false</internal_replication><replica><host>' + host + '</host><user>admin</user><password>' + user_admin_password + '</password><port>9000</port></replica></shard>'

cluster_name = config["clusterName"]

config_content = config['configurations']['clickhouse-env']['config_content']
users_content = config['configurations']['clickhouse-env']['users_content']
