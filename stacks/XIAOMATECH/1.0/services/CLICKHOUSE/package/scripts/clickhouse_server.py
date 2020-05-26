from resource_management import Script
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions.check_process_status import check_process_status

from clickhouse import clickhouse


class ClickhouseServer(Script):
    def install(self, env):
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        clickhouse()

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('service clickhouse-server start', user='root')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('service clickhouse-server stop', user='root')
        File(params.clickhouse_pid_file, action="delete")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.clickhouse_pid_file)


if __name__ == "__main__":
    ClickhouseServer().execute()
