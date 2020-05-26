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
        Directory([params.data_dir],
                  owner='jenkins',
                  group='jenkins',
                  mode=0775,
                  create_parents=True)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/sysconfig/jenkins',
            content=InlineTemplate(params.conf_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('service jenkins stop')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('service jenkins start')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('service jenkins status')


if __name__ == "__main__":
    Jenkins().execute()
