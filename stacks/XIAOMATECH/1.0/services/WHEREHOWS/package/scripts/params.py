#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions import default

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

wherehows_user = config['configurations']['wherehows-env']['wherehows_user']
user_group = config['configurations']['cluster-env']['user_group']
log_dir = config['configurations']['wherehows-env']['wherehows_log_dir']
mysql_user = config['configurations']['wherehows-env']['mysql_user']
mysql_password = config['configurations']['wherehows-env']['mysql_password']

frontend_conf = config['configurations']['wherehows-env']['frontend_conf']
backend_conf = config['configurations']['wherehows-env']['backend_conf']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

install_dir = stack_root + '/wherehows-frontend'
download_url = config['configurations']['wherehows-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

install_dir_backend = stack_root + '/wherehows-backend'
download_url_backend = config['configurations']['wherehows-env'][
    'download_url_backend']
filename_backend = download_url_backend.split('/')[-1]
version_dir_backend = filename_backend.replace('.tar.gz', '').replace(
    '.tgz', '')

conf_dir = '/etc/wherehows'

apache_hdfs_broker_conf = config['configurations']['wherehows-env'][
    'apache_hdfs_broker_conf']
wherehows_env_content = config['configurations']['wherehows-env'][
    'wherehows_env_content']

wherehowsfe_hosts = default("/clusterHostInfo/wherehows_frontend_hosts", [])
wherehowsbe_hosts = default("/clusterHostInfo/wherehows_backend_hosts", [])

frontend_env = 'PLAY_BINARY_OPTS="-Dconfig.file=/etc/wherehows/frontend/application.conf -Dhttp.address={{hostname}} -Dhttp.port=9001"'
frontend_systemd = '''
[Unit]
Description=Wherehows Frontend
After=network.target

[Service]
EnvironmentFile=-/etc/sysconfig/wherehows_frontend
PIDFile=/var/run/wherehows/frontend.pid
WorkingDirectory={{install_dir}}
ExecStart={{install_dir}}/bin/playBinary
Restart=on-failure
User={{wherehows_user}}
Group={{user_group}}
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
'''

backend_env = 'PLAY_BINARY_OPTS="-Dconfig.file=/etc/wherehows/backend/application.conf  -Dhttp.address={{hostname}} -Dhttp.port=19001"'

backend_systemd = '''
[Unit]
Description=Wherehows Backend
After=network.target

[Service]
EnvironmentFile=-/etc/sysconfig/wherehows_backend
PIDFile=/var/run/wherehows/backend.pid
WorkingDirectory={{install_dir_backend}}
ExecStart={{install_dir_backend}}/bin/playBinary
Restart=on-failure
User={{wherehows_user}}
Group={{user_group}}

SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
'''
