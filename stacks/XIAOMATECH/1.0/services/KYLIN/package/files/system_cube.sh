#!/usr/bin/env bash

kylin_conf_dir=/etc/kylin

source $kylin_conf_dir/kylin-env.sh

$KYLIN_HOME/bin/kylin.sh org.apache.kylin.tool.metrics.systemcube.SCCreator -inputConfig $kylin_conf_dir/SCSinkTools.json -output $kylin_conf_dir/system_cube

hive -f $kylin_conf_dir/system_cube/create_hive_tables_for_system_cubes.sql

$KYLIN_HOME/bin/metastore.sh restore $kylin_conf_dir/system_cube


echo -ne '
#!/bin/bash

CUBE=$1
INTERVAL=$2
DELAY=$3
CURRENT_TIME_IN_SECOND=`date +%s`
CURRENT_TIME=$((CURRENT_TIME_IN_SECOND * 1000))
END_TIME=$((CURRENT_TIME-DELAY))
END=$((END_TIME - END_TIME%INTERVAL))

ID="$END"
echo "building for ${CUBE}_${ID}" >> '$KYLIN_HOME'/logs/build_trace.log
sh '$KYLIN_HOME'/bin/kylin.sh org.apache.kylin.tool.job.CubeBuildingCLI --cube ${CUBE} --endTime ${END} > '$KYLIN_HOME'/logs/system_cube_${CUBE}_${END}.log 2>&1 &
' > $KYLIN_HOME/bin/system_cube_build.sh && chmod a+x $KYLIN_HOME/bin/system_cube_build.sh


echo -ne '''
0 */2 * * * root '$KYLIN_HOME'/bin/system_cube_build.sh KYLIN_HIVE_METRICS_QUERY_QA 3600000 1200000

20 */2 * * * root '$KYLIN_HOME'/bin/system_cube_build.sh KYLIN_HIVE_METRICS_QUERY_CUBE_QA 3600000 1200000

40 */4 * * * root '$KYLIN_HOME'/bin/system_cube_build.sh KYLIN_HIVE_METRICS_QUERY_RPC_QA 3600000 1200000

30 */4 * * * root '$KYLIN_HOME'/bin/system_cube_build.sh KYLIN_HIVE_METRICS_JOB_QA 3600000 1200000

50 */12 * * * root '$KYLIN_HOME'/bin/system_cube_build.sh KYLIN_HIVE_METRICS_JOB_EXCEPTION_QA 3600000 12000

''' > /etc/cron.d/system_cube_build