import os
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.core import shell
from resource_management.core.shell import as_user, as_sudo
from resource_management.core.source import Template, InlineTemplate
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config
from resource_management.libraries.script.script import Script
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status


def install_flume():
    import params
    Directory(params.data_dirs,
              owner=params.flume_user,
              group=params.flume_group,
              mode=0775,
              cd_access="a",
              create_parents=True)

    Directory(
        [params.flume_conf_dir, params.flume_log_dir, params.flume_run_dir],
        owner=params.flume_user,
        group=params.flume_group,
        mode=0775,
        cd_access="a",
        create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.flume_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.flume_conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/flume.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.flume_user, params.flume_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.flume_user, params.flume_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def flume(action=None):
    import params

    if action == 'config':
        if params.security_enabled:
            File(
                format("{flume_conf_dir}/flume_jaas.conf"),
                owner=params.flume_user,
                content=InlineTemplate(params.flume_jaas_conf_template))

        Directory([params.flume_log_dir, params.flume_conf_dir, params.flume_run_dir],
                  owner=params.flume_user,
                  group=params.flume_group,
                  mode=0775,
                  cd_access="a",
                  create_parents=True
                  )

        File(params.flume_conf_dir + '/flume.conf',
             content=InlineTemplate(params.flume_conf_content),
             owner=params.flume_user,
             mode=0644)

        File(
            params.flume_conf_dir + '/log4j.properties',
            content=Template('log4j.properties.j2'),
            owner=params.flume_user,
            mode=0644)

        File(
            params.flume_conf_dir + '/flume-env.sh',
            owner=params.flume_user,
            content=InlineTemplate(params.flume_env_sh_template))

        if params.has_metric_collector:
            File(params.flume_conf_dir + '/flume-metrics2.properties',
                 owner=params.flume_user,
                 content=Template("flume-metrics2.properties.j2"))

        generate_logfeeder_input_config(
            'flume',
            Template("input.config-flume.json.j2", extra_imports=[default]))

    elif action == 'start':

        flume_base = as_user(
            format(
                "{flume_bin} agent --name {{0}} --conf {{1}} --conf-file {{2}} {{3}} > {flume_log_dir}/flume.out 2>&1"
            ),
            params.flume_user,
            env={'JAVA_HOME': params.java_home}) + " &"

        extra_args = ''
        if params.has_metric_collector:
            extra_args = '-Dflume.monitoring.type=org.apache.hadoop.metrics2.sink.flume.FlumeTimelineMetricsSink ' \
                         '-Dflume.monitoring.node={0}:{1}'
            extra_args = extra_args.format(
                params.metric_collector_host,
                params.metric_collector_port)

        flume_cmd = flume_base.format('ingest', params.flume_conf_dir,
                                      params.flume_conf_dir + '/flume.conf',
                                      extra_args)

        Execute(
            flume_cmd,
            wait_for_finish=False,
            environment={'JAVA_HOME': params.java_home})
        pid_cmd = as_sudo(('pgrep', '-o', '-u', params.flume_user, '-f', format('^{java_home}'))) + \
                  " | " + as_sudo(('tee', params.flume_pid_file)) + "  && test ${PIPESTATUS[0]} -eq 0"

        try:
            Execute(pid_cmd, logoutput=True, tries=20, try_sleep=10)
        except:
            show_logs(params.flume_log_dir, params.flume_user)

    elif action == 'stop':

        pid = shell.checked_call(("cat", params.flume_pid_file), sudo=True)[1].strip()
        Execute(("kill", "-15", pid), sudo=True)
        show_logs(params.flume_log_dir, params.flume_user)
        File(params.flume_pid_file, action='delete')


class FlumeHandler(Script):
    def configure(self, env):
        import params
        env.set_params(params)
        flume(action='config')

    def get_component_name(self):
        return "flume"

    def install(self, env):
        import params
        install_flume()
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        install_flume()
        self.configure(env)
        flume(action='start')

    def stop(self, env):
        import params
        env.set_params(params)
        flume(action='stop')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.flume_pid_file)

    def pre_upgrade_restart(self, env):
        import params
        env.set_params(params)
        Logger.info("Executing Flume Stack Upgrade pre-restart")
        install_flume()

    def get_log_folder(self):
        import params
        return params.flume_log_dir


if __name__ == "__main__":
    FlumeHandler().execute()
