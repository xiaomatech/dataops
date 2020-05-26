from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Directory


class Nginx(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Directory([
            params.log_dir, params.conf_dir + '/vhost',
                            params.conf_dir + '/upstream',
                            params.conf_dir + '/stream_upstream',
                            params.conf_dir + '/stream_vhost', params.pid_dir
        ],
            owner=params.nginx_user,
            group=params.nginx_group,
            mode=0775,
            create_parents=True)
        Execute('systemctl enable openresty')
        Execute('cp -rf ' + params.agent_resty_dir +
                '/* /usr/local/openresty/site/lualib/resty/')
        Execute('mkdir -p ' + params.conf_dir + '/lua/ ' + params.conf_dir +
                '/vendor/')
        Execute('cp -rf' + params.agent_resty_dir + '/etl.lua  ' +
                params.conf_dir + '/lua/etl.lua')
        Execute('cp -rf' + params.agent_resty_dir + '/init.lua  ' +
                params.conf_dir + '/lua/init.lua')
        Execute('cp -rf' + params.agent_resty_dir + '/log2kafka.lua  ' +
                params.conf_dir + '/lua/log2kafka.lua')
        Execute('cp -rf' + params.agent_resty_dir + '/ip2location.datx  ' +
                params.conf_dir + '/vendor/ip2location.datx')
        Execute('cp -rf' + params.agent_resty_dir + '/phone.dat  ' +
                params.conf_dir + '/vendor/phone.dat')
        Execute('cp -rf' + params.agent_resty_dir + '/server_util.conf  ' +
                params.conf_dir + '/server_util.conf')

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_dir + '/nginx.conf',
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner=params.nginx_user,
            group=params.nginx_group)
        if len(params.clickhouse_hosts) > 0:
            File('/etc/clicktail/clicktail.conf',
                 content=InlineTemplate(params.clicktail_content),
                 mode=0755)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop openresty')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('systemctl start openresty')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status openresty')


if __name__ == "__main__":
    Nginx().execute()
