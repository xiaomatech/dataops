#!/usr/bin/env bash

backup_dir='/data/backup/namenode/'$(date '+%Y-%m-%d/%H-%M-%S')
current_image='/data/backup/namenode/current'
mkdir -p $backup_dir
hdfs dfsadmin -fetchImage $backup_dir
rm -rf $current_image
ln -s $backup_dir/fsimage_* $current_image