from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import Directory, File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.check_process_status import check_process_status

import os

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def install_zkui():
    import params
    Directory(['/etc/zkui', params.stack_root + '/zkui'],
              owner=params.zk_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(params.stack_root + '/zkui'):
        download_url = download_url_base + '/zkui-2.0.jar'
        Execute(
            'wget ' + download_url + ' -O ' + params.stack_root + '/zkui/zkui-2.0.jar',
            user=params.zk_user)


class Zkui(Script):
    pid_file = '/var/run/zkui.pid'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_zkui()

    def configure(self, env):
        import params
        env.set_params(params)
        # env.sh
        File(
            '/etc/zkui/config.cfg',
            owner=params.zk_user,
            group=params.user_group,
            mode=0644,
            content=InlineTemplate(params.zkui_content))
        File(
            '/etc/zkui/bootstrap.sh',
            owner=params.zk_user,
            group=params.user_group,
            mode=0644,
            content=InlineTemplate(params.zkui_script_content))

    def stop(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        install_zkui()
        self.configure(env)
        Execute('/etc/zkui/bootstrap.sh')
        Execute(
            "echo `ps aux|grep '/etc/zkui' | grep -v grep | awk '{print $2}'` > "
            + self.pid_file)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(self.pid_file)


if __name__ == "__main__":
    Zkui().execute()
