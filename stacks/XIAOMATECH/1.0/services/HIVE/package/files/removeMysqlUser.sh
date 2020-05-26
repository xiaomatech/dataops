#!/usr/bin/env bash

mysqldservice=$1
mysqldbuser=$2
userhost=$3
myhostname=$(hostname -f)
sudo_prefix = "/var/lib/ambari-agent/ambari-sudo.sh -H -E"

$sudo_prefix service $mysqldservice start
echo "Removing user $mysqldbuser@$userhost"
/var/lib/ambari-agent/ambari-sudo.sh su mysql -s /bin/bash - -c "mysql -u root -e \"DROP USER '$mysqldbuser'@'$userhost';\""
/var/lib/ambari-agent/ambari-sudo.sh su mysql -s /bin/bash - -c "mysql -u root -e \"flush privileges;\""
$sudo_prefix service $mysqldservice stop
