from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from agent import install_file


class Collector(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_file('jaeger-collector')

    def configure(self, env):
        import params
        env.set_params(params)
        conf_content = '''
        SPAN_STORAGE_TYPE=elasticsearch
        ES_SERVER_URLS=''' + params.es_url + '''
        '''
        File(
            params.conf_dir + '/jaeger',
            content=conf_content,
            mode=0755,
            owner=params.jaeger_user,
            group=params.user_group)
        systemd_content = '''
        [Unit]
        Description=Etcd Server
        After=network.target
        After=network-online.target
        Wants=network-online.target
        [Service]
        Type=notify
        EnvironmentFile=-''' + params.conf_dir + '''/jaeger
        User=etcd
        ExecStart=/usr/sbin/jaeger-collector
        Restart=on-failure
        RestartSec=5
        LimitNOFILE=1048576
        [Install]
        WantedBy=multi-user.target
        '''
        File(
            '/usr/lib/systemd/system/jaeger-collector.service',
            content=systemd_content,
            mode=0755,
            owner=params.jaeger_user,
            group=params.user_group)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop jaeger-collector')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start jaeger-collector')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status jaeger-collector')


if __name__ == "__main__":
    Collector().execute()
