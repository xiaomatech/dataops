#!/bin/bash

#
# Set script vars
#
SCRIPT_NAME=$(basename $0)
SCRIPT_DIR=`cd $(dirname $0) && pwd`

#
# Parse the args
#
LDAP_PASSWORD="$1"
LDAP_ADMIN_USER="$2"
LDAP_DOMAIN="$3"
LDAP_LDIF_DIR="$4"
LDAP_OU="$5"
ROOT_DN="$6"

echo -e "\n####  Installing OpenLDAP with the following args:
	password: $LDAP_PASSWORD
	admin user: $LDAP_ADMIN_USER
	ldap domain: $LDAP_DOMAIN
	ldif dir: $LDAP_LDIF_DIR
	rootdn : $ROOT_DN
"

#
# Start slapd on boot
#
echo -e "\n####  Enabling slapd to start on boot"
chkconfig --level 2345 slapd on


#
# Enabling logging
#
echo -e "\n####  Enabling OpenLDAP logging"
if [ ! -d "/var/log/slapd" ]; then
    mkdir /var/log/slapd
fi
chmod 755 /var/log/slapd/
chown ldap:ldap /var/log/slapd/
# Copy the schema and fix ownership
cp /usr/share/doc/krb5-server-ldap-*/kerberos.* /etc/openldap/schema/
cp /usr/share/doc/sudo-*/schema.OpenLDAP /etc/openldap/schema/sudoers.schema

chown -R ldap:ldap /var/lib/ldap /etc/openldap

# Remove existing config database and database files
rm -rf /etc/openldap/slapd.d/*
rm -rf /var/lib/ldap/*

#
# Copy DB_CONFIG and fix ownership
#
echo -e "\n####  Copying DB_CONFIG and fixing ownership"
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
echo "" | slapadd -f /etc/openldap/slapd.conf
chown -R ldap:ldap /var/lib/ldap /etc/openldap


#
# Fix ownership
#
echo -e "\n####  Fixing ownership"
chown -R ldap:ldap /var/lib/ldap /etc/openldap


#
# Start slapd
#
echo -e "\n####  Starting slapd"
service slapd start


#
# Setup ldif files
#
echo -e "\n####  Set domain in ldif files to $LDAP_DOMAIN"
sed -i "s/dc=example,dc=com/$LDAP_DOMAIN/g" $LDAP_LDIF_DIR/*.ldif
sed -i "s/ou: example.com/ou: $LDAP_OU/g" $LDAP_LDIF_DIR/*.ldif

#
# Add the base ou's
#
echo -e "\n####  Adding the base OU's"
ldapadd -D $ROOT_DN -w $LDAP_PASSWORD -f $LDAP_LDIF_DIR/base.ldif
ldapadd -D $ROOT_DN -w $LDAP_PASSWORD -f $LDAP_LDIF_DIR/cisco.ldif
ldapadd -D $ROOT_DN -w $LDAP_PASSWORD -f $LDAP_LDIF_DIR/wifi.ldif
ldapadd -D $ROOT_DN -w $LDAP_PASSWORD -f $LDAP_LDIF_DIR/freeradius.ldif
#
# Install phpldapadmin
#
echo -e "\n####  Installing phpldapadmin"
yum install -y phpldapadmin

#
# Configure phpldapadmin
#
echo -e "\n####  Configuring phpldapadmin"
sed -i "s#Require local#Require all granted#g" /etc/httpd/conf.d/phpldapadmin.conf
sed -i "s#^\$servers->setValue('login','attr','uid');#//\$servers->setValue('login','attr','uid');#g" /etc/phpldapadmin/config.php

#
# Start httpd on boot
#
echo -e "\n####  Starting and enabling httpd to start on boot"
chkconfig --level 2345 httpd on
service httpd start
