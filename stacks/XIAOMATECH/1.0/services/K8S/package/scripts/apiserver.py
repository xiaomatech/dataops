from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Apiserver(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/kube_apiserver_install.sh',
            content=InlineTemplate(params.kube_apiserver_install_content),
            mode=0755)
        Execute(
            'chmod a+x /tmp/kube_apiserver_install.sh; /tmp/kube_apiserver_install.sh'
        )
        Execute('systemctl enable kube-apiserver')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop kube-apiserver')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start kube-apiserver')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status kube-apiserver')


if __name__ == "__main__":
    Apiserver().execute()
