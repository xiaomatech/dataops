from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory
from resource_management.libraries.functions.check_process_status import check_process_status

import os


def install_confluence():
    import params
    Directory([params.conf_dir], owner='jira', mode=0775, create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/atlassian/confluence'):
        Execute('wget ' + params.download_url_confluence + ' -O /tmp/confluence.bin')
        Execute('sudo /tmp/confluence.bin')


class Confluence(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_confluence()

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/lib/systemd/system/confluence.service',
            content=InlineTemplate(params.confluence_systemd),
            mode=0755,
            owner='confluence')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop confluence')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start confluence')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(Script.get_stack_root() + '/atlassian/jira/work/confluence.pid')


if __name__ == "__main__":
    Confluence().execute()
