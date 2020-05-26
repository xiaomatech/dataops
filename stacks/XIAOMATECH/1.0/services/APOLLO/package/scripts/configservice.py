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
        [params.pid_dir, params.log_dir, params.conf_dir + '/configservice'],
        owner=params.apollo_user,
        group=params.user_group,
        mode=0755,
        create_parents=True)

    if not os.path.exists(
            Script.get_stack_root() + '/' + params.version_dir_configservice) or not os.path.exists(
                params.install_dir_configservice):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_configservice)
        Execute('rm -rf %s' % params.install_dir_configservice)
        Execute('/bin/rm -f /tmp/' + params.filename_configservice)
        Execute(
            'wget ' + params.download_url_configservice + ' -O /tmp/' + params.filename_configservice,
            user=params.apollo_user)
        Execute('unzip /tmp/' + params.filename_configservice + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_configservice + ' ' +
                params.install_dir_configservice)
        Execute('cp -r ' + params.install_dir_configservice + '/config/* ' +
                params.conf_dir + '/configservice')
        Execute('rm -rf ' + params.install_dir_configservice + '/config')
        Execute('ln -s ' + params.conf_dir + '/configservice' + ' ' +
                params.install_dir_configservice + '/config')
        Execute(
            'chown -R %s:%s %s/%s' % (params.apollo_user, params.user_group,
                                      Script.get_stack_root(),params.version_dir_configservice))
        Execute('chown -R %s:%s %s' % (params.apollo_user, params.user_group,
                                       params.install_dir_configservice))


class apollo(Script):
    pid_file = '/var/run/apollo_configservice.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_apollo()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/configservice/application-github.properties',
            content=InlineTemplate(params.configservice_conf_content),
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
        Execute(params.install_dir_configservice + "/startup.sh")
        Execute(
            "echo `ps aux|grep 'apollo-configservice' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    apollo().execute()
