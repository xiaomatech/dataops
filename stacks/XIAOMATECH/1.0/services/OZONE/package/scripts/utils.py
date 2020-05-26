import os
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute, Directory, File, Link
from resource_management.core.resources import Package
from resource_management.core.source import Template
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.check_process_status import check_process_status


def install_ozone():
    import params
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute('/bin/rm -f /tmp/' + params.filename)
        Execute('wget ' + params.download_url + ' -O /tmp/' + params.filename, user=params.hdfs_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/etc/hadoop')
        Execute('ln -s ' + params.hadoop_conf_dir + ' ' + params.install_dir +
                '/etc/hadoop')
        Execute('mkdir ' + params.install_dir + '/logs && chmod 777 ' +
                params.install_dir + '/logs')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/ozone.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.hdfs_user, params.user_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.hdfs_user, params.user_group,
                                       params.install_dir))
        Execute('chmod -R 755 %s/%s' % (params.stack_root, params.version_dir))
        Execute('chown root:%s %s/bin/container-executor' %
                (params.user_group, params.install_dir))

        Execute('/bin/rm -f /tmp/' + params.filename)


def config_ozone():
    pass


def ozone(name='scm', action='start'):
    pass
