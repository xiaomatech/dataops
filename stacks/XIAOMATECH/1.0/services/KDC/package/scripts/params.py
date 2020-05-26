#!/usr/bin/env python
from resource_management import *
from resource_management.libraries.functions import default
# server configurations
config = Script.get_config()

kdc_realm = config['configurations']['krb5-config']['kdc.realm']
kdc_domain = config['configurations']['krb5-config']['kdc.domain']
ldap_kerberos_container_dn = config['configurations']['krb5-config'][
    'ldap_kerberos_container_dn']
ldap_kdc_dn = config['configurations']['krb5-config']['ldap_kdc_dn']
ldap_kadmind_dn = config['configurations']['krb5-config']['ldap_kadmind_dn']
kdc_admin = config['configurations']['krb5-config']['kdc.admin']
kdc_adminpassword = config['configurations']['krb5-config'][
    'kdc.adminpassword']

ldap_password = config['configurations']['openldap-config']['ldap.password']
binddn = config['configurations']['openldap-config']['binddn']

clusterHostInfo = config['clusterHostInfo']
kdc_host = str(clusterHostInfo['krb5_master_hosts'][0])

kdc_hosts = clusterHostInfo['krb5_master_hosts']
ldap_hosts = default('clusterHostInfo/openldap_master_hosts', [])
ldap_url = ['ldap://' + item + '/' for item in ldap_hosts]
ldap_hosts = ' '.join(ldap_url)
