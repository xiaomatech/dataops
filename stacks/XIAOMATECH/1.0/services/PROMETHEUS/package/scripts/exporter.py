from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate


class Exporter(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        for exporter in params.exporter_lists:
            if exporter != '':
                params.install_from_file(file_name=exporter)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/blackbox.yml',
            content=InlineTemplate(params.blackbox_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            params.conf_dir + '/statsd.yml',
            content=InlineTemplate(params.statsd_content),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/blackbox_exporter.service',
            content=InlineTemplate(params.blackbox_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/snmp_exporter.service',
            content=InlineTemplate(params.snmp_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/statsd_exporter.service',
            content=InlineTemplate(params.statsd_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)
        File(
            '/usr/lib/systemd/system/graphite_exporter.service',
            content=InlineTemplate(params.graphite_systemd),
            mode=0755,
            owner=params.prometheus_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop blackbox_exporter')
        Execute('systemctl stop snmp_exporter')
        Execute('systemctl stop statsd_exporter')
        Execute('systemctl stop graphite_exporter')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start blackbox_exporter')
        Execute('systemctl start snmp_exporter')
        Execute('systemctl start statsd_exporter')
        Execute('systemctl start graphite_exporter')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status blackbox_exporter')
        Execute('systemctl status snmp_exporter')
        Execute('systemctl status statsd_exporter')
        Execute('systemctl status graphite_exporter')


if __name__ == "__main__":
    Exporter().execute()
