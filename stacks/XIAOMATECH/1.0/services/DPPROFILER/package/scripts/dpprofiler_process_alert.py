import os
from resource_management.libraries.functions.check_process_status import check_process_status

RESULT_CODE_OK = 'OK'
RESULT_CODE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'

DPPROFILER_PID_DIR_KEY = '{{dpprofiler-env/dpprofiler.pid.dir}}'


def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (DPPROFILER_PID_DIR_KEY,)


def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label

    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """

    try:
        dpprofiler_pid_dir = configurations[DPPROFILER_PID_DIR_KEY]
        dpprofiler_pid_file = os.path.join(dpprofiler_pid_dir, "profiler-agent.pid")
        check_process_status(dpprofiler_pid_file)
        return (RESULT_CODE_OK, ["Profiler Agent process is running"])
    except:
        return (RESULT_CODE_CRITICAL, ['Profiler Agent process is not running'])
