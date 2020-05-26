from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.libraries.resources.xml_config import XmlConfig
from hdfs import hdfs, install_hadoop
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import File
from resource_management.core.source import StaticFile, Template, InlineTemplate


class HDFSKMS(Script):

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
            "kms-site.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['kms-site'],
            configuration_attributes=params.config['configurationAttributes']
            ['kms-site'],
            owner=params.hdfs_user,
            group=params.user_group)
        XmlConfig(
            "kms-acls.xml",
            conf_dir=params.hadoop_conf_dir,
            configurations=params.config['configurations']['kms-acls'],
            configuration_attributes=params.config['configurationAttributes']
            ['kms-acls'],
            owner=params.hdfs_user,
            group=params.user_group)

        File(params.hadoop_conf_dir + "/kms-env.sh",
             mode=0644,
             owner=params.hdfs_user,
             group=params.user_group,
             content=InlineTemplate(params.config['configurations']['kms-log4j']['env_content']))

        File(params.hadoop_conf_dir + "/kms-log4j.properties",
             mode=0644,
             owner=params.hdfs_user,
             group=params.user_group,
             content=InlineTemplate(params.config['configurations']['kms-log4j']['content']))

    def start(self, env):
        import params
        env.set_params(params)
        install_hadoop()
        Execute(params.hadoop_bin_dir + 'hadoop --daemon start kms', user=params.hdfs_user)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.hadoop_bin_dir + 'hadoop --daemon stop kms', user=params.hdfs_user)

    def status(self, env):
        import status_params
        check_process_status(status_params.kms_pid_file)


if __name__ == "__main__":
    HDFSKMS().execute()
