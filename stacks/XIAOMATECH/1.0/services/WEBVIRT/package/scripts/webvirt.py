from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.source import StaticFile


class Webvirt(Script):
    def install(self, env):
        self.install_packages(env)
        Execute(
            'cd /usr/lib/python2.7/site-packages/webvirtmgr;python manage.py syncdb --noinput'
        )
        File(
            '/tmp/createsuperuser.py',
            mode=0755,
            content=StaticFile('createsuperuser.py'))
        Execute(
            'cd /usr/lib/python2.7/site-packages/webvirtmgr;cat /tmp/createsuperuser.py | python manage.py shell --plain'
        )

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/usr/local/openresty/nginx/conf/vhost/webvirt.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop webvirtmgr-console')
        Execute('systemctl stop webvirtmgr')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl start webvirtmgr')
        Execute('systemctl start webvirtmgr-console')

    def status(self, env):
        Execute('systemctl status webvirtmgr')


if __name__ == "__main__":
    Webvirt().execute()
