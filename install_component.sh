#!/usr/bin/env bash

ambari_server=127.0.0.1
ambari_user=admin
ambari_password=admin
cluster_name=test

hostname=${1:-test.example.com}
component=${2:-DATANODE}
service_name=$3

function install_start_component(){

    #Add a Service to the cluster
    [ -n "$service_name" ] && curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X POST -d '{"ServiceInfo":{"service_name":"'$service_name'"}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/services

    #Register the host component
    curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X POST http://$ambari_server:8080/api/v1/clusters/$cluster_name/hosts/$hostname/host_components/$component

    #Install the new component
    curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X POST -d '{"HostRoles": {"state" : "INSTALLED"}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/hosts/$hostname/host_components/$component

    #Start the new component
    curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X POST -d '{"HostRoles": {"state" : "STARTED"}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/hosts/$hostname/host_components/$component

}

install_start_component