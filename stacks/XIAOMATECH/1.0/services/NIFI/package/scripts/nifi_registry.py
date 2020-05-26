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

import nifi_toolkit_util_common, os
from resource_management import *
from resource_management.core import sudo
from resource_management.libraries.resources.modify_properties_file import ModifyPropertiesFile
from resource_management.libraries.functions.constants import Direction
from resource_management.core.exceptions import Fail

from resource_management.libraries.functions.format import format
from resource_management.libraries.script import Script
from resource_management.core.logger import Logger
from resource_management.libraries.resources.properties_file import PropertiesFile
from resource_management.libraries.functions.check_process_status import check_process_status

from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import Template, InlineTemplate

import config_utils
from nifi import install_nifi_toolkit


def install_nifi_registry():
    import params
    Directory([params.nifi_registry_config_dir],
              owner=params.nifi_user,
              group=params.nifi_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.registry_version_dir
                          ) or not os.path.exists(params.registry_install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.registry_version_dir)
        Execute('rm -rf %s' % params.registry_install_dir)
        Execute(
            'wget ' + params.registry_download_url + ' -O /tmp/' + params.registry_filename,
            user=params.nifi_registry_user)
        Execute('tar -zxf /tmp/' + params.registry_filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.registry_version_dir + ' ' +
                params.registry_install_dir)

        Execute(' cp -rf ' + params.registry_install_dir + '/conf/*  ' +
                params.registry_install_dir)
        Execute(' rm -rf ' + params.registry_install_dir + '/conf')
        Execute('ln -s ' + params.registry_install_dir + ' ' +
                params.registry_install_dir + '/conf')
        Execute('chown -R %s:%s %s/%s' %
                (params.nifi_registry_user, params.nifi_registry_group,
                 Script.get_stack_root(),params.registry_version_dir))
        Execute('chown -R %s:%s %s' %
                (params.nifi_registry_user, params.nifi_registry_group,
                 params.registry_install_dir))
        Execute('/bin/rm -f /tmp/' + params.registry_filename)
        Execute(
            'export JAVA_HOME=' + params.jdk64_home + ';' +
            params.nifi_registry_bin_dir + '/nifi-registry.sh install >> ' +
            params.nifi_registry_log_file,
            user=params.nifi_registry_user)


class Master(Script):
    def get_component_name(self):
        return "nifi-registry"

    def pre_upgrade_restart(self, env, upgrade_type=None):
        Logger.info("Executing Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def install(self, env):
        import params

        self.install_packages(env)
        install_nifi_registry()
        install_nifi_toolkit()
        # params.nifi_registry_dir,
        Directory([params.nifi_registry_log_dir],
                  owner=params.nifi_registry_user,
                  group=params.nifi_registry_group,
                  create_parents=True,
                  recursive_ownership=True,
                  cd_access='a')

        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_registry_user,
            params.nifi_registry_group,
            upgrade_type=None,
            service=nifi_toolkit_util_common.NIFI_REGISTRY)
        Execute(
            'touch ' + params.nifi_registry_log_file,
            user=params.nifi_registry_user)

    def configure(self, env, is_starting=False):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        # create the log, pid, conf dirs if not already present
        nifi_registry_dirs = [
            status_params.nifi_registry_pid_dir,
            params.nifi_registry_internal_dir,
            params.nifi_registry_internal_config_dir,
            params.nifi_registry_database_dir, params.nifi_registry_config_dir,
            params.nifi_registry_bin_dir, params.nifi_registry_lib_dir,
            params.nifi_registry_docs_dir
        ]

        Directory(
            nifi_registry_dirs,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            create_parents=True,
            recursive_ownership=True,
            cd_access='a')

        # write configurations
        self.write_configurations(params, is_starting)

    def stop(self, env, upgrade_type=None):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        Directory([params.nifi_registry_bin_dir],
                  owner=params.nifi_registry_user,
                  group=params.nifi_registry_group,
                  create_parents=True,
                  recursive_ownership=True,
                  cd_access='a')

        env_content = InlineTemplate(params.nifi_registry_env_content)
        File(
            format("{params.nifi_registry_bin_dir}/nifi-registry-env.sh"),
            content=env_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0755)

        Execute(
            'export JAVA_HOME=' + params.jdk64_home + ';' +
            params.nifi_registry_bin_dir + '/nifi-registry.sh stop >> ' +
            params.nifi_registry_log_file,
            user=params.nifi_registry_user)
        if os.path.isfile(status_params.nifi_registry_pid_file):
            sudo.unlink(status_params.nifi_registry_pid_file)

    def start(self, env, upgrade_type=None):
        import params
        import status_params
        install_nifi_registry()
        install_nifi_toolkit()
        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_registry_user,
            params.nifi_registry_group,
            upgrade_type=None,
            service=nifi_toolkit_util_common.NIFI_REGISTRY)
        self.configure(env, is_starting=True)
        # setup_ranger_nifi(upgrade_type=None)

        Execute(
            'export JAVA_HOME=' + params.jdk64_home + ';' +
            params.nifi_registry_bin_dir + '/nifi-registry.sh start >> ' +
            params.nifi_registry_log_file,
            user=params.nifi_registry_user)
        # If nifi pid file not created yet, wait a bit
        if not os.path.isfile(status_params.nifi_registry_pid_dir +
                              '/nifi-registry.pid'):
            Execute('sleep 5')

    def status(self, env):
        import status_params
        check_process_status(status_params.nifi_registry_pid_file)

    def setup_tls_toolkit_upgrade(self, env):
        import params
        env.set_params(params)

        if params.upgrade_direction == Direction.UPGRADE and params.nifi_registry_ssl_enabled and params.nifi_ca_host:
            version_file = params.nifi_registry_config_dir + '/config_version'
            client_json_file = params.nifi_registry_config_dir + '/nifi-certificate-authority-client.json'

            if not sudo.path_isfile(version_file):
                Logger.info(
                    format('Remove config version file if it does not exist'))
                sudo.unlink(version_file)

            if sudo.path_isfile(client_json_file):
                Logger.info(format('Remove client json file'))
                sudo.unlink(client_json_file)

    def write_configurations(self, params, is_starting):

        if os.path.isfile(params.nifi_registry_config_dir + '/bootstrap.conf'):
            bootstrap_current_conf = nifi_toolkit_util_common.convert_properties_to_dict(
                params.nifi_registry_config_dir + '/bootstrap.conf')
            master_key = bootstrap_current_conf[
                'nifi.registry.bootstrap.sensitive.key'] if 'nifi.registry.bootstrap.sensitive.key' in bootstrap_current_conf else None
        else:
            master_key = None

        if os.path.isfile(params.nifi_registry_config_dir +
                          '/nifi-registry.properties'):
            nifi_registry_current_properties = nifi_toolkit_util_common.convert_properties_to_dict(
                params.nifi_registry_config_dir + '/nifi-registry.properties')
            if 'nifi.registry.sensitive.props.key' in nifi_registry_current_properties and \
                    nifi_registry_current_properties['nifi.registry.sensitive.props.key']:
                params.nifi_registry_properties[
                    'nifi.registry.sensitive.props.key'] = nifi_registry_current_properties[
                        'nifi.registry.sensitive.props.key']
            if 'nifi.registry.sensitive.props.key.protected' in nifi_registry_current_properties and \
                    nifi_registry_current_properties['nifi.registry.sensitive.props.key.protected']:
                params.nifi_registry_properties['nifi.registry.sensitive.props.key.protected'] = \
                    nifi_registry_current_properties['nifi.registry.sensitive.props.key.protected']
        else:
            nifi_registry_current_properties = params.nifi_registry_properties
            params.nifi_toolkit_tls_regenerate = True

        # resolve and populate required security values and hashes
        params.nifi_registry_properties = nifi_toolkit_util_common.update_nifi_ssl_properties(
            params.nifi_registry_properties, params.nifi_registry_truststore,
            params.nifi_registry_truststoreType,
            params.nifi_registry_truststorePasswd,
            params.nifi_registry_keystore, params.nifi_registry_keystoreType,
            params.nifi_registry_keystorePasswd,
            params.nifi_registry_keyPasswd,
            nifi_toolkit_util_common.NIFI_REGISTRY)

        # determine whether new keystore/truststore should be regenerated
        run_tls = (params.nifi_ca_host
                   and params.nifi_registry_ssl_enabled) and (
                       params.nifi_toolkit_tls_regenerate or
                       nifi_toolkit_util_common.generate_keystore_truststore(
                           nifi_registry_current_properties,
                           params.nifi_registry_properties, master_key,
                           nifi_toolkit_util_common.NIFI_REGISTRY))

        if run_tls:
            nifi_toolkit_util_common.move_keystore_truststore(
                nifi_registry_current_properties,
                nifi_toolkit_util_common.NIFI_REGISTRY)
            params.nifi_registry_properties = nifi_toolkit_util_common.create_keystore_truststore(
                params.nifi_registry_properties, is_starting,
                params.nifi_toolkit_java_options,
                params.nifi_registry_config_dir, params.nifi_registry_user,
                params.nifi_registry_group,
                nifi_toolkit_util_common.NIFI_REGISTRY)
        elif not params.nifi_registry_ssl_enabled:
            params.nifi_registry_properties = nifi_toolkit_util_common.clean_toolkit_client_files(
                nifi_registry_current_properties,
                params.nifi_registry_properties,
                nifi_toolkit_util_common.NIFI_REGISTRY)
        elif params.nifi_registry_ssl_enabled and not run_tls and os.path.isfile(
                params.nifi_registry_config_dir + '/nifi-registry.properties'):
            params.nifi_registry_properties = nifi_toolkit_util_common.populate_ssl_properties(
                nifi_toolkit_util_common.convert_properties_to_dict(
                    params.nifi_registry_config_dir +
                    '/nifi-registry.properties'),
                params.nifi_registry_properties, params,
                nifi_toolkit_util_common.NIFI_REGISTRY)

        self.write_files(params)

        nifi_toolkit_util_common.encrypt_sensitive_properties(
            params.nifi_registry_config_dir, params.jdk64_home,
            params.nifi_toolkit_java_options, params.nifi_registry_user,
            master_key,
            params.nifi_registry_security_encrypt_configuration_password,
            is_starting, params.toolkit_tmp_dir, params.stack_version_buildnum,
            nifi_toolkit_util_common.NIFI_REGISTRY)

        # Apply Hashed Ambari parameters by retrieving new master key and hashing required parameters for Ambari
        bootstrap_current_conf = nifi_toolkit_util_common.convert_properties_to_dict(
            format("{params.nifi_registry_bootstrap_file}"))
        master_key = bootstrap_current_conf[
            'nifi.registry.bootstrap.sensitive.key'] if 'nifi.registry.bootstrap.sensitive.key' in bootstrap_current_conf else None
        if master_key:
            nifi_registry_hashed_params = nifi_toolkit_util_common.update_nifi_ambari_hash_properties(
                params.nifi_registry_truststorePasswd,
                params.nifi_registry_keystorePasswd,
                params.nifi_registry_keyPasswd, master_key,
                nifi_toolkit_util_common.NIFI_REGISTRY)
            ModifyPropertiesFile(
                format(
                    "{params.nifi_registry_config_dir}/nifi-registry.properties"
                ),
                properties=nifi_registry_hashed_params,
                owner=params.nifi_registry_user)
        else:
            raise Fail(
                "Unable to persist ambari hashes due to no master key! Please validate this was written to bootstrap.conf file."
            )

    def write_files(self, params):

        # write out nifi-registry.properties
        PropertiesFile(
            params.nifi_registry_config_dir + '/nifi-registry.properties',
            properties=params.nifi_registry_properties,
            mode=0600,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group)

        # write out boostrap.conf
        bootstrap_content = InlineTemplate(
            params.nifi_registry_boostrap_content)

        File(
            format("{params.nifi_registry_bootstrap_file}"),
            content=bootstrap_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0600)

        # write out logback.xml
        logback_content = InlineTemplate(params.nifi_registry_logback_content)

        File(
            format("{params.nifi_registry_config_dir}/logback.xml"),
            content=logback_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0400)

        # write out authorizers file

        authorizers_content = config_utils.append_xml_content(
            params.nifi_registry_authorizers_content,
            params.nifi_registry_authorizers_dict)

        File(
            format("{params.nifi_registry_config_dir}/authorizers.xml"),
            content=authorizers_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0600)

        # write out identity-providers.xml
        identity_providers_content = config_utils.append_xml_content(
            params.nifi_registry_identity_providers_content,
            params.nifi_registry_identity_providers_dict)

        File(
            format("{params.nifi_registry_config_dir}/identity-providers.xml"),
            content=identity_providers_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0600)

        # write out providers file
        providers_content = config_utils.append_xml_content(
            params.nifi_registry_providers_content,
            params.nifi_registry_providers_dict)

        File(
            format("{params.nifi_registry_config_dir}/providers.xml"),
            content=providers_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0400)

        # write out nifi-env in bin as 0755 (see BUG-61769)
        env_content = InlineTemplate(params.nifi_registry_env_content)

        File(
            format("{params.nifi_registry_bin_dir}/nifi-registry-env.sh"),
            content=env_content,
            owner=params.nifi_registry_user,
            group=params.nifi_registry_group,
            mode=0755)


if __name__ == "__main__":
    Master().execute()
