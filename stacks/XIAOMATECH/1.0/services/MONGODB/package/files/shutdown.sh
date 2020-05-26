#mongo --port $1 << EOF
#use admin;
#db.shutdownServer();
#EOF
ps -ef|grep $1 |grep -v grep|cut -c 9-15|xargs kill -2
