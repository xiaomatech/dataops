#!/usr/bin/env bash

ambari_server=127.0.0.1
ambari_user=admin
ambari_password=admin

ssh_user=root
ssh_key='''

'''

agent_host_list = '''
"hostname1",
"hostname2",
"hostname3"
'''


curl -i -$ambari_user:$ambari_password -H 'X-Requested-By: ambari' -H 'Content-Type: application/json' -X POST -d '{
   "verbose":true,
   "sshKey":"'$ssh_key'",
   "hosts":[
      'agent_host_list'
   ],
   "user":"'$ssh_user'"
}' http://$ambari_server:8080/api/v1/bootstrap