# -*- coding: utf-8 -*-

from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Directory, Execute, File, Link
import os
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status

from resource_management.libraries.functions.default import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def config_presto():
    import params
    File(
        params.daemon_control_script,
        owner=params.presto_user,
        content=InlineTemplate(params.env_sh_template),
        mode=0775)

    security_list = []
    security = ''
    if params.security_enabled:
        security_list.append("hive.metastore.authentication.type=KERBEROS")
        security_list.append("hive.metastore.service.principal=" +
                             params.hive_metastore_principal)
        security_list.append("hive.metastore.client.principal=" +
                             params.presto_principal)
        security_list.append("hive.metastore.client.keytab=" +
                             params.presto_keytab)
        security_list.append("hive.hdfs.authentication.type=KERBEROS")
        security_list.append("hive.hdfs.impersonation.enabled=true")
        security_list.append("hive.hdfs.presto.principal=" +
                             params.presto_principal)
        security_list.append("hive.hdfs.presto.keytab=" + params.presto_keytab)
        security = ',\n'.join(security_list)

    File(
        params.conf_dir + '/config.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.config_content),
        mode=0775)
    File(
        params.conf_dir + '/node.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.node_content),
        mode=0775)
    File(
        params.conf_dir + '/jvm.config',
        owner=params.presto_user,
        content=InlineTemplate(params.jvm_content),
        mode=0775)
    File(
        params.conf_dir + '/event-listener.propertie',
        owner=params.presto_user,
        content=InlineTemplate(params.event_listener_content),
        mode=0775)
    File(
        params.conf_dir + '/password-authenticator.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.password_authenticator_content),
        mode=0775)
    File(
        params.conf_dir + '/resource-groups.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.resource_groups_content),
        mode=0775)
    File(
        params.conf_dir + '/resource_groups.json',
        owner=params.presto_user,
        content=InlineTemplate(params.resource_groups_json_content),
        mode=0775)
    File(
        params.conf_dir + '/rules.json',
        owner=params.presto_user,
        content=InlineTemplate(params.rules_content),
        mode=0775)

    File(
        params.conf_dir + '/session-property-config.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.session_content),
        mode=0775)

    File(
        params.conf_dir + '/session_property_config.json',
        owner=params.presto_user,
        content=InlineTemplate(params.session_property_content),
        mode=0775)

    File(
        params.conf_dir + '/catalog/jmx.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.catalog_jmx_content),
        mode=0775)
    File(
        params.conf_dir + '/catalog/hive.properties',
        owner=params.presto_user,
        content=InlineTemplate(params.catalog_hive_content),
        mode=0775)

    if len(params.kafka_broker_hosts) > 0:
        File(
            params.conf_dir + '/catalog/kafka.properties',
            owner=params.presto_user,
            content=InlineTemplate(params.catalog_kafka_content),
            mode=0775)

    if params.hbase_zookeeper_quorum is not None:
        File(
            params.conf_dir + '/catalog/phoenix.properties',
            owner=params.presto_user,
            content=InlineTemplate(params.catalog_phoenix_content),
            mode=0775)


def install_presto_plugin():
    import params
    plugin_dir = params.install_dir + '/plugin/'
    Directory(
        plugin_dir,
        owner=params.presto_user,
        group=params.user_group,
        create_parents=True,
        mode=0755)

    plugin_jar_files_conf = default(
        "/configurations/presto-env/presto_plugins", '')
    if plugin_jar_files_conf.strip() != '':
        import json
        share_jar_files = json.loads(plugin_jar_files_conf.strip().replace("'", '"'))
        for plugin_name, jar_file in share_jar_files.iteritems():
            plugin_name = str(plugin_name)
            jar_file = str(jar_file)
            jar_file_path = plugin_dir + plugin_name + '/' + jar_file.strip()
            if not os.path.exists(jar_file_path):
                Directory(
                    plugin_dir + plugin_name,
                    owner=params.presto_user,
                    group=params.user_group,
                    create_parents=True,
                    mode=0755)
                Execute(
                    'wget ' + download_url_base + '/share/presto/' + jar_file + ' -O ' + jar_file_path,
                    user=params.presto_user)


def install_presto():
    install_presto_plugin()
    import params
    Directory([
        params.conf_dir, params.data_dir, params.log_dir, params.pid_dir,
        params.conf_dir + '/catalog'
    ],
              owner=params.presto_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.presto_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('rm -rf ' + params.install_dir + '/etc')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir + '/etc')
        Execute('chown -R %s:%s %s/%s' % (params.presto_user, params.user_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.presto_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -rf /etc/presto/catalog /tmp/' + params.filename)


class Coordinator(Script):
    def install(self, env):
        install_presto()
        self.configure(env)

    def stop(self, env):
        import params
        env.set_params(params)
        from params import daemon_control_script, presto_user
        Execute('{0} stop'.format(daemon_control_script), user=presto_user)

    def start(self, env):
        import params
        env.set_params(params)
        from params import daemon_control_script, presto_user
        install_presto()
        self.configure(env)
        Execute('{0} start'.format(daemon_control_script), user=presto_user)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status('/var/run/presto/presto.pid')

    def configure(self, env):
        import params
        env.set_params(params)
        config_presto()


if __name__ == '__main__':
    Coordinator().execute()
