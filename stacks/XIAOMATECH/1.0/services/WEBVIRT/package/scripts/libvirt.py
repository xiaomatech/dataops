from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.source import StaticFile
from resource_management.core.resources.system import File
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import Directory


class Libvirt(Script):
    def install(self, env):
        File(
            '/tmp/libvirt-bootstrap.sh',
            mode=0755,
            content=StaticFile('libvirt-bootstrap.sh'))
        Execute('/tmp/libvirt-bootstrap.sh')
        Execute('virsh net-destroy default')
        Execute('virsh net-undefine default')
        Execute('systemctl restart libvirtd')

        import params
        Directory([params.data_dir],
                  owner='root',
                  group='root',
                  mode=0775,
                  create_parents=True)

        Execute('virsh pool-define-as --name dir_pool dir --target ' +
                params.data_dir)
        Execute('virsh pool-autostart dir_pool')
        Execute('virsh pool-build dir_pool')
        Execute('virsh pool-start dir_pool')

        if params.enable_kvm:
            File('/tmp/lvm_pool.xml', mode=0755, content=params.lvm_pool)
            Execute('virsh pool-define /tmp/lvm_pool.xml')
            Execute('irsh pool-build storage_pool')
            Execute('virsh pool-autostart storage_pool')

        #https://www.ovirt.org/documentation/how-to/networking/bonding-vlan-bridge/
        if params.enable_net:
            File('/tmp/network.xml', mode=0755, content=params.lvm_pool)
            Execute('virsh iface-define /tmp/network.xml')
            Execute('virsh iface-start bond0')

        Execute('wget ' + params.base_os_image_url + ' -O ' + params.data_dir + '/base.qcow2')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop libvirtd')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl restart libvirtd')

    def status(self, env):
        check_process_status('/var/run/libvirtd.pid')


if __name__ == "__main__":
    Libvirt().execute()
