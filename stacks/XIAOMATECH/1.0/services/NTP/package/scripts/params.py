from resource_management.libraries.script import Script

config = Script.get_config()

conf_content = config['configurations']['ntpd-env']['conf_content']
