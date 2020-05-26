from resource_management.libraries.script.script import Script

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()

install_dir = stack_root + '/sonar'
download_url = config['configurations']['sonar-env']['download_url']
filename = download_url.split('/')[-1]
version_dir = filename.replace('.zip', '').replace('.tgz', '').replace(
    '.tar.gz', '')

conf_dir = '/etc/sonar'
conf_content = config['configurations']['sonar-env']['conf_content']
