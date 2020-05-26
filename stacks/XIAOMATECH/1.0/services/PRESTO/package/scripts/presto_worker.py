# -*- coding: utf-8 -*-

from resource_management.core.resources.system import Directory, Execute, File, Link
from presto_coordinator import install_presto, config_presto
from resource_management.libraries.script.script import Script

from resource_management.libraries.functions.check_process_status import check_process_status


class Worker(Script):
    def install(self, env):
        install_presto()
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        from params import daemon_control_script, presto_user
        Execute('{0} stop'.format(daemon_control_script), user=presto_user)

    def start(self, env):
        import params
        env.set_params(params)
        from params import daemon_control_script, presto_user
        install_presto()
        self.configure(env)
        Execute('{0} start'.format(daemon_control_script), user=presto_user)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status('/var/run/presto/presto.pid')

    def configure(self, env):
        import params
        env.set_params(params)
        config_presto()


if __name__ == '__main__':
    Worker().execute()
