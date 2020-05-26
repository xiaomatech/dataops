#!/usr/bin/env python


from resource_management.core.resources.system import Execute, File
from resource_management.core import shell
from resource_management.libraries.functions.format import format
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
from resource_management.libraries.functions.show_logs import show_logs
from ambari_commons.constants import UPGRADE_TYPE_NON_ROLLING, UPGRADE_TYPE_ROLLING
from resource_management.libraries.functions.constants import Direction
import os


def kms_service(action='start', upgrade_type=None):
    import params

    env_dict = {'JAVA_HOME': params.java_home}
    if params.db_flavor.lower() == 'sqla':
        env_dict = {'JAVA_HOME': params.java_home, 'LD_LIBRARY_PATH': params.ld_library_path}

    if action == 'start':
        no_op_test = format('ps -ef | grep proc_rangerkms | grep -v grep')
        cmd = format('{kms_home}/ranger-kms start')
        try:
            Execute(cmd, not_if=no_op_test, environment=env_dict, user=format('{kms_user}'))
        except:
            show_logs(params.kms_log_dir, params.kms_user)
            raise
    elif action == 'stop':
        if upgrade_type == UPGRADE_TYPE_NON_ROLLING and params.upgrade_direction == Direction.UPGRADE:
            if os.path.isfile(format('{kms_home}/ranger-kms')):
                File(format('{kms_home}/ranger-kms'),
                     owner=params.kms_user,
                     group=params.kms_group
                     )
        cmd = format('{kms_home}/ranger-kms stop')
        try:
            Execute(cmd, environment=env_dict, user=format('{kms_user}'))
        except:
            show_logs(params.kms_log_dir, params.kms_user)
            raise
