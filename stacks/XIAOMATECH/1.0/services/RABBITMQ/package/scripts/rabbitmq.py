from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script


class RabbitMQ(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop rabbitmq-server')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start rabbitmq-server')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status rabbitmq-server')


if __name__ == "__main__":
    RabbitMQ().execute()
