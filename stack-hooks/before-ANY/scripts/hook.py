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

from resource_management import *
from shared_initialization import *
from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.hook import Hook
from resource_management.libraries.functions import default
from random import shuffle
import os
base_lock_dir = '/var/lock/'


def install_packages():
    lock_file = base_lock_dir + '/install_packages'
    if not os.path.exists(lock_file):
        packages = [
            'tar', 'curl', 'wget', 'java-1.8.0-openjdk-devel','java-11-openjdk-devel', 'bzip2-libs', 'snappy',
            'lzo', 'zlib', 'lz4', 'libzstd', 'libisal', 'openssl-libs',
            'openssh-ldap', 'authconfig', 'openldap-clients', 'nss-pam-ldapd',
            'pam_krb5', 'sssd-ldap', 'nscd', 'numactl'
        ]
        Package(packages)
        Execute(" chkconfig nslcd on")
        Execute(" chkconfig nscd on")
        Execute('yum remove -y postfix mariadb-libs mariadb')
        Execute(" echo 1 > " + lock_file)


def ldap_client_conf():
    lock_file = base_lock_dir + '/install_ldap'
    if not os.path.exists(lock_file):
        ldap_url = ''
        basedn = default('openldap-config/ldap.domain', 'dc=example,dc=com')
        ldap_hosts = default('clusterHostInfo/openldap_master_hosts', [])
        ldap_hosts_input = default('configurations/zookeeper-env/ldap_hosts', '')
        if ldap_hosts_input.strip() != '':
            ldap_hosts = ldap_hosts_input.split(' ')
            ldap_url = ['ldap://' + item + '/' for item in ldap_hosts]
        elif len(ldap_hosts) > 0:
            ldap_url = ['ldap://' + item + '/' for item in ldap_hosts]
        if len(ldap_url) > 0:
            ldap_url = ' '.join(ldap_url)
            shuffle(ldap_url)
            Execute("mkdir -p /etc/openldap/cacerts")
            Execute(
                '/usr/sbin/authconfig --enablemkhomedir --enableshadow --useshadow --enablelocauthorize --enableldap --enableldapauth --ldapserver="'
                + ldap_url + '" --ldapbasedn="' + basedn + '" --update')
        Execute("echo 'threads 1' >>/etc/nslcd.conf")
        Execute("systemctl restart nslcd nscd")
        Execute(" echo 1 > " + lock_file)


def install_repo():
    import params
    repo_file = '/etc/yum.repos.d/hadoop.repo'
    if not os.path.exists(repo_file):
        Execute('rm -rf /etc/yum.repos.d/*')
        Execute('wget ' + params.download_url_base + '/hadoop.repo -O ' + repo_file)


def ln_jvmso():
    jvm_so_file = '/usr/lib/libjvm.so'
    if not os.path.exists(jvm_so_file):
        if os.path.exists('/etc/alternatives/jre/lib/amd64/server/libjvm.so'):
            Execute('ln -s /etc/alternatives/jre/lib/amd64/server/libjvm.so ' +
                    jvm_so_file)
        elif os.path.exists('/etc/alternatives/jre/lib/server/libjvm.so'):
            Execute('ln -s /etc/alternatives/jre/lib/server/libjvm.so ' +
                    jvm_so_file)


def ln_crypto():
    crypto_so_file = '/usr/lib64/libcrypto.so'
    if not os.path.exists(crypto_so_file):
        Execute('ln -s /usr/lib64/libssl.so.10 ' + crypto_so_file)


class BeforeAnyHook(Hook):
    def hook(self, env):
        import params
        env.set_params(params)
        Package(['wget'])
        install_repo()
        install_packages()
        ln_jvmso()
        ln_crypto()
        ldap_client_conf()
        setup_users()
        if params.has_namenode:
            setup_hadoop_env()
        setup_java()


if __name__ == "__main__":
    BeforeAnyHook().execute()
