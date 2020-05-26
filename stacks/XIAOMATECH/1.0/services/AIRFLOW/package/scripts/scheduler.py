from resource_management.core.resources.system import Directory, Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.source import Template, InlineTemplate


def install_airflow():
    import params
    Directory([
        params.conf_dir, '/var/run/airflow', params.airflow_base_log_folder,
        params.airflow_dags_folder
    ],
              owner=params.airflow_user,
              group=params.airflow_group,
              mode=0775,
              create_parents=True)
    Execute('yum install -y airflow')


class Scheduler(Script):
    def install(self, env):
        install_airflow()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.airflow_config_path,
            content=InlineTemplate(params.airflow_conf),
            mode=0755)

    def start(self, env):
        import params
        install_airflow()
        self.configure(env)
        Execute("source " + params.airflow_env_path +
                ";systemctl start airflow-scheduler")

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def stop(self, env):
        Execute("systemctl stop airflow-scheduler")

    def status(self, env):
        import params
        env.set_params(params)
        Execute("systemctl status airflow-scheduler")


if __name__ == "__main__":
    Scheduler().execute()
