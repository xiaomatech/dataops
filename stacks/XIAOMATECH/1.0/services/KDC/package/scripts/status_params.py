#!/usr/bin/env python
from resource_management import *

config = Script.get_config()

#kdc_piddir = config['configurations']['krb5-env']['kdc.piddir']
#kdc_pidfile = format("{kdc_piddir}/kdc-env.pid")
krb5_template_config = config['configurations']['krb5-env']['content']
