from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.script.script import Script

config = Script.get_config()
stack_root = Script.get_stack_root()

dpprofiler_pid_dir = config['configurations']['dpprofiler-env']['dpprofiler.pid.dir']
dpprofiler_pid_file = format('{dpprofiler_pid_dir}/profiler-agent.pid')

# Security related/required params
hostname = config['hostname']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
tmp_dir = Script.get_tmp_dir()
dpprofiler_user = config['configurations']['dpprofiler-env']['dpprofiler.user']

stack_name = default("/hostLevelParams/stack_name", None)
