#!/usr/bin/env python
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.default import default
import os
import random

# server configurations
config = Script.get_config()

service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

stack_log = config['configurations']['openldap-config']['stack.log']

ldap_adminuser = config['configurations']['openldap-config']['ldap.adminuser']

ldap_domain = config['configurations']['openldap-config']['ldap.domain']

ldap_password = config['configurations']['openldap-config']['ldap.password']

ldap_ldifdir = service_packagedir + '/scripts/ldifs'

ldap_ou = config['configurations']['openldap-config']['ldap.ou']

binddn = config['configurations']['openldap-config']['binddn']
people_dn = config['configurations']['openldap-config']['people_dn']
kdc_realm = default('configurations/krb5-config/kdc.realm', 'example.com')
ldap_kerberos_container_dn = default(
    'configurations/krb5-config/ldap_kerberos_container_dn',
    'cn=krbContainer,ou=Kerberos,dc=example,dc=com')
ldap_kdc_dn = default('configurations/krb5-config/ldap_kdc_dn',
                      'cn=kdc-srv,ou=Control,dc=example,dc=com')
ldap_kadmind_dn = default('configurations/krb5-config/ldap_kadmind_dn',
                          'cn=kdc-adm,ou=Control,dc=example,dc=com')

ldap_hosts = default('clusterHostInfo/openldap_master_hosts', [])
ldap_master_host = ldap_hosts[random.randint(0, len(ldap_hosts) - 1)]
ldap_hosts_dict = {}

hostname = config['agentLevelParams']['hostname']
ldap_hosts = sorted(ldap_hosts)
map(lambda x: ldap_hosts_dict.setdefault(x[1], x[0] + 1),
    list(enumerate(ldap_hosts)))

server_id = ldap_hosts_dict.get(hostname) or 1

other_host = ldap_hosts[-(len(ldap_hosts) - server_id)]
