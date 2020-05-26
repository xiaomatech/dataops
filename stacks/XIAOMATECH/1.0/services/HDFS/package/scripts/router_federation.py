from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.resources.xml_config import XmlConfig
from hdfs import hdfs, install_hadoop
from utils import get_hdfs_binary
from resource_management.libraries.functions.check_process_status import check_process_status


class HDFSRouterFederation(Script):
    def get_hdfs_binary(self):
        return get_hdfs_binary("hadoop-hdfs-router")

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_hadoop()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        hdfs()
        XmlConfig(
            "hdfs-rbf.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['hdfs-rbf'],
            configuration_attributes=params.config['configurationAttributes']['hdfs-rbf'],
            owner=params.hdfs_user,
            group=params.user_group)

    def start(self, env):
        import params
        env.set_params(params)
        install_hadoop()
        Execute(self.get_hdfs_binary() + ' --daemon start dfsrouter', user=params.hdfs_user)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(self.get_hdfs_binary() + ' --daemon stop dfsrouter', user=params.hdfs_user)

    def status(self, env):
        import status_params
        check_process_status(status_params.dfsrouter_pid_file)


if __name__ == "__main__":
    HDFSRouterFederation().execute()
