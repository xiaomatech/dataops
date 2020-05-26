from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.check_process_status import check_process_status
import os

from resource_management.libraries.functions import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

dnshttp_systemd = '''
[Unit]
Description=A dnshttp for dnsmasq
After=network.target dnsmasq.target

[Service]
Type=simple
ExecStart=/usr/bin/python /opt/dnshttp.py
TimeoutStopSec=180
Restart=yes

[Install]
WantedBy=multi-user.target
'''


class Master(Script):
    def install(self, env):
        self.install_packages(env)
        dnshttp_file = '/opt/dnshttp.py'
        if not os.path.exists(dnshttp_file):
            Execute('wget ' + download_url_base + '/dnshttp.py -O ' +
                    dnshttp_file)
        Execute('systemctl enable dnshttp')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            '/etc/dnsmasq.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755)
        File(
            '/usr/lib/systemd/system/dnshttp.service',
            content=InlineTemplate(dnshttp_systemd),
            mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop dnsmasq')
        Execute('systemctl stop dnshttp')

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl start dnsmasq')
        Execute('systemctl start dnshttp')

    def status(self, env):
        check_process_status('/var/run/dnsmasq.pid')


if __name__ == "__main__":
    Master().execute()
