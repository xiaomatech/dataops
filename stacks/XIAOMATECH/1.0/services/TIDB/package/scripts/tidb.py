from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


def install_tidb(file_name):
    import params
    Directory([
        params.conf_dir, params.log_dir, params.data_dir, params.raftdb_dir,
        params.wal_dir
    ],
              owner=params.tidb_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    params.install_from_file(file_name)


class Tidb(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_tidb('tidb-server')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/tidb.conf',
            content=InlineTemplate(params.tidb_content),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/tidb.service',
            content=InlineTemplate(params.tidb_systemd),
            mode=0755,
            owner=params.tidb_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop tidb')

    def start(self, env):
        import params
        env.set_params(params)
        install_tidb('tidb-server')
        self.configure(env)
        Execute('systemctl start tidb')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status tidb')


if __name__ == "__main__":
    Tidb().execute()
