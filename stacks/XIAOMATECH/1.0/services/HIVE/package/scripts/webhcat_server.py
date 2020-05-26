from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.logger import Logger
from webhcat import webhcat
from webhcat_service import webhcat_service


class WebHCatServer(Script):
    def install(self, env):
        import params
        self.install_packages(env)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)  # FOR SECURITY
        webhcat_service(action='start', upgrade_type=upgrade_type)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        webhcat_service(action='stop')

    def configure(self, env):
        import params
        env.set_params(params)
        webhcat()

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.webhcat_pid_file)

    def pre_upgrade_restart(self, env, upgrade_type=None):
        Logger.info("Executing WebHCat Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def get_log_folder(self):
        import params
        return params.hcat_log_dir

    def get_user(self):
        import params
        return params.webhcat_user

    def get_pid_files(self):
        import status_params
        return [status_params.webhcat_pid_file]


if __name__ == "__main__":
    WebHCatServer().execute()
