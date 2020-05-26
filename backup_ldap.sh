#!/usr/bin/env bash
ldap_url="ldap://ldap.example.com"
dn="cn=Manager,ou=Control,dc=example,dc=com"
password='example.com'
base_dn="dc=example,dc=com"

backup_dir='/data/backup/ldap/'$(date '+%Y-%m-%d/%H-%M-%S')
current_image='/data/backup/ldap/current'
mkdir -p $backup_dir
ldapsearch -x -LLL -H $ldap_url -D $dn -w $password -b $base_dn '(objectClass=*)' >$backup_dir/all.ldif
rm -rf $current_image
ln -s $backup_dir/all.ldif $current_image
