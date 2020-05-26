#!/usr/bin/env bash
repo_dir_base=/data/assets

yum install -y python36-devel python36-setuptools python36-pip
pip install virtualenv
cd /opt
virtualenv pythonenv --python=python3.6

source pythonenv/bin/activate
pip install -r ml_requirements.txt
tar -czvf pythonenv.tar.gz pythonenv

cp pythonenv.tar.gz $repo_dir_base/