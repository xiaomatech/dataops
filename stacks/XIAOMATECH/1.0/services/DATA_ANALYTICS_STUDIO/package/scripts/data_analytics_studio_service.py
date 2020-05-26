#!/usr/bin/env python

import os
import das_tools

from resource_management.core.exceptions import ComponentIsNotRunning, Fail
from resource_management.core.resources.packaging import Package
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions import get_user_call_output
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.security_commons import update_credential_provider_path
from ambari_commons.credential_store_helper import get_password_from_credential_store


def create_credential_providers():
    import params

    if not os.path.exists(params.conf_dir):
        os.makedirs(params.conf_dir)

    for c in ['data_analytics_studio-database', 'data_analytics_studio-properties',
              'data_analytics_studio-security-site']:
        update_credential_provider_path(
            params.config['configurations'][c],
            c,
            os.path.join(params.conf_dir, c + '.jceks'),
            params.data_analytics_studio_user,
            params.data_analytics_studio_group
        )


def data_analytics_studio_service(name, action="start"):
    if name == "data_analytics_studio_webapp":
        data_analytics_studio_postgresql_server_action(action)
        data_analytics_studio_webapp_action(action)
    elif name == "data_analytics_studio_event_processor":
        data_analytics_studio_event_processor_action(action)


def data_analytics_studio_webapp_action(action):
    import params
    if action == 'install':
        return

    pid = get_user_call_output.get_user_call_output(format("cat {data_analytics_studio_webapp_pid_file}"),
                                                    user=params.data_analytics_studio_user,
                                                    is_checked_call=False)[1]
    process_id_exists_command = format(
        "ls {data_analytics_studio_webapp_pid_file} > /dev/null 2>&1 && ps -p {pid} >/dev/null 2>&1")

    das_home = das_tools.get_das_home()
    cmd = format("source {conf_dir}/das-webapp-env.sh; {das_home}/bin/das-webapp {action}")
    env = {
        "JAVA_HOME": params.java64_home,
        "HADOOP_CONF": params.hadoop_conf_dir
    }
    if action == "start":
        create_credential_providers()
        Execute(cmd,
                not_if=process_id_exists_command,
                environment=env,
                user=params.data_analytics_studio_user)
    else:
        Execute(cmd,
                only_if=process_id_exists_command,
                environment=env,
                user=params.data_analytics_studio_user)


def data_analytics_studio_event_processor_action(action):
    import params

    pid = get_user_call_output.get_user_call_output(format("cat {data_analytics_studio_event_processor_pid_file}"),
                                                    user=params.data_analytics_studio_user,
                                                    is_checked_call=False)[1]
    process_id_exists_command = format(
        "ls {data_analytics_studio_event_processor_pid_file} > /dev/null 2>&1 && ps -p {pid} >/dev/null 2>&1")

    das_home = das_tools.get_das_home()
    cmd = format("source {conf_dir}/das-event-processor-env.sh; {das_home}/bin/das-event-processor {action}")
    env = {
        "JAVA_HOME": params.java64_home,
        "HADOOP_CONF": params.hadoop_conf_dir
    }
    if action == "start":
        create_credential_providers()
        Execute(cmd,
                not_if=process_id_exists_command,
                environment=env,
                user=params.data_analytics_studio_user)
    else:
        Execute(cmd,
                only_if=process_id_exists_command,
                environment=env,
                user=params.data_analytics_studio_user)


def data_analytics_studio_postgresql_server_action(action):
    import params

    # For custom postgres, everything should be setup by the user.
    if not params.data_analytics_studio_autocreate_db:
        return

    isSystemd = True

    if action == "install":
        postgresql_server_install(isSystemd)
    else:
        postgresql_server_action(action, isSystemd)


def postgresql_server_install(isSystemd):
    Package("postgresql96-server")
    Package("postgresql96-contrib")
    Execute("postgresql-setup initdb")

    import data_analytics_studio
    data_analytics_studio.setup_data_analytics_studio_postgresql_server()

    # Initialize the DBs for DAS.
    postgresql_server_action("start", isSystemd)
    data_analytics_studio_initdb()
    postgresql_server_action("stop", isSystemd)


def postgresql_server_action(action, isSystemd):
    pg_ctl = "/bin/pg_ctl"
    pg_data = "/data1/pgsql/"
    service_name = "postgresql"
    if action in ["start", "stop"]:
        if isSystemd:
            Execute(format("{pg_ctl} {action} -D {pg_data}"), user="postgres")
        else:
            Execute(format("service {service_name} {action}"))
    elif action == "status":
        try:
            if isSystemd:
                Execute(format("{pg_ctl} status -D {pg_data} | grep \"server is running\""), user="postgres")
            else:
                Execute(format("service {service_name} status | grep running"))
        except Fail as err:
            # raise ComponentIsNotRunning(), let webapp override this.
            return


def data_analytics_studio_initdb():
    import params
    create_credential_providers()
    dbPassword = get_password_from_credential_store("data_analytics_studio_database_password",
                                                    params.das_credential_provider_paths,
                                                    params.das_credential_store_class_path, params.java64_home,
                                                    params.jdk_location)
    pg_cmd = """
        psql -tc \"SELECT 1 FROM pg_database WHERE datname = '{data_analytics_studio_database_name}'\" | grep 1 || (
        psql -c \"CREATE ROLE {data_analytics_studio_database_username} WITH LOGIN PASSWORD '{password}';\" &&
        psql -c \"ALTER ROLE {data_analytics_studio_database_username} SUPERUSER;\" &&
        psql -c \"ALTER ROLE {data_analytics_studio_database_username} CREATEDB;\" &&
        psql -c \"CREATE DATABASE {data_analytics_studio_database_name};\" &&
        psql -c \"GRANT ALL PRIVILEGES ON DATABASE {data_analytics_studio_database_name} TO {data_analytics_studio_database_username};\")
    """
    Execute(format(pg_cmd, password=dbPassword), user="postgres")
