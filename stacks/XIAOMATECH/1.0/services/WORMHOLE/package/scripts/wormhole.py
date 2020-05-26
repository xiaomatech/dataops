from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_wormhole():
    import params
    Directory([params.pid_dir, params.log_dir, params.conf_dir],
              owner=params.wormhole_user,
              group=params.wormhole_group,
              mode=0755,
              create_parents=True)
    params.HdfsResource(
        '/user/wormhole',
        type="directory",
        action="create_on_execute",
        owner=params.wormhole_user,
        mode=0755)
    params.HdfsResource(
        '/wormhole',
        type="directory",
        action="create_on_execute",
        owner=params.wormhole_user,
        mode=0755)
    params.HdfsResource(
        '/wormhole/udfjars',
        type="directory",
        action="create_on_execute",
        owner=params.wormhole_user,
        mode=0755)
    params.HdfsResource(None, action="execute")

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.wormhole_user)
        Execute('tar -jxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute('rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/wormhole.sh" %
                params.install_dir)
        Execute(
            'chown -R %s:%s %s/%s' % (params.wormhole_user, params.wormhole_group, Script.get_stack_root(),params.version_dir))
        Execute(
            'chown -R %s:%s %s' % (params.wormhole_user, params.wormhole_group,
                                   params.install_dir))


class wormhole(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_wormhole()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/application.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.wormhole_user,
            group=params.wormhole_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + params.pid_file + '`')

    def start(self, env):
        import params
        env.set_params(params)
        install_wormhole()
        self.configure(env)
        Execute(
            "nohup java -DWORMHOLE_HOME=" + params.install_dir +
            " -cp $WORMHOLE_HOME/lib/wormhole-rider-server_1.3-0.5.5-beta.jar:$WORMHOLE_HOME/lib/* edp.rider.RiderStarter &"
        )
        Execute(
            "echo `ps aux|grep 'edp.rider.RiderStarter' | grep -v grep | awk '{print $2}'` > "
            + params.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    wormhole().execute()
