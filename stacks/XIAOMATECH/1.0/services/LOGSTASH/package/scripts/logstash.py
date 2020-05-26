from resource_management.core.logger import Logger
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status

from resource_management.libraries.functions.default import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


class Logstash(Script):
    def install(self, env):
        import params
        env.set_params(params)
        Logger.info("Install Logstash")
        self.install_packages(env)
        Execute('systemctl enable Logstash')
        Execute('mkdir -p /etc/logstash/patterns', user=params.logstash_user)
        Execute(
            '/bin/cp -rf /usr/share/logstash/vendor/bundle/jruby/*/gems/logstash-patterns-core-*/patterns/* /etc/logstash/patterns/',
            user=params.logstash_user)

    def configure(self, env):
        import params
        env.set_params(params)
        Logger.info("Configure logstash")
        directories = [
            params.log_dir, params.pid_dir, params.conf_dir,
            params.patterns_dir
        ]
        Directory(
            directories,
            mode=0755,
            owner=params.logstash_user,
            group=params.logstash_group)

        File(
            "{0}/logstash.yml".format(params.conf_dir),
            owner=params.logstash_user,
            group=params.logstash_group,
            content=InlineTemplate(params.logstash_content))

        File(
            "{0}/jvm.options".format(params.conf_dir),
            owner=params.logstash_user,
            group=params.logstash_group,
            content=InlineTemplate(params.jvm_content))

        File(
            "{0}/conf.d/indexer.conf".format(params.conf_dir),
            owner=params.logstash_user,
            group=params.logstash_group,
            content=InlineTemplate(params.indexer_content))
        File(
            "{0}/nginx".format(params.patterns_dir),
            owner=params.logstash_user,
            group=params.logstash_group,
            content=InlineTemplate(params.patterns_content))

        File(
            "/etc/init.d/logstash",
            owner=params.logstash_user,
            group=params.logstash_group,
            content=InlineTemplate(params.init_content))
        Execute(
            "chmod a+x /etc/init.d/logstash && chkconfig --add logstash && chkconfig logstash on"
        )
        Execute('/usr/share/logstash/bin/logstash --modules netflow --setup')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("service logstash stop")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("service logstash start")

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute("service logstash restart")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_file)


if __name__ == "__main__":
    Logstash().execute()
