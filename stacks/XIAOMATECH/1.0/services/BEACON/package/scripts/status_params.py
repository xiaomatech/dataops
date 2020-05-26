from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

hostname = config['agentLevelParams']['hostname']
stack_name = default("/clusterLevelParams/stack_name", None)

beacon_pid_dir = config['configurations']['beacon-env']['beacon_pid_dir']
server_pid_file = format('{beacon_pid_dir}/beacon.pid')

beacon_conf_dir = "/etc/beacon"
# Security related/required params
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()
beacon_user = config['configurations']['beacon-env']['beacon_user']

hadoop_home_dir = stack_root + '/hadoop/'
hadoop_bin_dir = stack_root + '/hadoop/bin/'
