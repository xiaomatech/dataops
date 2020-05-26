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

Ambari Agent

"""
import os
from resource_management.libraries.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.resources.execute_hadoop import ExecuteHadoop
from resource_management.libraries.functions import format
from resource_management.core.resources.system import File, Execute


class TezServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        path_to_tez_jar = format(params.tez_examples_jar)
        wordcount_command = format(
            "jar {path_to_tez_jar} orderedwordcount /tmp/tezsmokeinput/sample-tez-test /tmp/tezsmokeoutput/"
        )
        test_command = format("fs -test -e /tmp/tezsmokeoutput/_SUCCESS")

        File(
            format("{tmp_dir}/sample-tez-test"),
            content="foo\nbar\nfoo\nbar\nfoo",
            mode=0755)

        params.HdfsResource(
            "/tmp/tezsmokeoutput",
            action="delete_on_execute",
            type="directory")

        params.HdfsResource(
            "/tmp/tezsmokeinput",
            action="create_on_execute",
            type="directory",
            owner=params.smokeuser,
        )
        params.HdfsResource(
            "/tmp/tezsmokeinput/sample-tez-test",
            action="create_on_execute",
            type="file",
            owner=params.smokeuser,
            source=format("{tmp_dir}/sample-tez-test"),
        )

        params.HdfsResource(None, action="execute")

        if params.security_enabled:
            kinit_cmd = format(
                "{kinit_path_local} -kt {smoke_user_keytab} {smokeuser_principal};"
            )
            Execute(kinit_cmd, user=params.smokeuser)

        ExecuteHadoop(
            wordcount_command,
            tries=3,
            try_sleep=5,
            user=params.smokeuser,
            conf_dir=params.hadoop_conf_dir,
            bin_dir=params.hadoop_bin_dir)

        ExecuteHadoop(
            test_command,
            tries=10,
            try_sleep=6,
            user=params.smokeuser,
            conf_dir=params.hadoop_conf_dir,
            bin_dir=params.hadoop_bin_dir)


if __name__ == "__main__":
    TezServiceCheck().execute()
