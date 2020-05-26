from resource_management.core.resources.system import Directory, Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.source import Template, InlineTemplate
from scheduler import install_airflow


class Kerberos(Script):
    def install(self, env):
        print "Installing Airflow"
        install_airflow()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.airflow_config_path,
            content=InlineTemplate(params.airflow_conf),
            mode=0755)
        File(params.airflow_env_path, content=Template("airflow"), mode=0755)

    def start(self, env):
        install_airflow()
        self.configure(env)
        import params
        Execute("source " + params.airflow_env_path +
                ";systemctl start airflow-kerberos")

    def stop(self, env):
        Execute("systemctl stop airflow-kerberos")

    def status(self, env):
        import params
        env.set_params(params)
        Execute("systemctl status airflow-kerberos")


if __name__ == "__main__":
    Kerberos().execute()
