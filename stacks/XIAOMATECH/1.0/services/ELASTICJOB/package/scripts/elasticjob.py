import os
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status


def install_elasticjob():
    import params
    Directory([params.conf_dir],
              owner=params.elasticjob_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.elasticjob_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir +
                ' && rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute(
            'chown -R %s:%s %s/%s' % (params.elasticjob_user,
                                        params.user_group,params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.elasticjob_user,
                                       params.user_group, params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


class elasticjob(Script):
    pid_file = '/var/run/elasticjob.pid'

    def install(self, env):
        import params
        env.set_params(params)
        install_elasticjob()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/elasticjob-env.sh',
            owner=params.elasticjob_user,
            content=InlineTemplate(params.env_template))

        File(
            params.conf_dir + '/elasticjob.conf',
            owner=params.elasticjob_user,
            content=InlineTemplate(params.conf_template),
            mode=0755)

    def start(self, env):
        import params
        env.set_params(params)
        install_elasticjob()
        self.configure(env)
        Execute(
            'source ' + params.conf_dir + '/elasticjob-env.sh;' +
            params.install_dir + "/bin/start.sh",
            user=params.elasticjob_user)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(
            'source ' + params.conf_dir + '/elasticjob-env.sh;' +
            params.install_dir + "/bin/stop.sh",
            user=params.elasticjob_user)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    elasticjob().execute()
