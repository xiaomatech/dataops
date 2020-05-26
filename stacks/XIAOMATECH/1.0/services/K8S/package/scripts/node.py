from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Node(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/node_install.sh',
            content=InlineTemplate(params.node_install_content),
            mode=0755)
        Execute('chmod a+x /tmp/node_install.sh; /tmp/node_install.sh')
        Execute('systemctl enable kubelet kube-proxy')

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop kubelet kube-proxy')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start kubelet kube-proxy')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status kubelet')


if __name__ == "__main__":
    Node().execute()
