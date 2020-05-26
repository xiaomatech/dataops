from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.copy_tarball import copy_to_hdfs

import os


def install_dbus():
    import params
    Directory([params.pid_dir, params.log_dir, params.conf_dir],
              owner=params.dbus_user,
              group=params.dbus_group,
              mode=0755,
              create_parents=True)

    params.HdfsResource(
        '/user/dbus',
        type="directory",
        action="create_on_execute",
        owner=params.dbus_user,
        mode=0755)
    params.HdfsResource(
        '/dbus',
        type="directory",
        action="create_on_execute",
        owner=params.dbus_user,
        mode=0755)
    params.HdfsResource(None, action="execute")

    # copy_to_hdfs(
    #     "udf",
    #     params.user_group,
    #     params.hdfs_user,
    #     custom_src_file = '',
    #     custom_dest_file='/dbus/udf/abc.jar',
    #     replace_existing_files=True)

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.dbus_user)
        Execute('tar -jxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute('rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/dbus.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.dbus_user, params.dbus_group,params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.dbus_user, params.dbus_group,
                                       params.install_dir))


class dbus(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_dbus()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/application.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.dbus_user,
            group=params.dbus_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + params.pid_file + '`')

    def start(self, env):
        import params
        env.set_params(params)
        install_dbus()
        self.configure(env)
        Execute("")
        Execute(
            "echo `ps aux|grep 'edp.rider.RiderStarter' | grep -v grep | awk '{print $2}'` > "
            + params.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        import os
        if not os.path.exists(params.pid_file):
            Execute(
                "echo `ps aux|grep 'edp.rider.RiderStarter' | grep -v grep | awk '{print $2}'` > "
                + params.pid_file)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    dbus().execute()
