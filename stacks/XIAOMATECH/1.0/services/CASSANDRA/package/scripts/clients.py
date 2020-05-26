#!/usr/bin/env python

from resource_management import *
from resource_management.libraries.script.script import Script
from cassandra import *


class clients(Script):
    def configure(self, env):
        import params
        env.set_params(params)
        cassandra()

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)


if __name__ == "__main__":
    clients().execute()
