#!/usr/bin/env bash

ambari_server=127.0.0.1
ambari_user=admin
ambari_password=admin
cluster_name=test

component=$1
hostname=$2
service_name=$3

function stop_component(){

    #stop a Service
    [ -n "$service_name" ] && [ -z "$component" ] && curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X PUT -d '{"RequestInfo":{"context":"Stop Service"},"Body":{"ServiceInfo":{"state":"INSTALLED"}}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/services/$service_name

    #Stop one host components
    [ -n "$hostname" ] && curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X PUT -d '{"RequestInfo":{"context":"Stop Component"},"Body":{"HostRoles":{"state":"INSTALLED"}}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/hosts/$hostname/host_components/$component

    #Stop all host component
    [ -n "$component" ] && [ -n "$service_name" ] && curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X PUT -d '{"RequestInfo":{"context":"Stop All Components"},"Body":{"ServiceComponentInfo":{"state":"INSTALLED"}}}' http://$ambari_server:8080/api/v1/clusters/$cluster_name/services/$service_name/components/$component

}

stop_component