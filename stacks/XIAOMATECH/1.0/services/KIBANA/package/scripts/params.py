#!/usr/bin/env python
from urlparse import urlparse
from resource_management.libraries.functions import format
from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()

kibana_home = '/usr/share/kibana/'
kibana_bin = '/usr/share/kibana/bin/'

conf_dir = "/etc/kibana"
kibana_user = config['configurations']['kibana-env']['kibana_user']
kibana_group = config['configurations']['kibana-env']['kibana_group']
log_dir = config['configurations']['kibana-env']['kibana_log_dir']
pid_dir = config['configurations']['kibana-env']['kibana_pid_dir']
pid_file = format("{pid_dir}/kibanasearch.pid")

es_hosts = default('/clusterHostInfo/es_client_hosts', [])
es_url = 'http://' + es_hosts[0] + ':9200'

parsed = urlparse(es_url)
es_host = parsed.netloc.split(':')[0]
es_port = parsed.netloc.split(':')[1]
kibana_port = config['configurations']['kibana-env']['kibana_server_port']
kibana_default_application = config['configurations']['kibana-env'][
    'kibana_default_application']
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
kibana_yml_template = config['configurations']['kibana-site']['content']
