#!/usr/bin/env bash

export HADOOP_CLIENT_OPTS="-Xmx10240m"
export HADOOP_OPTS="-Xmx10240m"

HDFS_PATH="/fsimage/"

SPARK_DRIVER_MEM="4G"
SPARK_EXECUTOR_MEM="6G"

DATE=`date +"%Y-%m-%d"`

mkdir -p /data/fsimage

hdfs dfsadmin -rollEdits
hdfs dfsadmin -fetchImage /data/fsimage/fsimage_$DATE
hdfs oiv -i /data/fsimage/fsimage_$DATE -o /data/fsimage/fsimage_$DATE.tsv -p Delimited


hdfs dfs -put -f /data/fsimage/fsimage_$DATE.tsv $HDFS_PATH

rm -f /data/fsimage/fsimage_$DATE
rm -f /data/fsimage/fsimage_$DATE.tsv

spark2-submit --executor-memory $SPARK_EXECUTOR_MEM --driver-memory $SPARK_DRIVER_MEM fsimage_analyzer.py