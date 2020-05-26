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
from resource_management.core.logger import Logger

import sys, os

script_path = os.path.realpath(__file__).split(
    '/services')[0] + '/../../../stack-hooks/before-INSTALL/scripts/ranger'
sys.path.append(script_path)
from setup_ranger_plugin_xml import setup_ranger_plugin


def setup_ranger_kylin():
    import params

    if params.enable_ranger_kylin:

        if params.retryAble:
            Logger.info(
                "kylin: Setup ranger: command retry enables thus retrying if ranger admin is down !"
            )
        else:
            Logger.info(
                "kylin: Setup ranger: command retry not enabled thus skipping if ranger admin is down !"
            )

        if params.xa_audit_hdfs_is_enabled:
            try:
                params.HdfsResource(
                    "/ranger/audit",
                    type="directory",
                    action="create_on_execute",
                    owner=params.hdfs_user,
                    group=params.hdfs_user,
                    mode=0755,
                    recursive_chmod=True)
                params.HdfsResource(
                    "/ranger/audit/kylin",
                    type="directory",
                    action="create_on_execute",
                    owner=params.kylin_user,
                    group=params.kylin_user,
                    mode=0700,
                    recursive_chmod=True)
                params.HdfsResource(None, action="execute")
            except Exception, err:
                Logger.exception(
                    "Audit directory creation in HDFS for kylin Ranger plugin failed with error:\n{0}"
                        .format(err))

        setup_ranger_plugin(
            'kylin',
            'kylin',
            None,
            None,
            None,
            None,
            params.java64_home,
            params.repo_name,
            params.kylin_ranger_plugin_repo,
            params.ranger_env,
            params.ranger_plugin_properties,
            params.policy_user,
            params.policymgr_mgr_url,
            params.enable_ranger_kylin,
            conf_dict=params.conf_dir,
            component_user=params.kylin_user,
            component_group=params.kylin_group,
            cache_service_list=['kylin'],
            plugin_audit_properties=params.config['configurations']
            ['ranger-kylin-audit'],
            plugin_audit_attributes=params.config['configurationAttributes']
            ['ranger-kylin-audit'],
            plugin_security_properties=params.config['configurations']
            ['ranger-kylin-security'],
            plugin_security_attributes=params.config['configurationAttributes']
            ['ranger-kylin-security'],
            plugin_policymgr_ssl_properties=params.config['configurations']
            ['ranger-kylin-policymgr-ssl'],
            plugin_policymgr_ssl_attributes=params.
                config['configurationAttributes']['ranger-kylin-policymgr-ssl'],
            component_list=['kylin'],
            audit_db_is_enabled=params.xa_audit_db_is_enabled,
            credential_file=params.credential_file,
            xa_audit_db_password=params.xa_audit_db_password,
            ssl_truststore_password=params.ssl_truststore_password,
            ssl_keystore_password=params.ssl_keystore_password,
            api_version='v2',
            skip_if_rangeradmin_down=not params.retryAble,
            is_security_enabled=params.security_enabled,
            is_stack_supports_ranger_kerberos=params.
                stack_supports_ranger_kerberos,
            component_user_principal=params.kylin_kerberos_principal
            if params.security_enabled else None,
            component_user_keytab=params.kylin_kerberos_keytab
            if params.security_enabled else None)
    else:
        Logger.info('Ranger kylin plugin is not enabled')
