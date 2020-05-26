#!/usr/bin/env python

import os

from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.properties_file import PropertiesFile


def data_analytics_studio(name=None):
    if name == "data_analytics_studio_webapp":
        setup_data_analytics_studio_postgresql_server()
        setup_data_analytics_studio_configs()
        setup_data_analytics_studio_webapp()
    elif name == "data_analytics_studio_event_processor":
        setup_data_analytics_studio_configs()
        setup_data_analytics_studio_event_processor()


def setup_data_analytics_studio_webapp():
    import params

    File(params.das_webapp_json,
         content=InlineTemplate(params.das_webapp_properties_content),
         owner=params.data_analytics_studio_user,
         mode=0400
         )

    File(params.das_webapp_env_sh,
         content=InlineTemplate(params.das_webapp_env_content),
         owner=params.data_analytics_studio_user,
         mode=0400
         )


def setup_data_analytics_studio_event_processor():
    import params

    File(params.das_event_processor_json,
         content=InlineTemplate(params.das_event_processor_properties_content),
         owner=params.data_analytics_studio_user,
         mode=0400
         )

    File(params.das_event_processor_env_sh,
         content=InlineTemplate(params.das_event_processor_env_content),
         owner=params.data_analytics_studio_user,
         mode=0400
         )


def setup_data_analytics_studio_configs():
    import params

    Directory(os.path.dirname(params.conf_dir),
              owner=params.data_analytics_studio_user,
              create_parents=True,
              mode=0755)

    Directory(params.conf_dir,
              owner=params.data_analytics_studio_user,
              create_parents=True,
              mode=0755)

    Directory(params.data_analytics_studio_pid_dir,
              owner=params.data_analytics_studio_user,
              create_parents=True,
              mode=0755)

    Directory(params.data_analytics_studio_log_dir,
              owner=params.data_analytics_studio_user,
              create_parents=True,
              mode=0755)

    File(params.das_conf,
         content=InlineTemplate(params.das_conf_content),
         owner=params.data_analytics_studio_user,
         mode=0400
         )

    PropertiesFile(params.das_hive_site_conf,
                   properties=params.das_hive_site_conf_dict,
                   owner=params.data_analytics_studio_user,
                   mode=0400
                   )

    PropertiesFile(params.das_hive_interactive_site_conf,
                   properties=params.das_hive_interactive_site_conf_dict,
                   owner=params.data_analytics_studio_user,
                   mode=0400
                   )


def setup_data_analytics_studio_postgresql_server():
    import params

    if not params.data_analytics_studio_autocreate_db:
        return

    pgpath = "/var/lib/pgsql/data"

    File(format("{pgpath}/pg_hba.conf"),
         content=InlineTemplate(params.data_analytics_studio_postgresql_pg_hba_conf_content),
         owner="postgres",
         group="postgres",
         mode=0600)

    File(format("{pgpath}/postgresql.conf"),
         content=InlineTemplate(params.data_analytics_studio_postgresql_postgresql_conf_content),
         owner="postgres",
         group="postgres",
         mode=0600)
