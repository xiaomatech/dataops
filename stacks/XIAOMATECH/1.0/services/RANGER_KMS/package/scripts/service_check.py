#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.core.logger import Logger
from resource_management.core import shell
from resource_management.core.exceptions import ComponentIsNotRunning


class KmsServiceCheck(Script):
    def service_check(self, env):
        import params

        env.set_params(params)
        cmd = 'ps -ef | grep proc_rangerkms | grep -v grep'
        code, output = shell.call(cmd, timeout=20)
        if code == 0:
            Logger.info('KMS process up and running')
        else:
            Logger.debug('KMS process not running')
            raise ComponentIsNotRunning()


if __name__ == "__main__":
    KmsServiceCheck().execute()
