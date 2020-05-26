#!/usr/bin/env python

import ambari_simplejson as json
import base64
import urllib2
from ambari_commons.inet_utils import openurl
from ambari_commons.exceptions import TimeoutError
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger
from resource_management.libraries.functions.decorator import safe_retry
from resource_management.libraries.functions.format import format


@safe_retry(times=3, sleep_time=5, backoff_factor=1.5, err_class=Fail, return_on_fail=None)
def create_user(ranger_url, user_name, user_password, user_role, admin_username_password):
    """
    Create user in Ranger Admin
    """
    Logger.info(format("Creating {user_name} user with role as {user_role} in Ranger Admin"))
    url = format("{ranger_url}/service/xusers/secure/users")

    user = {
        'name': user_name,
        'password': user_password,
        'firstName': user_name,
        'userRoleList': [user_role],
        'status': '1'
    }

    base_64_string = base64.encodestring(admin_username_password).replace('\n', '')

    request = urllib2.Request(url, json.dumps(user))
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', format('Basic {base_64_string}'))

    try:
        result = openurl(request, timeout=20)
        response_code = result.getcode()
        if response_code == 200:
            Logger.info(format("Successfully created {user_name} user with role {user_role} in Ranger Admin"))
            return response_code
        else:
            Logger.error(format("Unable to create {user_name} user in Ranger Admin"))
            return None
    except urllib2.HTTPError as e:
        raise Fail("HTTPError while creating " + str(user_name) + " user. Reason = " + str(e.code))
    except urllib2.URLError as e:
        raise Fail("URLError while creating " + str(user_name) + " user. Reason = " + str(e.reason))
    except TimeoutError:
        raise Fail("Connection timeout error while creating " + str(user_name) + " user")
    except Exception as err:
        raise Fail(format("Error while creating {user_name} user. Reason = {err}"))


@safe_retry(times=3, sleep_time=5, backoff_factor=1.5, err_class=Fail, return_on_fail=None)
def get_user(ranger_url, user, admin_username_password):
    """
    Get user from Ranger Admin
    """
    url = format("{ranger_url}/service/xusers/users?name={user}")

    base_64_string = base64.encodestring(admin_username_password).replace('\n', '')

    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', format('Basic {base_64_string}'))

    try:
        result = openurl(request, timeout=20)
        response_code = result.getcode()
        response = json.loads(result.read())
        if response_code == 200 and len(response['vXUsers']) >= 0:
            for vxuser in response['vXUsers']:
                if vxuser['name'] == user:
                    Logger.info(format("User with username {user} exists in Ranger Admin"))
                    return vxuser
            Logger.info(format("User with username {user} doesn't exist in Ranger Admin"))
            return None
        else:
            Logger.error(format("Unable to get {user_name} user in Ranger Admin"))
            return None
    except urllib2.HTTPError as e:
        raise Fail("HTTPError while getting " + str(user) + " user. Reason = " + str(e.code))
    except urllib2.URLError as e:
        raise Fail("URLError while getting " + str(user) + " user. Reason = " + str(e.reason))
    except TimeoutError:
        raise Fail("Connection timeout error while getting " + str(user) + " user.")
    except Exception as err:
        raise Fail(format("Error while getting {user} user. Reason = {err}"))


@safe_retry(times=3, sleep_time=5, backoff_factor=1.5, err_class=Fail, return_on_fail=None)
def update_user_role(ranger_url, user_name, user_role, admin_username_password):
    """
    Updating user role by username in Ranger Admin
    """
    url = format("{ranger_url}/service/xusers/secure/users/roles/userName/{user_name}")

    role = {
        "vXStrings": [{"value": user_role}]
    }

    base_64_string = base64.encodestring(admin_username_password).replace('\n', '')

    request = urllib2.Request(url, json.dumps(role))
    request.get_method = lambda: 'PUT'
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', format('Basic {base_64_string}'))

    try:
        result = openurl(request, timeout=20)
        response_code = result.getcode()
        if response_code == 200:
            Logger.info(format("Successfully updated {user_name} user with role {user_role} in Ranger Admin"))
            return response_code
        else:
            Logger.error(format("Unable to update {user_name} user role with {user_role} in Ranger Admin"))
            return None
    except urllib2.HTTPError as e:
        raise Fail(
            "HTTPError while updating " + str(user_name) + " user role to " + str(user_role) + ". Reason = " + str(
                e.code))
    except urllib2.URLError as e:
        raise Fail(
            "URLError while updating " + str(user_name) + " user role to " + str(user_role) + ". Reason = " + str(
                e.reason))
    except TimeoutError:
        raise Fail("Connection timeout error while updating " + str(user_name) + " user role to " + str(user_role))
    except Exception as err:
        raise Fail(format("Error while updating {user_name} user role to {user_role}. Reason = {err}"))


@safe_retry(times=3, sleep_time=5, backoff_factor=1.5, err_class=Fail, return_on_fail=None)
def get_ranger_service_default_policy(ranger_url, service_name, admin_username_password,
                                      resource_list=['database', 'table', 'column']):
    """
    Get Policies by service name
    """
    url = format("{ranger_url}/service/public/v2/api/service/{service_name}/policy")

    base_64_string = base64.encodestring(admin_username_password).replace('\n', '')

    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', format('Basic {base_64_string}'))

    try:
        result = openurl(request, timeout=20)
        response_code = result.getcode()
        response = json.loads(result.read())

        if response_code == 200 and len(response) > 0:
            for policy in response:
                count = 0
                for resource in resource_list:
                    if resource in policy['resources'] and '*' in policy['resources'][resource]['values']:
                        count = count + 1
                    if count == len(resource_list):
                        Logger.info(format(
                            "Default policy exists in {service_name} in Ranger Admin for resources {resource_list}"))
                        return policy
            Logger.info(
                format("Default policy doesn't exists in {service_name} in Ranger Admin for resources {resource_list}"))
            return False
        else:
            Logger.error(format("Unable to get default policy from {service_name} service."))
            return None
    except urllib2.HTTPError as e:
        raise Fail(
            "HTTPError while getting default policy from " + str(service_name) + " service. Reason = " + str(e.code))
    except urllib2.URLError as e:
        raise Fail(
            "URLError while getting default policy from " + str(service_name) + " service. Reason = " + str(e.reason))
    except TimeoutError:
        raise Fail("Connection timeout error while getting default policy from " + str(service_name) + "service")
    except Exception as err:
        raise Fail(format("Error while getting default policy from {service_name} service. Reason = {err}"))


@safe_retry(times=3, sleep_time=5, backoff_factor=1.5, err_class=Fail, return_on_fail=None)
def update_policy(ranger_url, policy_id, policy_data, admin_username_password):
    """
    Updating policy in ranger admin using policy id
    """

    url = format("{ranger_url}/service/public/v2/api/policy/{policy_id}")

    base_64_string = base64.encodestring(admin_username_password).replace('\n', '')

    request = urllib2.Request(url, json.dumps(policy_data))
    request.get_method = lambda: 'PUT'
    request.add_header('Content-Type', 'application/json')
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', format('Basic {base_64_string}'))

    try:
        result = openurl(request, timeout=20)
        response_code = result.getcode()
        if response_code == 200:
            Logger.info(format("Successfully updated policy in Ranger Admin"))
            return response_code
        else:
            Logger.error(format("Unable to update policy in Ranger Admin"))
            return None
    except urllib2.HTTPError as e:
        raise Fail("HTTPError while updating policy Reason = " + str(e.code))
    except urllib2.URLError as e:
        raise Fail("URLError while updating policy. Reason = " + str(e.reason))
    except TimeoutError:
        raise Fail("Connection timeout error while updating policy")
    except Exception as err:
        raise Fail(format("Error while updating policy. Reason = {err}"))


def check_user_policy(policy, policy_user):
    if 'policyItems' in policy:
        policy_item = policy['policyItems']
        for item in policy_item:
            if policy_user in item['users']:
                Logger.info("User " + str(policy_user) + " exists in default policy: " + str(
                    policy['name']) + " for service: " + str(policy['service']))
                return True
    return False


def update_policy_item(policy, policy_item):
    existing_policy_item = policy['policyItems']
    existing_policy_item.append(policy_item)

    return policy
