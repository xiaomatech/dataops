from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_pika():
    import params
    Directory([
        params.pid_dir, params.log_dir, params.conf_dir, params.db_dir,
        params.dump_dir
    ],
              owner=params.pika_user,
              group=params.pika_group,
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.pika_user)
        Execute('tar -jxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s %s/output %s ' % (params.stack_root,params.version_dir))
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('mkdir ' + params.install_dir + '/log && chmod 777 ' +
                params.install_dir + '/log')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/pika.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.pika_user, params.pika_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.pika_user, params.pika_group,
                                       params.install_dir))


class Pika(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_pika()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/pika.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.pika_user,
            group=params.pika_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + "/bin/pika -c " + params.conf_dir +
                '/pika.conf')

    def start(self, env):
        import params
        env.set_params(params)
        install_pika()
        self.configure(env)
        Execute('kill -9 `cat ' + params.pid_file + '`')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    Pika().execute()
