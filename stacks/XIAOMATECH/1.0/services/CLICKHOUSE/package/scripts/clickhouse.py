#!/usr/bin/env python

from resource_management.core.resources.system import Directory, Execute, File, Link
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions import format


def clickhouse():
    import params
    Directory(
        [
            params.clickhouse_log_dir, params.clickhouse_pid_dir,
            params.conf_dir, params.conf_dir + '/conf.d', params.clickhouse_data_path
        ],
        mode=0755,
        cd_access='a',
        owner=params.clickhouse_user,
        group=params.clickhouse_group,
        create_parents=True,
        recursive_ownership=True,
    )

    File(params.conf_dir + '/conf.d/graphite_rollup.xml', content=StaticFile("graphite_rollup.xml"), mode=0755)

    File(
        format("{conf_dir}/config.xml"),
        owner=params.clickhouse_user,
        group=params.clickhouse_group,
        content=InlineTemplate(params.config_content))

    File(
        format("{conf_dir}/users.xml"),
        owner=params.clickhouse_user,
        group=params.clickhouse_group,
        content=InlineTemplate(params.users_content))

    File('/etc/security/limits.d/clickhouse.conf',
         owner='root',
         group='root',
         mode=0644,
         content=Template("clickhouse.conf.j2"))
