from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

config = Script.get_config()
stack_root = Script.get_stack_root()
tmp_dir = Script.get_tmp_dir()

conf_dir = '/etc/dbmanager'

install_dir_admin = stack_root + '/dbmanager'
download_url_admin = config['configurations']['dbmanager-env'][
    'download_url_admin']
filename_admin = download_url_admin.split('/')[-1]
version_dir_admin = filename_admin.replace('.tar.gz',
                                           '').replace('.tgz', '').replace(
                                               '.tar.bz2', '')

inception_content = config['configurations']['dbmanager-env'][
    'inception_content']
download_url_soar = config['configurations']['dbmanager-env'][
    'download_url_soar']
soar_content = config['configurations']['dbmanager-env']['soar_content']
nginx_content = config['configurations']['dbmanager-env']['nginx_content']
init_content = config['configurations']['dbmanager-env']['init_content']
backup_content = config['configurations']['dbmanager-env']['backup_content']

settings_content = config['configurations']['dbmanager-env'][
    'settings_content']
router_content = config['configurations']['dbmanager-env']['router_content']
proxy_content = config['configurations']['dbmanager-env']['proxy_content']
proxy_admin_content = config['configurations']['dbmanager-env'][
    'proxy_admin_content']

db_url = config['configurations']['dbmanager-env']['db_url']
db_user = config['configurations']['dbmanager-env']['db_user']
db_password = config['configurations']['dbmanager-env']['db_password']
log_dir = config['configurations']['dbmanager-env']['log_dir']
pid_dir = config['configurations']['dbmanager-env']['pid_dir']

hostname = config['agentLevelParams']['hostname']
proxysql_hosts = default('/clusterHostInfo/proxysql_hosts', [])
proxy_count = len(proxysql_hosts)
proxysql = ''
proxysql_list = []
for host in proxysql_hosts:
    proxysql_list.append('''
    {
        hostname="''' + host + '''"
        port=6032
        comment="''' + host + '''"
    }    
    ''')

proxysql = ','.join(proxysql_list)
