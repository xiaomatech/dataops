import os
from time import sleep
from resource_management import *
from mongo_base import MongoBase

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import File
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


class MongoMaster(MongoBase):
    mongo_packages = ['mongodb-org']

    def install(self, env):
        import params
        env.set_params(params)
        self.installMongo(env)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configureMongo(env)

    def start(self, env):
        import params
        self.configure(env)

        import socket
        current_host_name = socket.getfqdn(socket.gethostname())

        config = Script.get_config()
        shard_prefix = params.shard_prefix

        db_hosts = config['clusterHostInfo']['mongodb_hosts']

        auth_pattern = ''
        print params.auth
        if params.auth:
            print 'add keyFile'
            # add keyfile
            keyfile_path = '/etc/security/'
            keyfile_name = keyfile_path + 'mongodb-keyfile'
            auth_pattern = ' --keyFile ' + keyfile_name
            if current_host_name == db_hosts[0]:
                Execute(
                    format('openssl rand -base64 741 > {keyfile_name}'),
                    logoutput=True)
                Execute(format('chmod 600 {keyfile_name}'), logoutput=True)
                for index, item in enumerate(db_hosts, start=1):
                    Execute(
                        format(
                            'scp {keyfile_name} root@{item}:{keyfile_path}'),
                        logoutput=True)

        len_host = len(db_hosts)
        len_port = len(params.db_ports)

        if len(params.node_group) > 0:
            db_hosts = self.getdbhosts(db_hosts, params.node_group)
        #start shard service
        for index, item in enumerate(db_hosts, start=0):
            if item == current_host_name:
                #foreach db_ports
                for index_p, p in enumerate(params.db_ports, start=0):
                    #rm mongo_*.sock
                    Execute(
                        format('rm -rf /tmp/mongodb-{p}.sock'), logoutput=True)
                    #get shard_name
                    shard_name = shard_prefix + str(
                        (index - index_p) % len_host)
                    #pid_file_name = params.shard_prefix + str((index-index_p)%len_host)
                    #pid_file_name not the same to log,easy to status
                    pid_file_name = params.shard_prefix + str(index_p)
                    #get db_path
                    db_path = params.db_path + '/' + shard_name

                    if os.path.exists(db_path):
                        print "File exists"
                    else:
                        Execute(format('mkdir -p {db_path}'), logoutput=True)
                    log_file = params.log_path + '/' + shard_name + '.log'
                    pid_file = params.pid_db_path + '/' + pid_file_name + '.pid'
                    Execute(
                        format(
                            'mongod -f /etc/mongod.conf --shardsvr  -replSet {shard_name} -port {p} -dbpath {db_path} -oplogSize 100 -logpath {log_file} -pidfilepath {pid_file} {auth_pattern} '
                        ),
                        logoutput=True)

        sleep(5)
        print 'sleep waiting for all mongod started'

        if params.node_group == '':
            members = ''

            index = db_hosts.index(current_host_name)
            shard_name = shard_prefix + str(index)

            current_index = 0
            current_shard = index
            while (current_index < len_port):
                current_host = db_hosts[current_shard]
                current_port = params.db_ports[current_index]
                members = members + '{_id:' + format(
                    '{current_index},host:"{current_host}:{current_port}"')
                if current_index == 0:
                    members = members + ',priority:2'
                members = members + '},'
                current_index = current_index + 1
                current_shard = (current_shard + 1) % len(db_hosts)

            replica_param = 'rs.initiate( {_id:' + format(
                '"{shard_name}",version: 1,members:') + '[' + members + ']})'

            cmd = format(
                'mongo --host {current_host_name} --port 27017 <<EOF \n{replica_param} \nEOF\n'
            )
            File('/var/run/mongo_config.sh', content=cmd, mode=0755)
            Execute('su - mongodb /var/run/mongo_config.sh', logoutput=True)
        else:

            groups = params.node_group.split(';')

            members = ''

            index = db_hosts.index(current_host_name)
            shard_name = shard_prefix + str(index)

            current_index = 0
            current_shard = index
            while (current_index < len_port):
                current_host = db_hosts[current_shard]
                current_port = params.db_ports[current_index]
                members = members + '{_id:' + format(
                    '{current_index},host:"{current_host}:{current_port}"')
                if current_index == 0:
                    members = members + ',priority:2'
                members = members + '},'
                current_index = current_index + 1
                current_shard = (current_shard + 1) % len(db_hosts)

            #if len(groups) > 1 and current_host_name in groups[-1]:
            #    replica_param ='rs.initiate( {_id:'+format('"{shard_name}",version: 1,members:') + '[' + members + ']})'
            #else:
            replica_param = 'rs.reconfig( {_id:' + format(
                '"{shard_name}",version: 1,members:'
            ) + '[' + members + ']},{force:1})'

            cmd = format(
                'mongo --host {current_host_name} --port 27017 <<EOF \n{replica_param} \nEOF\n'
            )
            File('/var/run/mongo_config.sh', content=cmd, mode=0755)
            Execute('/var/run/mongo_config.sh', logoutput=True)

    def stop(self, env):
        print "stop services.."
        import params
        for port in params.db_ports:
            params.shutdown_port = port
            env.set_params(params)
            self.shutDown(env)

    def restart(self, env):
        self.configure(env)
        print "restart mongodb"
        self.stop(env)
        self.start(env)

    def status(self, env):
        db_ports = ["27017", "27018", "27019"]
        for index_p, p in enumerate(db_ports, start=0):
            shard_name = "shard" + str(index_p)
            pid_file = '/var/run/mongodb' + '/' + shard_name + '.pid'
            check_process_status(pid_file)


if __name__ == "__main__":
    MongoMaster().execute()
