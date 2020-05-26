#!/usr/bin/env bash

yum remove -y postfix mariadb mariadb-libs

yum install -y mysql-community-server gperftools-libs

#mkdir -p /data/mysql/{3306,binlog}
#chown -R mysql:mysql /data/mysql

mysqld --initialize #--datadir=/data/mysql/3306

wget http://assets.example.com/ambari/my.cnf -O /etc/my.cnf

systemctl start mysqld

#update mysql.user set authentication_string=password('123sdfs') where user='root' and Host = 'localhost';
#SET PASSWORD FOR root@localhost=PASSWORD('123sdfs');
#update mysql.user set Host='%' where User='root';
#flush privileges;

create database ambari character set utf8;
source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql;

#echo '123sdfs'>/etc/ambari-server/conf/password.dat