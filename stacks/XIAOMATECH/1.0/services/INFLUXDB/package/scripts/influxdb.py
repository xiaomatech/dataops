from resource_management import *
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import Template
from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status


def influxdb():
    import params

    Directory([params.conf_dir, params.influxd_dir, params.data_dir],
              owner=params.influxdb_user,
              group=params.user_group,
              recursive=True)

    File(
        format("{conf_dir}/influxdb.conf"),
        content=Template("influxdb-cluster.conf.j2"),
        owner=params.influxdb_user,
        group=params.user_group)

    File(
        format("{influxd_dir}/influxdb"),
        content=Template("influxdb.conf.j2"),
        owner=params.influxdb_user,
        group=params.user_group)


class influxdb_service(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        influxdb()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('service influxdb stop')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('service influxdb start')

    def restart(self, env):
        import params
        env.set_params(params)
        Execute('service influxdb restart')

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.influxdb_pid_file)


if __name__ == "__main__":
    influxdb_service().execute()
