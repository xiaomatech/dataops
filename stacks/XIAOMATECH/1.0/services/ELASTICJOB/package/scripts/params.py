from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/elasticjob'
download_url = config['configurations']['elasticjob-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

elasticjob_user = config['configurations']['elasticjob-env']['elasticjob_user']
user_group = config['configurations']['cluster-env']["user_group"]

hostname = config['agentLevelParams']['hostname']

run_dir = config['configurations']['elasticjob-env']['run_dir']
log_dir = config['configurations']['elasticjob-env']['log_dir']
conf_dir = config['configurations']['elasticjob-env']['conf_dir']
env_template = config['configurations']['elasticjob-env']['elasticjob_env']

conf_template = config['configurations']['elasticjob-env']['content']
