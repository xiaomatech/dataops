"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.hook import Hook
from resource_management.core.resources.packaging import Package
from resource_management.libraries.functions import default
from resource_management.libraries.functions import format
import urllib2
import json
import socket
import time
import os

from random import shuffle

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')

CONST_RACK_INFO_URL = 'http://cmdb.example.com/v1/rack/'

base_lock_dir = '/var/lock/'


def install_mysql_connector():
    import params
    mysql_connector_file = '/usr/share/java/mysql-connector-java.jar'
    if not os.path.exists(mysql_connector_file):
        Execute('mkdir -p /usr/share/java/')
        Execute('wget ' + params.download_url_base + '/mysql-connector-java-5.1.47.jar -O ' + mysql_connector_file)


def install_jsvc():
    import params
    jsvc_path = '/usr/bin/jsvc'
    if not os.path.exists(jsvc_path):
        Execute('wget ' + params.download_url_base + '/jsvc -O ' + jsvc_path)
        Execute('chmod a+x ' + jsvc_path)


def hadoop_ld_so_config():
    import params
    ld_so_path = '/etc/ld.so.conf.d/hadoop.conf'
    if not os.path.exists(ld_so_path):
        Execute('wget ' + params.download_url_base + '/hadoop_ld_so.conf -O ' + ld_so_path)
        Execute('ldconfig')


def conf_rack_awareness():
    import params
    hostname = params.config["hostname"].lower()
    ip = socket.gethostbyname(socket.gethostname())
    try:
        response = urllib2.urlopen(CONST_RACK_INFO_URL + ip)
        rack_info = response.read()
        rack_info = json.loads(rack_info)
        if isinstance(rack_info, list):
            topology_item = '/idc/switch/rack_id'
        else:
            datacenter = rack_info.get(ip).get('datacenter') or 'default'
            switch = rack_info.get(ip).get('switch') or 'default'
            rack = rack_info.get(ip).get('rack') or 'default'
            topology_item = '/' + datacenter.replace(
                '/', '').lower() + '/' + switch.replace(
                '/', '').lower() + '/' + rack.replace('/', '').lower()

        ambari_server_host = params.config['clusterHostInfo'][
            'ambari_server_host'][0]
        ambari_server_port = params.config['clusterHostInfo'][
            'ambari_server_port'][0]
        ambari_server_use_ssl = params.config['ambariLevelParams'][
                                    'ambari_server_use_ssl'][0] == 'true'
        ambari_server_protocol = 'https' if ambari_server_use_ssl else 'http'
        cluster_name = params.config['clusterName']
        ambari_server_auth_host_url = format(
            '{ambari_server_protocol}://{ambari_server_host}:{ambari_server_port}'
        )
        rack_update_url = ambari_server_auth_host_url + '/api/v1/clusters/' + cluster_name + '/hosts'

        rack_update = '{"RequestInfo":{"context":"Set Rack","query":"Hosts/host_name.in(' + hostname + ')"},"Body":{"Hosts":{"rack_info":"' + topology_item + '"}}}'
        Execute("curl -u 'admin:admin' -H 'X-Requested-By:ambari' -i " +
                rack_update_url + " -X PUT -d '" + rack_update + "'")
    except urllib2.HTTPError as e:
        print("can not get %s rack_info from cmdb" % ip)


def kerberos_client_conf():
    lock_file = base_lock_dir + '/install_kerberos'

    if not os.path.exists(lock_file):
        kerberos_host = default('clusterHostInfo/krb5_master_hosts', [])
        realm = default('configurations/krb5-config/kdc.realm', 'example.com')
        kdc_hosts = default('configurations/zookeeper-env/kdc_hosts', '')

        if kdc_hosts.strip() != '':
            Execute('/usr/sbin/authconfig --enablekrb5 --krb5kdc="' + kdc_hosts +
                    '"  --krb5adminserver="' + kdc_hosts + '"  --krb5realm="' +
                    realm + '"  --update')
        elif len(kerberos_host) > 0:
            shuffle(kerberos_host)
            Execute('/usr/sbin/authconfig --enablekrb5 --krb5kdc="' +
                    ' '.join(kerberos_host) + '"  --krb5adminserver="' +
                    ' '.join(kerberos_host) + '"  --krb5realm="' + realm +
                    '"  --update')

        Execute(" echo 1 > " + lock_file)


def backup_keytab():
    backup_dir = '/data/backup/keytab/' + time.strftime('%Y%m%d_%H')
    Directory(backup_dir, create_parents=True, owner='root', group='root')
    Execute('cp -rpf /etc/security/keytabs ' + backup_dir)


def set_irq_affinity():
    import params
    set_irq_affinity_file = '/usr/sbin/set_irq_affinity.sh'
    eth_devices = ['eno1', 'eno2', 'em1', 'em2']

    if not os.path.exists(set_irq_affinity_file):
        Execute('wget ' + params.download_url_base + '/set_irq_affinity.sh -O ' + set_irq_affinity_file)
        Execute('chmod a+x ' + set_irq_affinity_file)
        for eth in eth_devices:
            Execute(set_irq_affinity_file + ' ' + eth)


def tuned():
    lock_file = base_lock_dir + '/install_tuned'
    if not os.path.exists(lock_file):
        Package(['tuned'])
        Execute('tuned-adm profile throughput-performance')
        Execute(" echo 1 > " + lock_file)


def install_pythonenv():
    import params
    if not os.path.exists(params.stack_root + '/pythonenv'):
        Execute('wget ' + params.download_url_base + '/pythonenv.tgz -O /tmp/pythonenv.tar.gz')
        Execute('tar -zxvf /tmp/pythonenv.tar.gz -C ' + params.stack_root + '/')


def install_intel_mkl_daal():
    import params
    Package(['intel-mkl-64bit'])
    mkl_wrapper_jar = params.stack_root + '/intel/mkl/wrapper/mkl_wrapper.jar'
    if not os.path.exists(mkl_wrapper_jar):
        Execute('wget ' + params.download_url_base + '/intel/mkl_wrapper.jar -O ' + mkl_wrapper_jar)

    mkl_wrapper_so = params.stack_root + '/intel/mkl_wrapper/mkl_wrapper.so'
    if not os.path.exists(mkl_wrapper_so):
        Execute('wget ' + params.download_url_base + '/intel/mkl_wrapper.so -O ' + mkl_wrapper_so)

    ld_so_path = '/etc/ld.so.conf.d/intel.conf'
    if not os.path.exists(ld_so_path):
        Execute('wget ' + params.download_url_base + '/intel_ld_so.conf -O ' +
                ld_so_path)
        Execute('ldconfig')

    # mkl-dnn
    if not os.path.exists(params.stack_root + '/intel/mklml'):
        Execute('wget ' + params.download_url_base + '/intel/mklml_lnx.tgz -O /tmp/mklml.tar.gz')
        Execute('tar -zxvf /tmp/mklml.tar.gz -C ' + params.stack_root + '/intel/')
        Execute(
            'ln -s ' + params.stack_root + '/intel/mklml_lnx ' + params.stack_root + '/intel/mklml')


def conf_ntp():
    lock_file = base_lock_dir + '/install_ntp'
    ntp_file = '/etc/chrony.conf'
    ntp_server_hosts = default('clusterHostInfo/ntp_server_hosts', [])
    if len(ntp_server_hosts) > 0 and not os.path.exists(lock_file):
        hostname = get_hostname()
        if hostname not in ntp_server_hosts:
            ntp_server_list = ['server  ' + server + '   iburst' for server in ntp_server_hosts]
            ntp_server = '\n '.join(ntp_server_list)
            ntp_conf = ntp_server + '''

driftfile /var/lib/chrony/drift

makestep 1.0 3

rtcsync

allow 192.168.0.0/24
allow 172.16.0.0/16
allow 10.0.0.0/8

logdir /var/log/chrony
            '''
            Execute('echo -ne ' + ntp_conf + ' > ' + ntp_file)

            Execute('systemctl enable chronyd && systemctl restart chronyd')

            Execute(" echo 1 > " + lock_file)


def conf_sysctl():
    import params
    sysctl_file = '/etc/sysctl.d/hadoop.conf'
    if not os.path.exists(sysctl_file):
        Execute('wget ' + params.download_url_base + '/sysctl.conf -O ' + sysctl_file)


def get_hostname():
    import socket
    hostname = socket.gethostname()
    return hostname


def get_ip():
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


def conf_dns():
    lock_file = base_lock_dir + '/install_dns'
    dns_file = '/etc/resolv.conf'
    # add dns record
    hostname = get_hostname()
    ip = get_ip()
    dns_hosts = default('clusterHostInfo/dns_hosts', [])
    if len(dns_hosts) > 0 and os.path.exists(lock_file):
        nameserver_hosts = dns_hosts.append('8.8.8.8')
        nameserver = 'nameserver ' + '\nnameserver '.join(nameserver_hosts)
        Execute('echo -ne ' + nameserver + ' > ' + dns_file)
        for dns_host in dns_hosts:
            Execute('curl -XPOST -d "hostname=' + hostname + '&ip=' + ip +
                    '" http://' + dns_host + ':8088/')

        Execute(" echo 1 > " + lock_file)


def install_common_share_lib():
    import params
    share_dir = '/usr/share/java/common/'
    Directory(
        share_dir,
        owner='hdfs',
        group=params.user_group,
        create_parents=True,
        mode=0755)

    share_jar_files_conf = default(
        "/configurations/hadoop-env/common_share_jars", '').strip()
    if share_jar_files_conf != '':
        share_jar_files = share_jar_files_conf.split(',')
        for jar_file in share_jar_files:
            jar_file_path = share_dir + jar_file.strip()
            if not os.path.exists(jar_file_path):
                Execute('wget ' + download_url_base + '/share/common/' + jar_file + ' -O ' + jar_file_path,
                        user='root')


def install_gpu_cuda():
    import params
    lock_file = base_lock_dir + '/install_cuda'
    if not os.path.exists(lock_file):
        packages = ['cuda', 'libnccl']
        Package(packages)
        # cudnn
        if not os.path.exists('/usr/local/cuda/include/cudnn.h'):
            cudnn_file = 'cudnn.tar.bz2'
            Execute('wget ' + params.download_url_base + '/' + cudnn_file + ' -O /tmp/' + cudnn_file)
            Execute('cd /tmp && tar -jxvf ' + cudnn_file + ' -C /usr/local/cuda/')

            Execute(" echo 1 > " + lock_file)


def install_dl_soft():
    lock_file = base_lock_dir + '/install_dl'
    if not os.path.exists(lock_file):
        packages = ['LightGBM', 'libsvm', 'xgboost']
        Package(packages)

        Execute(" echo 1 > " + lock_file)


class BeforeInstallHook(Hook):
    def hook(self, env):
        import params

        self.run_custom_hook('before-ANY')
        env.set_params(params)
        set_irq_affinity()
        install_mysql_connector()
        install_jsvc()
        hadoop_ld_so_config()
        install_common_share_lib()
        tuned()
        conf_ntp()
        conf_sysctl()
        install_pythonenv()

        if str(params.gpu_module_enabled).lower() == 'true':
            install_gpu_cuda()
            install_dl_soft()
            install_intel_mkl_daal()


if __name__ == "__main__":
    BeforeInstallHook().execute()
