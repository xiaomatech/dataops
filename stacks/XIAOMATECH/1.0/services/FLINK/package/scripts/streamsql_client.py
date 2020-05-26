from resource_management import *
from resource_management.core.resources.system import Execute
from resource_management.core.exceptions import ClientComponentHasNoStatus
import os
from resource_management.libraries.script.script import Script


def install_flinksql():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' +
                          params.streamsql_version_dir) or not os.path.exists(
                              params.streamsql_install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.streamsql_version_dir)
        Execute(
            'rm -rf %s' % params.streamsql_install_dir, ignore_failures=True)
        Execute(
            'wget ' + params.streamsql_download_url + ' -O /tmp/' +
            params.streamsql_filename,
            user=params.flink_user)
        Execute('tar -zxf /tmp/' + params.streamsql_filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.streamsql_version_dir + ' ' +
                params.streamsql_install_dir)
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/streamsql.sh" %
                params.streamsql_install_dir)
        Execute(
            'chown -R %s:%s %s/%s' % (params.flink_user, params.flink_group,params.stack_root,params.streamsql_version_dir))
        Execute('chown -R %s:%s %s' % (params.flink_user, params.flink_group,
                                       params.streamsql_install_dir))
        Execute('/bin/rm -f /tmp/' + params.streamsql_filename)


class Client(Script):
    def install(self, env):
        install_flinksql()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)

    def stop(self, env):
        self.configure(env)

    def start(self, env):
        install_flinksql()
        self.configure(env)

    def status(self, env):
        raise ClientComponentHasNoStatus()


if __name__ == "__main__":
    Client().execute()
