import glob
import os
from resource_management.core.resources import Directory
from resource_management.core.resources.system import Execute, File
from resource_management.core.source import InlineTemplate, StaticFile
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.format import format
from resource_management.libraries.script.script import Script
from resource_management.libraries import XmlConfig


def install_kylin():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.kylin_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' mkdir -p ' + params.conf_dir + ' && cp -r ' +
                params.install_dir + '/conf/* ' + params.conf_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute(' rm -rf ' + params.install_dir + '/logs')
        Execute('ln -s ' + params.kylin_log_dir + ' ' + params.install_dir +
                '/logs')

        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/kylin.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.kylin_user, params.kylin_group,params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.kylin_user, params.kylin_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


class Job(Script):
    def install(self, env):
        import params
        env.set_params(params)
        install_kylin()
        self.create_kylin_dir()
        Execute('ln -s ' + params.install_dir + '/pid ' +
                params.kylin_pid_file)

        Directory([
            params.kylin_pid_dir, params.kylin_dir, params.conf_dir,
            params.kylin_log_dir
        ],
                  owner=params.kylin_user,
                  group=params.kylin_group,
                  cd_access="a",
                  create_parents=True,
                  mode=0755)

        File(
            params.conf_dir + '/kylin-env.sh',
            mode=0755,
            content=InlineTemplate(params.kylin_env_template),
            owner=params.kylin_user,
            group=params.kylin_group)
        File(
            params.conf_dir + '/SCSinkTools.json',
            mode=755,
            content=StaticFile('SCSinkTools.json'))
        File(
            params.conf_dir + '/system_cube.sh',
            mode=755,
            content=StaticFile('system_cube.sh'))

        Execute('source ' + params.conf_dir + '/kylin-env.sh; ' +
                params.conf_dir + '/system_cube.sh')

    def create_kylin_dir(self):
        import params
        params.HdfsResource(
            format("/user/{kylin_user}"),
            type="directory",
            action="create_on_execute",
            owner=params.kylin_user,
            group=params.kylin_group,
            recursive_chown=True,
            recursive_chmod=True)
        params.HdfsResource(
            format("/logs/spark/kylin"),
            type="directory",
            action="create_on_execute",
            owner=params.kylin_user,
            group=params.kylin_group,
            recursive_chown=True,
            recursive_chmod=True)
        params.HdfsResource(
            format("/kylin"),
            type="directory",
            action="create_on_execute",
            owner=params.kylin_user,
            group=params.kylin_group,
            recursive_chown=True,
            recursive_chmod=True)
        params.HdfsResource(None, action="execute")

    def configure(self, env):
        import params
        env.set_params(params)

        File(
            os.path.join(params.conf_dir, "kylin.properties"),
            content=InlineTemplate(params.kylin_properties_template),
            owner=params.kylin_user,
            group=params.kylin_group)

        XmlConfig(
            "kylin_hive_conf.xml",
            conf_dir=params.conf_dir,
            configurations=params.config['configurations']['kylin_hive_conf'],
            owner=params.kylin_user,
            group=params.kylin_group)
        XmlConfig(
            "kylin_job_conf.xml",
            conf_dir=params.conf_dir,
            configurations=params.config['configurations']['kylin_job_conf'],
            owner=params.kylin_user,
            group=params.kylin_group)
        XmlConfig(
            "kylin_job_conf_inmem.xml",
            conf_dir=params.conf_dir,
            configurations=params.config['configurations']
            ['kylin_job_conf_inmem'],
            owner=params.kylin_user,
            group=params.kylin_group)
        XmlConfig(
            "kylin-kafka-consumer.xml",
            conf_dir=params.conf_dir,
            configurations=params.config['configurations']
            ['kylin-kafka-consumer'],
            owner=params.kylin_user,
            group=params.kylin_group)
        File(
            os.path.join(params.conf_dir, "kylin-server-log4j.properties"),
            mode=0644,
            group=params.kylin_group,
            owner=params.kylin_user,
            content=InlineTemplate(params.log4j_server_props))
        File(
            os.path.join(params.conf_dir, "kylin-tools-log4j.properties"),
            mode=0644,
            group=params.kylin_group,
            owner=params.kylin_user,
            content=InlineTemplate(params.log4j_tool_props))

    def stop(self, env):
        import params
        Execute(
            params.kylin_dir + '/bin/kylin.sh stop >> ' +
            params.kylin_log_file,
            user=params.kylin_user)

    def start(self, env):
        import params
        install_kylin()
        self.configure(env)

        if params.security_enabled:
            kylin_kinit_cmd = format(
                "{kinit_path_local} -kt {kylin_kerberos_keytab} {kylin_kerberos_principal}; "
            )
            Execute(kylin_kinit_cmd, user=params.kylin_user)

        Execute(
            ' source ' + params.conf_dir + '/kylin-env.sh ;' + params.kylin_dir
            + '/bin/kylin.sh start >> ' + params.kylin_log_file,
            user=params.kylin_user)
        pidfile = params.kylin_pid_file
        Logger.info(format("Pid file is: {pidfile}"))

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.kylin_pid_file)

    def get_pid_files(self):
        import params
        return [params.kylin_pid_file]


if __name__ == "__main__":
    Job().execute()
