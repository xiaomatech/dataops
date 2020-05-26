import os
import socket
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template, StaticFile
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.resources.system import Directory

from resource_management.libraries.functions.default import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

systemd_content = '''
[Unit]
Description=Redis persistent key-value database
After=network.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis/instances/%d.conf --supervised systemd
ExecStop=/usr/libexec/redis-shutdown
Type=notify
User=redis
Group=redis
RuntimeDirectory=/data/redis
RuntimeDirectoryMode=0755
LimitNOFILE=1024000
Restart=on-failure

[Install]
WantedBy=multi-user.target
'''

redis_content = '''
include /etc/redis/common.conf            
bind %s
port %d
cluster-config-file /etc/redis/nodes-%d.conf

pidfile /var/run/redis/%d.pid
dir /data/redis/%d
dbfilename dump-%d.rdb
appendfilename appendonly-%d.aof
logfile /var/log/redis/%d.log
'''


class RedisMaster(Script):
    start_port = 6379
    end_port = 6396
    data_dir = '/data/redis'

    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)

        Directory([self.data_dir, '/etc/redis/instances', '/var/log/redis', '/var/run/redis'],
                  owner='redis',
                  group='redis',
                  mode=0775,
                  create_parents=True)

    def configure(self, env):
        import params
        env.set_params(params)
        File('/etc/redis/common.conf',
             mode=0644,
             content=params.redis_content
             )

        for instance in range(self.start_port, self.end_port):
            Directory([self.data_dir + '/%d' % instance],
                      owner='redis',
                      group='redis',
                      mode=0775,
                      create_parents=True)

            File('/etc/redis/instances/%d.conf' % instance,
                 mode=0644,
                 content=redis_content % (
                     params.hostname, instance, instance, instance, instance, instance, instance, instance)
                 )
            File('/usr/lib/systemd/system/redis@%d.service' % instance,
                 mode=0644,
                 content=systemd_content % instance)

        Execute('systemctl daemon-reload')

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        for instance in range(self.start_port, self.end_port):
            Execute('systemctl start redis@%d' % instance, ignore_failures=True)

        lock_file = '/tmp/redis_join_lock'
        ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        redis_hosts = [ip + ':%d' % instance for instance in range(self.start_port, self.end_port)]

        if not os.path.exists(lock_file):
            with open(lock_file, 'w') as f:
                f.write('1')
            if params.master_host == params.hostname.strip():
                Execute("echo 'yes' | redis-cli --cluster create " + ' '.join(redis_hosts) + " --cluster-replicas 1",
                        try_sleep=10,
                        ignore_failures=True)
            else:
                for instance in range(self.start_port, self.end_port):
                    if (instance - self.start_port) % 2 == 0:
                        Execute('redis-cli --cluster add-node %s %s' % (
                            ip + ':' + str(instance), params.master_host + ':' + str(self.start_port)))
                    else:
                        Execute('redis-cli --cluster add-node %s %s --cluster-slave' % (
                            ip + ':' + str(instance), params.master_host + ':' + str(self.start_port)))

                Execute(
                    'redis-cli --cluster reshard ' + params.master_host + ':' + str(self.start_port) + ' --cluster-yes')

    def stop(self, env):
        import params
        env.set_params(params)
        for instance in range(self.start_port, self.end_port):
            Execute('systemctl stop redis@%d' % instance, ignore_failures=True)

    def post_start(self, env):
        import params
        env.set_params(params)

    def status(self, env):
        import params
        env.set_params(params)
        for pid_file in self.get_pid_files():
            check_process_status(pid_file)

    def get_pid_files(self):
        return ['/var/run/redis/%d.pid' % instance for instance in range(self.start_port, self.end_port)]


if __name__ == "__main__":
    RedisMaster().execute()
