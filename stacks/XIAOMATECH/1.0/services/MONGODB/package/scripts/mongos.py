from time import sleep
from resource_management import *
from mongo_base import MongoBase

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


class MongoMaster(MongoBase):
    PID_FILE = '/var/run/mongodb/mongos.pid'

    def install(self, env):
        self.installMongo(env)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configureMongo(env)

    def start(self, env):
        import params
        env.set_params(params)
        sleep(3)
        #waiting for mongod start
        auth_pattern = ''
        if params.auth:
            print 'add keyFile'
            # add keyfile
            keyfile_path = '/etc/security/'
            keyfile_name = keyfile_path + 'mongodb-keyfile'
            auth_pattern = ' --keyFile ' + keyfile_name

        self.configure(env)
        Execute('rm -rf /tmp/mongodb-30000.sock', logoutput=True)
        config = Script.get_config()
        nodes = config['clusterHostInfo']['mongodc_hosts']
        hosts = ''
        for ip in nodes:
            hosts = hosts + ip + ":20000,"
        hosts = hosts[:-1]
        pid_file = self.PID_FILE
        port = params.mongos_tcp_port
        cmd = format(
            'mongos -configdb {hosts} -port {port} -logpath  /var/log/mongodb/mongos.log  {auth_pattern} & echo $! > {pid_file} '
        )
        Execute(cmd, logoutput=True)
        len_port = len(params.db_ports)

        import socket
        current_host_name = socket.getfqdn(socket.gethostname())

        #Add Shards to the Cluster
        shard_param = ''

        #node_group = ','.join(config['clusterHostInfo']['mongodb_hosts'])

        #groups = node_group.split(';')
        db_hosts = config['clusterHostInfo']['mongodb_hosts']
        if len(params.node_group) > 0:
            db_hosts = self.getdbhosts(db_hosts, params.node_group)

        len_host = len(db_hosts)
        shard_prefix = params.shard_prefix
        for index, item in enumerate(db_hosts, start=0):
            current_shard = index
            current_index = 0
            shard_nodes = ''
            while (current_index < len_port):
                current_index_host = db_hosts[current_shard]
                current_index_port = params.db_ports[current_index]
                shard_nodes = shard_nodes + format(
                    '{current_index_host}:{current_index_port},')
                current_index = current_index + 1
                current_shard = (current_shard + 1) % len_host
            shard_name = shard_prefix + str(index)
            shard_nodes = shard_nodes[:-1]
            shard_param = shard_param + "db.shards.update( { '_id' : '" + shard_name + "'},{'_id' : '" + shard_name + "','host':'" + shard_name + "/" + shard_nodes + "'},true);\n"
        cmd = 'mongo --host ' + current_host_name + ' --port ' + port + ' <<EOF\n  use config; \n ' + shard_param + ' \nEOF\n'
        File('/var/run/mongos.sh', content=cmd, mode=0755)
        sleep(5)
        Execute(
            'su - mongodb /var/run/mongos.sh',
            logoutput=True,
            try_sleep=3,
            tries=5)

        service_packagedir = params.service_packagedir
        register_user_path = service_packagedir + '/scripts/register_user.sh'
        File(
            register_user_path,
            content=Template("register_user.sh.j2"),
            mode=0777)
        cmd = format("{service_packagedir}/scripts/register_user.sh")
        Execute('echo "Running ' + cmd + '" as root')
        Execute(cmd, logoutput=True, ignore_failures=True)
        cmd = format("rm -rf {service_packagedir}/scripts/register_user.sh")
        Execute(cmd, logoutput=True)

    def stop(self, env):
        #no need stop
        print("stop mongos")
        import params
        params.shutdown_port = params.mongos_tcp_port
        env.set_params(params)
        self.shutDown(env)

    def restart(self, env):
        #no need restart
        print("restart")
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status(self.PID_FILE)


if __name__ == "__main__":
    MongoMaster().execute()
