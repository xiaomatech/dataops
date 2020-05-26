from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
import os
from resource_management.core.resources.system import Execute


def install_tomcat():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir_tomcat) or not os.path.exists(
            params.install_dir_tomcat):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_tomcat)
        Execute('rm -rf %s' % params.install_dir_tomcat)
        Execute(
            'wget ' + params.download_url_tomcat + ' -O /tmp/' + params.filename_tomcat,
            user=params.tez_user)
        Execute('tar -zxf /tmp/' + params.filename_tomcat + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir_tomcat + ' ' + params.install_dir_tomcat)

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/tez.sh" %
                params.install_dir_tomcat)
        Execute('chown -R %s:%s %s/%s' % (params.tez_user, params.user_group,
                                          params.stack_root, params.version_dir_tomcat))
        Execute('chown -R %s:%s %s' % (params.tez_user, params.user_group,
                                       params.install_dir_tomcat))
        Execute('/bin/rm -f /tmp/' + params.filename_tomcat)


def install_webui():
    import params
    if not os.path.exists(params.install_dir_tomcat):
        install_tomcat()
    if not os.path.exists(params.install_dir_tomcat + '/webapps/tez-ui.war'):
        Execute('rm -rf ' + params.install_dir_tomcat + '/webapps/*')
        Execute('cp -rf %s/tez-ui-*.war' % params.install_dir + params.install_dir_tomcat + '/webapps/tez-ui.war',
                user=params.tez_user)


class WebUI(Script):
    pid_file = '/var/run/tez_ui.pid'

    def install(self, env):
        self.install_packages(env)
        install_webui()

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.install_dir_tomcat + '/bin/catalina.sh stop', user=params.tez_user)

    def start(self, env):
        import params
        env.set_params(params)
        install_webui()
        self.configure(env)
        Execute(params.install_dir_tomcat + '/bin/catalina.sh start', user=params.tez_user)
        Execute(
            "echo `ps aux|grep 'org.apache.catalina.startup.Bootstrap' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def configure(self, env):
        import params
        env.set_params(params)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    WebUI().execute()
