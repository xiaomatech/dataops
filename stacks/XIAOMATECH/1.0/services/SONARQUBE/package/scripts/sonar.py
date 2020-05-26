import os
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Directory, Execute, File, Link
from resource_management.core.source import StaticFile, Template, InlineTemplate


def install_sonar():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user='root')
        Execute('cd %s ; unzip /tmp/%s' %(params.stack_root,params.filename))
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' mkdir -p ' + params.conf_dir + ' && cp -r ' +
                params.install_dir + '/conf/* ' + params.conf_dir)

        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)

        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')

        Execute('/bin/rm -f /tmp/' + params.filename)


class Artifactory(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_sonar()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/sonar.properties',
            content=InlineTemplate(params.conf_content))

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + '/bin/linux-x86-64/sonar.sh stop')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(params.install_dir + '/bin/linux-x86-64/sonar.sh start')

    def status(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + '/bin/linux-x86-64/sonar.sh status')


if __name__ == "__main__":
    Artifactory().execute()
