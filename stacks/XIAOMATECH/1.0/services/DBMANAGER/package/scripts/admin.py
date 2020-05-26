from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import Directory
from resource_management.libraries.functions.check_process_status import check_process_status
import os
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.source import StaticFile

config_file = 'archery'


def install_webadmin():
    import params
    Directory([params.log_dir, params.conf_dir],
              owner='nobody',
              group='nobody',
              mode=0755,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir_admin
                          ) or not os.path.exists(params.install_dir_admin):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir_admin)
        Execute('rm -rf %s' % params.install_dir_admin)
        Execute('/bin/rm -f /tmp/' + params.filename_admin)
        Execute(
            'wget ' + params.download_url_admin + ' -O /tmp/' + params.filename_admin,
            user='nobody')
        Execute('tar -zxvf /tmp/' + params.filename_admin + ' -C  ' + Script.get_stack_root())
        Execute('chown -R %s:%s %s/%s' % ('nobody', 'nobody',
                                          Script.get_stack_root(),params.version_dir_admin))
        Execute('chown -R %s:%s %s' % ('nobody', 'nobody',
                                       params.install_dir_admin))

        Execute(
            'wget ' + params.download_url_soar + ' -O /usr/sbin/soar',
            user='root')
        Execute('chmod a+x /usr/sbin/soar')


class Admin(Script):
    pid_file = ''

    def install(self, env):
        self.install_packages(env)
        install_webadmin()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/soar.yaml',
            content=InlineTemplate(params.soar_content),
            mode=0755,
            owner='mysql',
            group='mysql')
        File(
            '/opt/archery/archery/settings.py',
            content=params.settings_content,
            mode=0755,
            owner='mysql',
            group='mysql')
        File('/etc/init.d/archery', content=params.init_content, mode=0755)
        File(
            '/etc/pyxbackup.cnf',
            content=InlineTemplate(params.backup_content),
            mode=0755,
            owner='mysql',
            group='mysql')
        Execute(
            "echo 'px0nwi7Kbf25fkUaKwUdmG+eDmg7YZt9' > /etc/pyxbackup_encrypt.key",
            user='mysql')
        File(
            '/usr/sbin/pyxbackup',
            content=StaticFile('pyxbackup.py'),
            mode=0755,
            owner='mysql',
            group='mysql')

    def start(self, env):
        import params
        env.set_params(params)
        install_webadmin()
        Execute('service archery start')
        Execute("echo `ps aux|grep '" + config_file +
                "' | grep -v grep | awk '{print $2}'` > " + self.pid_file)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('kill -9 `cat ' + self.pid_file + ' ` ')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Admin().execute()
