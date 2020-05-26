from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_apollo():
    import params
    Directory(
        [params.pid_dir, params.log_dir, params.conf_dir + '/adminservice'],
        owner=params.apollo_user,
        group=params.user_group,
        mode=0755,
        create_parents=True)

    if not os.path.exists(
            Script.get_stack_root() + '/' + params.version_dir_adminservice) or not os.path.exists(
                params.install_dir_adminservice):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_adminservice)
        Execute('rm -rf %s' % params.install_dir_adminservice)
        Execute('/bin/rm -f /tmp/' + params.filename_adminservice)
        Execute(
            'wget ' + params.download_url_adminservice + ' -O /tmp/' + params.filename_adminservice,
            user=params.apollo_user)
        Execute('unzip /tmp/' + params.filename_adminservice + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_adminservice + ' ' +
                params.install_dir_adminservice)
        Execute('cp -r ' + params.install_dir_adminservice + '/config/* ' +
                params.conf_dir + '/adminservice')
        Execute('rm -rf ' + params.install_dir_adminservice + '/config')
        Execute('ln -s ' + params.conf_dir + '/adminservice' + ' ' +
                params.install_dir_adminservice + '/config')
        Execute(
            'chown -R %s:%s %s/%s' % (params.apollo_user, params.user_group,
                                      Script.get_stack_root(),params.version_dir_adminservice))
        Execute('chown -R %s:%s %s' % (params.apollo_user, params.user_group,
                                       params.install_dir_adminservice))


class apollo(Script):
    pid_file = '/var/run/apollo_adminservice.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_apollo()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/adminservice/application-github.properties',
            content=InlineTemplate(params.adminservice_conf_content),
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
        Execute(params.install_dir_adminservice + "/startup.sh")
        Execute(
            "echo `ps aux|grep 'apollo-adminservice' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    apollo().execute()
