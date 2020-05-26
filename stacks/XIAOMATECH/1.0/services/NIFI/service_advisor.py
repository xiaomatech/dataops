#!/usr/bin/env ambari-python-wrap
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
import os
import imp
import traceback
from os.path import dirname
from ambari_server.serverConfiguration import get_ambari_properties, get_ambari_version

SCRIPT_DIR = dirname(os.path.abspath(__file__))
STACKS_DIR = os.path.join(SCRIPT_DIR, '../../../../')
PARENT_FILE = os.path.join(STACKS_DIR, 'service_advisor.py')

try:
    with open(PARENT_FILE, 'rb') as fp:
        service_advisor = imp.load_module('service_advisor', fp, PARENT_FILE,
                                          ('.py', 'rb', imp.PY_SOURCE))
except Exception as e:
    traceback.print_exc()
    print "Failed to load parent"


class NIFI100ServiceAdvisor(service_advisor.ServiceAdvisor):
    def __init__(self, *args, **kwargs):
        self.as_super = super(NIFI100ServiceAdvisor, self)
        self.as_super.__init__(*args, **kwargs)

    def getSiteProperties(self, configurations, siteName):
        siteConfig = configurations.get(siteName)
        if siteConfig is None:
            return None
        return siteConfig.get("properties")

    def getServicesSiteProperties(self, services, siteName):
        configurations = services.get("configurations")
        if not configurations:
            return None
        siteConfig = configurations.get(siteName)
        if siteConfig is None:
            return None
        return siteConfig.get("properties")

    def __find_ca(self, services):
        for service in services['services']:
            if 'components' in service:
                for component in service['components']:
                    stackServiceComponent = component['StackServiceComponents']
                    if 'NIFI_CA' == stackServiceComponent[
                            'component_name'] and stackServiceComponent[
                                'hostnames']:
                        return True
        return False

    def getServiceComponentLayoutValidations(self, services, hosts):
        items = super(NIFI100ServiceAdvisor,
                      self).getServiceComponentLayoutValidations(
                          services, hosts)
        return items

    def getServiceConfigurationRecommendations(self, configurations,
                                               clusterData, services, hosts):
        nifi = self.getServicesSiteProperties(services, "nifi")

        if "ranger-env" in services["configurations"] and "ranger-nifi-plugin-properties" in services[
            "configurations"] and \
                "ranger-nifi-plugin-enabled" in services["configurations"]["ranger-env"]["properties"]:
            putNiFiRangerPluginProperty = self.putProperty(
                configurations, "ranger-nifi-plugin-properties", services)
            rangerEnvNiFiPluginProperty = services["configurations"][
                "ranger-env"]["properties"]["ranger-nifi-plugin-enabled"]
            putNiFiRangerPluginProperty("ranger-nifi-plugin-enabled",
                                        rangerEnvNiFiPluginProperty)

            if rangerEnvNiFiPluginProperty == 'Yes' and \
                    "nifi.authentication" in services["configurations"]["ranger-nifi-plugin-properties"][
                "properties"] and \
                    "nifi.node.ssl.isenabled" in services["configurations"]["nifi-ambari-ssl-config"]["properties"]:
                nifiAmbariSSLConfig = 'SSL' if services["configurations"][
                    "nifi-ambari-ssl-config"]["properties"][
                        "nifi.node.ssl.isenabled"] == 'true' else 'NONE'
                putNiFiRangerPluginProperty("nifi.authentication",
                                            nifiAmbariSSLConfig)

        # Recommend Ranger supported service's audit properties
        ranger_audit_dict = [{
            'filename':
            'ranger-env',
            'configname':
            'xasecure.audit.destination.solr',
            'target_configname':
            'xasecure.audit.destination.solr'
        },
                             {
                                 'filename':
                                 'ranger-env',
                                 'configname':
                                 'xasecure.audit.destination.hdfs',
                                 'target_configname':
                                 'xasecure.audit.destination.hdfs'
                             },
                             {
                                 'filename':
                                 'ranger-env',
                                 'configname':
                                 'xasecure.audit.destination.hdfs.dir',
                                 'target_configname':
                                 'xasecure.audit.destination.hdfs.dir'
                             },
                             {
                                 'filename':
                                 'ranger-admin-site',
                                 'configname':
                                 'ranger.audit.solr.urls',
                                 'target_configname':
                                 'xasecure.audit.destination.solr.urls'
                             },
                             {
                                 'filename':
                                 'ranger-admin-site',
                                 'configname':
                                 'ranger.audit.solr.zookeepers',
                                 'target_configname':
                                 'xasecure.audit.destination.solr.zookeepers'
                             }]

        for item in ranger_audit_dict:
            if item['filename'] in services['configurations'] and item['configname'] in \
                    services['configurations'][item['filename']]['properties']:
                if item['filename'] in configurations and item[
                        'configname'] in configurations[
                            item['filename']]['properties']:
                    rangerAuditProperty = configurations[
                        item['filename']]['properties'][item['configname']]
                else:
                    rangerAuditProperty = services['configurations'][
                        item['filename']]['properties'][item['configname']]
                putNifiRangerAuditProperty = self.putProperty(
                    configurations, "ranger-nifi-audit", services)
                putNifiRangerAuditProperty(item['target_configname'],
                                           rangerAuditProperty)

        if 'ranger-admin-site' in services['configurations'] and 'ranger.plugins.nifi.serviceuser' in \
                services['configurations']['ranger-admin-site']['properties']:
            nifi_user = services['configurations']['nifi-env']['properties'][
                'nifi_user']
            putRangerAdminSiteProperty = self.putProperty(
                configurations, "ranger-admin-site", services)
            putRangerAdminSiteProperty("ranger.plugins.nifi.serviceuser",
                                       nifi_user)

        properties = get_ambari_properties()
        ambari_version = get_ambari_version(properties)
        if not (ambari_version) or not (ambari_version.startswith('2.5')):
            putNiFiLogSearchConfAttribute = self.putPropertyAttribute(
                configurations, "nifi-logsearch-conf")
            putNiFiLogSearchConfAttribute('service_name', 'visible', 'false')
            putNiFiLogSearchConfAttribute('component_mappings', 'visible',
                                          'false')
            putNiFiLogSearchConfAttribute('content', 'visible', 'false')

    def validateConfigurationsForSite(self, configurations,
                                      recommendedDefaults, services, hosts,
                                      siteName, method):
        properties = self.getSiteProperties(configurations, siteName)
        if properties:
            if siteName == 'nifi-ambari-ssl-config' or siteName == 'nifi-ambari-config':
                return method(properties, None, configurations, services,
                              hosts)
            else:
                return super(NIFI100ServiceAdvisor,
                             self).validateConfigurationsForSite(
                                 configurations, recommendedDefaults, services,
                                 hosts, siteName, method)
        else:
            return []

    def validateNiFiSslProperties(self, properties, recommendedDefaults,
                                  configurations, services, hosts):
        validationItems = []
        ssl_enabled = properties['nifi.node.ssl.isenabled'] and str(
            properties['nifi.node.ssl.isenabled']).lower() != 'false'
        if ssl_enabled and not properties['nifi.initial.admin.identity']:
            validationItems.append({
                "config-name":
                'nifi.initial.admin.identity',
                'item':
                self.getWarnItem(
                    'If SSL is enabled, Initial Admin Identity should usually be configured to a DN that an admin will have a certificate for.'
                )
            })
        if (self.__find_ca(services)):
            if not properties['nifi.toolkit.tls.token']:
                validationItems.append({
                    "config-name":
                    'nifi.toolkit.tls.token',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is used, nifi.toolkit.tls.token must be set'
                    )
                })
            if not ssl_enabled:
                validationItems.append({
                    "config-name":
                    'nifi.node.ssl.isenabled',
                    'item':
                    self.getWarnItem(
                        'For NiFi Certificate Authority to be useful, ssl should be enabled'
                    )
                })
        else:
            if properties['nifi.toolkit.tls.token']:
                validationItems.append({
                    "config-name":
                    'nifi.toolkit.tls.token',
                    'item':
                    self.getWarnItem(
                        "If NiFi Certificate Authority is not used, nifi.toolkit.tls.token doesn't do anything."
                    )
                })
            if ssl_enabled:
                if not properties['nifi.security.keystorePasswd']:
                    validationItems.append({
                        "config-name":
                        'nifi.security.keystorePasswd',
                        'item':
                        self.getErrorItem(
                            'If NiFi Certificate Authority is not used and SSL is enabled, must specify nifi.security.keystorePasswd'
                        )
                    })
                if not properties['nifi.security.keyPasswd']:
                    validationItems.append({
                        "config-name":
                        'nifi.security.keyPasswd',
                        'item':
                        self.getErrorItem(
                            'If NiFi Certificate Authority is not used and SSL is enabled, must specify nifi.security.keyPasswd'
                        )
                    })
                if not properties['nifi.security.truststorePasswd']:
                    validationItems.append({
                        "config-name":
                        'nifi.security.truststorePasswd',
                        'item':
                        self.getErrorItem(
                            'If NiFi Certificate Authority is not used and SSL is enabled, must specify nifi.security.truststorePasswd'
                        )
                    })
                if not properties['nifi.security.keystoreType']:
                    validationItems.append({
                        "config-name":
                        'nifi.security.keystoreType',
                        'item':
                        self.getErrorItem(
                            'If NiFi Certificate Authority is not used and SSL is enabled, must specify nifi.security.keystoreType'
                        )
                    })
                if not properties['nifi.security.truststoreType']:
                    validationItems.append({
                        "config-name":
                        'nifi.security.truststoreType',
                        'item':
                        self.getErrorItem(
                            'If NiFi Certificate Authority is not used and SSL is enabled, must specify nifi.security.truststoreType'
                        )
                    })
        return self.toConfigurationValidationProblems(
            validationItems, "nifi-ambari-ssl-config")

    def validateNiFiAmbariConfigurations(self, properties, recommendedDefaults,
                                         configurations, services, hosts):
        validationItems = []

        if len(properties['nifi.sensitive.props.key']) < 10:
            validationItems.append({
                "config-name":
                'nifi.sensitive.props.key',
                'item':
                self.getWarnItem(
                    'Sensitive property encryption password should be 10 or more characters'
                )
            })

        return self.toConfigurationValidationProblems(validationItems,
                                                      "nifi-ambari-config")

    def validateNiFiRangerPluginConfigurations(
            self, properties, recommendedDefaults, configurations, services,
            hosts):
        validationItems = []
        ranger_plugin_properties = self.getSiteProperties(
            configurations, "ranger-nifi-plugin-properties")
        ranger_plugin_enabled = ranger_plugin_properties[
            'ranger-nifi-plugin-enabled'] if ranger_plugin_properties else 'No'

        if ranger_plugin_enabled.lower() == 'yes':
            ranger_env = self.getServicesSiteProperties(services, 'ranger-env')
            if not ranger_env or not 'ranger-nifi-plugin-enabled' in ranger_env or \
                    ranger_env['ranger-nifi-plugin-enabled'].lower() != 'yes':
                validationItems.append({
                    "config-name":
                    'ranger-nifi-plugin-enabled',
                    "item":
                    self.getWarnItem(
                        "ranger-nifi-plugin-properties/ranger-nifi-plugin-enabled must correspond ranger-env/ranger-nifi-plugin-enabled"
                    )
                })

        return self.toConfigurationValidationProblems(
            validationItems, "ranger-nifi-plugin-properties")

    def getServiceConfigurationsValidationItems(
            self, configurations, recommendedDefaults, services, hosts):
        siteName = "nifi-ambari-config"
        method = self.validateNiFiAmbariConfigurations
        items = self.validateConfigurationsForSite(
            configurations, recommendedDefaults, services, hosts, siteName,
            method)

        siteName = "ranger-nifi-plugin-properties"
        method = self.validateNiFiRangerPluginConfigurations
        items.extend(
            self.validateConfigurationsForSite(configurations,
                                               recommendedDefaults, services,
                                               hosts, siteName, method))

        siteName = "nifi-ambari-ssl-config"
        method = self.validateNiFiSslProperties
        items.extend(
            self.validateConfigurationsForSite(configurations,
                                               recommendedDefaults, services,
                                               hosts, siteName, method))

        return items


class NIFI110ServiceAdvisor(service_advisor.NIFI100ServiceAdvisor):
    def validateNiFiAmbariConfigurations(self, properties, recommendedDefaults,
                                         configurations, services, hosts):
        parentValidationProblems = super(
            NIFI110ServiceAdvisor, self).validateNiFiAmbariConfigurations(
                properties, recommendedDefaults, configurations, services,
                hosts)

        validationItems = []

        if 'nifi.security.encrypt.configuration.password' in properties and len(
                properties['nifi.security.encrypt.configuration.password']
        ) < 12:
            validationItems.append({
                "config-name":
                'nifi.security.encrypt.configuration.password',
                'item':
                self.getErrorItem(
                    'The password for encrypting configuration settings must be 12 or more characters.'
                )
            })

        validationProblems = self.toConfigurationValidationProblems(
            validationItems, "nifi-ambari-config")
        validationProblems.extend(parentValidationProblems)

        return validationProblems


class NIFI170ServiceAdvisor(service_advisor.NIFI110ServiceAdvisor):
    def validateNiFiAmbariConfigurations(self, properties, recommendedDefaults,
                                         configurations, services, hosts):

        parentValidationProblems = super(
            NIFI170ServiceAdvisor, self).validateNiFiAmbariConfigurations(
                properties, recommendedDefaults, configurations, services,
                hosts)

        validationItems = []

        if 'nifi.allow.explicit.keytab' in properties and properties[
                'nifi.allow.explicit.keytab'] == 'true':
            validationItems.append({
                "config-name":
                'nifi.allow.explicit.keytab',
                'item':
                self.getWarnItem(
                    'NiFi is currently set to "true" to allow explicit configuration of keytabs on processors. Please consider changing this value to false to force use of the Keytab controller for enhanced security.'
                )
            })

        validationProblems = self.toConfigurationValidationProblems(
            validationItems, "nifi-ambari-config")
        validationProblems.extend(parentValidationProblems)

        return validationProblems

    def validateNiFiSslProperties(self, properties, recommendedDefaults,
                                  configurations, services, hosts):

        parentValidationProblems = super(NIFI170ServiceAdvisor,
                                         self).validateNiFiSslProperties(
                                             properties, recommendedDefaults,
                                             configurations, services, hosts)

        validationItems = []
        ssl_enabled = properties['nifi.node.ssl.isenabled'] and str(
            properties['nifi.node.ssl.isenabled']).lower() != 'false'
        if properties['nifi.toolkit.tls.token'] and ssl_enabled and len(
                properties['nifi.toolkit.tls.token']) < 16:
            validationItems.append({
                "config-name":
                'nifi.toolkit.tls.token',
                'item':
                self.getErrorItem(
                    'The NiFi CA token must be 16 or more characters.')
            })

        validationProblems = self.toConfigurationValidationProblems(
            validationItems, "nifi-ambari-ssl-config")
        validationProblems.extend(parentValidationProblems)

        return validationProblems


class NIFI_REGISTRY010ServiceAdvisor(service_advisor.ServiceAdvisor):
    def __init__(self, *args, **kwargs):
        self.as_super = super(NIFI_REGISTRY010ServiceAdvisor, self)
        self.as_super.__init__(*args, **kwargs)
        Logger.initialize_logger()

    def getServiceConfigurationRecommenderDict(self):
        """
        Recommend configurations to set. NiFi Registry does not have any recommendations in this version.
        """
        Logger.info(
            "Class: %s, Method: %s. Recommending Service Configurations." %
            (self.__class__.__name__, inspect.stack()[0][3]))
        return self.as_super.getServiceConfigurationRecommenderDict()

    def getServiceConfigurationValidators(self):
        """
        Get a list of errors. NiFi Registry does not have any validations in this version.
        """
        Logger.info(
            "Class: %s, Method: %s. Validating Service Component Layout." %
            (self.__class__.__name__, inspect.stack()[0][3]))
        return self.as_super.getServiceConfigurationValidators()

    def recommendConfigurations(self, configurations, clusterData, services,
                                hosts):
        """
        Recommend configurations for this service.
        """
        Logger.info(
            "Class: %s, Method: %s. Recommending Service Configurations." %
            (self.__class__.__name__, inspect.stack()[0][3]))
        pass

    def getServiceConfigurationRecommendations(self, configurations,
                                               clusterData, services, hosts):
        Logger.info(
            "Class: %s, Method: %s. get Service Configurations Recommendations. "
            % (self.__class__.__name__, inspect.stack()[0][3]))

    def getServiceConfigurationsValidationItems(
            self, configurations, recommendedDefaults, services, hosts):
        Logger.info(
            "Class: %s, Method: %s. Validating Service Configuration Items." %
            (self.__class__.__name__, inspect.stack()[0][3]))

        siteName = "nifi-registry-ambari-ssl-config"
        method = self.validateNiFiRegistrySslProperties
        items = self.validateConfigurationsForSite(
            configurations, recommendedDefaults, services, hosts, siteName,
            method)

        siteName = "nifi-registry-ambari-config"
        method = self.validateNiFiRegistryAmbariConfigurations
        items.extend(
            self.validateConfigurationsForSite(configurations,
                                               recommendedDefaults, services,
                                               hosts, siteName, method))

        return items

    def getCardinalitiesDict(self, hosts):
        return {'NIFI_REGISTRY_MASTER': {"min": 1}}

    def putPropertyAttribute(self, config, configType):
        if configType not in config:
            config[configType] = {}

        def appendPropertyAttribute(key, attribute, attributeValue):
            if "property_attributes" not in config[configType]:
                if "property_attributes" not in config[configType]:
                    config[configType]["property_attributes"] = {}
            if key not in config[configType]["property_attributes"]:
                config[configType]["property_attributes"][key] = {}
            config[configType]["property_attributes"][key][
                attribute] = attributeValue if isinstance(
                    attributeValue, list) else str(attributeValue)

        return appendPropertyAttribute

    def validateConfigurationsForSite(self, configurations,
                                      recommendedDefaults, services, hosts,
                                      siteName, method):
        properties = self.getSiteProperties(configurations, siteName)
        if properties:
            if siteName == 'nifi-registry-ambari-ssl-config' or siteName == 'nifi-registry-ambari-config':
                return method(properties, None, configurations, services,
                              hosts)
            else:
                return super(NIFI_REGISTRY010ServiceAdvisor,
                             self).validateConfigurationsForSite(
                                 configurations, recommendedDefaults, services,
                                 hosts, siteName, method)
        else:
            return []

    def validateNiFiRegistryAmbariConfigurations(
            self, properties, recommendedDefaults, configurations, services,
            hosts):
        validationItems = []

        if 'nifi.registry.security.encrypt.configuration.password' in properties and len(
                properties[
                    'nifi.registry.security.encrypt.configuration.password']
        ) < 12:
            validationItems.append({
                "config-name":
                'nifi.registry.security.encrypt.configuration.password',
                'item':
                self.getErrorItem(
                    'The password for encrypting configuration settings must be 12 or more characters.'
                )
            })

        return self.toConfigurationValidationProblems(
            validationItems, "nifi-registry-ambari-config")

    def validateNiFiRegistrySslProperties(self, properties,
                                          recommendedDefaults, configurations,
                                          services, hosts):
        validationItems = []

        ssl_enabled = properties['nifi.registry.ssl.isenabled'] and str(
            properties['nifi.registry.ssl.isenabled']).lower() != 'false'
        initial_admin = properties['nifi.registry.initial.admin.identity']

        Logger.info("Validating nifi-registry-ambari-ssl-config")

        if ssl_enabled and not initial_admin:
            validationItems.append({
                "config-name":
                'nifi.registry.initial.admin.identity',
                'item':
                self.getWarnItem(
                    'If SSL is enabled, Initial Admin Identity should usually be configured to a DN that an admin will have a certificate for.'
                )
            })

        if ssl_enabled and not self.__find_ca(services):
            if not properties['nifi.registry.security.keystorePasswd']:
                validationItems.append({
                    "config-name":
                    'nifi.registry.security.keystorePasswd',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is not installed and SSL is enabled, must specify nifi.security.keystorePasswd'
                    )
                })
            if not properties['nifi.registry.security.keyPasswd']:
                validationItems.append({
                    "config-name":
                    'nifi.registry.security.keyPasswd',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is not installed and SSL is enabled, must specify nifi.security.keyPasswd'
                    )
                })
            if not properties['nifi.registry.security.truststorePasswd']:
                validationItems.append({
                    "config-name":
                    'nifi.registry.security.truststorePasswd',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is not installed and SSL is enabled, must specify nifi.security.truststorePasswd'
                    )
                })
            if not properties['nifi.registry.security.keystoreType']:
                validationItems.append({
                    "config-name":
                    'nifi.registry.security.keystoreType',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is not installed and SSL is enabled, must specify nifi.security.keystoreType'
                    )
                })
            if not properties['nifi.registry.security.truststoreType']:
                validationItems.append({
                    "config-name":
                    'nifi.registry.security.truststoreType',
                    'item':
                    self.getErrorItem(
                        'If NiFi Certificate Authority is not installed and SSL is enabled, must specify nifi.security.truststoreType'
                    )
                })

        return self.toConfigurationValidationProblems(
            validationItems, "nifi-registry-ambari-ssl-config")

    def __find_ca(self, services):
        for service in services['services']:
            if 'components' in service:
                for component in service['components']:
                    stackServiceComponent = component['StackServiceComponents']
                    if 'NIFI_CA' == stackServiceComponent[
                            'component_name'] and stackServiceComponent[
                                'hostnames']:
                        return True
        return False
