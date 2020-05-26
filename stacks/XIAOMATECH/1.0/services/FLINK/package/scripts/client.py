from resource_management import *

from resource_management.core.resources.system import Directory, File, Link
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Execute
from resource_management.core.exceptions import ClientComponentHasNoStatus
import os
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.format import format


def install_flink():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir, ignore_failures=True)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.flink_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('mkdir ' + params.install_dir + '/logs && chmod 777 ' +
                params.install_dir + '/logs')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/flink.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.flink_user, params.flink_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.flink_user, params.flink_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)

        params.HdfsResource(
            '/flink/ha',
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755,
            dfs_type=params.dfs_type)
        params.HdfsResource(
            '/flink/completed-jobs',
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755,
            dfs_type=params.dfs_type)
        params.HdfsResource(
            '/flink/checkpoints',
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755,
            dfs_type=params.dfs_type)
        params.HdfsResource(
            '/flink/savepoints',
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755,
            dfs_type=params.dfs_type)
        params.HdfsResource(None, action="execute")

        params.HdfsResource(
            params.flink_dir,
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755)
        params.HdfsResource(
            params.flink_checkpoints_dir,
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755)
        params.HdfsResource(
            params.flink_recovery_dir,
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755)
        params.HdfsResource(
            params.flink_savepoint_dir,
            type="directory",
            action="create_on_execute",
            owner=params.flink_user,
            mode=0755)
        params.HdfsResource(None, action="execute")


def config_flink():
    import params
    Directory(params.mounts, owner=params.flink_user, group=params.flink_group)
    Directory([params.flink_pid_dir, params.flink_log_dir, params.conf_dir, '/data/flink'],
              owner=params.flink_user,
              group=params.flink_group)
    File(
        format("{conf_dir}/flink-conf.yaml"),
        content=InlineTemplate(params.flink_yaml_content),
        owner=params.flink_user)
    File(
        format("{conf_dir}/masters"),
        content=InlineTemplate(params.flink_master_hosts_str),
        owner=params.flink_user)
    File(
        format("{conf_dir}/slaves"),
        content=InlineTemplate(params.flink_slave_hosts_str),
        owner=params.flink_user)


class Client(Script):
    def install(self, env):
        install_flink()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        config_flink()

    def stop(self, env):
        self.configure(env)

    def start(self, env):
        install_flink()
        self.configure(env)

    def status(self, env):
        raise ClientComponentHasNoStatus()


if __name__ == "__main__":
    Client().execute()
