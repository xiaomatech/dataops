CREATE DATABASE graphite;

CREATE TABLE graphite.metrics ( date Date DEFAULT toDate(0),  name String,  level UInt16,  parent String,  updated DateTime DEFAULT now(),  status Enum8('SIMPLE' = 0, 'BAN' = 1, 'APPROVED' = 2, 'HIDDEN' = 3, 'AUTO_HIDDEN' = 4)) ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/single/graphite.metrics', '{replica}', date, (parent, name), 1024, updated);

CREATE TABLE graphite.data_lr ( metric String,  value Float64,  timestamp UInt32,  date Date,  updated UInt32) ENGINE = ReplicatedGraphiteMergeTree('/clickhouse/tables/{shard}/graphite.data_lr', '{replica}', date, (metric, timestamp), 8192, 'graphite_rollup')

CREATE TABLE graphite.data ( metric String,  value Float64,  timestamp UInt32,  date Date,  updated UInt32) ENGINE Distributed('ck_cluster', 'graphite', 'data_lr', sipHash64(metric))
