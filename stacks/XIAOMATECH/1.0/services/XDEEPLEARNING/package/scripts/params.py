from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default

config = Script.get_config()
stack_root = Script.get_stack_root()

download_url = config['configurations']['xdeeplearning-env']['download_url']
filename = download_url.split('/')[-1]
xdl_submit_content = config['configurations']['xdeeplearning-env']['xdl_submit_content']