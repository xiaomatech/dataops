from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.packaging import Package

import os


def install_registry():
    import params
    Directory(['/data1/registry', '/etc/harbor'],
              mode=0755,
              create_parents=True)

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute('wget ' + params.download_url + ' -O /tmp/' + params.filename)
        Execute('tar -jxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        File(
            '/etc/harbor/harbor.cfg',
            content=InlineTemplate(params.harbor_cfg_content),
            mode=0755)

        Execute(params.install_dir + '/install.sh')


class dbus(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Package(['docker-compose'])
        install_registry()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/harbor/harbor.cfg',
            content=InlineTemplate(params.harbor_cfg_content),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('')

    def start(self, env):
        import params
        env.set_params(params)
        install_registry()
        self.configure(env)
        Execute("")

    def status(self, env):
        import params
        env.set_params(params)
        Execute("")


if __name__ == "__main__":
    dbus().execute()
