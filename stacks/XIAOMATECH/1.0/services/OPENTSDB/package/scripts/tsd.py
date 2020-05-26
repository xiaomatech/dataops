from resource_management import *
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.libraries.script.script import Script
from resource_management.core.source import Template, InlineTemplate
import os


def install_opentsdb():
    import params
    Directory(
        [params.conf_dir, params.opentsdb_pid_dir, params.opentsdb_log_dir],
        owner=params.opentsdb_user,
        group=params.opentsdb_group,
        mode=0775,
        create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.opentsdb_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(
            'chown -R %s:%s %s/%s' % (params.opentsdb_user, params.opentsdb_group, Script.get_stack_root(),params.version_dir))
        Execute(
            'chown -R %s:%s %s' % (params.opentsdb_user, params.opentsdb_group,
                                   params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute(params.install_dir + '/tools/create_table.sh')


class Master(Script):
    def install(self, env):
        self.install_packages(env)
        install_opentsdb()
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            format("{conf_dir}/opentsdb.conf"),
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.opentsdb_user,
            group=params.opentsdb_group)
        File(
            format("/etc/init.d/opentsdb"),
            content=InlineTemplate(params.init_content),
            mode=0755,
            owner=params.opentsdb_user,
            group=params.opentsdb_group)
        File(
            format("{conf_dir}/logback.xml"),
            content=InlineTemplate(params.log_content),
            mode=0755,
            owner=params.opentsdb_user,
            group=params.opentsdb_group)
        File(
            format("{conf_dir}/opentsdb_jaas.conf"),
            content=InlineTemplate(params.jaas_content),
            mode=0755,
            owner=params.opentsdb_user,
            group=params.opentsdb_group)

    def stop(self, env):
        Execute("service opentsdb stop")

    def start(self, env):
        install_opentsdb()
        self.configure(env)
        Execute("service opentsdb start")

    def restart(self, env):
        self.configure(env)
        Execute("service opentsdb restart")

    def status(self, env):
        Execute("service opentsdb status")


if __name__ == "__main__":
    Master().execute()
