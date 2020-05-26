from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Docker(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/docker_install.sh',
            content=InlineTemplate(params.install_content),
            mode=0755)
        Execute('chmod a+x /tmp/docker_install.sh; /tmp/docker_install.sh')
        Execute('systemctl enable docker lxcfs')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop docker')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start docker')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status docker')


if __name__ == "__main__":
    Docker().execute()
