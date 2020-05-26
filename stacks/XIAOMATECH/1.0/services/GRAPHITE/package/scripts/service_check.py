#!/usr/bin/env python

from __future__ import print_function

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        exit(0)


if __name__ == "__main__":
    ServiceCheck().execute()
