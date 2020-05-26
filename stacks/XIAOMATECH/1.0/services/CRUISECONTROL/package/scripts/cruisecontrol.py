from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status


def install_cruisecontrol():
    pass


class CruiseControl(Script):
    pid_file = '/var/run/cruisecontrol.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_cruisecontrol()

    def configure(self, env):
        import params
        env.set_params(params)
        File(params.conf_dir + '/cruisecontrol.properties',
             owner=params.cruisecontrol_user,
             group=params.user_group,
             mode=0644,
             content=InlineTemplate(params.cruisecontrol_content))
        File(params.conf_dir + '/log4j.properties',
             owner=params.cruisecontrol_user,
             group=params.user_group,
             mode=0644,
             content=InlineTemplate(params.log4j_content))

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        Execute(
            params.install_dir + "/kafka-cruise-control-start.sh -daemon " + params.conf_dir + "/cruisecontrol.properties")
        Execute(
            "echo `ps aux|grep " + params.conf_dir + "/cruisecontrol.properties' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    CruiseControl().execute()
