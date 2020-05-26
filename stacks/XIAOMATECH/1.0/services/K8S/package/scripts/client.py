from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.exceptions import ClientComponentHasNoStatus


class HbaseClient(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        File(
            '/tmp/ca_init_install.sh',
            content=InlineTemplate(params.ca_init_content),
            mode=0755)
        Execute('chmod a+x /tmp/ca_init_install.sh; /tmp/ca_init_install.sh')

    def configure(self, env):
        import params
        env.set_params(params)

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)


if __name__ == "__main__":
    HbaseClient().execute()
