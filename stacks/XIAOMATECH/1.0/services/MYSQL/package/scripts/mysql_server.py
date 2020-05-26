from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.source import StaticFile


class MysqlServer(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('systemctl reset-failed')
        Execute('systemctl disable mysqld')
        Execute('chkconfig mysqld_multi on')
        self.configure(env)
        Execute(
            'mkdir -p /data{0,1,2,3}/mysql /data{0,1,2,3}/binlog /data{0,1,2,3}/redolog /data{0,1,2,3}/undolog /data{0,1,2,3}/relaylog /data1/log/mysql /data/backup/mysql',
            user='mysql')

        Execute(
            'mkdir -p /data{0,1,2,3}/tokudbdata /data{0,1,2,3}/tokudblog /data{0,1,2,3}/tokudbtmp',
            user='mysql')

        Execute(
            'mkdir -p /data{0,1,2,3}/rocksdbdata /data{0,1,2,3}/rocksdbwal /data{0,1,2,3}/rocksdbtmp',
            user='mysql')

        Execute(
            '/usr/sbin/mysqld --initialize --init-file=/var/lib/mysql-files/privileges --datadir=/data0/mysql --relay-log=/data0/relaylog --innodb-undo-directory=/data0/undolog --innodb-data-home-dir=/data0/binlog --innodb-log-group-home-dir=/data0/redolog --lc-messages-dir=/usr/share/percona-server --lc-messages=en_US',
            user='mysql')
        Execute(
            '/usr/sbin/mysqld --initialize --init-file=/var/lib/mysql-files/privileges --datadir=/data1/mysql --relay-log=/data1/relaylog --innodb-undo-directory=/data1/undolog --innodb-data-home-dir=/data1/binlog --innodb-log-group-home-dir=/data1/redolog --lc-messages-dir=/usr/share/percona-server --lc-messages=en_US',
            user='mysql')
        Execute(
            '/usr/sbin/mysqld --initialize --init-file=/var/lib/mysql-files/privileges --datadir=/data2/mysql --relay-log=/data2/relaylog --innodb-undo-directory=/data2/undolog --innodb-data-home-dir=/data2/binlog --innodb-log-group-home-dir=/data2/redolog --lc-messages-dir=/usr/share/percona-server --lc-messages=en_US',
            user='mysql')
        Execute(
            '/usr/sbin/mysqld --initialize --init-file=/var/lib/mysql-files/privileges --datadir=/data3/mysql --relay-log=/data3/relaylog --innodb-undo-directory=/data3/undolog --innodb-data-home-dir=/data3/binlog --innodb-log-group-home-dir=/data3/redolog --lc-messages-dir=/usr/share/percona-server --lc-messages=en_US',
            user='mysql')

        Execute(
            'chown -R mysql:mysql /data{0,1,2,3}/mysql /data1/log/mysql /data{0,1,2,3}/binlog /data{0,1,2,3}/relaylog /data{0,1,2,3}/undolog /data{0,1,2,3}/redolog /data/backup/mysql /data{0,1,2,3}/tokudbdata /data{0,1,2,3}/tokudblog /data{0,1,2,3}/tokudbtmp /data{0,1,2,3}/rocksdbtmp /data{0,1,2,3}/rocksdbwal /data{0,1,2,3}/rocksdbdata'
        )

        Execute('systemctl enable mysqld@3306 ')
        Execute('systemctl enable mysqld@3307 ')
        Execute('systemctl enable mysqld@3308 ')
        Execute('systemctl enable mysqld@3309 ')

    def clean(self, env):
        import params
        env.set_params(params)

    def configure(self, env):
        import params
        env.set_params(params)
        File(
            params.conf_file,
            content=InlineTemplate(params.conf_content),
            mode=0755,
            owner='mysql',
            group='mysql')
        File(
            '/var/lib/mysql-files/privileges',
            content=InlineTemplate(params.privileges),
            mode=0755,
            owner='mysql',
            group='mysql')
        File(
            '/etc/sysconfig/mysql',
            content='''
LD_PRELOAD=/usr/lib64/libjemalloc.so.1 /usr/lib64/mysql/libHotBackup.so
THP_SETTING=never             
             ''',
            mode=0755,
            user='mysql')

        File(
            '/var/lib/mysql-files/group_replication_first.sql',
            content=StaticFile("group_replication_first.sql"),
            mode=0755,
            user='mysql')
        File(
            '/var/lib/mysql-files/group_replication_other.sql',
            content=StaticFile("group_replication_other.sql"),
            mode=0755,
            user='mysql')
        if len(params.clickhouse_hosts) > 0:
            File('/etc/clicktail/clicktail.conf',
                 content=InlineTemplate(params.clicktail_slow_content),
                 mode=0755)
            File('/etc/clicktail/clicktail_audit.conf',
                 content=InlineTemplate(params.clicktail_audit_content),
                 mode=0755)

    def start(self, env):
        import params
        env.set_params(params)
        Execute('systemctl start mysqld@3306 ')
        Execute('systemctl start mysqld@3307 ')
        Execute('systemctl start mysqld@3308 ')
        Execute('systemctl start mysqld@3309 ')

    def stop(self, env):
        import params
        env.set_params(params)
        Execute('systemctl stop mysqld@3306 ')
        Execute('systemctl stop mysqld@3307 ')
        Execute('systemctl stop mysqld@3308 ')
        Execute('systemctl stop mysqld@3309 ')

    def status(self, env):
        import params
        env.set_params(params)
        Execute('systemctl status mysqld@3306 ')
        Execute('systemctl status mysqld@3307 ')
        Execute('systemctl status mysqld@3308 ')
        Execute('systemctl status mysqld@3309 ')


if __name__ == "__main__":
    MysqlServer().execute()
