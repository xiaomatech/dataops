from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_canal():
    import params
    Directory([params.conf_dir, params.log_dir],
              owner=params.canal_user,
              group=params.user_group,
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.canal_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('ln -s ' + params.log_dir + ' ' + params.install_dir +
                '/logs/canal')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/canal.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.canal_user, params.user_group,params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.canal_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


class Canal(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_canal()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("{conf_dir}/canal.properties"),
            owner=params.canal_user,
            group=params.canal_group,
            mode=0644,
            content=InlineTemplate(params.canal_properties_content))
        File(
            format("{conf_dir}/kafka.yaml"),
            owner=params.canal_user,
            group=params.canal_group,
            mode=0644,
            content=InlineTemplate(params.kafka_content))
        File(
            format("{conf_dir}/{instance_name}/instance.properties"),
            owner=params.canal_user,
            group=params.canal_group,
            mode=0644,
            content=InlineTemplate(params.instance_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('source ' + params.conf_dir + '/canal-env.sh;' +
                params.install_dir + "/bin/stop.sh")

    def start(self, env):
        import params
        env.set_params(params)
        install_canal()
        self.configure(env)
        Execute('source ' + params.conf_dir + '/canal-env.sh;' +
                params.install_dir + "/bin/startup.sh")

    def status(self, env):
        import params
        check_process_status(params.canal_pid_file)


if __name__ == "__main__":
    Canal().execute()
