from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()
exec_tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/cruise-control'
download_url = config['configurations']['cruisecontrol-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

install_dir_ui = stack_root + '/cruise-control-ui'
download_url_ui = config['configurations']['cruisecontrol-env']['download_url']
filename_ui = download_url_ui.split('/')[-1]
version_dir_ui = filename_ui.replace('.tar.gz', '').replace('.tgz', '')

conf_dir = '/etc/cruisecontrol'

hostname = config['agentLevelParams']['hostname']

cruisecontrol_user = config['configurations']['cruisecontrol-env']['cruisecontrol_user']

user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['ambariLevelParams']['java_home']

zookeeper_connect = default("/configurations/confluent-env/zookeeper.connect",
                            None)
zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()

kafka_broker_port = default('/configurations/confluent-env/port', '6667')
kafka_host_arr = []

kafka_hosts = default('/clusterHostInfo/kafka_hosts', [])
from random import shuffle

shuffle(kafka_hosts)
for i in range(len(kafka_hosts)):
    kafka_host_arr.append('PLAINTEXT://' + kafka_hosts[i] + ':' +
                          kafka_broker_port)
bootstrap_servers = ",".join(kafka_host_arr)

zk_quorum = ""
zookeeper_port = default('/configurations/zoo.cfg/clientPort', 2181)
if 'zookeeper_server_hosts' in config['clusterHostInfo']:
    for host in config['clusterHostInfo']['zookeeper_server_hosts']:
        if zk_quorum:
            zk_quorum += ','
        zk_quorum += host + ":" + str(zookeeper_port)

cruisecontrol_content = config['configurations']['cruisecontrol-env']['cruisecontrol_content']
log4j_content = config['configurations']['cruisecontrol-env']['log4j_content']