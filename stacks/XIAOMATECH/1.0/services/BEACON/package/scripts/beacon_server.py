import beacon_server_upgrade

from resource_management.libraries.script import Script
from resource_management.libraries.functions import check_process_status

from beacon import beacon, install_beacon


class BeaconServer(Script):
    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        beacon('server', action='config', upgrade_type=upgrade_type)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        install_beacon()
        self.configure(env)
        beacon('server', action='start', upgrade_type=upgrade_type)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        beacon('server', action='stop', upgrade_type=upgrade_type)

        if upgrade_type is not None:
            beacon_server_upgrade.post_stop_backup()

    def get_component_name(self):
        return "beacon-server"

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_beacon()

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.server_pid_file)

    def pre_upgrade_restart(self, env, upgrade_type=None):
        pass

    def security_status(self, env):
        self.put_structured_out({"securityState": "UNSECURED"})

    def get_log_folder(self):
        import params
        return params.beacon_log_dir

    def get_user(self):
        import params
        return params.beacon_user


if __name__ == "__main__":
    BeaconServer().execute()
