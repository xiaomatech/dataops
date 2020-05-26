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
from resource_management.core.exceptions import Fail
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions import upgrade_summary
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Execute, File
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core import shell
from ranger_service import ranger_service
from resource_management.libraries.functions import solr_cloud_util
from ambari_commons.constants import UPGRADE_TYPE_NON_ROLLING, UPGRADE_TYPE_ROLLING
import upgrade
import os, errno

import setup_ranger_xml

from resource_management.core.resources.system import Directory, Execute, File, Link


class RangerAdmin(Script):
    def install_ranger(self):
        import os, params
        Directory([params.ranger_conf, params.admin_log_dir],
                  owner=params.unix_user,
                  group=params.user_group,
                  mode=0775,
                  create_parents=True)
        if not os.path.exists(Script.get_stack_root() + '/' +
                              params.version_dir_admin) or not os.path.exists(
                                  params.install_dir_admin):
            Execute('rm -rf %s' % params.install_dir_admin)
            Execute(
                'wget ' + params.download_url_admin + ' -O /tmp/' + params.filename_admin,
                user=params.unix_user)
            Execute('tar -zxf /tmp/' + params.filename_admin + ' -C  ' + Script.get_stack_root())
            Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_admin + ' ' +
                    params.install_dir_admin)
            Execute(' rm -rf ' + params.install_dir_admin + '/conf')
            Execute(' rm -rf ' + params.ranger_conf + '/conf/*')
            Execute(' rm -rf ' + params.install_dir_admin + '/ews/webapp/WEB-INF/classes/conf')
            Execute('ln -s ' + params.ranger_conf + ' ' +
                    params.install_dir_admin + '/conf')
            Execute('ln -s ' + params.ranger_conf + ' ' +
                    params.install_dir_admin +
                    '/ews/webapp/WEB-INF/classes/conf')
            Execute('ln -s ' + params.admin_log_dir + ' ' +
                    params.install_dir_admin + '/ews/logs')
            Execute('chown -R %s:%s %s/%s' % (params.unix_user, params.user_group, Script.get_stack_root(),
                                              params.version_dir_admin))
            Execute('chown -R %s:%s %s' % (params.unix_user, params.user_group,
                                           params.install_dir_admin))
            Execute('/bin/rm -f /tmp/' + params.filename_admin)

    def install(self, env):
        self.install_packages(env)
        self.install_ranger()
        import params
        env.set_params(params)

        # taking backup of install.properties file
        Execute(('cp', '-f', format('{ranger_home}/install.properties'),
                 format('{ranger_home}/install-backup.properties')),
                not_if=format('ls {ranger_home}/install-backup.properties'),
                only_if=format('ls {ranger_home}/install.properties'),
                sudo=True)

        # call config and setup db only in case of stack version < 2.6
        if not params.stack_supports_ranger_setup_db_on_start:
            self.configure(env, setup_db=True)

    def stop(self, env):
        import params
        env.set_params(params)

        Execute(
            format('{params.ranger_stop}'),
            environment={'JAVA_HOME': params.java_home},
            user=params.unix_user)
        if params.stack_supports_pid:
            File(params.ranger_admin_pid_file, action="delete")

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)

        upgrade.prestart(env)

        self.set_ru_rangeradmin_in_progress(params.upgrade_marker_file)

    def post_upgrade_restart(self, env):
        import params
        env.set_params(params)

        if os.path.isfile(params.upgrade_marker_file):
            os.remove(params.upgrade_marker_file)

        if upgrade_type and params.upgrade_direction == Direction.UPGRADE and not params.stack_supports_multiple_env_sh_files:
            files_name_list = [
                'ranger-admin-env-piddir.sh', 'ranger-admin-env-logdir.sh'
            ]
            for file_name in files_name_list:
                File(format("{ranger_conf}/{file_name}"), action="delete")

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.install_ranger()
        Execute("chown -R %s:%s %s" % (params.unix_user, params.unix_group,
                                       params.install_dir_admin))
        if upgrade_type is None:
            setup_ranger_xml.validate_user_password()

        # setup db only if in case stack version is > 2.6
        self.configure(
            env,
            upgrade_type=upgrade_type,
            setup_db=params.stack_supports_ranger_setup_db_on_start)

        if params.stack_supports_infra_client and params.audit_solr_enabled and params.is_solrCloud_enabled:
            solr_cloud_util.setup_solr_client(
                params.config, custom_log4j=params.custom_log4j)
            setup_ranger_xml.setup_ranger_audit_solr()

        setup_ranger_xml.update_password_configs()
        ranger_service('ranger_admin')

    def status(self, env):
        import status_params

        env.set_params(status_params)

        if status_params.stack_supports_pid:
            check_process_status(status_params.ranger_admin_pid_file)
            return

        cmd = 'ps -ef | grep proc_rangeradmin | grep -v grep'
        code, output = shell.call(cmd, timeout=20)

        if code != 0:
            if self.is_ru_rangeradmin_in_progress(
                    status_params.upgrade_marker_file):
                Logger.info(
                    'Ranger admin process not running - skipping as stack upgrade is in progress'
                )
            else:
                Logger.debug('Ranger admin process not running')
                raise ComponentIsNotRunning()
        pass

    def configure(self, env, setup_db=False, upgrade_type=None):
        import params
        env.set_params(params)

        # set up db if we are not upgrading and setup_db is true
        if setup_db and upgrade_type is None:
            setup_ranger_xml.setup_ranger_db()

        setup_ranger_xml.ranger('ranger_admin', upgrade_type=upgrade_type)

        # set up java patches if we are not upgrading and setup_db is true
        if setup_db and upgrade_type is None:
            setup_ranger_xml.setup_java_patch()

            # Updating password for Ranger Admin user
            setup_ranger_xml.setup_ranger_admin_passwd_change(
                params.admin_username, params.admin_password,
                params.default_admin_password)
            # Updating password for Ranger Usersync user
            setup_ranger_xml.setup_ranger_admin_passwd_change(
                params.rangerusersync_username,
                params.rangerusersync_user_password,
                params.default_rangerusersync_user_password)
            # Updating password for Ranger Tagsync user
            setup_ranger_xml.setup_ranger_admin_passwd_change(
                params.rangertagsync_username,
                params.rangertagsync_user_password,
                params.default_rangertagsync_user_password)
            # Updating password for Ranger Keyadmin user
            setup_ranger_xml.setup_ranger_admin_passwd_change(
                params.keyadmin_username, params.keyadmin_user_password,
                params.default_keyadmin_user_password)

    def set_ru_rangeradmin_in_progress(self, upgrade_marker_file):
        config_dir = os.path.dirname(upgrade_marker_file)
        try:
            msg = "Starting Upgrade"
            if (not os.path.exists(config_dir)):
                os.makedirs(config_dir)
            ofp = open(upgrade_marker_file, 'w')
            ofp.write(msg)
            ofp.close()
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(config_dir):
                pass
            else:
                raise

    def is_ru_rangeradmin_in_progress(self, upgrade_marker_file):
        return os.path.isfile(upgrade_marker_file)

    def setup_ranger_database(self, env):
        import params
        env.set_params(params)

        setup_ranger_xml.setup_ranger_db()

    def setup_ranger_java_patches(self, env):
        import params
        env.set_params(params)

        setup_ranger_xml.setup_java_patch()

    def set_pre_start(self, env):
        import params
        env.set_params(params)

    def get_log_folder(self):
        import params
        return params.admin_log_dir

    def get_user(self):
        import params
        return params.unix_user

    def get_pid_files(self):
        import status_params
        return [status_params.ranger_admin_pid_file]


if __name__ == "__main__":
    RangerAdmin().execute()
