from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.resources.xml_config import XmlConfig
import os


def install_xlearning():
    import params
    Directory([params.conf_dir, params.log_dir],
              owner=params.xlearning_user,
              group=params.xlearning_group,
              mode=0755,
              create_parents=True)
    params.HdfsResource(
        '/xlearning/staging',
        type="directory",
        action="create_on_execute",
        owner=params.xlearning_user,
        mode=0755)
    params.HdfsResource(
        '/xlearning/eventlog',
        type="directory",
        action="create_on_execute",
        owner=params.xlearning_user,
        mode=0755)
    params.HdfsResource(
        '/xlearning/history',
        type="directory",
        action="create_on_execute",
        owner=params.xlearning_user,
        mode=0755)
    params.HdfsResource(None, action="execute")

    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.xlearning_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' cp -r ' + params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('ln -s ' + params.log_dir + ' ' + params.install_dir +
                '/logs/xlearning')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/xlearning.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.xlearning_user, params.xlearning_group,params.stack_root, params.version_dir))
        Execute(
            'chown -R %s:%s %s' % (params.xlearning_user,
                                   params.xlearning_group, params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def config_xlearning():
    import params
    File(
        params.conf_dir + "/log4j.properties",
        owner=params.xlearning_user,
        group=params.user_group,
        mode=0644,
        content=InlineTemplate(params.log_content))

    File(
        params.conf_dir + "/xlearning-env.sh",
        owner=params.xlearning_user,
        group=params.user_group,
        mode=0644,
        content=InlineTemplate(params.env_content))

    XmlConfig(
        "xlearning-site.xml",
        conf_dir=params.conf_dir,
        configurations=params.config['configurations']['xlearning-site'],
        owner=params.xlearning_user,
        group=params.user_group,
        mode=0644)


class xlearning(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_xlearning()

    def configure(self, env):
        import params
        env.set_params(params)
        config_xlearning()

    def stop(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        install_xlearning()
        self.configure(env)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.xlearning_pid_file)


if __name__ == "__main__":
    xlearning().execute()
