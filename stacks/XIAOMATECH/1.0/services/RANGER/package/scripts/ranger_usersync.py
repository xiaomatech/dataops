#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute, File
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core import shell
from ranger_service import ranger_service
from ambari_commons.constants import UPGRADE_TYPE_NON_ROLLING, UPGRADE_TYPE_ROLLING
from resource_management.libraries.functions.constants import Direction
import upgrade
import setup_ranger_xml
import os

from resource_management.core.resources.system import Directory, Execute, File, Link


class RangerUsersync(Script):
    def install_ranger(self, ):
        import os, params
        Directory([params.ranger_ugsync_conf],
                  owner=params.unix_user,
                  group=params.user_group,
                  mode=0775,
                  create_parents=True)
        if not os.path.exists(
                Script.get_stack_root() + '/' + params.version_dir_usersync) or not os.path.exists(
                    params.install_dir_usersync):
            Execute('rm -rf %s' % params.install_dir_usersync)
            Execute(
                'wget ' + params.download_url_usersync + ' -O /tmp/' + params.filename_usersync,
                user=params.unix_user)
            Execute('tar -zxf /tmp/' + params.filename_usersync + ' -C  ' + Script.get_stack_root())
            Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_usersync + ' ' +
                    params.install_dir_usersync)
            Execute(' rm -rf ' + params.install_dir_usersync + '/conf')
            Execute('ln -s ' + params.ranger_ugsync_conf + ' ' +
                    params.install_dir_usersync + '/conf')
            Execute('ln -s ' + params.usersync_log_dir + ' ' +
                    params.install_dir_usersync + '/logs')
            Execute('chown -R %s:%s %s/%s' % (params.unix_user, params.user_group,
                                              Script.get_stack_root(),params.version_dir_usersync))
            Execute('chown -R %s:%s %s' % (params.unix_user, params.user_group,
                                           params.install_dir_usersync))
            Execute('/bin/rm -f /tmp/' + params.filename_usersync)

    def install(self, env):
        self.install_packages(env)
        self.install_ranger()

        import params
        env.set_params(params)

        setup_ranger_xml.validate_user_password('rangerusersync_user_password')

        if params.stack_supports_usersync_passwd:
            setup_ranger_xml.ranger_credential_helper(
                params.ugsync_cred_lib, params.ugsync_policymgr_alias,
                params.rangerusersync_user_password,
                params.ugsync_policymgr_keystore)

            File(
                params.ugsync_policymgr_keystore,
                owner=params.unix_user,
                group=params.unix_group,
                mode=0640)

    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)

        setup_ranger_xml.ranger('ranger_usersync', upgrade_type=upgrade_type)

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.install_ranger()
        self.configure(env, upgrade_type=upgrade_type)
        Execute("chown -R %s:%s %s" % (params.unix_user, params.unix_group,
                                       params.install_dir_usersync))
        Execute("chown -R %s:%s %s" % (params.unix_user, params.unix_group,
                                       params.ranger_ugsync_conf))

        if params.security_enabled:
            kinit_cmd = format(
                "{kinit_path_local} -kt {ugsync_keytab} {ugsync_principal};")
            Execute(kinit_cmd, user=params.unix_user)
        ranger_service('ranger_usersync')

    def stop(self, env):
        import params
        env.set_params(params)

        Execute(
            format('{params.usersync_stop}'),
            environment={'JAVA_HOME': params.java_home},
            user=params.unix_user)
        if params.stack_supports_pid:
            File(params.ranger_usersync_pid_file, action="delete")

    def status(self, env):
        import status_params
        env.set_params(status_params)

        if status_params.stack_supports_pid:
            check_process_status(status_params.ranger_usersync_pid_file)
            return

        cmd = 'ps -ef | grep proc_rangerusersync | grep -v grep'
        code, output = shell.call(cmd, timeout=20)

        if code != 0:
            Logger.debug('Ranger usersync process not running')
            raise ComponentIsNotRunning()
        pass

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)
        upgrade.prestart(env)

    def post_upgrade_restart(self, env):
        import params
        env.set_params(params)

        if upgrade_type and params.upgrade_direction == Direction.UPGRADE and not params.stack_supports_multiple_env_sh_files:
            files_name_list = [
                'ranger-usersync-env-piddir.sh',
                'ranger-usersync-env-logdir.sh'
            ]
            for file_name in files_name_list:
                File(
                    format("{ranger_ugsync_conf}/{file_name}"),
                    action="delete")

    def get_log_folder(self):
        import params
        return params.usersync_log_dir

    def get_user(self):
        import params
        return params.unix_user

    def get_pid_files(self):
        import status_params
        return [status_params.ranger_usersync_pid_file]


if __name__ == "__main__":
    RangerUsersync().execute()
