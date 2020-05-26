from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class GitLab(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('yum install -y gitlab-ee')
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/gitlab/gitlab.rb',
            content=InlineTemplate(params.gitlab_content))
        Execute('gitlab-ctl reconfigure')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('gitlab-ctl stop')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('gitlab-ctl start')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('gitlab-ctl status')


if __name__ == "__main__":
    GitLab().execute()
