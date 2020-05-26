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
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.resources.modify_properties_file import ModifyPropertiesFile
from resource_management.core.exceptions import Fail
from setup_ranger_nifi import setup_ranger_nifi
from resource_management.core.logger import Logger
from resource_management.libraries.resources.properties_file import PropertiesFile
from resource_management.libraries.functions.check_process_status import check_process_status

from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.script import Script

import nifi_cli
import config_utils


def install_nifi():
    import params
    Directory([params.nifi_config_dir],
              owner=params.nifi_user,
              group=params.nifi_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.nifi_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)

        Execute(' cp -rf ' + params.install_dir + '/conf/*  ' +
                params.nifi_config_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.nifi_config_dir + ' ' + params.install_dir +
                '/conf')
        Execute('chown -R %s:%s %s/%s' % (params.nifi_user, params.nifi_group,Script.get_stack_root(), params.version_dir))
        Execute('chown -R %s:%s %s' % (params.nifi_user, params.nifi_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def install_nifi_toolkit():
    import params
    Directory([params.toolkit_tmp_dir, params.nifi_toolkit_conf_dir],
              owner=params.nifi_user,
              group=params.nifi_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.toolkit_version_dir
                          ) or not os.path.exists(params.toolkit_install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.toolkit_version_dir)
        Execute('rm -rf %s' % params.toolkit_install_dir)
        Execute(
            'wget ' + params.toolkit_download_url + ' -O /tmp/' + params.toolkit_filename,
            user=params.nifi_user)
        Execute('tar -zxf /tmp/' + params.toolkit_filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.toolkit_version_dir + ' ' +
                params.toolkit_install_dir)

        Execute(' cp -rf ' + params.toolkit_install_dir + '/conf/*  ' +
                params.nifi_toolkit_conf_dir)
        Execute(' rm -rf ' + params.toolkit_install_dir + '/conf')
        Execute('ln -s ' + params.nifi_toolkit_conf_dir + ' ' +
                params.toolkit_install_dir + '/conf')
        Execute(
            'chown -R %s:%s %s/%s' % (params.nifi_user, params.nifi_group,
                                      Script.get_stack_root(),params.toolkit_version_dir))
        Execute('chown -R %s:%s %s' % (params.nifi_user, params.nifi_group,
                                       params.toolkit_install_dir))
        Execute('/bin/rm -f /tmp/' + params.toolkit_filename)


class Master(Script):
    def get_component_name(self):
        return "nifi"

    def pre_upgrade_restart(self, env):
        Logger.info("Executing Stack Upgrade pre-restart")
        import params
        env.set_params(params)

    def install(self, env):
        import params

        self.install_packages(env)
        install_nifi()
        install_nifi_toolkit()

        Directory([params.nifi_node_dir, params.nifi_node_log_dir],
                  owner=params.nifi_user,
                  group=params.nifi_group,
                  create_parents=True,
                  recursive_ownership=True,
                  cd_access='a')

        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_user,
            params.nifi_group,
            upgrade_type=None,
            service=nifi_toolkit_util_common.NIFI)
        Execute('touch ' + params.nifi_node_log_file, user=params.nifi_user)

    def configure(self, env, is_starting=False):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        # create the log, pid, conf dirs if not already present
        nifi_dirs = [
            status_params.nifi_pid_dir, params.nifi_internal_dir,
            params.nifi_database_dir, params.nifi_flowfile_repo_dir,
            params.nifi_provenance_repo_dir_default, params.nifi_config_dir,
            params.nifi_flow_config_dir, params.nifi_state_dir, params.lib_dir
        ]
        nifi_dirs.extend(params.nifi_content_repo_dirs)
        Directory(
            nifi_dirs,
            owner=params.nifi_user,
            group=params.nifi_group,
            create_parents=True,
            recursive_ownership=True,
            cd_access='a')

        # On some OS this folder may not exist, so we will create it before pushing files there
        Directory(
            params.limits_conf_dir,
            create_parents=True,
            owner='root',
            group='root')

        File(
            os.path.join(params.limits_conf_dir, 'nifi.conf'),
            owner='root',
            group='root',
            mode=0644,
            content=Template("nifi.conf.j2"))

        # determine whether or not a cluster already exists based on zookeeper entries and determine if this is the first start of this node
        # if so authorizations and flow file will not be writen
        if not sudo.path_isfile(
                params.nifi_flow_config_dir + '/flow.xml.gz'
        ) and nifi_toolkit_util_common.existing_cluster(params):
            params.is_additional_node = True

        # write configurations
        self.write_configurations(params, is_starting)

        generate_logfeeder_input_config(
            'nifi',
            Template("input.config-nifi.json.j2", extra_imports=[default]))

        # if this is not an additional node being added to an existing cluster write out flow.xml.gz to internal dir only if AMS installed (must be writable by Nifi)
        #  and only during first install. It is used to automate setup of Ambari metrics reporting task in Nifi
        if not params.is_additional_node:
            if params.metrics_collector_host and params.nifi_ambari_reporting_enabled and not sudo.path_isfile(
                    params.nifi_flow_config_dir + '/flow.xml.gz'):
                Execute(
                    'echo "First time setup so generating flow.xml.gz" >> ' +
                    params.nifi_node_log_file,
                    user=params.nifi_user)
                flow_content = InlineTemplate(params.nifi_flow_content)
                File(
                    format("{params.nifi_flow_config_dir}/flow.xml"),
                    content=flow_content,
                    owner=params.nifi_user,
                    group=params.nifi_group,
                    mode=0600)
                Execute(
                    format("cd {params.nifi_flow_config_dir}; gzip flow.xml;"),
                    user=params.nifi_user)

    def stop(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        env_content = InlineTemplate(params.nifi_env_content)
        File(
            format("{params.bin_dir}/nifi-env.sh"),
            content=env_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0755)

        Execute(
            'export JAVA_HOME=' + params.jdk64_home + ';' + params.bin_dir +
            '/nifi.sh stop >> ' + params.nifi_node_log_file,
            user=params.nifi_user)
        if os.path.isfile(status_params.nifi_node_pid_file):
            sudo.unlink(status_params.nifi_node_pid_file)

    def start(self, env, upgrade_type=None):
        import params
        import status_params
        install_nifi()
        install_nifi_toolkit()
        nifi_toolkit_util_common.copy_toolkit_scripts(
            params.toolkit_files_dir,
            params.toolkit_tmp_dir,
            params.nifi_user,
            params.nifi_group,
            upgrade_type,
            service=nifi_toolkit_util_common.NIFI)
        self.configure(env, is_starting=True)
        setup_ranger_nifi(upgrade_type=None)

        Execute(
            'export JAVA_HOME=' + params.jdk64_home + ';' + params.bin_dir +
            '/nifi.sh start >> ' + params.nifi_node_log_file,
            user=params.nifi_user)
        # If nifi pid file not created yet, wait a bit
        if not os.path.isfile(status_params.nifi_pid_dir + '/nifi.pid'):
            Execute('sleep 5')

        if params.nifi_registry_url and params.stack_support_nifi_auto_client_registration:
            Logger.info(
                "Trying to register NIFI Registry. This can take up to several minutes. Please, wait..."
            )
            try:
                nifi_cli.create_or_update_reg_client(params.nifi_registry_host,
                                                     params.nifi_registry_url)
            except:
                Logger.warning(
                    "Unable to create or update registry client. Please review NiFi to setup the registry manually if necessary."
                )

    def status(self, env):
        import status_params
        check_process_status(status_params.nifi_node_pid_file)

    def setup_tls_toolkit_upgrade(self, env):
        import params
        env.set_params(params)

        if params.upgrade_direction == Direction.UPGRADE and params.nifi_ssl_enabled and params.nifi_ca_host:
            version_file = params.nifi_config_dir + '/config_version'
            client_json_file = params.nifi_config_dir + '/nifi-certificate-authority-client.json'

            if sudo.path_isfile(version_file):
                Logger.info(format('Remove config version file if does exist'))
                sudo.unlink(version_file)

            if sudo.path_isfile(client_json_file):
                Logger.info(format('Remove client json file'))
                sudo.unlink(client_json_file)

    def write_configurations(self, params, is_starting):

        if os.path.isfile(params.nifi_config_dir + '/bootstrap.conf'):
            bootstrap_current_conf = nifi_toolkit_util_common.convert_properties_to_dict(
                params.nifi_config_dir + '/bootstrap.conf')
            master_key = bootstrap_current_conf[
                'nifi.bootstrap.sensitive.key'] if 'nifi.bootstrap.sensitive.key' in bootstrap_current_conf else None
        else:
            master_key = None

        if os.path.isfile(params.nifi_config_dir + '/nifi.properties'):
            nifi_current_properties = nifi_toolkit_util_common.convert_properties_to_dict(
                params.nifi_config_dir + '/nifi.properties')
            if 'nifi.sensitive.props.key' in nifi_current_properties and nifi_current_properties[
                    'nifi.sensitive.props.key']:
                params.nifi_properties[
                    'nifi.sensitive.props.key'] = nifi_current_properties[
                        'nifi.sensitive.props.key']
            if 'nifi.sensitive.props.key.protected' in nifi_current_properties and nifi_current_properties[
                    'nifi.sensitive.props.key.protected']:
                params.nifi_properties[
                    'nifi.sensitive.props.key.protected'] = nifi_current_properties[
                        'nifi.sensitive.props.key.protected']
        else:
            nifi_current_properties = params.nifi_properties
            params.nifi_toolkit_tls_regenerate = True

        # Resolve and populate required security values and hashes
        params.nifi_properties = nifi_toolkit_util_common.update_nifi_ssl_properties(
            params.nifi_properties, params.nifi_truststore,
            params.nifi_truststoreType, params.nifi_truststorePasswd,
            params.nifi_keystore, params.nifi_keystoreType,
            params.nifi_keystorePasswd, params.nifi_keyPasswd,
            nifi_toolkit_util_common.NIFI)

        # determine whether new keystore/truststore should be regenerated
        run_tls = (params.nifi_ca_host and params.nifi_ssl_enabled) and (
            params.nifi_toolkit_tls_regenerate
            or nifi_toolkit_util_common.generate_keystore_truststore(
                nifi_current_properties, params.nifi_properties, master_key,
                nifi_toolkit_util_common.NIFI))

        if run_tls:
            nifi_toolkit_util_common.move_keystore_truststore(
                nifi_current_properties, nifi_toolkit_util_common.NIFI)
            params.nifi_properties = nifi_toolkit_util_common.create_keystore_truststore(
                params.nifi_properties, is_starting,
                params.nifi_toolkit_java_options, params.nifi_config_dir,
                params.nifi_user, params.nifi_group,
                nifi_toolkit_util_common.NIFI)
        elif not params.nifi_ssl_enabled:
            params.nifi_properties = nifi_toolkit_util_common.clean_toolkit_client_files(
                nifi_current_properties, params.nifi_properties,
                nifi_toolkit_util_common.NIFI)
        elif params.nifi_ssl_enabled and not run_tls and os.path.isfile(
                params.nifi_config_dir + '/nifi.properties'):
            params.nifi_properties = nifi_toolkit_util_common.populate_ssl_properties(
                nifi_toolkit_util_common.convert_properties_to_dict(
                    params.nifi_config_dir + '/nifi.properties'),
                params.nifi_properties, params, nifi_toolkit_util_common.NIFI)

        # if this is an additional node being added to an existing cluster do not include the node identity information
        if params.is_additional_node:
            Logger.info(
                "Excluding initial admin and node identity section from authorizers due to existing cluster"
            )
            params.nifi_authorizers_content = params.nifi_authorizers_content.replace(
                '{{nifi_ssl_config_content | replace("Node","Initial User")}}',
                '')
            params.nifi_authorizers_content = params.nifi_authorizers_content.replace(
                '{{nifi_ssl_config_content}}', '')
            params.nifi_authorizers_content = params.nifi_authorizers_content.replace(
                '{{nifi_initial_admin_id}}', '')

        # Write configuration files
        self.write_files(params)

        # Encrypt files
        nifi_toolkit_util_common.encrypt_sensitive_properties(
            params.nifi_config_dir,
            params.jdk64_home,
            params.nifi_toolkit_java_options,
            params.nifi_user,
            master_key,
            params.nifi_security_encrypt_configuration_password,
            is_starting,
            params.toolkit_tmp_dir,
            params.stack_version_buildnum,
            nifi_toolkit_util_common.NIFI,
            nifi_flow_config_dir=params.nifi_flow_config_dir,
            nifi_sensitive_props_key=params.nifi_sensitive_props_key,
            support_encrypt_authorizers=params.
            stack_support_encrypt_authorizers)

        # Apply Hashed Ambari parameters by retrieving new master key and hashing required parameters for Ambari
        bootstrap_current_conf = nifi_toolkit_util_common.convert_properties_to_dict(
            format("{params.nifi_bootstrap_file}"))
        new_master_key = bootstrap_current_conf[
            'nifi.bootstrap.sensitive.key'] if 'nifi.bootstrap.sensitive.key' in bootstrap_current_conf else None
        if new_master_key:
            nifi_hashed_params = nifi_toolkit_util_common.update_nifi_ambari_hash_properties(
                params.nifi_truststorePasswd, params.nifi_keystorePasswd,
                params.nifi_keyPasswd, new_master_key,
                nifi_toolkit_util_common.NIFI)
            ModifyPropertiesFile(
                format("{params.nifi_config_dir}/nifi.properties"),
                properties=nifi_hashed_params,
                owner=params.nifi_user)
        else:
            raise Fail(
                "Unable to persist ambari hashes due to no master key! Please validate this was written to bootstrap.conf file."
            )

    def write_files(self, params):

        # write out nifi.properties
        PropertiesFile(
            format("{params.nifi_config_dir}/nifi.properties"),
            properties=params.nifi_properties,
            mode=0600,
            owner=params.nifi_user,
            group=params.nifi_group)

        # write out boostrap.conf
        bootstrap_content = InlineTemplate(params.nifi_boostrap_content)
        File(
            format("{params.nifi_bootstrap_file}"),
            content=bootstrap_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0600)

        # write out logback.xml
        logback_content = InlineTemplate(params.nifi_node_logback_content)
        File(
            format("{params.nifi_config_dir}/logback.xml"),
            content=logback_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0400)

        # write out state-management.xml
        statemgmt_content = InlineTemplate(
            params.nifi_state_management_content)
        File(
            format("{params.nifi_config_dir}/state-management.xml"),
            content=statemgmt_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0400)

        # write out authorizers file
        authorizers_content = config_utils.append_xml_content(
            params.nifi_authorizers_content, params.nifi_authorizers_dict)
        File(
            format("{params.nifi_config_dir}/authorizers.xml"),
            content=authorizers_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0600)

        # write out login-identity-providers.xml
        login_identity_providers_content = config_utils.append_xml_content(
            params.nifi_login_identity_providers_content,
            params.nifi_login_identity_providers_dict)
        File(
            format("{params.nifi_config_dir}/login-identity-providers.xml"),
            content=login_identity_providers_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0600)

        # write out nifi-env in bin as 0755 (see BUG-61769)
        env_content = InlineTemplate(params.nifi_env_content)
        File(
            format("{params.bin_dir}/nifi-env.sh"),
            content=env_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0755)

        # write out bootstrap-notification-services.xml
        boostrap_notification_content = config_utils.append_xml_content(
            params.nifi_boostrap_notification_content,
            params.nifi_boostrap_notification_dict)
        File(
            format(
                "{params.nifi_config_dir}/bootstrap-notification-services.xml"
            ),
            content=boostrap_notification_content,
            owner=params.nifi_user,
            group=params.nifi_group,
            mode=0400)

        # if security is enabled for kerberos create the nifi_jaas.conf file
        if params.security_enabled and params.stack_support_nifi_jaas:
            File(
                params.nifi_jaas_conf,
                content=InlineTemplate(params.nifi_jaas_conf_template),
                owner=params.nifi_user,
                group=params.nifi_group,
                mode=0400)


if __name__ == "__main__":
    Master().execute()
