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
import sys
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.execute_hadoop import ExecuteHadoop
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import Execute, File
from resource_management.core.source import StaticFile
from resource_management.core.logger import Logger


class MapReduce2ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        jar_path = format(
            "{hadoop_mapred2_jar_location}/{hadoopMapredExamplesJarName}")
        input_file = format("/user/{smokeuser}/mapredsmokeinput")
        output_file = format("/user/{smokeuser}/mapredsmokeoutput")

        test_cmd = format("fs -test -e {output_file}")
        run_wordcount_job = format(
            "jar {jar_path} wordcount {input_file} {output_file}")

        params.HdfsResource(
            format("/user/{smokeuser}"),
            type="directory",
            action="create_on_execute",
            owner=params.smokeuser,
            mode=params.smoke_hdfs_user_mode,
        )
        params.HdfsResource(
            output_file,
            action="delete_on_execute",
            type="directory",
            dfs_type=params.dfs_type,
        )

        test_file = params.mapred2_service_check_test_file
        if not os.path.isfile(test_file):
            try:
                Execute(
                    format(
                        "dd if=/dev/urandom of={test_file} count=1 bs=1024"))
            except:
                try:
                    Execute(format("rm {test_file}"))  #clean up
                except:
                    pass
                test_file = "/etc/passwd"

        params.HdfsResource(
            input_file,
            action="create_on_execute",
            type="file",
            source=test_file,
            dfs_type=params.dfs_type,
        )
        params.HdfsResource(None, action="execute")

        # initialize the ticket
        if params.security_enabled:
            kinit_cmd = format(
                "{kinit_path_local} -kt {smoke_user_keytab} {smokeuser_principal};"
            )
            Execute(kinit_cmd, user=params.smokeuser)

        ExecuteHadoop(
            run_wordcount_job,
            tries=1,
            try_sleep=5,
            user=params.smokeuser,
            bin_dir=params.execute_path,
            conf_dir=params.hadoop_conf_dir,
            logoutput=True)

        # the ticket may have expired, so re-initialize
        if params.security_enabled:
            kinit_cmd = format(
                "{kinit_path_local} -kt {smoke_user_keytab} {smokeuser_principal};"
            )
            Execute(kinit_cmd, user=params.smokeuser)

        ExecuteHadoop(
            test_cmd,
            user=params.smokeuser,
            bin_dir=params.execute_path,
            conf_dir=params.hadoop_conf_dir)


if __name__ == "__main__":
    MapReduce2ServiceCheck().execute()
