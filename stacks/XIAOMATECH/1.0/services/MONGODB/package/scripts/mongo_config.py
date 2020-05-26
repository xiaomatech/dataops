from resource_management import *
from mongo_base import MongoBase
from resource_management.libraries.functions.check_process_status import check_process_status


class MongoMaster(MongoBase):
    PID_CONFIG_FILE = '/var/run/mongodb/mongod-config.pid'

    def install(self, env):
        self.installMongo(env)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configureMongo(env)

    def start(self, env):
        import params
        self.configure(env)
        print "start mongodb"
        auth_pattern = ''
        if params.auth:
            print 'add keyFile'
            # add keyfile
            keyfile_path = '/etc/security/'
            keyfile_name = keyfile_path + 'mongodb-keyfile'
            auth_pattern = ' --keyFile ' + keyfile_name
        Execute(
            'rm -rf /tmp/mongodb-20000.sock',
            logoutput=True,
            try_sleep=3,
            tries=5)
        Execute(
            format(
                'mongod -f /etc/mongod-config.conf -port 20000 {auth_pattern}'
            ),
            logoutput=True,
            try_sleep=3,
            tries=5)

    def stop(self, env):
        print "stop services.."
        import params
        params.shutdown_port = '20000'
        env.set_params(params)
        self.shutDown(env)

    def restart(self, env):
        self.configure(env)
        print "restart mongodb"
        self.stop(env)
        self.start(env)

    def status(self, env):
        print "checking status..."
        check_process_status(self.PID_CONFIG_FILE)


if __name__ == "__main__":
    MongoMaster().execute()
