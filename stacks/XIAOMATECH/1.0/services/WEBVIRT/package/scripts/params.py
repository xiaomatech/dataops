from resource_management.libraries.script import Script

config = Script.get_config()

conf_content = config['configurations']['webvirt-env']['conf_content']

base_os_image_url = config['configurations']['webvirt-env'][
    'base_os_image_url']

data_dir = config['configurations']['webvirt-env']['data_dir']

enable_kvm = config['configurations']['webvirt-env']['enable_kvm']
lvm_pool = config['configurations']['webvirt-env']['lvm_pool']

enable_net = config['configurations']['webvirt-env']['enable_net']
kvm_net = config['configurations']['webvirt-env']['kvm_net']
