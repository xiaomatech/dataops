from resource_management import *
from resource_management.libraries.script import Script

config = Script.get_config()

conf_dir = "/etc/influxdb"
influxd_dir = "/etc/default"
influxdb_user = "root"
user_group = "root"

reporting_disabled = config['configurations']['influxdb-cluster'][
    'reporting-disabled']

hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']

bind_address = config['configurations']['influxdb-cluster']['bind-address']

meta_dir = config['configurations']['influxdb-cluster']['meta-dir']
retention_autocreate = config['configurations']['influxdb-cluster'][
    'retention-autocreate']

election_timeout = config['configurations']['influxdb-cluster'][
    'election-timeout']
heartbeat_timeout = config['configurations']['influxdb-cluster'][
    'heartbeat-timeout']

leader_lease_timeout = config['configurations']['influxdb-cluster'][
    'leader-lease-timeout']
commit_timeout = config['configurations']['influxdb-cluster']['commit-timeout']

cluster_tracing = config['configurations']['influxdb-cluster'][
    'cluster-tracing']
data_dir = config['configurations']['influxdb-cluster']['data-dir']
max_wal_size = config['configurations']['influxdb-cluster']['max-wal-size']

wal_flush_interval = config['configurations']['influxdb-cluster'][
    'wal-flush-interval']
wal_partition_flush_delay = config['configurations']['influxdb-cluster'][
    'wal-partition-flush-delay']

wal_dir = config['configurations']['influxdb-cluster']['wal-dir']
wal_enable_logging = config['configurations']['influxdb-cluster'][
    'wal-enable-logging']

hinted_handoff_enabled = config['configurations']['influxdb-cluster'][
    'hinted-handoff-enabled']
hinted_handoff_dir = config['configurations']['influxdb-cluster'][
    'hinted-handoff-dir']
hinted_handoff_max_size = config['configurations']['influxdb-cluster'][
    'hinted-handoff-max-size']
hinted_handoff_max_age = config['configurations']['influxdb-cluster'][
    'hinted-handoff-max-age']

hinted_handoff_retry_rate_limit = config['configurations']['influxdb-cluster'][
    'hinted-handoff-retry-rate-limit']
hinted_handoff_retry_interval = config['configurations']['influxdb-cluster'][
    'hinted-handoff-retry-interval']
hinted_handoff_retry_max_interval = config['configurations'][
    'influxdb-cluster']['hinted-handoff-retry-max-interval']

hinted_handoff_purge_interval = config['configurations']['influxdb-cluster'][
    'hinted-handoff-purge-interval']
cluster_shard_writer_timeout = config['configurations']['influxdb-cluster'][
    'cluster-shard-writer-timeout']

cluster_write_timeout = config['configurations']['influxdb-cluster'][
    'cluster-write-timeout']
retention_enabled = config['configurations']['influxdb-cluster'][
    'retention-enabled']

retention_check_interval = config['configurations']['influxdb-cluster'][
    'retention-check-interval']

shard_precreation_enabled = config['configurations']['influxdb-cluster'][
    'shard-precreation-enabled']
shard_precreation_check_interval = config['configurations'][
    'influxdb-cluster']['shard-precreation-check-interval']
shard_precreation_advance_period = config['configurations'][
    'influxdb-cluster']['shard-precreation-advance-period']
monitor_store_enabled = config['configurations']['influxdb-cluster'][
    'monitor-store-enabled']
monitor_store_database = config['configurations']['influxdb-cluster'][
    'monitor-store-database']
monitor_store_interval = config['configurations']['influxdb-cluster'][
    'monitor-store-interval']
admin_enabled = config['configurations']['influxdb-cluster']['admin-enabled']

admin_bind_address = config['configurations']['influxdb-cluster'][
    'admin-bind-address']
admin_https_enabled = config['configurations']['influxdb-cluster'][
    'admin-https-enabled']

admin_https_certificate = config['configurations']['influxdb-cluster'][
    'admin-https-certificate']
http_enabled = config['configurations']['influxdb-cluster']['http-enabled']

http_bind_address = config['configurations']['influxdb-cluster'][
    'http-bind-address']
http_auth_enabled = config['configurations']['influxdb-cluster'][
    'http-auth-enabled']
http_log_enabled = config['configurations']['influxdb-cluster'][
    'http-log-enabled']
http_write_tracing = config['configurations']['influxdb-cluster'][
    'http-write-tracing']
http_pprof_enabled = config['configurations']['influxdb-cluster'][
    'http-pprof-enabled']
http_https_enabled = config['configurations']['influxdb-cluster'][
    'http-https-enabled']
http_https_certificate = config['configurations']['influxdb-cluster'][
    'http-https-certificate']

graphite_enabled = config['configurations']['influxdb-cluster'][
    'graphite-enabled']
collectd_enabled = config['configurations']['influxdb-cluster'][
    'collectd-enabled']
opentsdb_enabled = config['configurations']['influxdb-cluster'][
    'opentsdb-enabled']
udp_enabled = config['configurations']['influxdb-cluster']['udp-enabled']

continuous_queries_log_enabled = config['configurations']['influxdb-cluster'][
    'continuous-queries-log-enabled']

continuous_queries_enabled = config['configurations']['influxdb-cluster'][
    'continuous-queries-enabled']
continuous_queries_recompute_previous_n = config['configurations'][
    'influxdb-cluster']['continuous-queries-recompute-previous-n']
continuous_queries_recompute_no_older_than = config['configurations'][
    'influxdb-cluster']['continuous-queries-recompute-no-older-than']
continuous_queries_compute_runs_per_interval = config['configurations'][
    'influxdb-cluster']['continuous-queries-compute-runs-per-interval']
continuous_queries_compute_no_more_than = config['configurations'][
    'influxdb-cluster']['continuous-queries-compute-no-more-than']

INFLUXD_OPTS = config['configurations']['influxdb-cluster']['INFLUXD_OPTS']
