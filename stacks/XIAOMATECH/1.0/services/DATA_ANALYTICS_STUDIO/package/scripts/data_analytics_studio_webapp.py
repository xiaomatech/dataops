#!/usr/bin/env python

from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.script.script import Script

from data_analytics_studio import data_analytics_studio
from data_analytics_studio_service import data_analytics_studio_service


class DataAnalyticsStudioWebapp(Script):
    def install(self, env):
        self.install_packages(env)
        import params
        env.set_params(params)
        data_analytics_studio_service(name="data_analytics_studio_webapp", action="install")

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)
        data_analytics_studio(name="data_analytics_studio_webapp")

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)

        data_analytics_studio_service("data_analytics_studio_webapp", action="start")

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        data_analytics_studio_service("data_analytics_studio_webapp", action="stop")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.data_analytics_studio_webapp_pid_file)

    def get_log_folder(self):
        import params
        return params.data_analytics_studio_log_dir

    def get_user(self):
        import params
        return params.data_analytics_studio_user

    def get_pid_files(self):
        import status_params
        return [status_params.data_analytics_studio_webapp_pid_file]


if __name__ == "__main__":
    DataAnalyticsStudioWebapp().execute()
