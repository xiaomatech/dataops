from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import get_kinit_path
config = Script.get_config()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/dr-elephant'
download_url = config['configurations']['doctor-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.tar.gz', '').replace('.tgz', '')

doctor_user = config['configurations']['doctor-env']['doctor_user']
user_group = config['configurations']['cluster-env']["user_group"]

hostname = config['agentLevelParams']['hostname']
principal_name = default('configurations/doctor-env/principal_name',
                         "").replace("_HOST", hostname)
keytab_path = default('configurations/doctor-env/keytab_path', "")

run_dir = config['configurations']['doctor-env']['run_dir']
log_dir = config['configurations']['doctor-env']['log_dir']
conf_dir = config['configurations']['doctor-env']['conf_dir']
drelephant_env_template = config['configurations']['doctor-env'][
    'drelephant_env']
db_host = config['configurations']['doctor-env']['db_host']
db_name = config['configurations']['doctor-env']['db_name']
db_user = config['configurations']['doctor-env']['db_user']
db_password = config['configurations']['doctor-env']['db_password']
app_conf_template = config['configurations']['doctor-env']['app_conf']

pid_file = '/var/run/drelephant.pid'
# smokeuser
kinit_path_local = get_kinit_path(
    default('/configurations/kerberos-env/executable_search_paths', None))
smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env'][
    'smokeuser_principal_name']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
