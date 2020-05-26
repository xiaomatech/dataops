from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.resources.system import Directory
import os
from resource_management.libraries.functions.default import default


class Etcd(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Directory([params.data_dir, params.conf_dir],
                  owner=params.etcd_user,
                  group=params.user_group,
                  mode=0775,
                  create_parents=True)

        download_url_base = default(
            "/configurations/cluster-env/download_url_base",
            'http://assets.example.com/')
        file_path = '/usr/bin/etcd'
        if not os.path.exists(file_path):
            Execute(
                'wget ' + download_url_base + '/etcd -O ' + file_path,
                user=params.etcd_user)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/etcd.conf',
            content=params.conf_content,
            mode=0755,
            owner=params.etcd_user,
            group=params.user_group)

        File(
            '/usr/lib/systemd/system/etcd.service',
            content=params.systemd_content,
            mode=0755,
            owner=params.etcd_user,
            group=params.user_group)

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
