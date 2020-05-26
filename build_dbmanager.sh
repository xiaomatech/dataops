#!/usr/bin/env bash
yum install -y python36-devel python36-setuptools mysql-devel python-devel openldap-devel openssl-devel
easy_install-3.6 pip
cd /opt
virtualenv venv4archery --python=python3.6
git clone https://github.com/hhyo/archery.git && cd archery
source /opt/venv4archery/bin/activate
pip3 install -r /opt/archery/src/docker/requirements.txt
cd /opt/archery
cat archery/settings.py #edit config
python3.6 manage.py makemigrations sql
python3.6 manage.py migrate
python3.6 manage.py createsuperuser

cd /opt
virtualenv venv4schemasync  --python=python2
source venv4schemasync/bin/activate
git clone https://github.com/hhyo/SchemaSync.git
git clone https://github.com/hhyo/SchemaObject.git
cd SchemaObject && python setup.py install
cd ../SchemaSync && python setup.py install
cd /opt && rm -rf /opt/SchemaObject/ && rm -rf /opt/SchemaSync/
pip install mysql-python


rm -rf /opt/archery/.git
cd /opt
tar -czvf archery-1.0.tar.gz archery venv4archery venv4schemasync

ls /opt/archery.tar.gz

repo_dir_base=/data/assets
cp /opt/archery.tar.gz $repo_dir_base/archery.tar.gz