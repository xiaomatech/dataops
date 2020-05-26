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

import urllib2
import httplib
import nifi_toolkit_util_common
from resource_management.core import shell

from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script

from ambari_commons.inet_utils import openurl
from ambari_commons.exceptions import TimeoutError
from resource_management.core.exceptions import Fail
from resource_management.core.resources import File
from resource_management.libraries.functions.decorator import retry


class NifiServiceCheck(Script):
    def service_check(self, env):
        import params
        Logger.info("Running Nifi service check")
        urls = []

        for nifi_master_host in params.nifi_master_hosts:
            if params.nifi_ssl_enabled:
                urls.append("https://{0}:{1}".format(
                    nifi_master_host, params.nifi_node_ssl_port))
            else:
                urls.append("http://{0}:{1}".format(nifi_master_host,
                                                    params.nifi_node_port))

        if params.stack_support_admin_toolkit:
            NifiServiceCheck.check_nifi_portal_with_toolkit(
                urls, params.jdk64_home, params.nifi_install_dir,
                params.nifi_bootstrap_file, params.toolkit_tmp_dir,
                params.stack_version_buildnum)
        else:
            for url in urls:
                Logger.info("Checking Nifi portal {0} status".format(url))
                NifiServiceCheck.check_nifi_portal_with_python(url + "/nifi")

    @staticmethod
    @retry(
        times=30,
        sleep_time=5,
        max_sleep_time=20,
        backoff_factor=2,
        err_class=Fail)
    def check_nifi_portal_with_python(url):
        try:
            request = urllib2.Request(url)
            result = openurl(request, timeout=20)
            response_code = result.getcode()
            if response_code == 200 or response_code == 401:
                Logger.info("Nifi portal {0} is up. Response code {1}".format(
                    url, response_code))
            else:
                raise Fail("Error connecting to {0}. Response code {1}".format(
                    url, response_code))
        except urllib2.URLError, e:
            if isinstance(e, urllib2.HTTPError):
                if e.code == 401:
                    Logger.info(
                        "Nifi portal {0} is up. Response code {1}".format(
                            url, e.code))
                else:
                    raise Fail(
                        "Error connecting to {0}. Http status code - {1}. \n {2}"
                        .format(url, e.code, e.read()))
            elif e.reason and "violation of protocol" in str(e.reason):
                Logger.info("Ignore certificate validation error - {0}".format(
                    e.reason))
                pass
            else:
                raise Fail("Error connecting to {0}. Reason - {1}.".format(
                    url, e.reason))
        except httplib.BadStatusLine:
            raise Fail(
                "Error connecting to {0}. Reason - Not Reachable".format(url))
        except TimeoutError:
            raise Fail("Error connecting to {0}. Reason - Timeout".format(url))

    @staticmethod
    @retry(
        times=30,
        sleep_time=5,
        max_sleep_time=20,
        backoff_factor=2,
        err_class=Fail)
    def check_nifi_portal_with_toolkit(urls, jdk64_home, nifi_dir,
                                       nifi_bootstrap, toolkit_tmp_dir,
                                       stack_version_buildnum):

        node_manager_script = nifi_toolkit_util_common.get_toolkit_script(
            'node-manager.sh', toolkit_tmp_dir, stack_version_buildnum)
        File(node_manager_script, mode=0755)
        command = 'ambari-sudo.sh JAVA_HOME=' + jdk64_home + ' ' + node_manager_script + ' -d ' + nifi_dir + ' -b ' + nifi_bootstrap + ' -o status -u "' + ','.join(
            urls) + '"'
        code, out = shell.call(command, quiet=True, logoutput=False)

        if code > 0:
            raise Fail(
                "Call to admin-toolkit encountered error: {0}".format(out))
        else:
            if out.find('did not complete due to exception') > -1:
                raise Fail("Error connecting to one or more nifi nodes: {0}".
                           format(out))


class NifiRegistryServiceCheck(Script):
    def service_check(self, env):
        import params
        Logger.info("Running Nifi Registry service check")

        url = "http://{0}:{1}".format(params.nifi_registry_host,
                                      params.nifi_registry_port)

        if params.nifi_registry_ssl_enabled:
            url = "https://{0}:{1}".format(params.nifi_registry_host,
                                           params.nifi_registry_ssl_port)

        Logger.info("Checking Nifi Registry portal {0} status".format(url))
        if params.nifi_registry_ssl_enabled:
            NifiRegistryServiceCheck.check_nifi_registry_portal_with_toolkit(
                url, params.jdk64_home, params.nifi_registry_install_dir,
                params.nifi_registry_bootstrap_file, params.toolkit_tmp_dir,
                params.stack_version_buildnum)
        else:
            NifiRegistryServiceCheck.check_nifi_registry_portal_with_python(
                url + "/nifi-registry")

    @staticmethod
    @retry(
        times=30,
        sleep_time=5,
        max_sleep_time=20,
        backoff_factor=2,
        err_class=Fail)
    def check_nifi_registry_portal_with_python(url):
        try:
            request = urllib2.Request(url)
            result = openurl(request, timeout=20)
            response_code = result.getcode()
            if response_code == 200 or response_code == 401:
                Logger.info(
                    "Nifi Registry portal {0} is up. Response code {1}".format(
                        url, response_code))
            else:
                raise Fail("Error connecting to {0}. Response code {1}".format(
                    url, response_code))
        except urllib2.URLError, e:
            if isinstance(e, urllib2.HTTPError):
                if e.code == 401:
                    Logger.info(
                        "Nifi Registry portal {0} is up. Response code {1}".
                        format(url, e.code))
                else:
                    raise Fail(
                        "Error connecting to {0}. Http status code - {1}. \n {2}"
                        .format(url, e.code, e.read()))
            elif e.reason and "violation of protocol" in str(e.reason):
                Logger.info("Ignore certificate validation error - {0}".format(
                    e.reason))
                pass
            else:
                raise Fail("Error connecting to {0}. Reason - {1}.".format(
                    url, e.reason))
        except httplib.BadStatusLine:
            raise Fail(
                "Error connecting to {0}. Reason - Not Reachable".format(url))
        except TimeoutError:
            raise Fail("Error connecting to {0}. Reason - Timeout".format(url))

    @staticmethod
    @retry(
        times=30,
        sleep_time=5,
        max_sleep_time=20,
        backoff_factor=2,
        err_class=Fail)
    def check_nifi_registry_portal_with_toolkit(
            url, jdk64_home, nifi_registry_dir, nifi_registry_bootstrap,
            toolkit_tmp_dir, stack_version_buildnum):
        Logger.info("Checking Nifi Registry portal with toolkit")

        tls_toolkit_script = nifi_toolkit_util_common.get_toolkit_script(
            'tls-toolkit.sh', toolkit_tmp_dir, stack_version_buildnum)
        File(tls_toolkit_script, mode=0755)

        nifi_registry_props_file = nifi_registry_dir + '/conf/nifi-registry.properties'

        nifi_registry_props = NifiRegistryServiceCheck.convert_properties_to_dict(
            jdk64_home, nifi_registry_props_file, nifi_registry_bootstrap,
            toolkit_tmp_dir, stack_version_buildnum)

        if len(nifi_registry_props) == 0:
            raise Fail('Unable to read properties from {0}'.format(
                nifi_registry_props_file))
        else:
            keystore = nifi_registry_props['nifi.registry.security.keystore']
            keystoreType = nifi_registry_props[
                'nifi.registry.security.keystoreType']
            keystorePasswd = nifi_registry_props[
                'nifi.registry.security.keystorePasswd']
            keyPasswd = nifi_registry_props['nifi.registry.security.keyPasswd']
            truststore = nifi_registry_props[
                'nifi.registry.security.truststore']
            truststoreType = nifi_registry_props[
                'nifi.registry.security.truststoreType']
            truststorePasswd = nifi_registry_props[
                'nifi.registry.security.truststorePasswd']

            command = 'ambari-sudo.sh JAVA_HOME=' + jdk64_home + ' ' + tls_toolkit_script + ' status -u ' + url + ' -ks ' + keystore + ' -kst ' + keystoreType + ' -ksp ' + keystorePasswd + ' -kp ' + keyPasswd + ' -ts ' + truststore + ' -tst ' + truststoreType + ' -tsp ' + truststorePasswd

            # Only uncomment for debugging, otherwise the passwords will get logged
            # Logger.info("Executing: " + command)

            code, out = shell.call(command, quiet=True, logoutput=False)

            if code > 0:
                raise Fail(
                    "Call to tls-toolkit encountered error: {0}".format(out))
            else:
                if out.find('Error communicating with') > -1:
                    raise Fail(
                        "Error connecting to NiFi Registry: {0}".format(out))

    @staticmethod
    def convert_properties_to_dict(jdk64_home, nifi_registry_props_file,
                                   nifi_registry_bootstrap, toolkit_tmp_dir,
                                   stack_version_buildnum):
        dict = {}
        if sudo.path_isfile(nifi_registry_props_file):
            encrypt_tool_script = nifi_toolkit_util_common.get_toolkit_script(
                'encrypt-config.sh', toolkit_tmp_dir, stack_version_buildnum)
            File(encrypt_tool_script, mode=0755)

            command = 'ambari-sudo.sh JAVA_HOME=' + jdk64_home + ' ' + encrypt_tool_script + ' --nifiRegistry --decrypt -r ' + nifi_registry_props_file + ' -b ' + nifi_registry_bootstrap
            code, out = shell.call(command, quiet=True, logoutput=False)

            lines = out.split('\n')
            for line in lines:
                props = line.rstrip().split('=')
                if len(props) == 2:
                    dict[props[0]] = props[1]
                elif len(props) == 1:
                    dict[props[0]] = ''
        return dict


if __name__ == "__main__":
    NifiServiceCheck().execute()
