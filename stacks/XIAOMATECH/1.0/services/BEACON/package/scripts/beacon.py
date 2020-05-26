import os.path
import time

from resource_management.core.exceptions import Fail
from resource_management.core.source import Template
from resource_management.core.source import StaticFile
from resource_management.core.source import DownloadSource
from resource_management.core.resources import Execute
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.libraries.functions import get_user_call_output
from resource_management.libraries.functions import format
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.security_commons import update_credential_provider_path
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.core.logger import Logger
from resource_management.libraries.script.config_dictionary import UnknownConfiguration
import beacon_utils

from resource_management.libraries.script import Script

import ranger_api_functions


def install_beacon():
    import params
    Directory([params.etc_prefix_dir],
              owner=params.beacon_user,
              group=params.user_group,
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.beacon_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.etc_prefix_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.etc_prefix_dir + ' ' + params.install_dir +
                '/conf')

        Execute('chown -R %s:%s %s/%s' %
                (params.beacon_user, params.user_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.beacon_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def beacon(type, action=None, upgrade_type=None):
    import params

    if action == 'config':
        create_directory(params.beacon_home_dir)
        create_directory(params.beacon_plugin_staging_dir)

        cloud_cred_provider = params.beacon_cloud_cred_provider_dir.split('://')[1]
        cloud_cred_parts = cloud_cred_provider.split('/', 1)
        create_directory("/" + cloud_cred_parts[1], cloud_cred_parts[0])

        if params.is_hive_installed:
            if not isinstance(params.hive_repl_cmrootdir, UnknownConfiguration):
                beacon_utils.create_hdfs_directory(params.hive_repl_cmrootdir,
                                                   params.hive_user,
                                                   01777)
            if not isinstance(params.hive_repl_rootdir, UnknownConfiguration):
                beacon_utils.create_hdfs_directory(params.hive_repl_rootdir,
                                                   params.hive_user,
                                                   0700)

        Directory(params.beacon_pid_dir,
                  owner=params.beacon_user,
                  create_parents=True,
                  mode=0755,
                  cd_access="a",
                  )

        Directory(params.beacon_data_dir,
                  owner=params.beacon_user,
                  create_parents=True,
                  mode=0755,
                  cd_access="a",
                  )

        Directory(params.beacon_log_dir,
                  owner=params.beacon_user,
                  create_parents=True,
                  mode=0755,
                  cd_access="a",
                  )

        Directory(params.beacon_webapp_dir,
                  owner=params.beacon_user,
                  create_parents=True)

        Directory(params.beacon_home,
                  owner=params.beacon_user,
                  create_parents=True)

        Directory(params.etc_prefix_dir,
                  mode=0755,
                  create_parents=True)

        Directory(params.beacon_conf_dir,
                  owner=params.beacon_user,
                  create_parents=True)

    environment_dictionary = {
        "HADOOP_HOME": params.hadoop_home_dir,
        "JAVA_HOME": params.java_home,
        "BEACON_LOG_DIR": params.beacon_log_dir,
        "BEACON_PID_DIR": params.beacon_pid_dir,
        "BEACON_DATA_DIR": params.beacon_data_dir,
        "BEACON_CLUSTER": params.beacon_cluster_name,
        "HADOOP_CONF": params.hadoop_conf_dir
    }
    pid = get_user_call_output.get_user_call_output(format("cat {server_pid_file}"), user=params.beacon_user,
                                                    is_checked_call=False)[1]
    process_exists = format("ls {server_pid_file} && ps -p {pid}")

    if type == 'server':
        if action == 'start':
            try:

                if params.credential_store_enabled:
                    if 'hadoop.security.credential.provider.path' in params.beacon_env:
                        credential_provider_path = params.beacon_env['hadoop.security.credential.provider.path']
                        credential_provider_src_path = credential_provider_path[len('jceks://file'):]
                        File(params.beacon_credential_provider_path[len('jceks://file'):],
                             owner=params.beacon_user,
                             group=params.user_group,
                             mode=0640,
                             content=StaticFile(credential_provider_src_path)
                             )
                    else:
                        Logger.error(
                            "hadoop.security.credential.provider.path property not found in beacon-env config-type")

                File(os.path.join(params.beacon_conf_dir, 'beacon.yml'),
                     owner='root',
                     group='root',
                     mode=0644,
                     content=Template("beacon.yml.j2")
                     )

                params.beacon_security_site = update_credential_provider_path(
                    params.beacon_security_site,
                    'beacon-security-site',
                    os.path.join(params.beacon_conf_dir, 'beacon-security-site.jceks'),
                    params.beacon_user,
                    params.user_group
                )

                XmlConfig("beacon-security-site.xml",
                          conf_dir=params.beacon_conf_dir,
                          configurations=params.beacon_security_site,
                          configuration_attributes=params.config['configuration_attributes']['beacon-security-site'],
                          owner=params.beacon_user,
                          group=params.user_group,
                          mode=0644
                          )

                Execute(format('{beacon_home}/bin/beacon setup'),
                        user=params.beacon_user,
                        path=params.hadoop_bin_dir,
                        environment=environment_dictionary
                        )

                if params.download_mysql_driver:
                    download_mysql_driver()

                Execute(format('{beacon_home}/bin/beacon start'),
                        user=params.beacon_user,
                        path=params.hadoop_bin_dir,
                        environment=environment_dictionary,
                        not_if=process_exists,
                        )

                if params.has_ranger_admin:
                    ranger_admin_url = params.config['configurations']['admin-properties']['policymgr_external_url']
                    ranger_admin_user = params.config['configurations']['ranger-env']['admin_username']
                    ranger_admin_passwd = params.config['configurations']['ranger-env']['admin_password']

                    if not params.security_enabled:
                        # Creating/Updating beacon.ranger.user with role "ROLE_SYS_ADMIN"
                        response_user = ranger_api_functions.get_user(ranger_admin_url, params.beacon_ranger_user,
                                                                      format(
                                                                          "{ranger_admin_user}:{ranger_admin_passwd}"))
                        if response_user is not None and response_user['name'] == params.beacon_ranger_user:
                            response_user_role = response_user['userRoleList'][0]
                            Logger.info(format(
                                "Beacon Ranger User with username {beacon_ranger_user} exists with role {response_user_role}"))
                            if response_user_role != "ROLE_SYS_ADMIN":
                                response_user_role = ranger_api_functions.update_user_role(ranger_admin_url,
                                                                                           params.beacon_ranger_user,
                                                                                           "ROLE_SYS_ADMIN", format(
                                        "{ranger_admin_user}:{ranger_admin_passwd}"))
                        else:
                            response_code = ranger_api_functions.create_user(ranger_admin_url,
                                                                             params.beacon_ranger_user,
                                                                             params.beacon_ranger_password,
                                                                             "ROLE_SYS_ADMIN", format(
                                    "{ranger_admin_user}:{ranger_admin_passwd}"))

                    # Updating beacon_user role depending upon cluster environment
                    count = 0
                    while count < 10:
                        beacon_user_get = ranger_api_functions.get_user(ranger_admin_url, params.beacon_user, format(
                            "{ranger_admin_user}:{ranger_admin_passwd}"))
                        if beacon_user_get is not None:
                            break
                        else:
                            time.sleep(10)  # delay for 10 seconds
                            count = count + 1
                            Logger.error(
                                format('Retrying to fetch {beacon_user} user from Ranger Admin for {count} time(s)'))

                    if beacon_user_get is not None and beacon_user_get['name'] == params.beacon_user:
                        beacon_user_get_role = beacon_user_get['userRoleList'][0]
                        if params.security_enabled and beacon_user_get_role != "ROLE_SYS_ADMIN":
                            beacon_service_user = ranger_api_functions.update_user_role(ranger_admin_url,
                                                                                        params.beacon_user,
                                                                                        "ROLE_SYS_ADMIN", format(
                                    "{ranger_admin_user}:{ranger_admin_passwd}"))
                        elif not params.security_enabled and beacon_user_get_role != "ROLE_USER":
                            beacon_service_user = ranger_api_functions.update_user_role(ranger_admin_url,
                                                                                        params.beacon_user, "ROLE_USER",
                                                                                        format(
                                                                                            "{ranger_admin_user}:{ranger_admin_passwd}"))

                    if params.ranger_hive_plugin_enabled:
                        # Get Ranger Hive default policy for resource database, table, column
                        response_policy = ranger_api_functions.get_ranger_service_default_policy(ranger_admin_url,
                                                                                                 params.service_name,
                                                                                                 format(
                                                                                                     "{ranger_admin_user}:{ranger_admin_passwd}"),
                                                                                                 ['database', 'table',
                                                                                                  'column'])
                        if response_policy:
                            user_present = ranger_api_functions.check_user_policy(response_policy, params.beacon_user)
                            if not user_present and beacon_user_get is not None and beacon_user_get[
                                'name'] == params.beacon_user:
                                policy_id = response_policy['id']
                                beacon_user_policy_item = {'groups': [], 'conditions': [],
                                                           'users': [params.beacon_user],
                                                           'accesses': [{'isAllowed': True, 'type': 'all'},
                                                                        {'isAllowed': True, 'type': 'repladmin'}],
                                                           'delegateAdmin': False}
                                policy_data = ranger_api_functions.update_policy_item(response_policy,
                                                                                      beacon_user_policy_item)
                                update_policy_response = ranger_api_functions.update_policy(ranger_admin_url, policy_id,
                                                                                            policy_data, format(
                                        "{ranger_admin_user}:{ranger_admin_passwd}"))

                        # Get Ranger Hive default policy for resource hiveservice
                        response_policy = ranger_api_functions.get_ranger_service_default_policy(ranger_admin_url,
                                                                                                 params.service_name,
                                                                                                 format(
                                                                                                     "{ranger_admin_user}:{ranger_admin_passwd}"),
                                                                                                 ['hiveservice'])
                        if response_policy:
                            user_present = ranger_api_functions.check_user_policy(response_policy, params.beacon_user)
                            if not user_present and beacon_user_get is not None and beacon_user_get[
                                'name'] == params.beacon_user:
                                # Updating beacon_user in Ranger Hive default policy for resource hiveservice
                                policy_id = response_policy['id']
                                beacon_user_policy_item = {'groups': [], 'conditions': [],
                                                           'users': [params.beacon_user],
                                                           'accesses': [{'isAllowed': True, 'type': 'serviceadmin'}],
                                                           'delegateAdmin': False}
                                policy_data = ranger_api_functions.update_policy_item(response_policy,
                                                                                      beacon_user_policy_item)
                                update_policy_response = ranger_api_functions.update_policy(ranger_admin_url, policy_id,
                                                                                            policy_data, format(
                                        "{ranger_admin_user}:{ranger_admin_passwd}"))

                    if params.ranger_atlas_plugin_enabled:
                        # Creating beacon.atlas.user with role "ROLE_USER"
                        beacon_atlas_user_response = ranger_api_functions.get_user(ranger_admin_url,
                                                                                   params.beacon_atlas_user, format(
                                "{ranger_admin_user}:{ranger_admin_passwd}"))
                        if beacon_atlas_user_response is not None and beacon_atlas_user_response[
                            'name'] == params.beacon_atlas_user:
                            beacon_atlas_user_role = beacon_atlas_user_response['userRoleList'][0]
                            Logger.info(format(
                                "Beacon Atlas User with username {beacon_atlas_user} exists with role {beacon_atlas_user_role}"))
                        else:
                            beacon_atlas_user_create_response_code = ranger_api_functions.create_user(ranger_admin_url,
                                                                                                      params.beacon_atlas_user,
                                                                                                      params.beacon_atlas_password,
                                                                                                      "ROLE_USER",
                                                                                                      format(
                                                                                                          "{ranger_admin_user}:{ranger_admin_passwd}"))

                        if params.security_enabled:
                            get_beacon_atlas_user = params.beacon_user
                        else:
                            get_beacon_atlas_user = params.beacon_atlas_user

                        if params.is_stack_3_0_or_further:
                            # Get Ranger Atlas default policy for ENTITY TYPE, ENTITY CLASSIFICATION and ENTITY ID resource
                            atlas_entity_policy_response = ranger_api_functions.get_ranger_service_default_policy(
                                ranger_admin_url, params.ranger_atlas_service_name,
                                format("{ranger_admin_user}:{ranger_admin_passwd}"),
                                ['entity', 'entity-classification', 'entity-type'])

                            if atlas_entity_policy_response:
                                beacon_atlas_user_present = ranger_api_functions.check_user_policy(
                                    atlas_entity_policy_response, get_beacon_atlas_user)
                                if not beacon_atlas_user_present:
                                    # Updating beacon atlas user in Ranger Atlas default policy for entity resource
                                    atlas_entity_policy_id = atlas_entity_policy_response['id']
                                    beacon_atlas_user_policy_item = {'groups': [], 'conditions': [],
                                                                     'users': [get_beacon_atlas_user], 'accesses': [
                                            {'type': 'entity-read', 'isAllowed': True},
                                            {'type': 'entity-create', 'isAllowed': True},
                                            {'type': 'entity-update', 'isAllowed': True}]}
                                    atlas_entity_policy_data = ranger_api_functions.update_policy_item(
                                        atlas_entity_policy_response, beacon_atlas_user_policy_item)
                                    atlas_update_entity_policy_response = ranger_api_functions.update_policy(
                                        ranger_admin_url, atlas_entity_policy_id, atlas_entity_policy_data,
                                        format("{ranger_admin_user}:{ranger_admin_passwd}"))

                            # Get Ranger Atlas default policy for ATLAS SERVICE resource
                            atlas_service_policy_response = ranger_api_functions.get_ranger_service_default_policy(
                                ranger_admin_url, params.ranger_atlas_service_name,
                                format("{ranger_admin_user}:{ranger_admin_passwd}"), ['atlas-service'])
                            if atlas_service_policy_response:
                                beacon_atlas_user_present = ranger_api_functions.check_user_policy(
                                    atlas_service_policy_response, get_beacon_atlas_user)
                                if not beacon_atlas_user_present:
                                    # Updating beacon atlas user in Ranger Atlas default policy for service resource
                                    atlas_service_policy_id = atlas_service_policy_response['id']
                                    beacon_atlas_user_policy_item = {'groups': [], 'conditions': [],
                                                                     'users': [get_beacon_atlas_user], 'accesses': [
                                            {'type': 'admin-export', 'isAllowed': True},
                                            {'type': 'admin-import', 'isAllowed': True}]}
                                    atlas_service_policy_data = ranger_api_functions.update_policy_item(
                                        atlas_service_policy_response, beacon_atlas_user_policy_item)
                                    atlas_service_policy_update_response = ranger_api_functions.update_policy(
                                        ranger_admin_url, atlas_service_policy_id, atlas_service_policy_data,
                                        format("{ranger_admin_user}:{ranger_admin_passwd}"))

                            # Get Ranger Atlas default policy for TYPE CATEGORY and TYPE resource
                            atlas_type_category_policy_response = ranger_api_functions.get_ranger_service_default_policy(
                                ranger_admin_url, params.ranger_atlas_service_name,
                                format("{ranger_admin_user}:{ranger_admin_passwd}"), ['type', 'type-category'])

                            if atlas_type_category_policy_response:
                                beacon_atlas_user_present = ranger_api_functions.check_user_policy(
                                    atlas_type_category_policy_response, get_beacon_atlas_user)
                                if not beacon_atlas_user_present:
                                    # Updating beacon atlas user in Ranger Atlas default policy for type category and type resource
                                    atlas_type_category_policy_id = atlas_type_category_policy_response['id']
                                    beacon_atlas_user_policy_item = {'groups': [], 'conditions': [],
                                                                     'users': [get_beacon_atlas_user], 'accesses': [
                                            {'type': 'type-create', 'isAllowed': True},
                                            {'type': 'type-update', 'isAllowed': True},
                                            {'type': 'type-delete', 'isAllowed': True}]}
                                    atlas_type_category_policy_data = ranger_api_functions.update_policy_item(
                                        atlas_type_category_policy_response, beacon_atlas_user_policy_item)
                                    atlas_update_type_category_policy_response = ranger_api_functions.update_policy(
                                        ranger_admin_url, atlas_type_category_policy_id,
                                        atlas_type_category_policy_data,
                                        format("{ranger_admin_user}:{ranger_admin_passwd}"))
                        else:
                            # Get Ranger Atlas default policy for ENTITY resource
                            atlas_policy_response = ranger_api_functions.get_ranger_service_default_policy(
                                ranger_admin_url, params.ranger_atlas_service_name,
                                format("{ranger_admin_user}:{ranger_admin_passwd}"), ['entity'])

                            if atlas_policy_response:
                                beacon_atlas_user_present = ranger_api_functions.check_user_policy(
                                    atlas_policy_response, get_beacon_atlas_user)
                                if not beacon_atlas_user_present:
                                    # Updating beacon atlas user in Ranger Atlas default policy for entity resource
                                    atlas_policy_id = atlas_policy_response['id']
                                    beacon_atlas_user_policy_item = {'groups': [], 'conditions': [],
                                                                     'users': [get_beacon_atlas_user],
                                                                     'accesses': [{'type': 'read', 'isAllowed': True},
                                                                                  {'type': 'create', 'isAllowed': True},
                                                                                  {'type': 'update', 'isAllowed': True},
                                                                                  {'type': 'delete', 'isAllowed': True},
                                                                                  {'type': 'all', 'isAllowed': True}]}
                                    atlas_policy_data = ranger_api_functions.update_policy_item(atlas_policy_response,
                                                                                                beacon_atlas_user_policy_item)
                                    atlas_update_policy_response = ranger_api_functions.update_policy(ranger_admin_url,
                                                                                                      atlas_policy_id,
                                                                                                      atlas_policy_data,
                                                                                                      format(
                                                                                                          "{ranger_admin_user}:{ranger_admin_passwd}"))

                            # Get Ranger Atlas default policy for OPERATION resource
                            atlas_operation_policy_response = ranger_api_functions.get_ranger_service_default_policy(
                                ranger_admin_url, params.ranger_atlas_service_name,
                                format("{ranger_admin_user}:{ranger_admin_passwd}"), ['operation'])
                            if atlas_operation_policy_response:
                                beacon_atlas_user_present = ranger_api_functions.check_user_policy(
                                    atlas_operation_policy_response, get_beacon_atlas_user)
                                if not beacon_atlas_user_present:
                                    # Updating beacon atlas user in Ranger Atlas default policy for operation resource
                                    atlas_operation_policy_id = atlas_operation_policy_response['id']
                                    beacon_atlas_user_policy_item = {'groups': [], 'conditions': [],
                                                                     'users': [get_beacon_atlas_user],
                                                                     'accesses': [{'type': 'read', 'isAllowed': True},
                                                                                  {'type': 'create', 'isAllowed': True},
                                                                                  {'type': 'update', 'isAllowed': True},
                                                                                  {'type': 'delete', 'isAllowed': True},
                                                                                  {'type': 'all', 'isAllowed': True}]}
                                    atlas_operation_policy_data = ranger_api_functions.update_policy_item(
                                        atlas_operation_policy_response, beacon_atlas_user_policy_item)
                                    atlas_operation_policy_update_response = ranger_api_functions.update_policy(
                                        ranger_admin_url, atlas_operation_policy_id, atlas_operation_policy_data,
                                        format("{ranger_admin_user}:{ranger_admin_passwd}"))
            except Exception as e:
                show_logs(params.beacon_log_dir, params.beacon_user)

        if action == 'stop':
            try:
                Execute(format('{beacon_home}/bin/beacon stop'),
                        user=params.beacon_user,
                        path=params.hadoop_bin_dir,
                        environment=environment_dictionary)
            except:
                show_logs(params.beacon_log_dir, params.beacon_user)

            File(params.server_pid_file, action='delete')


def create_directory(directory, scheme=None):
    import params

    if (scheme is None or scheme == ''):
        if params.is_hdfs_installed:
            scheme = 'hdfs'
        else:
            scheme = 'file'

    Logger.info("Creating directory {0}:/{1}".format(scheme, directory))
    if scheme == 'file':
        Directory(directory,
                  owner=params.beacon_user,
                  create_parents=True,
                  mode=0755,
                  cd_access="a")
    elif scheme == 'hdfs':
        beacon_utils.create_hdfs_directory(directory, params.beacon_user, 0775)
        params.HdfsResource(None, action="execute")


def download_mysql_driver():
    import params

    if params.jdbc_jar_name is None:
        raise Fail("Mysql JDBC driver not installed on ambari-server")

    File(
        params.mysql_driver_target,
        content=DownloadSource(params.driver_source),
        mode=0644
    )
