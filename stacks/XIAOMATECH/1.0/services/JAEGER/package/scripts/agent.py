from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.resources.system import Directory

import os
from resource_management.libraries.functions.default import default


def install_file(file_name):
    import params
    Directory([params.data_dir, params.conf_dir],
              owner=params.jaeger_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    download_url_base = default(
        "/configurations/cluster-env/download_url_base",
        'http://assets.example.com/')
    file_path = '/usr/sbin/' + file_name
    if not os.path.exists(file_path):
        Execute('wget ' + download_url_base + '/jaeger/' + file_name + ' -O ' + file_path,
                user=params.jaeger_user)
        Execute('chmod a+x ' + file_path)


class Agent(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_file('jaeger-agent')

    def configure(self, env):
        import params
        env.set_params(params)
        systemd_content = '''
        [Unit]
        Description=Jaeger Agent
        After=network.target
        After=network-online.target
        Wants=network-online.target
        [Service]
        Type=notify
        User=etcd
        ExecStart=/usr/sbin/jaeger-agent --collector.host-port ''' + params.collector_host_url + '''
        Restart=on-failure
        RestartSec=5
        LimitNOFILE=1048576
        [Install]
        WantedBy=multi-user.target
        '''
        File(
            '/usr/lib/systemd/system/jaeger-agent.service',
            content=systemd_content,
            mode=0755,
            owner=params.jaeger_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop jaeger-agent')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start jaeger-agent')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status jaeger-agent')


if __name__ == "__main__":
    Agent().execute()
