#!/usr/bin/env bash
ambari_server=127.0.0.1
ambari_user=admin
ambari_password=admin

curl -i \
  -u $ambari_user:$ambari_password \
  -H 'X-Requested-By: ambari' \
  -XPOST \
  "http://"$ambari_server":8080/api/v1/alert_targets" \
  -d '
  {
    "AlertTarget":
      {
        "name": "custom_dispatcher",
        "description": "Custom Dispatcher",
        "notification_type": "ALERT_SCRIPT",
        "global": true,
        "alert_states": ["CRITICAL"],
        "properties": {
          "ambari.dispatch-property.script": "notification.dispatch.alert.script"
        }
      }
  }
'

