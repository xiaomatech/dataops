from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.resources.system import Directory
import os


class Etcd(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Directory([params.etcd_data_dir, params.etcd_conf_dir],
                  owner='etcd',
                  mode=0775,
                  create_parents=True)

        file_path = '/usr/bin/etcd'
        if not os.path.exists(file_path):
            Execute(
                'wget ' + params.download_url_base + '/etcd -O ' + file_path,
                user='etcd')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.etcd_conf_dir + '/etcd.conf',
            content=params.etcd_content,
            mode=0755,
            owner='etcd')

        File(
            '/usr/lib/systemd/system/etcd.service',
            content=params.etcd_systemd_content,
            mode=0755,
            owner='etcd')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop etcd')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start etcd')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status etcd')


if __name__ == "__main__":
    Etcd().execute()
