#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/graphouse'
download_url = config['configurations']['graphite-env']['download_url']
filename = download_url.split('/')[-1]

download_url_graphite_api = config['configurations']['graphite-env']['download_url_graphite_api']
install_dir_graphite_api = stack_root + '/graphite-api'
filename_graphite_api = download_url_graphite_api.split('/')[-1]

download_url_graphite_web = config['configurations']['graphite-env']['download_url_graphite_web']
install_dir_graphite_web = stack_root + '/graphite'
filename_graphite_web = install_dir_graphite_web.split('/')[-1]

version_dir = filename.replace('.tar.gz', '').replace('.tar', '').replace('.tgz', '')

graphite_user = config['configurations']['graphite-env']['graphite_user']
user_group = config['configurations']['cluster-env']['user_group']
log_dir = config['configurations']['graphite-env']['log_dir']
pid_dir = config['configurations']['graphite-env']['pid_dir']
graphite_pid_file = format("{graphite_pid_dir}/graphite.pid")

graphouse_content = config['configurations']['graphite-env']['graphouse_content']
graphouse_vmoptions_content = config['configurations']['graphite-env']['graphouse_vmoptions_content']
log4j_content = config['configurations']['graphite-env']['log4j_content']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

graphouse_conf_dir = '/etc/graphouse'
graphite_conf_dir = '/etc/graphite'

graphite_api_hosts = default("/clusterHostInfo/graphite_api_hosts", [])
graphouse_hosts = default("/clusterHostInfo/graphouse_hosts", [])
graphouse_host = ','.join(graphouse_hosts)
graphite_web_hosts = default("/clusterHostInfo/graphite_web_hosts", [])

import multiprocessing

cpu_count = multiprocessing.cpu_count()

# /etc/sysconfig/memcached
memcached_content = '''
PORT="11211"
USER="memcached"
MAXCONN="65535"
CACHESIZE="2048"
OPTIONS=" -l ''' + hostname + ''' -t ''' + str(cpu_count)

graphite_api_systemd_content = '''
[Unit]
Description=Graphite-API service
[Service]
RuntimeDirectoryMode=755
ExecStart=/opt/graphite-api/bin/gunicorn graphite_api.app:app -w ''' + str(cpu_count) + ''' --chdir /opt/graphite-api/lib/python3.6/site-packages --bind 0.0.0.0:8001 --backlog 20480 --pid /var/run/graphite/api.pid --error-logfile /var/log/graphite/error_api.log --access-logfile /var/log/graphite/access_api.log
Restart=on-failure
User=graphite
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true
[Install]
WantedBy=multi-user.target
'''


graphite_web_systemd_content = '''
Description=Graphite-WEB service
[Service]
RuntimeDirectoryMode=755
ExecStart=/opt/graphite/bin/gunicorn graphite.wsgi -w ''' + str(cpu_count) + ''' --chdir /opt/graphite/webapp/ --pid /var/run/graphite/web.pid  --bind 0.0.0.0:8002 --backlog 20480 --error-logfile /var/log/graphite/error_web.log --access-logfile /var/log/graphite/access_web.log
Restart=on-failure
User=graphite
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true
[Install]
WantedBy=multi-user.target
'''