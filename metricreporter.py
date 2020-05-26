import requests
import json
import socket
from time import time
from pprint import pprint


class MetricsReporter(object):
    PATH = "/ws/v1/timeline/metrics"
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, url_base, metricname, appid):
        self.url_base = url_base
        self.metricname = metricname
        self.appid = appid
        self.hostname = None
        self.url = url_base + self.PATH
        self.value = None
        self.response = None
        self.metrics_jso = None
        self.metrics_dict = {
            "metrics": []
        }
        self.metrics = []

    def post(self):
        '''
        Obtain metric, build dictionary, convert to json and send POST request
        '''
        value = self.calculate_metric()
        self.generate_metrics_dict(value)
        self.response = requests.post(self.url,
                                      data=self.metrics_jso,
                                      headers=self.HEADERS)
        return self.response

    def set_metricname(self, metricname):
        self.metricname = metricname

    def set_appid(self, appid):
        self.appid = appid

    def set_hostname(self, hostname):
        self.hostname = hostname

    def calculate_metric(self):
        '''
        Here the logic is implemented
        returns: numeric value (int, float,...)
        '''
        pass

    def generate_metrics_dict(self, value):
        '''
        Build the dictionary, that will eventually be posted as JSON
        and print it.
        '''
        ts_now = int(time() * 1000)
        metric = {}
        metric["timestamp"] = ts_now
        metric["metricname"] = self.metricname
        metric["appid"] = self.appid
        if self.hostname:
            metric["hostname"] = self.hostname or socket.getfqdn()
        metric["starttime"] = ts_now
        metric["metrics"] = {
            str(ts_now): value
        }
        self.metrics.append(metric)
        self.metrics_dict["metrics"] = self.metrics
        pprint(self.metrics_dict)
        self.metrics_jso = json.dumps(self.metrics_dict)

    def get_response(self):
        return self.response


class GenericMetricsReporter(MetricsReporter):
    '''
    Give the MetricsReporter a function that obtains the value and report it
    to AMS.
    Example: ms = GenericMetricsReporter(url, )
    '''

    def __init__(self, url_base, metricname, appid, obtain_metric):
        MetricsReporter.__init__(self, url_base, metricname, appid)
        if not callable(obtain_metric):
            raise Exception("Parameter obtain_metric must be callable.")
        self.obtain_metric = obtain_metric

    def calculate_metric(self):
        '''
        Call function and return value
        '''
        return self.obtain_metric()


class RESTMetricsReporter(MetricsReporter):
    '''
    Get a metric from a REST call to a service
    '''

    def __init__(self, url_base, metricname, appid, source_url, json_key):
        MetricsReporter.__init__(self, url_base, metricname, appid)
        self.source_url = source_url
        self.json_key = json_key

    def set_source_url(self):
        self.source_url = self.source_url

    def set_json_key(self):
        self.json_key = self.json_key

    def calculate_metric(self):
        '''
        Do a REST call evaluate the response and obtain a value to store as metric.
        '''
        response = requests.get(self.source_url)
        if response.status_code == 200:
            json = response.json()
            return json[self.json_key]
        else:
            raise Exception("No value could be obtained from response!")
