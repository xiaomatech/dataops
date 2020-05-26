change master to master_user='repl', master_password='E_u5Ve-s2_k_a78343' for channel 'group_replication_recovery';

set global group_replication_allow_local_disjoint_gtids_join=on;
start group_replication;