#!/usr/bin/env python


from resource_management.core.logger import Logger
import base64
import urllib2
import ambari_simplejson as json
from resource_management.core.source import Template


class RangerPolicyUpdate:
    def create_policy_if_needed(self):
        service_name = self.get_service()
        Logger.info("Ranger Hdfs service name : {0}".format(service_name))
        if service_name:
            if self.check_if_policy_does_not_exist(service_name):
                self.create_policy(service_name)
            else:
                Logger.info("Policy already exists.")
        else:
            Logger.error("Ranger hdfs service not found")

    def get_service(self):
        try:
            url = self.ranger_url + "/service/public/v2/api/service?serviceType=hdfs"
            Logger.info("Getting ranger service name for hdfs. Url : {0}".format(url))
            request = urllib2.Request(url, None, self.headers)
            result = urllib2.urlopen(request, timeout=20)
            response_code = result.getcode()
            if response_code == 200:
                response = json.loads(result.read())
                if (len(response) > 0):
                    return response[0]['name']
                else:
                    return None

        except urllib2.HTTPError  as e:
            Logger.error(
                "Error during Ranger service authentication. Http status code - {0}. {1}".format(e.code, e.read()))
            return None

        except urllib2.URLError as  e:
            Logger.error("Error during Ranger service authentication. {0}".format(e.reason))
            return None
        except Exception as e:
            Logger.error("Error occured when connecting Ranger admin. {0} ".format(e))
            return None

    def check_if_policy_does_not_exist(self, service_name):
        try:
            url = self.ranger_url + "/service/public/v2/api/service/" + \
                  service_name + "/policy?policyName=dpprofiler-audit-read"
            Logger.info("Checking ranger policy. Url : {0}".format(url))
            request = urllib2.Request(url, None, self.headers)
            result = urllib2.urlopen(request, timeout=20)
            response_code = result.getcode()
            if response_code == 200:
                response = json.loads(result.read())
                return (len(response) == 0)

        except urllib2.HTTPError as  e:
            Logger.error(
                "Error during Ranger service authentication. Http status code - {0}. {1}".format(e.code, e.read()))
            return False

        except urllib2.URLError as e:
            Logger.error("Error during Ranger service authentication. {0}".format(e.reason))
            return False
        except Exception as e:
            Logger.error("Error occured when connecting Ranger admin. {0}".format(e))
            return False

    def create_policy(self, service_name):
        try:
            variable = {
                'ranger_audit_hdfs_path': self.ranger_audit_hdfs_path,
                'dpprofiler_user': self.dpprofiler_user,
                'service_name': service_name
            }
            self.env.set_params(variable)
            data = Template("dpprofiler_ranger_policy.json").get_content()
            url = self.ranger_url + "/service/public/v2/api/policy"
            Logger.info("Creating ranger policy. Url : {0}".format(url))
            Logger.info("data: {0}".format(data))
            request = urllib2.Request(url, data, self.headers)
            result = urllib2.urlopen(request, timeout=20)
            response_code = result.getcode()
            Logger.info("Response code for create policy : {0}".format(response_code))
            if response_code == 200:
                response = json.loads(result.read())
                return response

        except urllib2.HTTPError as e:
            Logger.error(
                "Error during Ranger service authentication. Http status code - {0}. {1}".format(e.code, e.read()))
            return None

        except urllib2.URLError as e:
            Logger.error("Error during Ranger service authentication. {0}".format(e.reason))
            return None
        except Exception as e:
            Logger.error("Error occured when connecting Ranger admin. {0}".format(e))
            return None

    def __init__(self, ranger_url, username, password, ranger_audit_hdfs_path, dpprofiler_user, env):
        self.ranger_url = ranger_url
        self.ranger_audit_hdfs_path = ranger_audit_hdfs_path
        self.dpprofiler_user = dpprofiler_user
        self.env = env
        username_password = '{0}:{1}'.format(username, password)
        base_64_string = base64.encodestring(username_password).replace('\n', '')
        self.headers = {"Content-Type": "application/json", "Accept": "application/json", \
                        "Authorization": "Basic {0}".format(base_64_string)}
