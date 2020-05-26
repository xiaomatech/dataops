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
        Execute('yum install -y gitlab-runner')
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        Execute('gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.example.com/" \
  --registration-token "token" \
  --executor "docker" \
  --docker-image alpine:3 \
  --description "docker-runner" \
  --tag-list "docker" \
  --run-untagged \
  --locked="false"')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('gitlab-runner stop')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('gitlab-runner start')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('gitlab-runner status')


if __name__ == "__main__":
    GitLab().execute()
