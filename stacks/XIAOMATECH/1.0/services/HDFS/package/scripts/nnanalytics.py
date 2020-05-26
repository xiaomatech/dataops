from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.libraries.functions.check_process_status import check_process_status
import os

systemd = '''
[Unit]
Description=NameNode Analytics
After=network.target
After=NetworkManager.target

[Service]
Type=forking
ExecStart=/bin/bash -c "ulimit -c unlimited; /usr/local/nn-analytics/bin/nn-analytics start"
ExecStop=/bin/bash -c "/usr/local/nn-analytics/bin/nn-analytics stop"
TimeoutStopSec=20
User=hdfs
Group=hadoop
PIDFile=/var/run/nn-analytics.pid
LimitNOFILE=1048576
LimitNPROC=-1
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
Alias=nn-analytics.service
'''


class NNanalytics(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('yum install -y nn-analytics')
        File(
            '/usr/lib/systemd/system/nn-analytics.service',
            owner='root',
            group='root',
            mode=0644,
            content=InlineTemplate(systemd))
        nn_java_path = '/usr/java/latest'
        if not os.path.exists(nn_java_path):
            Execute('ln -s %s %s ' % (params.java_home, nn_java_path))
            
        Execute("systemctl daemon-reload")

    def configure(self, env):
        import params
        env.set_params(params)
        XmlConfig(
            "hdfs-site.xml",
            conf_dir='/usr/local/nn-analytics/config/',
            configurations=params.config['configurations']['hdfs-site'],
            configuration_attributes=params.config['configurationAttributes']
            ['hdfs-site'],
            owner=params.hdfs_user,
            group=params.user_group)

        XmlConfig(
            "core-site.xml",
            conf_dir='/usr/local/nn-analytics/config/',
            configurations=params.config['configurations']['core-site'],
            configuration_attributes=params.config['configurationAttributes']
            ['core-site'],
            owner=params.hdfs_user,
            group=params.user_group,
            mode=0644,
            xml_include_file=params.mount_table_xml_inclusion_file_full_path)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)

        Execute("systemctl start nn-analytics")

    def stop(self, env):
        import params
        env.set_params(params)
        Execute("systemctl stop nn-analytics")

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status('/var/run/nn-analytics.pid')


if __name__ == "__main__":
    NNanalytics().execute()
