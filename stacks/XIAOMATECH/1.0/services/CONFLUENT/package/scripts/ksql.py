from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


class KSQL(Script):
    pid_file = '/var/run/ksql-server.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/ksql/ksql-server.properties',
            owner='cp-ksql',
            group='confluent',
            mode=0644,
            content=InlineTemplate(params.ksql_server_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        Execute("systemctl start confluent-ksql")
        Execute(
            "echo `ps aux|grep '/etc/ksql/ksql-server.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop confluent-ksql")

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(self.pid_file):
            Execute(
                "echo `ps aux|grep '/etc/ksql/ksql-server.properties' | grep -v grep | awk '{print $2}'` > "
                + self.pid_file)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    KSQL().execute()
