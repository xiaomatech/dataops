from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from yarn import yarn, install_yarn
from resource_management.core.resources.system import Execute
from resource_management.libraries.resources.xml_config import XmlConfig


class Federation(Script):
    def install(self, env):
        self.install_packages(env)
        install_yarn()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.hadoop_bin_dir + '/yarn --daemon stop router', user=params.yarn_user)

    def start(self, env):
        import params
        env.set_params(params)
        install_yarn()
        self.configure(env)
        Execute(params.hadoop_bin_dir + '/yarn --daemon start router', user=params.yarn_user)

    def configure(self, env):
        import params
        env.set_params(params)
        yarn(name="nodemanager")
        XmlConfig(
            "yarn-federation.xml",
            conf_dir=params.config_dir,
            configurations=params.config['configurations']['yarn-federation'],
            configuration_attributes=params.config['configurationAttributes']['yarn-federation'],
            owner=params.yarn_user,
            group=params.user_group,
            mode=0644)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.yarn_pid_dir + '/hadoop-' + params.yarn_user + '-router.pid')


if __name__ == "__main__":
    Federation().execute()
