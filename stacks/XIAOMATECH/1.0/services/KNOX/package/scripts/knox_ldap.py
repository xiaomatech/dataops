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
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


def ldap():
    import params

    File(
        os.path.join(params.knox_conf_dir, 'ldap-log4j.properties'),
        mode=params.mode,
        group=params.knox_group,
        owner=params.knox_user,
        content=InlineTemplate(params.ldap_log4j))

    File(
        os.path.join(params.knox_conf_dir, 'users.ldif'),
        mode=params.mode,
        group=params.knox_group,
        owner=params.knox_user,
        content=params.users_ldif)
