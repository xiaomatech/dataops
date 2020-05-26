from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.source import StaticFile
import os


def install_apollo():
    import params
    Directory([params.pid_dir, params.log_dir, params.conf_dir + '/portal'],
              owner=params.apollo_user,
              group=params.user_group,
              mode=0755,
              create_parents=True)

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir_portal
                          ) or not os.path.exists(params.install_dir_portal):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_portal)
        Execute('rm -rf %s' % params.install_dir_portal)
        Execute('/bin/rm -f /tmp/' + params.filename_portal)
        Execute(
            'wget ' + params.download_url_portal + ' -O /tmp/' +
            params.filename_portal,
            user=params.apollo_user)
        Execute('unzip /tmp/' + params.filename_portal + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_portal + ' ' +
                params.install_dir_portal)
        Execute('cp -r ' + params.install_dir_portal + '/config/* ' +
                params.conf_dir + '/portal')
        Execute('rm -rf ' + params.install_dir_portal + '/config')
        Execute('ln -s ' + params.conf_dir + '/portal' + ' ' +
                params.install_dir_portal + '/config')
        Execute(
            'chown -R %s:%s %s/%s' % (params.apollo_user, params.user_group,
                                      Script.get_stack_root(),params.version_dir_portal))
        Execute('chown -R %s:%s %s' % (params.apollo_user, params.user_group,
                                       params.install_dir_portal))


class apollo(Script):
    pid_file = '/var/run/apollo_portal.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_apollo()
        File(
            '/tmp/apolloportaldb.sql',
            content=StaticFile("apolloportaldb.sql"),
            mode=0755)
        Execute('mysql -u' + params.db_user + ' -p' + params.db_password +
                ' -DApolloConfigDB</tmp/apolloportaldb.sql')

        File(
            '/tmp/apolloconfigdb.sql',
            content=StaticFile("apolloconfigdb.sql"),
            mode=0755)
        Execute('mysql -h' + params.db_host + ' -u' + params.db_user + ' -p' +
                params.db_password +
                ' ApolloConfigDB_test</tmp/apolloconfigdb.sql')
        Execute('mysql -h' + params.db_host + ' -u' + params.db_user + ' -p' +
                params.db_password +
                ' ApolloConfigDB_pro</tmp/apolloconfigdb.sql')
        Execute('mysql -h' + params.db_host + ' -u' + params.db_user + ' -p' +
                params.db_password +
                ' ApolloConfigDB_uat</tmp/apolloconfigdb.sql')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/portal/application-github.properties',
            content=InlineTemplate(params.portal_conf_content),
            mode=0755,
            owner=params.apollo_user,
            group=params.user_group)
        File(
            params.conf_dir + '/portal/apollo-env.properties',
            content=InlineTemplate(params.env_conf_content),
            mode=0755,
            owner=params.apollo_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + self.pid_file + '`')

    def start(self, env):
        import params
        env.set_params(params)
        install_apollo()
        self.configure(env)
        Execute(params.install_dir_portal + "/startup.sh")
        Execute(
            "echo `ps aux|grep 'apollo-portal' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    apollo().execute()
