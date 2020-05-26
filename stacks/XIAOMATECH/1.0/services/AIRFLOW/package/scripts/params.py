from resource_management import *
from resource_management.libraries.functions.default import default
from resource_management.libraries.script.script import Script

config = Script.get_config()

conf_dir = '/etc/airflow'
airflow_user = config['configurations']['airflow-env']['airflow_user']
airflow_group = user_group = config['configurations']['cluster-env'][
    "user_group"]

hostname = config['agentLevelParams']['hostname']

install_dir = airflow_home = '/usr/share/airflow'

airflow_base_url = default('configurations/airflow-env/base_url',
                           'http://' + hostname + ':8082')
airflow_base_log_folder = default('configurations/airflow-env/base_log_folder',
                                  '/var/log/airflow')
airflow_dags_folder = default('configurations/airflow-env/dags_folder',
                              '/data1/airflow/dags')
airflow_sql_alchemy_conn = default(
    'configurations/airflow-env/sql_alchemy_conn',
    'sqlite:////data1/airflow/airflow.db')

celery_broker_url = default('configurations/airflow-env/celery_broker_url',
                            'redis://127.0.0.1:6379/0')
celery_result_backend = default(
    'configurations/airflow-env/celery_result_backend',
    'redis://127.0.0.1:6379/0')

airflow_conf = default('configurations/airflow-env/content', "")

airflow_config_path = "/etc/airflow.cfg"
airflow_env_path = "/etc/airflow/airflow-env.sh"

scheduler_runs = default('configurations/airflow-env/scheduler_runs', 6)

principal_name_webserver = default(
    'configurations/airflow-env/principal_name_webserver', 'airflow')
keytab_path_webserver = default(
    'configurations/airflow-env/keytab_path_webserver', '')

#/usr/share/airflow/airflow.cfg
