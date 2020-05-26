from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory
from resource_management.libraries.functions.check_process_status import check_process_status
import os


def install_jira():
    import params
    Directory([params.conf_dir], owner='jira', mode=0775, create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/atlassian/jira'):
        Execute('wget ' + params.download_url_jira + ' -O /tmp/jira.bin')
        Execute('sudo /tmp/jira.bin')


class Jira(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_jira()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/lib/systemd/system/jira.service',
            content=InlineTemplate(params.jira_systemd),
            mode=0755,
            owner='jira')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop jira')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start jira')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(Script.get_stack_root() + '/atlassian/jira/work/jira.pid')
        # Execute('systemctl status jira')


if __name__ == "__main__":
    Jira().execute()
