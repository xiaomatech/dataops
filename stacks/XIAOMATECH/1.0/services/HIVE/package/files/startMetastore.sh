#!/usr/bin/env bash
source /etc/hive/hive-env.sh

HIVE_CONF_DIR=$4 $HADOOP_HOME/bin/hadoop jar $HIVE_HOME/lib/hive-metastore-*.jar org.apache.hadoop.hive.metastore.HiveMetaStore > $1 2> $2 &
echo $!|cat>$3
