from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.source import StaticFile, Template, InlineTemplate
import os


def install_graphite_web():
    import params
    Directory(
        [params.graphite_conf_dir, params.log_dir, params.pid_dir],
        owner=params.graphite_user,
        group=params.user_group,
        mode=0775,
        cd_access="a",
        create_parents=True)

    if not os.path.exists(params.install_dir_graphite_web):
        Execute(
            'wget ' + params.download_url_graphite_web + ' -O /tmp/' + params.filename_graphite_web,
            user=params.graphite_user)
        Execute('tar -xf /tmp/' + params.filename_graphite_web + ' -C  ' + Script.get_stack_root())

        Execute(' rm -rf ' + params.install_dir_graphite_web + '/conf')
        Execute('ln -s ' + params.graphite_conf_dir + ' ' + params.install_dir_graphite_web +
                '/conf')

        Execute('chown -R %s:%s %s' % (params.graphite_user, params.user_group,
                                       params.install_dir_graphite_web))
        Execute('/bin/rm -f /tmp/' + params.filename_graphite_web)

        File(params.install_dir_graphite_web + '/webapp/graphite/graphouse.py', content=StaticFile("graphouse.py"),
             mode=0755)

        File('/usr/lib/systemd/system/graphite-web.service', content=params.graphite_web_systemd_content, mode=0755)
        File('/etc/sysconfig/memcached', content=params.memcached_content, mode=0755)
        Execute('systemctl daemon-reload')
        Execute('systemctl enable graphite-web')
        Execute('systemctl enable memcached')
        Execute('systemctl start memcached')


class GraphiteWeb(Script):
    pid_file = '/var/run/graphite/web.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_graphite_web()

    def configure(self, env):
        import params
        env.set_params(params)
        File(params.install_dir_graphite_web + '/conf/dashboard.conf', content=StaticFile("dashboard.conf"), mode=0755)
        File(params.install_dir_graphite_web + '/conf/graphite.wsgi', content=StaticFile("graphite.wsgi"), mode=0755)
        File(params.install_dir_graphite_web + '/conf/graphTemplates.conf', content=StaticFile("graphTemplates.conf"), mode=0755)
        File(params.install_dir_graphite_web + '/webapp/graphite/local_settings.py', content=StaticFile("graphite_settings.py"),
             mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop graphite-web")

    def start(self, env):
        import params
        env.set_params(params)
        install_graphite_web()
        self.configure(env)
        Execute("systemctl start graphite-web")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    GraphiteWeb().execute()
