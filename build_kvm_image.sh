#!/usr/bin/env bash

yum install -y libguestfs-tools

systemctl start libvirtd

wget https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 -O /tmp/centos7.qcow2

virt-customize -a /tmp/centos7.qcow2 --root-password password:admin
virt-customize -a /tmp/centos7.qcow2 --ssh-inject centos:string:"`cat /root/.ssh/id_rsa.pub`"

mkdir -p /mnt/centos7
guestmount -a /tmp/centos7.qcow2 -i --rw /mnt/centos7

unalias cp

cp /etc/resolv.conf /mnt/centos7/etc/resolv.conf
cp /etc/localtime /mnt/centos7/etc/localtime
cp /etc/sudoers /mnt/centos7/etc/sudoers
cp /etc/chrony.conf /mnt/centos7/etc/chrony.conf

rm -rf /mnt/centos7/etc/yum.repos.d/*
cp /etc/yum.repos.d/hadoop.repo /mnt/centos7/etc/yum.repos.d/hadoop.repo

if [-f /root/.ssh/authorized_keys]; then
    mkdir --mode=700 /mnt/centos7/root/.ssh
    cp /root/.ssh/authorized_keys /mnt/centos7/root/.ssh/authorized_keys
    chmod 600 /mnt/centos7/root/.ssh/authorized_keys
fi

umount /mnt/centos7

ls /tmp/centos7.qcow2

repo_dir_base=/data/assets

cp /opt/centos7.qcow2 $repo_dir_base/centos7.qcow2
