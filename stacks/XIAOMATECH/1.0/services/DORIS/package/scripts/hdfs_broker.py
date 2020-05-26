from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from be import install_doris


class dorisHdfsBroker(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_doris()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("{install_dir}/apache_hdfs_broker/bin/doris-env.sh"),
            content=InlineTemplate(params.doris_env_content),
            mode=0755,
            owner=params.doris_user,
            group=params.doris_group)
        File(
            format(
                "{install_dir}/apache_hdfs_broker/conf/apache_hdfs_broker.conf"
            ),
            content=InlineTemplate(params.fe_conf),
            mode=0755,
            owner=params.doris_user,
            group=params.doris_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + "/apache_hdfs_broker/bin/stop_broker.sh")

    def start(self, env):
        import params
        env.set_params(params)
        install_doris()
        self.configure(env)
        Execute(params.install_dir + "/apache_hdfs_broker/bin/start_broker.sh --daemon")

    def status(self, env):
        import params
        check_process_status(params.pid_dir + '/apache_hdfs_broker.pid')


if __name__ == "__main__":
    dorisHdfsBroker().execute()
