from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.source import StaticFile
import os


def install_azkaban():
    import params
    Directory([params.conf_dir, params.log_dir],
              owner=params.azkaban_user,
              group=params.user_group,
              mode=0755,
              create_parents=True)

    File('/tmp/azkaban.sql', content=StaticFile("azkaban.sql"), mode=0755)
    File(
        params.install_dir +
        '/lib/azkaban-ldap-usermanager-1.2.1-SNAPSHOT.jar',
        content=StaticFile("azkaban-ldap-usermanager-1.2.1-SNAPSHOT.jar"),
        mode=0755)

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.azkaban_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('ln -s ' + params.log_dir + ' ' + params.install_dir +
                '/logs/azkaban')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/azkaban_web.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.azkaban_user, params.user_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.azkaban_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)

        Execute('mysql -h' + params.db_host + ' -u' + params.db_user + ' -p' +
                params.db_password + ' azkaban </tmp/azkaban.sql')


class WebServer(Script):
    pid_file = ''

    def install(self, env):
        install_azkaban()

    def stop(self, env):
        import params
        Execute(params.install_dir + '/bin/shutdown-web.sh')

    def start(self, env):
        import params
        self.configure(env)
        Execute(params.install_dir + '/bin/start-web.sh')
        Execute(
            "echo `ps aux|grep 'azkaban-web' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/azkaban.properties',
            content=InlineTemplate(params.azkaban_web_properties),
            mode=0755,
            owner=params.azkaban_user,
            group=params.user_group)
        File(
            params.conf_dir + '/azkaban-users.xml',
            content=InlineTemplate(params.azkaban_users),
            mode=0755,
            owner=params.azkaban_user,
            group=params.user_group)
        File(
            params.conf_dir + '/global.properties',
            content=InlineTemplate(params.global_properties),
            mode=0755,
            owner=params.azkaban_user,
            group=params.user_group)
        File(
            params.conf_dir + '/log4j.properties',
            content=InlineTemplate(params.log4j_properties),
            mode=0755,
            owner=params.azkaban_user,
            group=params.user_group)


if __name__ == '__main__':
    WebServer().execute()
