#!/usr/bin/env python

import base64
import ssl
import urllib2
from resource_management.core.logger import Logger

redirect_codes = {307, 303, 302}


class AtlasRequestHandler:
    def __init__(self, url_list, atlas_username, atlas_password, timeout=50):
        username_password = '{0}:{1}'.format(atlas_username, atlas_password)
        base_64_string = base64.encodestring(username_password).replace('\n', '')
        self.headers = {"Content-Type": "application/json", "Accept": "application/json", \
                        "Authorization": "Basic {0}".format(base_64_string)}
        self.url_list = url_list
        self.timeout = timeout

    def handle_request(self, api_endpoint, payload=None, is_put=False):
        for url in self.url_list:
            try:
                Logger.info("Trying to connect to Atlas at  {}".format(url))
                request = urllib2.Request(url + api_endpoint, payload, self.headers)
                request_context = None
                if url.startswith("https"):
                    request_context = ssl._create_unverified_context()
                if is_put:
                    request.get_method = lambda: 'PUT'
                result = urllib2.urlopen(request, timeout=self.timeout, context=request_context)
                if result.code not in redirect_codes:
                    return result.code, result.read()
                else:
                    Logger.info("Received redirect code {} from {}".format(result.code, url))

            except urllib2.HTTPError as e:
                Logger.error("HTTP Error while handling the request - {0}. {1}".format(e.code, e.read()))
                if e.code not in redirect_codes:
                    return e.code, e.read()
                else:
                    Logger.info("Received redirect code {} from {}".format(e.code, url))

            except urllib2.URLError as e:
                Logger.error("URL Error {0} while handling request. Trying another URL".format(e.reason))

            except Exception  as e:
                Logger.error("Got Exception {0} while handling the request. Trying another URL".format(e))

        return None, None
