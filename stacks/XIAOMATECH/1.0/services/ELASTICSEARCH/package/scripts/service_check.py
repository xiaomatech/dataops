#!/usr/bin/env python

from __future__ import print_function

import subprocess
import sys

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        doc = '{"name": "Ambari Smoke test"}'
        index = "ambari_smoke_test"

        print("Running Elastic search service check", file=sys.stdout)

        # Make sure the service is actually up.  We can live without everything allocated.
        # Need both the retry and ES timeout.  Can hit the URL before ES is ready at all and get no response, but can
        # also hit ES before things are green.
        host = "localhost:9200"
        Execute(
            "curl -XGET 'http://%s/_cluster/health?wait_for_status=green&timeout=120s'"
            % host,
            logoutput=True,
            tries=6,
            try_sleep=20)

        # Put a document into a new index.

        Execute(
            "curl -XPUT '%s/%s/test/1' -d '%s'" % (host, index, doc),
            logoutput=True)

        # Retrieve the document.  Use subprocess because we actually need the results here.
        cmd_retrieve = "curl -XGET '%s/%s/test/1'" % (host, index)
        proc = subprocess.Popen(
            cmd_retrieve,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        (stdout, stderr) = proc.communicate()
        response_retrieve = stdout
        print("Retrieval response is: %s" % response_retrieve)
        expected_retrieve = '{"_index":"%s","_type":"test","_id":"1","_version":1,"found":true,"_source":%s}' \
                            % (index, doc)

        # Delete the index
        cmd_delete = "curl -XDELETE '%s/%s'" % (host, index)
        proc = subprocess.Popen(
            cmd_delete,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        (stdout, stderr) = proc.communicate()
        response_delete = stdout
        print("Delete index response is: %s" % response_retrieve)
        expected_delete = '{"acknowledged":true}'

        if (expected_retrieve == response_retrieve) and (
                expected_delete == response_delete):
            print("Smoke test able to communicate with Elasticsearch")
        else:
            print("Elasticsearch service unable to retrieve document.")
            sys.exit(1)

        exit(0)


if __name__ == "__main__":
    ServiceCheck().execute()
