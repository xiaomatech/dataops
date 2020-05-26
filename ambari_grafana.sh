#!/usr/bin/env bash

yum install -y grafana

grafana-cli plugins install praj-ams-datasource
