from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_rocketmq():
    import params
    Directory([
        params.pid_dir, params.log_dir, params.conf_dir, params.store_commitlog, params.store_queue],
        owner=params.rocketmq_user,
        group=params.user_group,
        mode=0755,
        create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.rocketmq_user)
        Execute('tar -zxvf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)

        Execute('rm -rf ' + params.install_dir + '/conf  ')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir + '/conf  ')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/rocketmq.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.rocketmq_user, params.user_group, Script.get_stack_root(), params.version_dir))
        Execute('chown -R %s:%s %s' % (params.rocketmq_user, params.user_group,
                                       params.install_dir))


def config_rocketmq():
    import params
    File(
        params.conf_dir + '/broker.conf',
        content=InlineTemplate(params.broker_content),
        mode=0755,
        owner=params.rocketmq_user,
        group=params.user_group)
    File(
        params.conf_dir + '/logback_broker.xml',
        content=InlineTemplate(params.logback_broker_content),
        mode=0755,
        owner=params.rocketmq_user,
        group=params.user_group)
    File(
        params.conf_dir + '/logback_namesrv.xml',
        content=InlineTemplate(params.logback_namesrv_content),
        mode=0755,
        owner=params.rocketmq_user,
        group=params.user_group)
    File(
        params.conf_dir + '/logback_tools.xml',
        content=InlineTemplate(params.logback_tools_content),
        mode=0755,
        owner=params.rocketmq_user,
        group=params.user_group)
    File(
        params.conf_dir + '/plain_acl.yml',
        content=InlineTemplate(params.acl_content),
        mode=0755,
        owner=params.rocketmq_user,
        group=params.user_group)


class Rocketmq(Script):
    pid_file = '/var/run/mqnamesrv.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_rocketmq()

    def configure(self, env):
        import params
        env.set_params(params)
        config_rocketmq()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir + '/bin/mqshutdown namesrv')

    def start(self, env):
        import params
        env.set_params(params)
        install_rocketmq()
        self.configure(env)
        Execute('nohup ' + params.install_dir + '/bin/runserver.sh org.apache.rocketmq.namesrv.NamesrvStartup &')
        Execute(
            "echo `ps ax | grep -i 'org.apache.rocketmq.namesrv.NamesrvStartup' |grep java | grep -v grep | awk '{print $1}'` > " + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Rocketmq().execute()
