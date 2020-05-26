#!/usr/bin/env bash

yum install -y python36-devel python36-setuptools python36-pip
pip install virtualenv
cd /opt

#graphite-web
virtualenv graphite --python=python3.6
source graphite/bin/activate
pip install gunicorn cffi requests
pip install --no-binary=:all: https://github.com/graphite-project/graphite-web/tarball/master
tar -czvf graphite.tar.gz graphite

#graphite-api
cd /opt
virtualenv graphite-api --python=python3.6
source graphite-api/bin/activate
pip install graphite-api[cache]
pip install gunicorn requests
tar -czvf graphite-api.tar.gz graphite-api

ls *.tar.gz

repo_dir_base=/data/assets
cp /opt/graphite.tar.gz $repo_dir_base/graphite.tar.gz
cp /opt/graphite-api.tar.gz $repo_dir_base/graphite-api.tar.gz