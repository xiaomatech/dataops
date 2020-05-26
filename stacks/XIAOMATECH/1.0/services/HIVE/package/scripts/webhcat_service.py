from resource_management.core.logger import Logger
from resource_management.core.exceptions import Fail
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.core.resources.system import Execute, File
import traceback


def webhcat_service(action='start', upgrade_type=None):
    import params

    cmd = format('{webhcat_bin_dir}/webhcat_server.sh')

    if action == 'start':
        daemon_cmd = format('cd {hcat_pid_dir} ; {cmd} start')
        no_op_test = format('ls {webhcat_pid_file} >/dev/null 2>&1 && ps -p `cat {webhcat_pid_file}` >/dev/null 2>&1')
        try:
            Execute(daemon_cmd,
                    user=params.webhcat_user,
                    not_if=no_op_test)
        except:
            show_logs(params.hcat_log_dir, params.webhcat_user)
            raise
    elif action == 'stop':
        try:
            # try stopping WebHCat using its own script
            graceful_stop(cmd)
        except Fail:
            show_logs(params.hcat_log_dir, params.webhcat_user)
            Logger.info(traceback.format_exc())

        pid_expression = format("`cat {webhcat_pid_file}`")

        process_id_exists_command = format(
            "ls {webhcat_pid_file} >/dev/null 2>&1 && ps -p {pid_expression} >/dev/null 2>&1")

        # kill command to run
        daemon_hard_kill_cmd = format("{sudo} kill -9 {pid_expression}")

        Execute(daemon_hard_kill_cmd,
                only_if=process_id_exists_command,
                ignore_failures=True)

        try:
            # check if stopped the process, else fail the task
            Execute(format("! ({process_id_exists_command})"))
        except:
            show_logs(params.hcat_log_dir, params.webhcat_user)
            raise

        File(params.webhcat_pid_file, action="delete")


def graceful_stop(cmd):
    """
    Attemps to stop WebHCat using its own shell script. On some versions this may not correctly
    stop the daemon.
    :param cmd: the command to run to stop the daemon
    :return:
    """
    import params
    daemon_cmd = format('{cmd} stop')

    Execute(daemon_cmd, user=params.webhcat_user)
