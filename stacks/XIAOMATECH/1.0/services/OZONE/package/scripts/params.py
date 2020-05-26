from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/ozone'
download_url = config['configurations']['ozone-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

hadoop_conf_dir = '/etc/hadoop'
hdfs_user = config['configurations']['ozone-env']['ozone_user']
user_group = config['configurations']['cluster-env']['user_group']
