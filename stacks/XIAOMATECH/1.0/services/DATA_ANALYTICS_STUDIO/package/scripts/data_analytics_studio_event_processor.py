#!/usr/bin/env python


from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.script.script import Script

from data_analytics_studio import data_analytics_studio
from data_analytics_studio_service import data_analytics_studio_service


class DataAnalyticsStudioEventProcessor(Script):
    def install(self, env):
        self.install_packages(env)

    def configure(self, env, upgrade_type=None, config_dir=None):
        import params
        env.set_params(params)
        data_analytics_studio(name="data_analytics_studio_event_processor")

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env)

        data_analytics_studio_service("data_analytics_studio_event_processor", action="start")

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        data_analytics_studio_service("data_analytics_studio_event_processor", action="stop")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.data_analytics_studio_event_processor_pid_file)

    def get_log_folder(self):
        import params
        return params.data_analytics_studio_log_dir

    def get_user(self):
        import params
        return params.data_analytics_studio_user

    def get_pid_files(self):
        import status_params
        return [status_params.data_analytics_studio_event_processor_pid_file]


if __name__ == "__main__":
    DataAnalyticsStudioEventProcessor().execute()
