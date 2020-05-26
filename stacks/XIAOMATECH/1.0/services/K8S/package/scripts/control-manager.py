from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class ControlManager(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/kube_controller_manager_install.sh',
            content=InlineTemplate(
                params.kube_controller_manager_install_content),
            mode=0755)
        Execute(
            'chmod a+x /tmp/kube_controller_manager_install.sh; /tmp/kube_controller_manager_install.sh'
        )
        Execute('systemctl enable kube-controller-manager')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop kube-controller-manager')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start kube-controller-manager')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status kube-controller-manager')


if __name__ == "__main__":
    ControlManager().execute()
