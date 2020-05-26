# encoding=utf8
from resource_management import *
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import InlineTemplate, Template
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.logger import Logger
from resource_management.libraries.script.script import Script


def kdc_nginx_conf():
    import params
    kdc_hosts = params.kdc_hosts
    upstream = ''
    for kdc_host in kdc_hosts:
        upstream += 'server ' + kdc_host + ':88;\n        '

    nginx_conf = '''
user  nginx;
worker_processes  auto;
worker_rlimit_nofile 1048576;

error_log  /var/log/nginx/error.log debug;
pid        /var/run/nginx.pid;


events {
    worker_connections  65535;
}

stream {
    log_format proxy '$remote_addr [$time_local] '
                 '$protocol $status $bytes_sent $bytes_received '
                 '$session_time "$upstream_addr" '
                 '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
    access_log  /var/log/nginx/access.log proxy buffer=32k;

    open_log_file_cache max=1000 inactive=20s valid=1m min_uses=2;

    upstream kdc {
        hash $remote_addr consistent;
        %s
    }

    server {
        listen 81 backlog=16384;
        proxy_timeout 3s;
        proxy_pass kdc;
    }

    server {
        listen 81 udp;
        proxy_timeout 3s;
        proxy_pass kdc;
    }
}
        ''' % upstream
    File(
        format("/etc/nginx/nginx.conf"),
        content=nginx_conf,
        owner='nginx',
        group='nginx',
        mode=0644)


class Master(Script):
    def install(self, env):
        # Install packages listed in metainfo.xml
        self.install_packages(env)
        self.configure(env)
        import params

        Execute('echo "' + params.ldap_password + '" > passwd.txt')
        Execute('echo k5 >> passwd.txt')
        Execute('echo k5 >> passwd.txt')
        Execute('echo >> passwd.txt')
        try:
            Execute('kdb5_ldap_util -D ' + params.ldap_kadmind_dn +
                    ' -H ldapi:// create -r ' + params.kdc_realm +
                    ' -s< passwd.txt')
        except Exception as e:
            print(str(e))
        Execute('rm passwd.txt')

        Execute('echo "' + params.ldap_password + '" > passwd.txt')
        Execute('echo "' + params.ldap_password + '" >> passwd.txt')
        Execute('echo "' + params.ldap_password + '" >> passwd.txt')
        Execute('echo >> passwd.txt')
        Execute('kdb5_ldap_util -D ' + params.binddn +
                ' stashsrvpw -f /var/kerberos/krb5kdc/service.keyfile ' +
                params.ldap_kdc_dn + '< passwd.txt')
        Execute('kdb5_ldap_util -D ' + params.binddn +
                ' stashsrvpw -f /var/kerberos/krb5kdc/service.keyfile ' +
                params.ldap_kadmind_dn + '< passwd.txt')

        Execute('rm passwd.txt')

        Execute('service krb5kdc start')
        Execute('service kadmin start')

        Execute('chkconfig krb5kdc on')
        Execute('chkconfig kadmin on')

        Execute('echo "' + params.kdc_adminpassword + '" > passwd.txt')
        Execute('echo "' + params.kdc_adminpassword + '" >> passwd.txt')
        Execute('echo >> passwd.txt')
        Execute('kadmin.local -q "addprinc ' + params.kdc_admin +
                '" < passwd.txt')
        Execute('rm passwd.txt')

        Execute('echo "*/admin@' + params.kdc_realm +
                ' *" > /var/kerberos/krb5kdc/kadm5.acl')
        Execute("echo 'KRB5KDC_ARGS= -w 64'> /etc/sysconfig/krb5kdc")
        Execute('yum install -y nginx')
        kdc_nginx_conf()
        Execute('chkconfig nginx on')
        Execute('service nginx start')

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)

        content = InlineTemplate(status_params.krb5_template_config)
        File(
            format("/etc/krb5.conf"),
            content=content,
            owner='root',
            group='root',
            mode=0644)

        kdc_content = Template('kdc.conf.j2')

        File(
            format("/var/kerberos/krb5kdc/kdc.conf"),
            content=kdc_content,
            owner='root',
            group='root',
            mode=0644)

    def stop(self, env):
        self.configure(env)
        Logger.info(u"KDC不能stop stop后会导致授权不对!!!")
        Execute('service krb5kdc stop')
        Execute('service kadmin stop')

    def start(self, env):
        self.configure(env)

        Execute('service krb5kdc start')
        Execute('service kadmin start')

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status('/var/run/krb5kdc.pid')


if __name__ == "__main__":
    Master().execute()
