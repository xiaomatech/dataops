#!/usr/bin/env bash

download_server=$(hostname -f)
password=admin123!@#

yum install -y wget

rm -rf /etc/yum.repos.d/*

wget http://assets.example.com/hadoop.repo -O /etc/yum.repos.d/ambari.repo

yum install -y ambari-server java-1.8.0-openjdk openldap-clients nss-pam-ldapd authconfig


if [ ! -f /usr/lib/ambari-server/mysql-connector-java-5.1.47.jar ]; then
    wget http://assets.example.com/mysql-connector-java-5.1.47.jar -O /usr/lib/ambari-server/mysql-connector-java.jar
fi
if [ ! -f /usr/share/java/mysql-connector-java-5.1.47.jar ] ; then
    wget http://assets.example.com/mysql-connector-java-5.1.47.jar -O /usr/share/java/mysql-connector-java.jar
fi


sed -i -e 's/-Xmx2048m/-Xmx64g/g' /var/lib/ambari-server/ambari-env.sh
sed -i -e 's/-Xms512m/-Xms64g/g' /var/lib/ambari-server/ambari-env.sh

wget http://assets.example.com/ambari/ambari.properties -O /etc/ambari-server/conf/ambari.properties

rm -rf /var/lib/ambari-server/resources/stacks/XIAOMATECH
wget http://assets.example.com/ambari/stacks.tar.gz -O /tmp/stacks.tar.gz
cd /var/lib/ambari-server/resources && tar -zxvf /tmp/stacks.tar.gz && rm -rf /tmp/stacks.tar.gz

find /var/lib/ambari-server/resources/stacks* -type f -exec sed -i -e "s/assets.example.com/"$download_server"/g" {} \;

find /var/lib/ambari-server/resources/stacks* -type f -exec sed -i -e "s/example!@#/"$password"/g" {} \;

rm -rf /var/lib/ambari-server/resources/stack-hooks
wget http://assets.example.com/ambari/stack-hooks.tar.gz -O /tmp/stack-hooks.tar.gz
cd /var/lib/ambari-server/resources/ && tar -zxvf /tmp/stack-hooks.tar.gz && rm -rf /tmp/stack-hooks.tar.gz

ambari-server setup --jdbc-db=mysql --jdbc-driver=/usr/share/java/mysql-connector-java.jar

chown -R root:root /var/lib/ambari-server/resources

sed -i -e "s/if (!validator.isValidDataNodeDir(value)) return Em.I18n.t('errorMessage.config.directory.heterogeneous');//g" /usr/lib/ambari-server/web/javascripts/app.js
sed -i -e "s/if (!validator.isValidDir(value)) return Em.I18n.t('errorMessage.config.directory.default');//g" /usr/lib/ambari-server/web/javascripts/app.js
sed -i -e "s/return Em.I18n.t('errorMessage.config.directory.allowed');//g" /usr/lib/ambari-server/web/javascripts/app.js
#ambari-server setup

chkconfig ambari-server on

ambari-server start

#genarate ldap password
#slappasswd

#rpm -e --nodeps postgresql-libs postgresql postgresql-server

#/usr/sbin/authconfig --enablekrb5 --enableshadow --useshadow --enablelocauthorize --enableldap --enableldapauth --ldapserver="ldap://ldap.example.com/ ldap://ldap2.example.com/" --ldapbasedn="dc=example,dc=com" --update