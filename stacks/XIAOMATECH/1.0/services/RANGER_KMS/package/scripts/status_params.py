#!/usr/bin/env python

from resource_management.libraries.script import Script
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.default import default

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

stack_name = default("/clusterLevelParams/stack_name", None)
stack_supports_pid = True
ranger_kms_pid_dir = default("/configurations/kms-env/ranger_kms_pid_dir", "/var/run/ranger_kms")
ranger_kms_pid_file = format('{ranger_kms_pid_dir}/rangerkms.pid')
