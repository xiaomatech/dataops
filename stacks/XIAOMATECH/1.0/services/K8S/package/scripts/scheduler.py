from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Scheduler(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/kube_scheduler_install.sh',
            content=InlineTemplate(params.kube_scheduler_install_content),
            mode=0755)
        Execute(
            'chmod a+x /tmp/kube_scheduler_install.sh; /tmp/kube_scheduler_install.sh'
        )
        Execute('systemctl enable kube-scheduler')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop kube-scheduler')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start kube-scheduler')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status kube-scheduler')


if __name__ == "__main__":
    Scheduler().execute()
