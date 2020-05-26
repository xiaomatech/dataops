
import os
from resource_management.libraries.functions.check_process_status import check_process_status

RESULT_CODE_OK = 'OK'
RESULT_CODE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'

BEACON_PID_DIR_KEY = '{{beacon-env/beacon_pid_dir}}'


def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (BEACON_PID_DIR_KEY,)


def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label

    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """

    try:
        beacon_pid_dir = configurations[BEACON_PID_DIR_KEY]
        beacon_pid_file = os.path.join(beacon_pid_dir, "beacon.pid")
        check_process_status(beacon_pid_file)
        return (RESULT_CODE_OK, ["Beacon Server process is running"])
    except:
        return (RESULT_CODE_CRITICAL, ['Beacon Server process is not running'])
