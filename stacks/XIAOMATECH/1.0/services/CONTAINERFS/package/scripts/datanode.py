from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory
from params import install_from_file


class ContainerFS(Script):
    binary_file_name = 'datanode'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_from_file(self.binary_file_name)
        Directory([params.conf_dir], mode=0775, create_parents=True)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/datanode.json',
            content=InlineTemplate(params.datanode_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('/usr/sbin/' + self.binary_file_name + ' -c ' +
                params.conf_dir + '/datanode.json')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('/usr/sbin/' + self.binary_file_name + ' -c ' +
                params.conf_dir + '/datanode.json')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('/usr/sbin/' + self.binary_file_name + ' -c ' +
                params.conf_dir + '/datanode.json')


if __name__ == "__main__":
    ContainerFS().execute()
