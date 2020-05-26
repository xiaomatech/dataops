from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
import os


def install_graphite_api():
    import params
    Directory(
        [params.graphite_conf_dir, params.log_dir, params.pid_dir, '/srv/graphite'],
        owner=params.graphite_user,
        group=params.user_group,
        mode=0775,
        cd_access="a",
        create_parents=True)

    if not os.path.exists(params.install_dir_graphite_api):
        Execute('wget ' + params.download_url_graphite_api + ' -O /tmp/' + params.filename_graphite_api,
                user=params.graphite_user)
        Execute('tar -xf /tmp/' + params.filename_graphite_api + ' -C  ' + Script.get_stack_root())

        Execute('chown -R %s:%s %s' % (params.graphite_user, params.user_group,
                                       params.install_dir_graphite_api))
        Execute('/bin/rm -f /tmp/' + params.filename_graphite_api)

        File(params.install_dir_graphite_api + '/lib/python3.6/site-packages/graphite_api/finders/graphouse_api.py',
             content=StaticFile("graphouse_api.py"), mode=0755)
        File('/usr/lib/systemd/system/graphite-api.service', content=params.graphite_api_systemd_content, mode=0755)
        File('/etc/sysconfig/memcached', content=params.memcached_content, mode=0755)
        Execute('systemctl daemon-reload')
        Execute('systemctl enable graphite-api')
        Execute('systemctl enable memcached')
        Execute('systemctl start memcached')


class GraphiteAPI(Script):
    pid_file = '/var/run/graphite/api.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_graphite_api()

    def configure(self, env):
        import params
        env.set_params(params)
        graphite_api_conf = '''
finders:
  - graphite_api.finders.graphouse_api.GraphouseFinder 
graphouse:
  url: http://localhost:2005
        '''

        File('/etc/graphite-api.yaml', content=graphite_api_conf, mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop graphite-api")

    def start(self, env):
        import params
        env.set_params(params)
        install_graphite_api()

        self.configure(env)
        Execute("systemctl start graphite-api")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    GraphiteAPI().execute()
