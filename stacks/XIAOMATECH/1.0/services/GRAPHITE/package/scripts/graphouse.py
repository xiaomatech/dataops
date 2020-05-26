from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, StaticFile
from resource_management.libraries.functions.check_process_status import check_process_status
import os

graphouse_log_dir = '/var/log/graphouse'


def install_graphouse():
    import params
    Directory(
        [params.graphouse_conf_dir, graphouse_log_dir],
        owner=params.graphite_user,
        group=params.user_group,
        mode=0775,
        cd_access="a",
        create_parents=True)

    File('/tmp/init_clickhouse.sql', content=StaticFile("init_clickhouse.sql"), mode=0755)
    # todo excute clickhouse.sql

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.graphite_user)
        Execute('tar -xf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)

        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.graphouse_conf_dir + ' ' + params.install_dir +
                '/conf')

        Execute(' rm -rf ' + params.install_dir + '/log')
        Execute('ln -s ' + params.log_dir + ' ' + params.install_dir +
                '/log')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/graphouse.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.graphite_user, params.user_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.graphite_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)

        File('/etc/init.d/graphouse', content=StaticFile("graphouse.init"), mode=0755)
        Execute('chkconfig graphouse on')


class Graphouse(Script):
    pid_file = '/var/run/graphouse.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_graphouse()

    def configure(self, env):
        import params
        env.set_params(params)
        File(params.graphouse_conf_dir + '/graphouse.properties',
             content=InlineTemplate(params.graphouse_content),
             owner=params.graphite_user,
             group=params.user_group,
             mode=0755
             )
        File(params.graphouse_conf_dir + '/graphouse.vmoptions',
             content=InlineTemplate(params.graphouse_vmoptions_content),
             owner=params.graphite_user,
             group=params.user_group,
             mode=0755
             )
        File(params.graphouse_conf_dir + 'log4j.xml',
             content=InlineTemplate(params.log4j_content),
             owner=params.graphite_user,
             group=params.user_group,
             mode=0755
             )

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("service graphouse stop")

    def start(self, env):
        import params
        env.set_params(params)
        install_graphouse()
        self.configure(env)
        Execute("service graphouse start")
        Execute("echo `ps aux|grep 'graphouse.GraphouseMain' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def status(self, env):
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Graphouse().execute()
