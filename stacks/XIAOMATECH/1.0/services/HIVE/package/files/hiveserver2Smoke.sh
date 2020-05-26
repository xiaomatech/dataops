#!/usr/bin/env bash

smokeout={{hive_home_dir}} + `/bin/beeline -u $1 -n fakeuser -p fakepwd -d org.apache.hive.jdbc.HiveDriver -e '!run $2' 2>&1| awk '{print}'|grep Error`

if [ "x$smokeout" == "x" ]; then
  echo "Smoke test of hiveserver2 passed"
  exit 0
else
  echo "Smoke test of hiveserver2 wasnt passed"
  echo $smokeout
  exit 1
fi
