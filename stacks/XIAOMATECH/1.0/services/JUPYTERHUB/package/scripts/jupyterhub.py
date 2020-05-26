from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Jenkins(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Directory([params.data_dir], mode=0775, create_parents=True)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/jupyterhub/jupyterhub_config.py',
            content=InlineTemplate(params.conf_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop jupyterhub')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start jupyterhub')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status jupyterhub')


if __name__ == "__main__":
    Jenkins().execute()
