from resource_management import *
from resource_management.core.resources.system import Directory, File, Link
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Execute
import os
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


def install_geoserver():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir, ignore_failures=True)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.geoserver_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('mkdir ' + params.install_dir + '/logs && chmod 777 ' +
                params.install_dir + '/logs')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/geoserver.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.geoserver_user, params.geoserver_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.geoserver_user, params.geoserver_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def config_geoserver():
    import params
    Directory([params.pid_dir, params.log_dir, params.conf_dir, params.data_dir],
              owner=params.geoserver_user,
              group=params.geoserver_group)
    File(
        format("{conf_dir}/geoserver.conf"),
        content=InlineTemplate(params.geoserver_content),
        owner=params.geoserver_user)


class GeoServer(Script):
    pid_file = '/var/run/geoserver.pid'

    def install(self, env):
        install_geoserver()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        config_geoserver()

    def stop(self, env):
        import params
        Execute(params.install_dir + '/bin/startup.sh')

    def start(self, env):
        import params
        install_geoserver()
        self.configure(env)
        Execute(params.install_dir + '/bin/startup.sh')
        Execute("echo `ps aux|grep 'geoserver' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    GeoServer().execute()
