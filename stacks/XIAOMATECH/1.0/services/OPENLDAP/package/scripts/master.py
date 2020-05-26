# encoding=utf8

import sys, os, pwd, signal, time
from resource_management import *
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import InlineTemplate, Template, StaticFile
from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import format


class Master(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)
        import params

        File(
            '/etc/openldap/schema/cisco.schema',
            mode=0755,
            content=StaticFile('cisco.schema'))
        File(
            '/etc/openldap/schema/tacacs.schema',
            mode=0755,
            content=StaticFile('tacacs.schema'))
        File(
            '/etc/openldap/schema/radius.schema',
            mode=0755,
            content=StaticFile('radius.schema'))
        File(
            '/etc/openldap/schema/dnsdomain2.schema',
            mode=0755,
            content=StaticFile('dnsdomain2.schema'))
        File(
            '/etc/openldap/schema/public_key.schema',
            mode=0755,
            content=StaticFile('public_key.schema'))

        File(
            '/etc/httpd/conf.d/self-service-password.conf',
            mode=0755,
            content=StaticFile('self-service-password.conf'))

        setup_file = '/usr/sbin/ldap_setup.sh'
        File(setup_file, mode=0755, content=StaticFile('setup.sh'))

        Execute('echo Running /usr/sbin/ldap_setup.sh')

        # run setup script which has simple shell setup
        Execute(setup_file + ' ' + params.ldap_password + ' ' +
                params.ldap_adminuser + ' ' + params.ldap_domain + ' ' +
                params.ldap_ldifdir + ' ' + params.ldap_ou + ' "' +
                params.binddn + '" >> ' + params.stack_log)

    def configure(self, env):
        import params
        env.set_params(params)

        content = Template('slapd.j2')
        File(
            format("/etc/openldap/slapd.conf"),
            content=content,
            owner='root',
            group='root',
            mode=0644)
        Execute('chkconfig slapd on')

    def stop(self, env):
        Execute(
            "sed -i 's/#mirrormode  on/mirrormode  on/g' /etc/openldap/slapd.conf"
        )
        Execute('service slapd stop')

    def start(self, env):
        self.configure(env)
        Execute('service slapd start')

    def status(self, env):
        Execute('service slapd status')


if __name__ == "__main__":
    Master().execute()
