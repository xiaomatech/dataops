from resource_management import *
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        Execute('service influxdb status')


if __name__ == "__main__":
    ServiceCheck().execute()
