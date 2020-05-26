#!/usr/bin/env bash
repo_dir_base=/data/assets

yum install -y yum-utils createrepo unzip

mkdir -p $repo_dir_base/7
cd $repo_dir_base/7

echo -ne '''
[Confluent.dist]
name=Confluent repository (dist)
baseurl=https://packages.confluent.io/rpm/5.3/7
enabled=1

[Confluent]
name=Confluent repository
baseurl=https://packages.confluent.io/rpm/5.3
enabled=1

[mysql57]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/$releasever/$basearch/
enabled=1

[mysql80]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/$releasever/$basearch/
enabled=1

[mysql-tools]
name=MySQL Tools Community
baseurl=http://repo.mysql.com/yum/mysql-tools-community/el/$releasever/$basearch/
enabled=1

[mongodb]
name=mongodb
baseurl=https://mirrors.aliyun.com/mongodb/yum/redhat/$releasever/mongodb-org/4.1/x86_64
enabled=1
gpgcheck=0

[cuda]
name=cuda
baseurl=https://mirrors.aliyun.com/nvidia-cuda/rhel7/x86_64/
enabled=1
gpgcheck=0


[ambari]
name=ambari
baseurl=http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.7.3.0
enabled=1

[hdp-gpl]
baseurl=http://public-repo-1.hortonworks.com/HDP-GPL/centos7/3.x/updates/3.1.0.0
enabled=1

[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
enabled=1
failovermethod=priority
baseurl=http://mirrors.aliyun.com/epel/$releasever/$basearch
gpgcheck=0


[base]
name=CentOS-$releasever
enabled=1
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/

[updates]
name=CentOS-$releasever
enabled=1
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/

[extras]
name=CentOS-$releasever
enabled=1
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/


[ceph]
name=ceph
baseurl=https://mirrors.aliyun.com/ceph/rpm-mimic/el7/x86_64/
enabled=1

[qemu]
name=CentOS-$releasever - QEMU EV
baseurl=http://mirror.centos.org/$contentdir/$releasever/virt/$basearch/kvm-common/
enabled=1

[kubernetes]
name=Kubernetes
baseurl=http://yum.kubernetes.io/repos/kubernetes-el7-x86_64
enabled=1

[clickhouse]
name=clickhouse
baseurl=https://packagecloud.io/Altinity/clickhouse/el/$releasever/$basearch
enabled=1

[intel-mkl]
name=Intel(R) Math Kernel Library
baseurl=https://yum.repos.intel.com/mkl
enabled=1

[percona-release]
name = Percona-Release YUM repository - $basearch
baseurl = http://repo.percona.com/ps-80/yum/release/$releasever/RPMS/$basearch
enabled = 1

[percona-tools]
name = Percona-tools
baseurl = http://repo.percona.com/tools/yum/release/$releasever/RPMS/x86_64/
enabled = 1

[percona-mongodb]
name = Percona-mongodb
baseurl = http://repo.percona.com/psmdb-40/yum/release/7/RPMS/x86_64/
enabled = 1

[openresty]
name=Official OpenResty Open Source Repository for CentOS
baseurl=https://openresty.org/package/centos/$releasever/$basearch
skip_if_unavailable=False
enabled=1

[elrepo-kernel]
name=ELRepo.org Community Enterprise Linux Kernel Repository - el7
baseurl=http://elrepo.org/linux/kernel/el7/$basearch/
	http://mirrors.coreix.net/elrepo/kernel/el7/$basearch/
	http://mirror.rackspace.com/elrepo/kernel/el7/$basearch
enabled=1

[pouch]
name=Pouch Stable - $basearch
baseurl=http://mirrors.aliyun.com/opsx/pouch/linux/centos/$releasever/$basearch/stable
enabled=1

[remi]
name=remi
baseurl=http://mirrors.aliyun.com/remi/enterprise/7/remi/x86_64/
enabled=1

[gitlab]
name=gitlab
baseurl=https://packages.gitlab.com/gitlab/gitlab-ee/el/7/$basearch
enabled=1

[jenkins]
name=Jenkins-stable
baseurl=http://pkg.jenkins.io/redhat-stable
enabled=1

[gluster]
name=gluster
baseurl=http://mirrors.aliyun.com/centos/7/storage/x86_64/gluster-5/
enabled=1

''' > /etc/yum.repos.d/other.repo


repo_list=(Confluent Confluent.dist base extras epel updates ambari ceph clickhouse cuda hdp-gpl intel-mkl mongodb kubernetes mysql-tools mysql57 mysql80 qemu percona-release percona-tools percona-mongodb openresty elrepo-kernel pouch remi gitlab jenkins gluster)
for repo in ${repo_list[@]}
do
    nohup reposync -r $repo &
    rm -rf /var/tmp/yum-*/x86_64/7/yum.pid
done


elk_version=7.2.0
mkdir $repo_dir_base/7/elk
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-$elk_version.rpm -P elk/
wget https://artifacts.elastic.co/downloads/kibana/kibana-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/logstash/logstash-$elk_version.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/auditbeat/auditbeat-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-$elk_version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/apm-server/apm-server-$version-x86_64.rpm -P elk/
wget https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-$version-x86_64.rpm -P elk/

wget https://dl.grafana.com/oss/release/grafana-6.0.0-1.x86_64.rpm -P elk/

wget https://dev.mysql.com/get/Downloads/MySQL-Shell/mysql-shell-8.0.13-1.el7.x86_64.rpm -P $repo_dir_base/7/
wget https://dev.mysql.com/get/Downloads/MySQL-Router/mysql-router-community-8.0.13-1.el7.x86_64.rpm -P $repo_dir_base/7/
wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.8-1.el7.x86_64.rpm -P $repo_dir_base/7/
wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-8.0.13-1.el7.x86_64.rpm -P $repo_dir_base/7/
wget https://github.com/github/gh-ost/releases/download/v1.0.47/gh-ost-1.0.47-1.x86_64.rpm -P $repo_dir_base/7/

wget https://github.com/xiaomatech/repo/archive/master.zip /tmp/master.zip
cd /tmp && unzip master.zip && mv repo-master/rpm/* $repo_dir_base/7/other

wget https://mirrors.aliyun.com/apache/cassandra/redhat/311x/cassandra-3.11.3-1.noarch.rpm -P $repo_dir_base/7/
wget https://mirrors.aliyun.com/apache/cassandra/redhat/311x/cassandra-tools-3.11.3-1.noarch.rpm -P $repo_dir_base/7/

cd $repo_dir_base

createrepo 7

mkdir $repo_dir_base/es
wget https://artifacts.elastic.co/downloads/elasticsearch-plugins/ingest-geoip/ingest-geoip-$elk_version.zip -O $repo_dir_base/es/ingest-geoip.zip
wget https://artifacts.elastic.co/downloads/elasticsearch-plugins/ingest-user-agent/ingest-user-agent-$elk_version.zip -O $repo_dir_base/es/ingest-user-agent.zip
wget https://artifacts.elastic.co/downloads/elasticsearch-plugins/repository-hdfs/repository-hdfs-$elk_version.zip -O $repo_dir_base/es/repository-hdfs.zip
wget https://artifacts.elastic.co/downloads/elasticsearch-plugins/analysis-smartcn/analysis-smartcn-$elk_version.zip -O $repo_dir_base/es/analysis-smartcn.zip

mkdir -p $repo_dir_base/{druid,atlas,ranger,share,intel,tidb,prometheus,m3db,jaeger}
mkdir -p $repo_dir_base/share/{common,hadoop,spark,presto,hbase,geoserver}

wget https://github.com/xiaomatech/dataops/archive/master.zip -O /tmp/master.zip
cd /tmp && unzip /tmp/master.zip && rm -rf /tmp/master.zip
mv /tmp/bigdata-master/* $repo_dir_base/

#download compoment
cd $repo_dir_base
wget http://downloads.alluxio.org/downloads/files//1.8.1/alluxio-1.8.1-hadoop-2.9-bin.tar.gz -P ./
wget https://github.com/Angel-ML/angel/releases/download/Release-2.0.0/angel-2.0.0-bin.zip -P ./
wget https://github.com/ctripcorp/apollo/releases/download/v1.2.0/apollo-portal-1.2.0-github.zip -P ./
wget https://github.com/ctripcorp/apollo/releases/download/v1.2.0/apollo-configservice-1.2.0-github.zip -P ./
wget https://github.com/ctripcorp/apollo/releases/download/v1.2.0/apollo-adminservice-1.2.0-github.zip -P ./
wget http://mirrors.aliyun.com/apache/incubator/druid/0.16.0-incubating/apache-druid-0.16.0-incubating-bin.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/flink/flink-1.10.1/flink-1.10.1-bin-scala_2.12.tgz -P ./
wget https://mirrors.aliyun.com/apache/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/kafka/2.3.1/kafka_2.12-2.3.1.tgz -P ./
wget https://mirrors.aliyun.com/apache/knox/1.2.0/knox-1.2.0.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/knox/1.2.0/knoxshell-1.2.0.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/kylin/apache-kylin-2.6.4/apache-kylin-2.6.4-bin-hbase1x.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/nifi/1.8.0/nifi-1.8.0-bin.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/nifi/nifi-registry/nifi-registry-0.3.0/nifi-registry-0.3.0-bin.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/incubator/livy/0.5.0-incubating/livy-0.5.0-incubating-bin.zip -P ./
wget https://mirrors.aliyun.com/apache/sqoop/1.99.7/sqoop-1.99.7-bin-hadoop200.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/storm/apache-storm-2.1.0/apache-storm-2.1.0.tar.gz -P ./
wget https://mirrors.aliyun.com/apache/zeppelin/zeppelin-0.8.0/zeppelin-0.8.0-bin-all.tgz -P ./
wget http://mirrors.aliyun.com/apache/zookeeper/zookeeper-3.5.6/apache-zookeeper-3.5.6.tar.gz -P ./
wget http://central.maven.org/maven2/org/apache/parquet/parquet-tools/1.11.0/parquet-tools-1.11.0.jar -P ./

wget https://github.com/linkedin/cruise-control-ui/releases/download/v0.1.0/cruise-control-ui.tar.gz -P ./

wget http://central.maven.org/maven2/com/hadoop/compression/hadoop-gpl-compression/0.1.0/hadoop-gpl-compression-0.1.0.jar -P ./share/hadoop/
wget http://central.maven.org/maven2/org/apache/commons/commons-configuration2/2.4/commons-configuration2-2.4.jar -P ./share/hadoop/

wget https://mirrors.aliyun.com/apache/tez/0.9.2/apache-tez-0.9.2-bin.tar.gz -P ./
wget http://central.maven.org/maven2/org/apache/tez/tez-ui/0.9.2/tez-ui-0.9.2.war -P ./
wget http://central.maven.org/maven2/org/apache/tez/tez-aux-services/0.9.2/tez-aux-services-0.9.2.jar -P ./share/hadoop/

wget https://repo1.maven.org/maven2/io/prestosql/presto-server/325/presto-server-325.tar.gz -P ./
wget https://repo1.maven.org/maven2/io/prestosql/presto-cli/307/presto-cli-307-executable.jar -P ./
wget http://mirrors.aliyun.com/apache/tomcat/tomcat-8/v8.5.38/bin/apache-tomcat-8.5.38.tar.gz -P ./

cd $repo_dir_base/tidb
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz -P ./
tar -zxvf tidb-enterprise-tools-latest-linux-amd64.tar.gz && mv tidb-enterprise-tools-latest-linux-amd64/bin/* . && rm -rf tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz -P ./
tar -zxvf tidb-latest-linux-amd64.tar.gz && mv tidb-latest-linux-amd64/bin/* . &&  rm -rf tidb-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz -P ./
tar -zxvf tidb-binlog-kafka-linux-amd64.tar.gz && mv tidb-binlog-kafka-linux-amd64/bin/* . && rm -rf tidb-binlog-kafka-linux-amd64.tar.gz
rm -rf tidb-*amd64

cd $repo_dir_base/
wget http://mirrors.aliyun.com/apache/pulsar/pulsar-2.4.1/apache-pulsar-2.4.1-bin.tar.gz -P ./
mv apache-pulsar-2.4.1-bin.tar.gz apache-pulsar-2.4.1.tar.gz

wget  https://github.com/locationtech/geomesa/releases/download/geomesa_2.11-2.3.0/geomesa-kafka_2.11-2.3.0-bin.tar.gz -P ./
mv geomesa-kafka_2.11-2.3.0-bin.tar.gz geomesa-kafka_2.11-2.3.0.tar.gz


wget  https://github.com/locationtech/geomesa/releases/download/geomesa_2.11-2.3.0/geomesa-hbase_2.11-2.3.0-bin.tar.gz -P ./
mv geomesa-hbase_2.11-2.3.0-bin.tar.gz geomesa-hbase_2.11-2.3.0.tar.gz
tar -zxvf geomesa-hbase_2.11-2.3.0.tar.gz
mv geomesa-hbase_2.11-2.3.0/dist/hbase/geomesa-hbase-distributed-runtime_2.11-2.3.0.jar $repo_dir_base/share/hbase/
tar -zxvf geomesa-hbase_2.11-2.3.0/dist/gs-plugins/geomesa-hbase-gs-plugin_2.11-2.3.0-install.tar.gz

wget https://netix.dl.sourceforge.net/project/geoserver/GeoServer/2.15.2/geoserver-2.15.2-bin.zip -P ./
unzip geoserver-2.15.2-bin.zip

mv geomesa-hbase-gs-plugin_2.11-2.3.0-shaded.jar geoserver-2.15.2/webapps/geoserver/WEB-INF/lib/
mv geomesa-hbase_2.11-2.3.0/dist/gs-plugins/geomesa-process-wps_2.11-2.3.0.jar  geoserver-2.15.2/webapps/geoserver/WEB-INF/lib/
tar -czvf geoserver-2.15.2.tar.gz geoserver-2.15.2
rm -rf geoserver-2.15.2-bin.zip geoserver-2.15.2
rm -rf geomesa-hbase_2.11-2.3.0


wget https://mirrors.aliyun.com/apache/phoenix/apache-phoenix-5.0.0-HBase-2.0/bin/apache-phoenix-5.0.0-HBase-2.0-bin.tar.gz -P ./
tar -zxvf apache-phoenix-5.0.0-HBase-2.0-bin.tar.gz -C /tmp/
cd /tmp
mv /tmp/apache-phoenix-5.0.0-HBase-2.0-bin/phoenix-5.0.0-HBase-2.0-server.jar $repo_dir_base/share/hbase/
rm -rf /tmp/apache-phoenix-5.0.0-HBase-2.0-bin
cd $repo_dir_base

wget http://mirrors.aliyun.com/apache/hbase/2.2.2/hbase-2.2.2-bin.tar.gz -O ./hbase-2.2.2.tar.gz
tar -zxvf hbase-2.2.2.tar.gz -C /tmp/
cd /tmp
rm -rf /tmp/hbase-2.2.2/lib/hadoop-*
tar -czvf $repo_dir_base/hbase-2.2.2.tar.gz hbase-2.2.2
cd $repo_dir_base

wget https://mirrors.aliyun.com/apache/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz -P ./
tar -zxvf spark-2.4.3-bin-hadoop2.7.tgz -C /tmp/
cp /tmp/spark-2.4.3-bin-hadoop2.7/yarn/spark-2.4.3-yarn-shuffle.jar $repo_dir_base/share/spark/
rm -rf /tmp/spark-*
cd $repo_dir_base

