CREATE DATABASE wherehows
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

CREATE USER 'wherehows'@'localhost' IDENTIFIED BY 'wherehows';
CREATE USER 'wherehows'@'%' IDENTIFIED BY 'wherehows';
GRANT ALL ON wherehows.* TO 'wherehows'@'wherehows';
GRANT ALL ON wherehows.* TO 'wherehows'@'%';

CREATE USER 'wherehows_ro'@'localhost' IDENTIFIED BY 'readmetadata';
CREATE USER 'wherehows_ro'@'%' IDENTIFIED BY 'readmetadata';
GRANT SELECT ON wherehows.* TO 'wherehows_ro'@'localhost';
GRANT SELECT ON wherehows.* TO 'wherehows_ro'@'%';


use wherehows;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--


CREATE TABLE dataset_deployment (
  `dataset_id`      INT UNSIGNED NOT NULL,
  `dataset_urn`     VARCHAR(200) NOT NULL,
  `deployment_tier` VARCHAR(20)  NOT NULL,
  `datacenter`      VARCHAR(20)  NOT NULL,
  `region`          VARCHAR(50)        DEFAULT NULL,
  `zone`            VARCHAR(50)        DEFAULT NULL,
  `cluster`         VARCHAR(100)       DEFAULT NULL,
  `container`       VARCHAR(100)       DEFAULT NULL,
  `enabled`         BOOLEAN      NOT NULL,
  `additional_info` TEXT CHAR SET utf8 DEFAULT NULL,
  `modified_time`   INT UNSIGNED       DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `deployment_tier`, `datacenter`),
  UNIQUE KEY (`dataset_urn`, `deployment_tier`, `datacenter`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_capacity (
  `dataset_id`    INT UNSIGNED NOT NULL,
  `dataset_urn`   VARCHAR(200) NOT NULL,
  `capacity_name` VARCHAR(100) NOT NULL,
  `capacity_type` VARCHAR(50)  DEFAULT NULL,
  `capacity_unit` VARCHAR(20)  DEFAULT NULL,
  `capacity_low`  DOUBLE       DEFAULT NULL,
  `capacity_high` DOUBLE       DEFAULT NULL,
  `modified_time` INT UNSIGNED DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `capacity_name`),
  UNIQUE KEY (`dataset_urn`, `capacity_name`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_tag (
  `dataset_id`    INT UNSIGNED NOT NULL,
  `dataset_urn`   VARCHAR(200) NOT NULL,
  `tag`           VARCHAR(100) NOT NULL,
  `modified_time` INT UNSIGNED DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `tag`),
  UNIQUE KEY (`dataset_urn`, `tag`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_case_sensitivity (
  `dataset_id`    INT UNSIGNED NOT NULL,
  `dataset_urn`   VARCHAR(200) NOT NULL,
  `dataset_name`  BOOLEAN      NOT NULL,
  `field_name`    BOOLEAN      NOT NULL,
  `data_content`  BOOLEAN      NOT NULL,
  `modified_time` INT UNSIGNED DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY (`dataset_urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_reference (
  `dataset_id`       INT UNSIGNED NOT NULL,
  `dataset_urn`      VARCHAR(200) NOT NULL,
  `reference_type`   VARCHAR(20)  NOT NULL,
  `reference_format` VARCHAR(50)  NOT NULL,
  `reference_list`   TEXT CHAR SET utf8 DEFAULT NULL,
  `modified_time`    INT UNSIGNED       DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `reference_type`, `reference_format`),
  UNIQUE KEY (`dataset_urn`, `reference_type`, `reference_format`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_partition (
  `dataset_id`                INT UNSIGNED NOT NULL,
  `dataset_urn`               VARCHAR(200) NOT NULL,
  `total_partition_level`     SMALLINT UNSIGNED  DEFAULT NULL,
  `partition_spec_text`       TEXT CHAR SET utf8 DEFAULT NULL,
  `has_time_partition`        BOOLEAN            DEFAULT NULL,
  `has_hash_partition`        BOOLEAN            DEFAULT NULL,
  `partition_keys`            TEXT CHAR SET utf8 DEFAULT NULL,
  `time_partition_expression` VARCHAR(100)       DEFAULT NULL,
  `modified_time`             INT UNSIGNED       DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY (`dataset_urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE `dataset_compliance` (
  `dataset_id`                INT(10) UNSIGNED NOT NULL,
  `dataset_urn`               VARCHAR(500)     NOT NULL,
  `compliance_purge_type`     VARCHAR(30)      DEFAULT NULL
  COMMENT 'AUTO_PURGE,CUSTOM_PURGE,LIMITED_RETENTION,PURGE_NOT_APPLICABLE,PURGE_EXEMPTED',
  `compliance_purge_note`     MEDIUMTEXT       DEFAULT NULL
  COMMENT 'The additional information about purging if the purge type is PURGE_EXEMPTED',
  `compliance_entities`       MEDIUMTEXT       DEFAULT NULL
  COMMENT 'JSON: compliance fields',
  `confidentiality`           VARCHAR(50)      DEFAULT NULL
  COMMENT 'dataset level confidential category: confidential, highly confidential, etc',
  `dataset_classification`    VARCHAR(1000)    DEFAULT NULL
  COMMENT 'JSON: dataset level confidential classification',
  `modified_by`               VARCHAR(50)      DEFAULT NULL
  COMMENT 'last modified by',
  `modified_time`             INT UNSIGNED DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY `dataset_urn` (`dataset_urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_constraint (
  `dataset_id`            INT UNSIGNED NOT NULL,
  `dataset_urn`           VARCHAR(200) NOT NULL,
  `constraint_type`       VARCHAR(20)  NOT NULL,
  `constraint_sub_type`   VARCHAR(20)  NOT NULL,
  `constraint_name`       VARCHAR(50)        DEFAULT NULL,
  `constraint_expression` VARCHAR(200) NOT NULL,
  `enabled`               BOOLEAN      NOT NULL,
  `referred_fields`       TEXT               DEFAULT NULL,
  `additional_reference`  TEXT CHAR SET utf8 DEFAULT NULL,
  `modified_time`         INT UNSIGNED       DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `constraint_type`, `constraint_sub_type`, `constraint_expression`),
  UNIQUE KEY (`dataset_urn`, `constraint_type`, `constraint_sub_type`, `constraint_expression`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_index (
  `dataset_id`     INT UNSIGNED NOT NULL,
  `dataset_urn`    VARCHAR(200) NOT NULL,
  `index_type`     VARCHAR(20)  NOT NULL,
  `index_name`     VARCHAR(50)  NOT NULL,
  `is_unique`      BOOLEAN      NOT NULL,
  `indexed_fields` TEXT         DEFAULT NULL,
  `modified_time`  INT UNSIGNED DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`, `index_name`),
  UNIQUE KEY (`dataset_urn`, `index_name`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_schema_info (
  `dataset_id`                   INT UNSIGNED NOT NULL,
  `dataset_urn`                  VARCHAR(200) NOT NULL,
  `is_backward_compatible`       BOOLEAN                  DEFAULT NULL,
  `create_time`                  BIGINT       NOT NULL,
  `revision`                     INT UNSIGNED             DEFAULT NULL,
  `version`                      VARCHAR(20)              DEFAULT NULL,
  `name`                         VARCHAR(100)             DEFAULT NULL,
  `description`                  TEXT CHAR SET utf8       DEFAULT NULL,
  `original_schema`              MEDIUMTEXT CHAR SET utf8 DEFAULT NULL,
  `key_schema`                   MEDIUMTEXT CHAR SET utf8 DEFAULT NULL,
  `is_field_name_case_sensitive` BOOLEAN                  DEFAULT NULL,
  `field_schema`                 MEDIUMTEXT CHAR SET utf8 DEFAULT NULL,
  `change_data_capture_fields`   TEXT                     DEFAULT NULL,
  `audit_fields`                 TEXT                     DEFAULT NULL,
  `modified_time`                INT UNSIGNED             DEFAULT NULL
  COMMENT 'the modified time in epoch',
  PRIMARY KEY (`dataset_id`),
  UNIQUE KEY (`dataset_urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE dataset_inventory (
  `event_date`                    DATE         NOT NULL,
  `data_platform`                 VARCHAR(50)  NOT NULL,
  `native_name`                   VARCHAR(200) NOT NULL,
  `data_origin`                   VARCHAR(20)  NOT NULL,
  `change_actor_urn`              VARCHAR(200)       DEFAULT NULL,
  `change_type`                   VARCHAR(20)        DEFAULT NULL,
  `change_time`                   BIGINT UNSIGNED    DEFAULT NULL,
  `change_note`                   TEXT CHAR SET utf8 DEFAULT NULL,
  `native_type`                   VARCHAR(20)        DEFAULT NULL,
  `uri`                           VARCHAR(200)       DEFAULT NULL,
  `dataset_name_case_sensitivity` BOOLEAN            DEFAULT NULL,
  `field_name_case_sensitivity`   BOOLEAN            DEFAULT NULL,
  `data_content_case_sensitivity` BOOLEAN            DEFAULT NULL,
  PRIMARY KEY (`data_platform`, `native_name`, `data_origin`, `event_date`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- create statement for dataset related tables :
-- dict_dataset, dict_dataset_sample, dict_field_detail, dict_dataset_schema_history

-- stagging table for dataset
CREATE TABLE `stg_dict_dataset` (
  `name`                        VARCHAR(200) NOT NULL,
  `schema`                      MEDIUMTEXT CHARACTER SET utf8,
  `schema_type`                 VARCHAR(50) DEFAULT 'JSON' COMMENT 'JSON, Hive, DDL, XML, CSV',
  `properties`                  TEXT CHARACTER SET utf8,
  `fields`                      MEDIUMTEXT CHARACTER SET utf8,
  `db_id`                       SMALLINT UNSIGNED,
  `urn`                         VARCHAR(500) NOT NULL,
  `source`                      VARCHAR(50) NULL,
  `location_prefix`             VARCHAR(200) NULL,
  `parent_name`                 VARCHAR(500) NULL COMMENT 'Schema Name for RDBMS, Group Name for Jobs/Projects/Tracking Datasets on HDFS',
  `storage_type`                ENUM('Table', 'View', 'Avro', 'ORC', 'RC', 'Sequence', 'Flat File', 'JSON', 'BINARY_JSON', 'XML', 'Thrift', 'Parquet', 'Protobuff') NULL,
  `ref_dataset_name`            VARCHAR(200) NULL,
  `ref_dataset_id`              INT(11) UNSIGNED NULL COMMENT 'Refer to Master/Main dataset for Views/ExternalTables',
  `is_active`                   BOOLEAN NULL COMMENT 'is the dataset active / exist ?',
  `is_deprecated`               BOOLEAN NULL COMMENT 'is the dataset deprecated by user ?',
  `dataset_type`                VARCHAR(30) NULL
  COMMENT 'hdfs, hive, kafka, teradata, mysql, sqlserver, file, nfs, pinot, salesforce, oracle, db2, netezza, cassandra, hbase, qfs, zfs',
  `hive_serdes_class`           VARCHAR(300)                                                                                NULL,
  `is_partitioned`              CHAR(1)                                                                                     NULL,
  `partition_layout_pattern_id` SMALLINT(6)                                                                                 NULL,
  `sample_partition_full_path`  VARCHAR(256) COMMENT 'sample partition full path of the dataset',
  `source_created_time`         INT UNSIGNED                                                                                NULL
  COMMENT 'source created time of the flow',
  `source_modified_time`        INT UNSIGNED                                                                                NULL
  COMMENT 'latest source modified time of the flow',
  `created_time`                INT UNSIGNED COMMENT 'wherehows created time',
  `modified_time`               INT UNSIGNED COMMENT 'latest wherehows modified',
  `wh_etl_exec_id`              BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`urn`, `db_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1
  PARTITION BY HASH(db_id)
  PARTITIONS 8;

-- dataset table
CREATE TABLE `dict_dataset` (
  `id`                          INT(11) UNSIGNED NOT NULL                                                                   AUTO_INCREMENT,
  `name`                        VARCHAR(200)                                                                                NOT NULL,
  `schema`                      MEDIUMTEXT CHARACTER SET utf8,
  `schema_type`                 VARCHAR(50)                                                                                 DEFAULT 'JSON'
  COMMENT 'JSON, Hive, DDL, XML, CSV',
  `properties`                  TEXT CHARACTER SET utf8,
  `fields`                      MEDIUMTEXT CHARACTER SET utf8,
  `urn`                         VARCHAR(500)                                                                                NOT NULL,
  `source`                      VARCHAR(50)                                                                                 NULL
  COMMENT 'The original data source type (for dataset in data warehouse). Oracle, Kafka ...',
  `location_prefix`             VARCHAR(200)                                                                                NULL,
  `parent_name`                 VARCHAR(500)                                                                                NULL
  COMMENT 'Schema Name for RDBMS, Group Name for Jobs/Projects/Tracking Datasets on HDFS ',
  `storage_type`                ENUM('Table', 'View', 'Avro', 'ORC', 'RC', 'Sequence', 'Flat File', 'JSON', 'BINARY_JSON', 'XML', 'Thrift', 'Parquet', 'Protobuff') NULL,
  `ref_dataset_id`              INT(11) UNSIGNED                                                                            NULL
  COMMENT 'Refer to Master/Main dataset for Views/ExternalTables',
  `is_active`                   BOOLEAN NULL COMMENT 'is the dataset active / exist ?',
  `is_deprecated`               BOOLEAN NULL COMMENT 'is the dataset deprecated by user ?',
  `dataset_type`                VARCHAR(30)                                                                                 NULL
  COMMENT 'hdfs, hive, kafka, teradata, mysql, sqlserver, file, nfs, pinot, salesforce, oracle, db2, netezza, cassandra, hbase, qfs, zfs',
  `hive_serdes_class`           VARCHAR(300)                                                                                NULL,
  `is_partitioned`              CHAR(1)                                                                                     NULL,
  `partition_layout_pattern_id` SMALLINT(6)                                                                                 NULL,
  `sample_partition_full_path`  VARCHAR(256)
  COMMENT 'sample partition full path of the dataset',
  `source_created_time`         INT UNSIGNED                                                                                NULL
  COMMENT 'source created time of the flow',
  `source_modified_time`        INT UNSIGNED                                                                                NULL
  COMMENT 'latest source modified time of the flow',
  `created_time`                INT UNSIGNED COMMENT 'wherehows created time',
  `modified_time`               INT UNSIGNED COMMENT 'latest wherehows modified',
  `wh_etl_exec_id`              BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_dataset_urn` (`urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

-- stagging table for sample data
CREATE TABLE `stg_dict_dataset_sample` (
  `db_id`      SMALLINT  UNSIGNED,
  `urn`        VARCHAR(200) NOT NULL DEFAULT '',
  `dataset_id` INT(11)               NULL,
  `ref_urn`    VARCHAR(200)          NULL,
  `ref_id`     INT(11)               NULL,
  `data`       MEDIUMTEXT,
  PRIMARY KEY (`db_id`, `urn`),
  KEY `ref_urn_key` (`ref_urn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- sample data table
CREATE TABLE `dict_dataset_sample` (
  `id`         INT(11) NOT NULL AUTO_INCREMENT,
  `dataset_id` INT(11)          NULL,
  `urn`        VARCHAR(200)     NULL,
  `ref_id`     INT(11)          NULL
  COMMENT 'Reference dataset id of which dataset that we fetch sample from. e.g. for tables we do not have permission, fetch sample data from DWH_STG correspond tables',
  `data`       MEDIUMTEXT,
  `modified`   DATETIME         NULL,
  `created`    DATETIME         NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ak_dict_dataset_sample__datasetid` (`dataset_id`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
  DEFAULT CHARSET = utf8;

-- stagging table for field detail
CREATE TABLE `stg_dict_field_detail` (
  `db_id`          SMALLINT  UNSIGNED,
  `urn`            VARCHAR(200)         NOT NULL,
  `sort_id`        SMALLINT(5) UNSIGNED NOT NULL,
  `parent_sort_id` SMALLINT(5) UNSIGNED NOT NULL,
  `parent_path`    VARCHAR(200)                  NULL,
  `field_name`     VARCHAR(100)         NOT NULL,
  `field_label`    VARCHAR(100)                  NULL,
  `data_type`      VARCHAR(50)          NOT NULL,
  `data_size`      INT(10) UNSIGNED              NULL,
  `data_precision` TINYINT(3) UNSIGNED           NULL,
  `data_scale`     TINYINT(3) UNSIGNED           NULL,
  `is_nullable`    CHAR(1)                       NULL,
  `is_indexed`     CHAR(1)                       NULL,
  `is_partitioned` CHAR(1)                       NULL,
  `is_distributed` CHAR(1)                       NULL,
  `default_value`  VARCHAR(200)                  NULL,
  `namespace`      VARCHAR(200)                  NULL,
  `description`    VARCHAR(1000)                 NULL,
  `last_modified`  TIMESTAMP            NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dataset_id`     INT UNSIGNED         NULL COMMENT 'used to opitimize metadata ETL performance',
  KEY `idx_stg_dict_field_detail__description` (`description`(100)),
  PRIMARY KEY (`urn`, `sort_id`, `db_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1
  PARTITION BY HASH(db_id)
  PARTITIONS 8;

-- field detail table
CREATE TABLE `dict_field_detail` (
  `field_id`           INT(11) UNSIGNED     NOT NULL AUTO_INCREMENT,
  `dataset_id`         INT(11) UNSIGNED     NOT NULL,
  `fields_layout_id`   INT(11) UNSIGNED     NOT NULL,
  `sort_id`            SMALLINT(6) UNSIGNED NOT NULL,
  `parent_sort_id`     SMALLINT(5) UNSIGNED NOT NULL,
  `parent_path`        VARCHAR(200)                  NULL,
  `field_name`         VARCHAR(100)         NOT NULL,
  `field_label`        VARCHAR(100)                  NULL,
  `data_type`          VARCHAR(50)          NOT NULL,
  `data_size`          INT(10) UNSIGNED              NULL,
  `data_precision`     TINYINT(4)                    NULL
  COMMENT 'only in decimal type',
  `data_fraction`      TINYINT(4)                    NULL
  COMMENT 'only in decimal type',
  `default_comment_id` INT(11) UNSIGNED              NULL
  COMMENT 'a list of comment_id',
  `comment_ids`        VARCHAR(500)                  NULL,
  `is_nullable`        CHAR(1)                       NULL,
  `is_indexed`         CHAR(1)                       NULL
  COMMENT 'only in RDBMS',
  `is_partitioned`     CHAR(1)                       NULL
  COMMENT 'only in RDBMS',
  `is_distributed`     TINYINT(4)                    NULL
  COMMENT 'only in RDBMS',
  `is_recursive`       CHAR(1)                       NULL,
  `confidential_flags` VARCHAR(200)                  NULL,
  `default_value`      VARCHAR(200)                  NULL,
  `namespace`          VARCHAR(200)                  NULL,
  `java_data_type`     VARCHAR(50)                   NULL
  COMMENT 'correspond type in java',
  `jdbc_data_type`     VARCHAR(50)                   NULL
  COMMENT 'correspond type in jdbc',
  `pig_data_type`      VARCHAR(50)                   NULL
  COMMENT 'correspond type in pig',
  `hcatalog_data_type` VARCHAR(50)                   NULL
  COMMENT 'correspond type in hcatalog',
  `modified`           TIMESTAMP            NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`field_id`),
  UNIQUE KEY `uix_dict_field__datasetid_parentpath_fieldname` (`dataset_id`, `parent_path`, `field_name`) USING BTREE,
  UNIQUE KEY `uix_dict_field__datasetid_sortid` (`dataset_id`, `sort_id`) USING BTREE
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
  DEFAULT CHARSET = latin1
  COMMENT = 'Flattened Fields/Columns';

-- schema history
CREATE TABLE `dict_dataset_schema_history` (
  `id`            INT(11) AUTO_INCREMENT NOT NULL,
  `dataset_id`    INT(11)                NULL,
  `urn`           VARCHAR(200)           NOT NULL,
  `modified_date` DATE                   NULL,
  `schema`        MEDIUMTEXT CHARACTER SET utf8 NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `uk_dict_dataset_schema_history__urn_modified` (`urn`, `modified_date`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0;

-- staging table table of fields to comments mapping
CREATE TABLE `stg_dict_dataset_field_comment` (
  `field_id` int(11) UNSIGNED NOT NULL,
  `comment_id` bigint(20) NOT NULL,
  `dataset_id` int(11) UNSIGNED NOT NULL,
  `db_id` smallint(6) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`field_id`,`comment_id`, `db_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8
  PARTITION BY HASH(db_id)
  PARTITIONS 8
;

-- fields to comments mapping
CREATE TABLE `dict_dataset_field_comment` (
  `field_id`   INT(11) UNSIGNED NOT NULL,
  `comment_id` BIGINT(20) NOT NULL,
  `dataset_id` INT(11) UNSIGNED NOT NULL,
  `is_default` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (field_id, comment_id),
  KEY (comment_id)
)
  ENGINE = InnoDB;

-- dataset comments
CREATE TABLE comments (
  `id`           INT(11) AUTO_INCREMENT                                                                       NOT NULL,
  `text`         TEXT CHARACTER SET utf8                                                                      NOT NULL,
  `user_id`      INT(11)                                                                                      NOT NULL,
  `dataset_id`   INT(11)                                                                                      NOT NULL,
  `created`      DATETIME                                                                                     NULL,
  `modified`     DATETIME                                                                                     NULL,
  `comment_type` ENUM('Description', 'Grain', 'Partition', 'ETL Schedule', 'DQ Issue', 'Question', 'Comment') NULL,
  PRIMARY KEY (id),
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `dataset_id` (`dataset_id`) USING BTREE,
  FULLTEXT KEY `fti_comment` (`text`)
)
  ENGINE = InnoDB
  CHARACTER SET latin1
  COLLATE latin1_swedish_ci
  AUTO_INCREMENT = 0;

-- field comments
CREATE TABLE `field_comments` (
  `id`                     INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id`                INT(11)          NOT NULL DEFAULT '0',
  `comment`                VARCHAR(4000)    NOT NULL,
  `created`                TIMESTAMP        NOT NULL,
  `modified`               TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comment_crc32_checksum` INT(11) UNSIGNED          NULL COMMENT '4-byte CRC32',
  PRIMARY KEY (`id`),
  KEY `comment_key` (`comment`(100)),
  FULLTEXT KEY `fti_comment` (`comment`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
  DEFAULT CHARSET = utf8;

-- dict_dataset_instance
CREATE TABLE dict_dataset_instance  (
	dataset_id           	int(11) UNSIGNED NOT NULL,
	db_id                	smallint(6) UNSIGNED COMMENT 'FK to cfg_database'  NOT NULL DEFAULT '0',
	deployment_tier      	enum('local','grid','dev','int','ei','ei2','ei3','qa','stg','prod') NOT NULL DEFAULT 'dev',
	data_center          	varchar(30) COMMENT 'data center code: lva1, ltx1, dc2, dc3...'  NULL DEFAULT '*',
	server_cluster       	varchar(150) COMMENT 'sfo1-bigserver, jfk3-sqlserver03'  NULL DEFAULT '*',
	slice                	varchar(50) COMMENT 'virtual group/tenant id/instance tag'  NOT NULL DEFAULT '*',
  is_active             BOOLEAN NULL COMMENT 'is the dataset active / exist ?',
  is_deprecated         BOOLEAN NULL COMMENT 'is the dataset deprecated by user ?',
	native_name          	varchar(250) NOT NULL,
	logical_name         	varchar(250) NOT NULL,
	version              	varchar(30) COMMENT '1.2.3 or 0.3.131'  NULL,
	version_sort_id      	bigint(20) COMMENT '4-digit for each version number: 000100020003, 000000030131'  NOT NULL DEFAULT '0',
	schema_text           MEDIUMTEXT CHARACTER SET utf8 NULL,
	ddl_text              MEDIUMTEXT CHARACTER SET utf8 NULL,
	instance_created_time	int(10) UNSIGNED COMMENT 'source instance created time'  NULL,
	created_time         	int(10) UNSIGNED COMMENT 'wherehows created time'  NULL,
	modified_time        	int(10) UNSIGNED COMMENT 'latest wherehows modified'  NULL,
	wh_etl_exec_id       	bigint(20) COMMENT 'wherehows etl execution id that modified this record'  NULL,
	PRIMARY KEY(dataset_id,db_id,version_sort_id)
)
ENGINE = InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci
AUTO_INCREMENT = 0
	PARTITION BY HASH(db_id)
	(PARTITION p0,
	PARTITION p1,
	PARTITION p2,
	PARTITION p3,
	PARTITION p4,
	PARTITION p5,
	PARTITION p6,
	PARTITION p7);

CREATE INDEX logical_name USING BTREE
	ON dict_dataset_instance(logical_name);
CREATE INDEX server_cluster USING BTREE
	ON dict_dataset_instance(server_cluster, deployment_tier, data_center, slice);
CREATE INDEX native_name USING BTREE
	ON dict_dataset_instance(native_name);


CREATE TABLE stg_dict_dataset_instance  (
	dataset_urn          	varchar(200) NOT NULL,
	db_id                	smallint(6) UNSIGNED NOT NULL DEFAULT '0',
	deployment_tier      	enum('local','grid','dev','int','ei','ei2','ei3','qa','stg','prod') NOT NULL DEFAULT 'dev',
	data_center          	varchar(30) COMMENT 'data center code: lva1, ltx1, dc2, dc3...'  NULL DEFAULT '*',
	server_cluster       	varchar(150) COMMENT 'sfo1-bigserver'  NULL DEFAULT '*',
	slice                	varchar(50) COMMENT 'virtual group/tenant id/instance tag'  NOT NULL DEFAULT '*',
  is_active             BOOLEAN NULL COMMENT 'is the dataset active / exist ?',
  is_deprecated         BOOLEAN NULL COMMENT 'is the dataset deprecated by user ?',
	native_name          	varchar(250) NOT NULL,
	logical_name         	varchar(250) NOT NULL,
	version              	varchar(30) COMMENT '1.2.3 or 0.3.131'  NULL,
	schema_text           MEDIUMTEXT CHARACTER SET utf8 NULL,
	ddl_text              MEDIUMTEXT CHARACTER SET utf8 NULL,
	instance_created_time	int(10) UNSIGNED COMMENT 'source instance created time'  NULL,
	created_time         	int(10) UNSIGNED COMMENT 'wherehows created time'  NULL,
	wh_etl_exec_id       	bigint(20) COMMENT 'wherehows etl execution id that modified this record'  NULL,
	dataset_id           	int(11) UNSIGNED NULL,
	abstract_dataset_urn 	varchar(200) NULL,
	PRIMARY KEY(dataset_urn,db_id)
)
ENGINE = InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci
AUTO_INCREMENT = 0
	PARTITION BY HASH(db_id)
	(PARTITION p0,
	PARTITION p1,
	PARTITION p2,
	PARTITION p3,
	PARTITION p4,
	PARTITION p5,
	PARTITION p6,
	PARTITION p7);
CREATE INDEX server_cluster USING BTREE
	ON stg_dict_dataset_instance(server_cluster, deployment_tier, data_center, slice);

--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- configuration tables
CREATE TABLE `wh_etl_job_schedule` (
  `wh_etl_job_name` VARCHAR(127)  NOT NULL
  COMMENT 'etl job name',
  `enabled`         BOOLEAN       DEFAULT NULL
  COMMENT 'job currently enabled or disabled',
  `next_run`        INT(10) UNSIGNED     DEFAULT NULL
  COMMENT 'next run time',
  PRIMARY KEY (`wh_etl_job_name`),
  UNIQUE KEY `etl_unique` (`wh_etl_job_name`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET=utf8
  COMMENT='WhereHows ETL job scheduling table';

CREATE TABLE `wh_etl_job_history` (
  `wh_etl_exec_id`  BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT
  COMMENT 'job execution id',
  `wh_etl_job_name` VARCHAR(127)                 NOT NULL
  COMMENT 'name of the etl job',
  `status`          VARCHAR(31)                  DEFAULT NULL
  COMMENT 'status of etl job execution',
  `request_time`    INT(10) UNSIGNED             DEFAULT NULL
  COMMENT 'request time of the execution',
  `start_time`      INT(10) UNSIGNED             DEFAULT NULL
  COMMENT 'start time of the execution',
  `end_time`        INT(10) UNSIGNED             DEFAULT NULL
  COMMENT 'end time of the execution',
  `message`         VARCHAR(1024)                DEFAULT NULL
  COMMENT 'debug information message',
  `host_name`       VARCHAR(200)                 DEFAULT NULL
  COMMENT 'host machine name of the job execution',
  `process_id`      INT UNSIGNED                 DEFAULT NULL
  COMMENT 'job execution process id',
  PRIMARY KEY (`wh_etl_exec_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'WhereHows ETL execution history table';

CREATE TABLE `cfg_application` (
  `app_id`                  SMALLINT    UNSIGNED NOT NULL,
  `app_code`                VARCHAR(128)         NOT NULL,
  `description`             VARCHAR(512)         NOT NULL,
  `tech_matrix_id`          SMALLINT(5) UNSIGNED DEFAULT '0',
  `doc_url`                 VARCHAR(512)         DEFAULT NULL,
  `parent_app_id`           INT(11) UNSIGNED     NOT NULL,
  `app_status`              CHAR(1)              NOT NULL,
  `last_modified`           TIMESTAMP            NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_logical`              CHAR(1)                       DEFAULT NULL,
  `uri_type`                VARCHAR(25)                   DEFAULT NULL,
  `uri`                     VARCHAR(1000)                 DEFAULT NULL,
  `lifecycle_layer_id`      TINYINT(4) UNSIGNED           DEFAULT NULL,
  `short_connection_string` VARCHAR(50)                   DEFAULT NULL,
  PRIMARY KEY (`app_id`),
  UNIQUE KEY `idx_cfg_application__appcode` (`app_code`) USING HASH
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE cfg_database  (
	db_id                  	smallint(6) UNSIGNED NOT NULL,
	db_code                	varchar(30) COMMENT 'Unique string without space'  NOT NULL,
	primary_dataset_type    varchar(30) COMMENT 'What type of dataset this DB supports' NOT NULL DEFAULT '*',
	description            	varchar(128) NOT NULL,
	is_logical             	char(1) COMMENT 'Is a group, which contains multiple physical DB(s)'  NOT NULL DEFAULT 'N',
	deployment_tier        	varchar(20) COMMENT 'Lifecycle/FabricGroup: local,dev,sit,ei,qa,canary,preprod,pr'  NULL DEFAULT 'prod',
	data_center            	varchar(200) COMMENT 'Code name of its primary data center. Put * for all data cen'  NULL DEFAULT '*',
	associated_dc_num      	tinyint(4) UNSIGNED COMMENT 'Number of associated data centers'  NOT NULL DEFAULT '1',
	cluster                	varchar(200) COMMENT 'Name of Fleet, Group of Servers or a Server'  NULL DEFAULT '*',
	cluster_size           	smallint(6) COMMENT 'Num of servers in the cluster'  NOT NULL DEFAULT '1',
	extra_deployment_tag1  	varchar(50) COMMENT 'Additional tag. Such as container_group:HIGH'  NULL,
	extra_deployment_tag2  	varchar(50) COMMENT 'Additional tag. Such as slice:i0001'  NULL,
	extra_deployment_tag3  	varchar(50) COMMENT 'Additional tag. Such as region:eu-west-1'  NULL,
	replication_role       	varchar(10) COMMENT 'master or slave or broker'  NULL,
	jdbc_url               	varchar(1000) NULL,
	uri                    	varchar(1000) NULL,
	short_connection_string	varchar(50) COMMENT 'Oracle TNS Name, ODBC DSN, TDPID...' NULL,
  last_modified          	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(db_id),
  UNIQUE KEY `uix_cfg_database__dbcode` (db_code) USING HASH
)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COMMENT = 'Abstract different storage instances as databases' ;


CREATE TABLE stg_cfg_object_name_map  (
	object_type             	varchar(100) NOT NULL,
	object_sub_type         	varchar(100) NULL,
	object_name             	varchar(350) NOT NULL,
	object_urn              	varchar(350) NULL,
	object_dataset_id       	int(11) UNSIGNED NULL,
	map_phrase              	varchar(100) NULL,
	is_identical_map        	char(1) NULL DEFAULT 'N',
	mapped_object_type      	varchar(100) NOT NULL,
	mapped_object_sub_type  	varchar(100) NULL,
	mapped_object_name      	varchar(350) NOT NULL,
	mapped_object_urn       	varchar(350) NULL,
	mapped_object_dataset_id	int(11) UNSIGNED NULL,
	description             	varchar(500) NULL,
	last_modified           	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(object_name, mapped_object_name),
  KEY idx_stg_cfg_object_name_map__mappedobjectname (mapped_object_name) USING BTREE
)
ENGINE = InnoDB
CHARACTER SET latin1
COLLATE latin1_swedish_ci
COMMENT = 'Map alias (when is_identical_map=Y) and view dependency' ;

CREATE TABLE cfg_object_name_map  (
  obj_name_map_id         int(11) AUTO_INCREMENT NOT NULL,
  object_type             varchar(100) NOT NULL,
  object_sub_type         varchar(100) NULL,
  object_name             varchar(350) NOT NULL COMMENT 'this is the derived/child object',
  map_phrase              varchar(100) NULL,
  object_dataset_id       int(11) UNSIGNED NULL COMMENT 'can be the abstract dataset id for versioned objects',
  is_identical_map        char(1) NOT NULL DEFAULT 'N' COMMENT 'Y/N',
  mapped_object_type      varchar(100) NOT NULL,
  mapped_object_sub_type  varchar(100) NULL,
  mapped_object_name      varchar(350) NOT NULL COMMENT 'this is the original/parent object',
  mapped_object_dataset_id	int(11) UNSIGNED NULL COMMENT 'can be the abstract dataset id for versioned objects',
  description             varchar(500) NULL,
  last_modified           timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(obj_name_map_id),
  KEY idx_cfg_object_name_map__mappedobjectname (mapped_object_name) USING BTREE,
  CONSTRAINT uix_cfg_object_name_map__objectname_mappedobjectname UNIQUE (object_name, mapped_object_name)
)
ENGINE = InnoDB
CHARACTER SET latin1
AUTO_INCREMENT = 1
COMMENT = 'Map alias (when is_identical_map=Y) and view dependency. Always map from Derived/Child (object) back to its Original/Parent (mapped_object)' ;


CREATE TABLE cfg_deployment_tier  (
  tier_id      	tinyint(4) NOT NULL,
  tier_code    	varchar(25) COMMENT 'local,dev,test,qa,stg,prod' NOT NULL,
  tier_label    varchar(50) COMMENT 'display full name' NULL,
  sort_id       smallint(6) COMMENT '3-digit for group, 3-digit within group' NOT NULL,
  last_modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(tier_id),
  UNIQUE KEY uix_cfg_deployment_tier__tiercode (tier_code)
)
ENGINE = InnoDB
AUTO_INCREMENT = 0
COMMENT = 'http://en.wikipedia.org/wiki/Deployment_environment';


CREATE TABLE cfg_data_center  (
	data_center_id    	smallint(6) NOT NULL DEFAULT '0',
	data_center_code  	varchar(30) NOT NULL,
	data_center_name  	varchar(50) NOT NULL,
	time_zone         	varchar(50) NOT NULL,
	city              	varchar(50) NOT NULL,
	state             	varchar(25) NULL,
	country           	varchar(50) NOT NULL,
	longtitude        	decimal(10,6) NULL,
	latitude          	decimal(10,6) NULL,
	data_center_status	char(1) COMMENT 'A,D,U' NULL,
	last_modified     	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(data_center_id),
  UNIQUE KEY uix_cfg_data_center__datacentercode (data_center_code)
)
ENGINE = InnoDB
AUTO_INCREMENT = 0
COMMENT = 'https://en.wikipedia.org/wiki/Data_center' ;


CREATE TABLE cfg_cluster  (
	cluster_id    	        smallint(6) NOT NULL DEFAULT '0',
	cluster_code  	        varchar(80) NOT NULL,
	cluster_short_name      varchar(50) NOT NULL,
	cluster_type       	varchar(50) NOT NULL,
	deployment_tier_code    varchar(25) NOT NULL,
	data_center_code        varchar(30) NULL,
	description             varchar(200) NULL,
	last_modified     	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(cluster_id),
  UNIQUE KEY uix_cfg_cluster__clustercode (cluster_code)
)
COMMENT = 'https://en.wikipedia.org/wiki/Computer_cluster' ;


CREATE TABLE IF NOT EXISTS cfg_search_score_boost (
  `id` INT COMMENT 'dataset id',
  `static_boosting_score` INT COMMENT 'static boosting score for elastic search',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

CREATE TABLE flow (
  app_id               SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id              INT UNSIGNED      NOT NULL
  COMMENT 'flow id either inherit from source or generated',
  flow_name            VARCHAR(255) COMMENT 'name of the flow',
  flow_group           VARCHAR(255) COMMENT 'flow group or project name',
  flow_path            VARCHAR(1024) COMMENT 'flow path from top level',
  flow_level           SMALLINT COMMENT 'flow level, 0 for top level flow',
  source_created_time  INT UNSIGNED COMMENT 'source created time of the flow',
  source_modified_time INT UNSIGNED COMMENT 'latest source modified time of the flow',
  source_version       VARCHAR(255) COMMENT 'latest source version of the flow',
  is_active            CHAR(1) COMMENT 'determine if it is an active flow',
  is_scheduled         CHAR(1) COMMENT 'determine if it is a scheduled flow',
  pre_flows            VARCHAR(2048) COMMENT 'comma separated flow ids that run before this flow',
  main_tag_id          INT COMMENT 'main tag id',
  created_time         INT UNSIGNED COMMENT 'wherehows created time of the flow',
  modified_time        INT UNSIGNED COMMENT 'latest wherehows modified time of the flow',
  wh_etl_exec_id       BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255)),
  INDEX flow_name_idx (app_id, flow_group(127), flow_name(127))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow (
  app_id               SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id              INT UNSIGNED COMMENT 'flow id either inherit from source or generated',
  flow_name            VARCHAR(255) COMMENT 'name of the flow',
  flow_group           VARCHAR(255) COMMENT 'flow group or project name',
  flow_path            VARCHAR(1024) COMMENT 'flow path from top level',
  flow_level           SMALLINT COMMENT 'flow level, 0 for top level flow',
  source_created_time  INT UNSIGNED COMMENT 'source created time of the flow',
  source_modified_time INT UNSIGNED COMMENT 'latest source modified time of the flow',
  source_version       VARCHAR(255) COMMENT 'latest source version of the flow',
  is_active            CHAR(1) COMMENT 'determine if it is an active flow',
  is_scheduled         CHAR(1) COMMENT 'determine if it is a scheduled flow',
  pre_flows            VARCHAR(2048) COMMENT 'comma separated flow ids that run before this flow',
  main_tag_id          INT COMMENT 'main tag id',
  created_time         INT UNSIGNED COMMENT 'wherehows created time of the flow',
  modified_time        INT UNSIGNED COMMENT 'latest wherehows modified time of the flow',
  wh_etl_exec_id       BIGINT COMMENT 'wherehows etl execution id that modified this record',
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_source_id_map (
  app_id           SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id          INT UNSIGNED      NOT NULL AUTO_INCREMENT
  COMMENT 'flow id generated ',
  source_id_string VARCHAR(1024) COMMENT 'source string id of the flow',
  source_id_uuid   VARCHAR(255) COMMENT 'source uuid id of the flow',
  source_id_uri    VARCHAR(255) COMMENT 'source uri id of the flow',
  PRIMARY KEY (app_id, flow_id),
  INDEX flow_path_idx (app_id, source_id_string(255))
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow id mapping table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_job (
  app_id               SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id              INT UNSIGNED      NOT NULL
  COMMENT 'flow id',
  first_source_version VARCHAR(255) COMMENT 'first source version of the flow under this dag version',
  last_source_version  VARCHAR(255) COMMENT 'last source version of the flow under this dag version',
  dag_version          INT               NOT NULL
  COMMENT 'derived dag version of the flow',
  job_id               INT UNSIGNED      NOT NULL
  COMMENT 'job id either inherit from source or generated',
  job_name             VARCHAR(255) COMMENT 'job name',
  job_path             VARCHAR(1024) COMMENT 'job path from top level',
  job_type_id          SMALLINT COMMENT 'type id of the job',
  job_type             VARCHAR(63) COMMENT 'type of the job',
  ref_flow_id          INT UNSIGNED NULL COMMENT 'the reference flow id of the job if the job is a subflow',
  pre_jobs             VARCHAR(20000) CHAR SET latin1 COMMENT 'comma separated job ids that run before this job',
  post_jobs            VARCHAR(20000) CHAR SET latin1 COMMENT 'comma separated job ids that run after this job',
  is_current           CHAR(1) COMMENT 'determine if it is a current job',
  is_first             CHAR(1) COMMENT 'determine if it is the first job',
  is_last              CHAR(1) COMMENT 'determine if it is the last job',
  created_time         INT UNSIGNED COMMENT 'wherehows created time of the flow',
  modified_time        INT UNSIGNED COMMENT 'latest wherehows modified time of the flow',
  wh_etl_exec_id       BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, job_id, dag_version),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX ref_flow_id_idx (app_id, ref_flow_id),
  INDEX job_path_idx (app_id, job_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler job table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_job (
  app_id         SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id        INT UNSIGNED COMMENT 'flow id',
  flow_path      VARCHAR(1024) COMMENT 'flow path from top level',
  source_version VARCHAR(255) COMMENT 'last source version of the flow under this dag version',
  dag_version    INT COMMENT 'derived dag version of the flow',
  job_id         INT UNSIGNED COMMENT 'job id either inherit from source or generated',
  job_name       VARCHAR(255) COMMENT 'job name',
  job_path       VARCHAR(1024) COMMENT 'job path from top level',
  job_type_id    SMALLINT COMMENT 'type id of the job',
  job_type       VARCHAR(63) COMMENT 'type of the job',
  ref_flow_id    INT UNSIGNED  NULL COMMENT 'the reference flow id of the job if the job is a subflow',
  ref_flow_path  VARCHAR(1024) COMMENT 'the reference flow path of the job if the job is a subflow',
  pre_jobs       VARCHAR(20000) CHAR SET latin1 COMMENT 'comma separated job ids that run before this job',
  post_jobs      VARCHAR(20000) CHAR SET latin1 COMMENT 'comma separated job ids that run after this job',
  is_current     CHAR(1) COMMENT 'determine if it is a current job',
  is_first       CHAR(1) COMMENT 'determine if it is the first job',
  is_last        CHAR(1) COMMENT 'determine if it is the last job',
  wh_etl_exec_id BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX (app_id, job_id, dag_version),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255)),
  INDEX ref_flow_path_idx (app_id, ref_flow_path(255)),
  INDEX job_path_idx (app_id, job_path(255)),
  INDEX job_type_idx (job_type)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler job table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE job_source_id_map (
  app_id           SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  job_id           INT UNSIGNED      NOT NULL AUTO_INCREMENT
  COMMENT 'job id generated',
  source_id_string VARCHAR(1024) COMMENT 'job full path string',
  source_id_uuid   VARCHAR(255) COMMENT 'source uuid id of the flow',
  source_id_uri    VARCHAR(255) COMMENT 'source uri id of the flow',
  PRIMARY KEY (app_id, job_id),
  INDEX job_path_idx (app_id, source_id_string(255))
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow id mapping table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_dag (
  app_id         SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id        INT UNSIGNED NOT NULL
  COMMENT 'flow id',
  source_version VARCHAR(255) COMMENT 'last source version of the flow under this dag version',
  dag_version    INT COMMENT 'derived dag version of the flow',
  dag_md5        VARCHAR(255) COMMENT 'md5 checksum for this dag version',
  is_current     CHAR(1) COMMENT 'if this source version of the flow is current',
  wh_etl_exec_id BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, flow_id, source_version),
  INDEX flow_dag_md5_idx (app_id, flow_id, dag_md5),
  INDEX flow_id_idx (app_id, flow_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Flow dag reference table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_dag (
  app_id         SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id        INT UNSIGNED NOT NULL
  COMMENT 'flow id',
  source_version VARCHAR(255) COMMENT 'last source version of the flow under this dag version',
  dag_version    INT COMMENT 'derived dag version of the flow',
  dag_md5        VARCHAR(255) COMMENT 'md5 checksum for this dag version',
  wh_etl_exec_id BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, flow_id, source_version),
  INDEX flow_dag_md5_idx (app_id, flow_id, dag_md5),
  INDEX flow_id_idx (app_id, flow_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Flow dag reference table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_dag_edge (
  app_id          SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id         INT UNSIGNED COMMENT 'flow id',
  flow_path       VARCHAR(1024) COMMENT 'flow path from top level',
  source_version  VARCHAR(255) COMMENT 'last source version of the flow under this dag version',
  source_job_id   INT UNSIGNED COMMENT 'job id either inherit from source or generated',
  source_job_path VARCHAR(1024) COMMENT 'source job path from top level',
  target_job_id   INT UNSIGNED COMMENT 'job id either inherit from source or generated',
  target_job_path VARCHAR(1024) COMMENT 'target job path from top level',
  wh_etl_exec_id  BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX flow_version_idx (app_id, flow_id, source_version),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255)),
  INDEX source_job_path_idx (app_id, source_job_path(255)),
  INDEX target_job_path_idx (app_id, target_job_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Flow dag table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_execution (
  app_id           SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_exec_id     BIGINT UNSIGNED   NOT NULL
  COMMENT 'flow execution id either from the source or generated',
  flow_exec_uuid   VARCHAR(255) COMMENT 'source flow execution uuid',
  flow_id          INT UNSIGNED      NOT NULL
  COMMENT 'flow id',
  flow_name        VARCHAR(255) COMMENT 'name of the flow',
  source_version   VARCHAR(255) COMMENT 'source version of the flow',
  flow_exec_status VARCHAR(31) COMMENT 'status of flow execution',
  attempt_id       SMALLINT COMMENT 'attempt id',
  executed_by      VARCHAR(127) COMMENT 'people who executed the flow',
  start_time       INT UNSIGNED COMMENT 'start time of the flow execution',
  end_time         INT UNSIGNED COMMENT 'end time of the flow execution',
  is_adhoc         CHAR(1) COMMENT 'determine if it is a ad-hoc execution',
  is_backfill      CHAR(1) COMMENT 'determine if it is a back-fill execution',
  created_time     INT UNSIGNED COMMENT 'etl create time',
  modified_time    INT UNSIGNED COMMENT 'etl modified time',
  wh_etl_exec_id   BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, flow_exec_id),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_name_idx (app_id, flow_name)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow execution table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_execution_id_map (
  app_id             SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_exec_id       BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT
  COMMENT 'generated flow execution id',
  source_exec_string VARCHAR(1024) COMMENT 'source flow execution string',
  source_exec_uuid   VARCHAR(255) COMMENT 'source uuid id of the flow execution',
  source_exec_uri    VARCHAR(255) COMMENT 'source uri id of the flow execution',
  PRIMARY KEY (app_id, flow_exec_id),
  INDEX flow_exec_uuid_idx (app_id, source_exec_uuid)
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow execution id mapping table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_execution (
  app_id           SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_exec_id     BIGINT UNSIGNED COMMENT 'flow execution id',
  flow_exec_uuid   VARCHAR(255) COMMENT 'source flow execution uuid',
  flow_id          INT UNSIGNED COMMENT 'flow id',
  flow_name        VARCHAR(255) COMMENT 'name of the flow',
  flow_path        VARCHAR(1024) COMMENT 'flow path from top level',
  source_version   VARCHAR(255) COMMENT 'source version of the flow',
  flow_exec_status VARCHAR(31) COMMENT 'status of flow execution',
  attempt_id       SMALLINT COMMENT 'attempt id',
  executed_by      VARCHAR(127) COMMENT 'people who executed the flow',
  start_time       INT UNSIGNED COMMENT 'start time of the flow execution',
  end_time         INT UNSIGNED COMMENT 'end time of the flow execution',
  is_adhoc         CHAR(1) COMMENT 'determine if it is a ad-hoc execution',
  is_backfill      CHAR(1) COMMENT 'determine if it is a back-fill execution',
  wh_etl_exec_id   BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX flow_exec_idx (app_id, flow_exec_id),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow execution table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE job_execution (
  app_id          SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_exec_id    BIGINT UNSIGNED COMMENT 'flow execution id',
  job_exec_id     BIGINT UNSIGNED   NOT NULL
  COMMENT 'job execution id either inherit or generated',
  job_exec_uuid   VARCHAR(255) COMMENT 'job execution uuid',
  flow_id         INT UNSIGNED      NOT NULL
  COMMENT 'flow id',
  source_version  VARCHAR(255) COMMENT 'source version of the flow',
  job_id          INT UNSIGNED      NOT NULL
  COMMENT 'job id',
  job_name        VARCHAR(255) COMMENT 'job name',
  job_exec_status VARCHAR(31) COMMENT 'status of flow execution',
  attempt_id      SMALLINT COMMENT 'attempt id',
  start_time      INT UNSIGNED COMMENT 'start time of the execution',
  end_time        INT UNSIGNED COMMENT 'end time of the execution',
  is_adhoc        CHAR(1) COMMENT 'determine if it is a ad-hoc execution',
  is_backfill     CHAR(1) COMMENT 'determine if it is a back-fill execution',
  created_time    INT UNSIGNED COMMENT 'etl create time',
  modified_time   INT UNSIGNED COMMENT 'etl modified time',
  wh_etl_exec_id  BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, job_exec_id),
  INDEX flow_exec_id_idx (app_id, flow_exec_id),
  INDEX job_id_idx (app_id, job_id),
  INDEX flow_id_idx (app_id, flow_id),
  INDEX job_name_idx (app_id, flow_id, job_name)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler job execution table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE job_execution_id_map (
  app_id             SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the job',
  job_exec_id        BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT
  COMMENT 'generated job execution id',
  source_exec_string VARCHAR(1024) COMMENT 'source job execution string',
  source_exec_uuid   VARCHAR(255) COMMENT 'source uuid id of the job execution',
  source_exec_uri    VARCHAR(255) COMMENT 'source uri id of the job execution',
  PRIMARY KEY (app_id, job_exec_id),
  INDEX job_exec_uuid_idx (app_id, source_exec_uuid)
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler job execution id mapping table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_job_execution (
  app_id          SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id         INT UNSIGNED COMMENT 'flow id',
  flow_path       VARCHAR(1024) COMMENT 'flow path from top level',
  source_version  VARCHAR(255) COMMENT 'source version of the flow',
  flow_exec_id    BIGINT UNSIGNED COMMENT 'flow execution id',
  flow_exec_uuid  VARCHAR(255) COMMENT 'flow execution uuid',
  job_id          INT UNSIGNED COMMENT 'job id',
  job_name        VARCHAR(255) COMMENT 'job name',
  job_path        VARCHAR(1024) COMMENT 'job path from top level',
  job_exec_id     BIGINT UNSIGNED COMMENT 'job execution id either inherit or generated',
  job_exec_uuid   VARCHAR(255) COMMENT 'job execution uuid',
  job_exec_status VARCHAR(31) COMMENT 'status of flow execution',
  attempt_id      SMALLINT COMMENT 'attempt id',
  start_time      INT UNSIGNED COMMENT 'start time of the execution',
  end_time        INT UNSIGNED COMMENT 'end time of the execution',
  is_adhoc        CHAR(1) COMMENT 'determine if it is a ad-hoc execution',
  is_backfill     CHAR(1) COMMENT 'determine if it is a back-fill execution',
  wh_etl_exec_id  BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX flow_id_idx (app_id, flow_id),
  INDEX flow_path_idx (app_id, flow_path(255)),
  INDEX job_path_idx (app_id, job_path(255)),
  INDEX flow_exec_idx (app_id, flow_exec_id),
  INDEX job_exec_idx (app_id, job_exec_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler job execution table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_schedule (
  app_id               SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id              INT UNSIGNED      NOT NULL
  COMMENT 'flow id',
  unit                 VARCHAR(31) COMMENT 'unit of time',
  frequency            INT COMMENT 'frequency of the unit',
  cron_expression      VARCHAR(127) COMMENT 'cron expression',
  is_active            CHAR(1) COMMENT 'determine if it is an active schedule',
  included_instances   VARCHAR(127) COMMENT 'included instance',
  excluded_instances   VARCHAR(127) COMMENT 'excluded instance',
  effective_start_time INT UNSIGNED COMMENT 'effective start time of the flow execution',
  effective_end_time   INT UNSIGNED COMMENT 'effective end time of the flow execution',
  created_time         INT UNSIGNED COMMENT 'etl create time',
  modified_time        INT UNSIGNED COMMENT 'etl modified time',
  ref_id               VARCHAR(255) COMMENT 'reference id of this schedule',
  wh_etl_exec_id       BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, flow_id, ref_id),
  INDEX (app_id, flow_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow schedule table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_schedule (
  app_id               SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id              INT UNSIGNED COMMENT 'flow id',
  flow_path            VARCHAR(1024) COMMENT 'flow path from top level',
  unit                 VARCHAR(31) COMMENT 'unit of time',
  frequency            INT COMMENT 'frequency of the unit',
  cron_expression      VARCHAR(127) COMMENT 'cron expression',
  included_instances   VARCHAR(127) COMMENT 'included instance',
  excluded_instances   VARCHAR(127) COMMENT 'excluded instance',
  effective_start_time INT UNSIGNED COMMENT 'effective start time of the flow execution',
  effective_end_time   INT UNSIGNED COMMENT 'effective end time of the flow execution',
  ref_id               VARCHAR(255) COMMENT 'reference id of this schedule',
  wh_etl_exec_id       BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX (app_id, flow_id),
  INDEX (app_id, flow_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler flow schedule table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE flow_owner_permission (
  app_id         SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id        INT UNSIGNED      NOT NULL
  COMMENT 'flow id',
  owner_id       VARCHAR(63) COMMENT 'identifier of the owner',
  permissions    VARCHAR(255) COMMENT 'permissions of the owner',
  owner_type     VARCHAR(31) COMMENT 'whether is a group owner or not',
  created_time   INT UNSIGNED COMMENT 'etl create time',
  modified_time  INT UNSIGNED COMMENT 'etl modified time',
  wh_etl_exec_id BIGINT COMMENT 'wherehows etl execution id that create this record',
  PRIMARY KEY (app_id, flow_id, owner_id),
  INDEX flow_index (app_id, flow_id),
  INDEX owner_index (app_id, owner_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler owner table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE stg_flow_owner_permission (
  app_id         SMALLINT UNSIGNED NOT NULL
  COMMENT 'application id of the flow',
  flow_id        INT UNSIGNED COMMENT 'flow id',
  flow_path      VARCHAR(1024) COMMENT 'flow path from top level',
  owner_id       VARCHAR(63) COMMENT 'identifier of the owner',
  permissions    VARCHAR(255) COMMENT 'permissions of the owner',
  owner_type     VARCHAR(31) COMMENT 'whether is a group owner or not',
  wh_etl_exec_id BIGINT COMMENT 'wherehows etl execution id that create this record',
  INDEX flow_index (app_id, flow_id),
  INDEX owner_index (app_id, owner_id),
  INDEX flow_path_idx (app_id, flow_path(255))
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'Scheduler owner table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE job_execution_ext_reference (
	app_id         	smallint(5) UNSIGNED COMMENT 'application id of the flow'  NOT NULL,
	job_exec_id    	bigint(20) UNSIGNED COMMENT 'job execution id either inherit or generated'  NOT NULL,
	attempt_id     	smallint(6) COMMENT 'job execution attempt id'  DEFAULT '0',
	ext_ref_type	varchar(50) COMMENT 'YARN_JOB_ID, DB_SESSION_ID, PID, INFA_WORKFLOW_RUN_ID, CASSCADE_WORKFLOW_ID'  NOT NULL,
    ext_ref_sort_id smallint(6) COMMENT 'sort id 0..n within each ext_ref_type' NOT NULL DEFAULT '0',
	ext_ref_id      varchar(100) COMMENT 'external reference id' NOT NULL,
	created_time   	int(10) UNSIGNED COMMENT 'etl create time'  NULL,
	wh_etl_exec_id 	bigint(20) COMMENT 'wherehows etl execution id that create this record'  NULL,
	PRIMARY KEY(app_id,job_exec_id,attempt_id,ext_ref_type,ext_ref_sort_id)
)
ENGINE = InnoDB
DEFAULT CHARSET = latin1
COMMENT = 'External reference ids for the job execution'
PARTITION BY HASH(app_id)
   (	PARTITION p0,
	PARTITION p1,
	PARTITION p2,
	PARTITION p3,
	PARTITION p4,
	PARTITION p5,
	PARTITION p6,
	PARTITION p7)
;

CREATE INDEX idx_job_execution_ext_ref__ext_ref_id USING BTREE
	ON job_execution_ext_reference(ext_ref_id);


CREATE TABLE stg_job_execution_ext_reference (
	app_id         	smallint(5) UNSIGNED COMMENT 'application id of the flow'  NOT NULL,
	job_exec_id    	bigint(20) UNSIGNED COMMENT 'job execution id either inherit or generated'  NOT NULL,
	attempt_id     	smallint(6) COMMENT 'job execution attempt id'  DEFAULT '0',
	ext_ref_type	varchar(50) COMMENT 'YARN_JOB_ID, DB_SESSION_ID, PID, INFA_WORKFLOW_RUN_ID, CASSCADE_WORKFLOW_ID'  NOT NULL,
    ext_ref_sort_id smallint(6) COMMENT 'sort id 0..n within each ext_ref_type' NOT NULL DEFAULT '0',
	ext_ref_id      varchar(100) COMMENT 'external reference id' NOT NULL,
	created_time   	int(10) UNSIGNED COMMENT 'etl create time'  NULL,
	wh_etl_exec_id 	bigint(20) COMMENT 'wherehows etl execution id that create this record'  NULL,
	PRIMARY KEY(app_id,job_exec_id,attempt_id,ext_ref_type,ext_ref_sort_id)
)
ENGINE = InnoDB
DEFAULT CHARSET = latin1
COMMENT = 'staging table for job_execution_ext_reference'
PARTITION BY HASH(app_id)
   (	PARTITION p0,
	PARTITION p1,
	PARTITION p2,
	PARTITION p3,
	PARTITION p4,
	PARTITION p5,
	PARTITION p6,
	PARTITION p7)
;

CREATE TABLE `cfg_job_type` (
  `job_type_id` SMALLINT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `job_type`    VARCHAR(50)          NOT NULL,
  `description` VARCHAR(200)         NULL,
  PRIMARY KEY (`job_type_id`),
  UNIQUE KEY `ak_cfg_job_type__job_type` (`job_type`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 55
  DEFAULT CHARSET = utf8
  COMMENT = 'job types used in mutliple schedulers';

CREATE TABLE `cfg_job_type_reverse_map` (
  `job_type_actual`   VARCHAR(50)
                      CHARACTER SET ascii NOT NULL,
  `job_type_id`       SMALLINT(6) UNSIGNED NOT NULL,
  `description`       VARCHAR(200)         NULL,
  `job_type_standard` VARCHAR(50)          NOT NULL,
  PRIMARY KEY (`job_type_actual`),
  UNIQUE KEY `cfg_job_type_reverse_map_uk` (`job_type_actual`),
  KEY `cfg_job_type_reverse_map_job_type_id_fk` (`job_type_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = 'The reverse map of the actual job type to standard job type';
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

CREATE TABLE `source_code_commit_info` (
  `app_id`          SMALLINT(5) UNSIGNED DEFAULT NULL,
  `repository_urn`  VARCHAR(300) CHAR SET latin1 NOT NULL COMMENT 'the git repo urn',
  `commit_id`       VARCHAR(50) CHAR SET latin1  NOT NULL COMMENT 'the sha-1 hash of the commit',
  `file_path`       VARCHAR(600) CHAR SET latin1 NOT NULL COMMENT 'the path to the file',
  `file_name`       VARCHAR(127)                 NOT NULL COMMENT 'the file name',
  `commit_time`     INT UNSIGNED COMMENT 'the commit time',
  `committer_name`  VARCHAR(128)                 NOT NULL COMMENT 'name of the committer',
  `committer_email` VARCHAR(128)         DEFAULT NULL COMMENT 'email of the committer',
  `author_name`     VARCHAR(128)                 NOT NULL COMMENT 'name of the author',
  `author_email`    VARCHAR(128)                 NOT NULL COMMENT 'email of the author',
  `message`         VARCHAR(1024)                NOT NULL COMMENT 'message of the commit',
  `created_time`    INT UNSIGNED COMMENT 'wherehows created time',
  `modified_time`   INT UNSIGNED COMMENT 'latest wherehows modified',
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (repository_urn, file_path, commit_id),
  KEY (commit_id),
  KEY (repository_urn, file_name, committer_email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE `stg_source_code_commit_info` (
  `app_id`          SMALLINT(5) UNSIGNED DEFAULT NULL,
  `repository_urn`  VARCHAR(300) CHAR SET latin1 NOT NULL COMMENT 'the git repo urn',
  `commit_id`       VARCHAR(50) CHAR SET latin1  NOT NULL COMMENT 'the sha-1 hash of the commit',
  `file_path`       VARCHAR(600) CHAR SET latin1 NOT NULL COMMENT 'the path to the file',
  `file_name`       VARCHAR(127)                 NOT NULL COMMENT 'the file name',
  `commit_time`     INT UNSIGNED COMMENT 'the commit time',
  `committer_name`  VARCHAR(128)                 NOT NULL COMMENT 'name of the committer',
  `committer_email` VARCHAR(128)         DEFAULT NULL COMMENT 'email of the committer',
  `author_name`     VARCHAR(128)                 NOT NULL COMMENT 'name of the author',
  `author_email`    VARCHAR(128)                 NOT NULL COMMENT 'email of the author',
  `message`         VARCHAR(1024)                NOT NULL COMMENT 'message of the commit',
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (repository_urn, file_path, commit_id),
  KEY (commit_id),
  KEY (repository_urn, file_name, committer_email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;


CREATE TABLE `stg_git_project` (
  `app_id`          SMALLINT(5) UNSIGNED NOT NULL,
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  `project_name`    VARCHAR(100) NOT NULL,
  `scm_type`        VARCHAR(20) NOT NULL COMMENT 'git, svn or other',
  `owner_type`      VARCHAR(50) DEFAULT NULL,
  `owner_name`      VARCHAR(300) DEFAULT NULL COMMENT 'owner names in comma separated list',
  `create_time`     VARCHAR(50) DEFAULT NULL,
  `num_of_repos`    INT UNSIGNED DEFAULT NULL,
  `repos`           MEDIUMTEXT DEFAULT NULL COMMENT 'repo names in comma separated list',
  `license`         VARCHAR(100) DEFAULT NULL,
  `description`     MEDIUMTEXT CHAR SET utf8 DEFAULT NULL,
  PRIMARY KEY (`project_name`, `scm_type`, `app_id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `stg_product_repo` (
  `app_id`          SMALLINT(5) UNSIGNED NOT NULL,
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  `scm_repo_fullname` VARCHAR(100) NOT NULL,
  `scm_type`        VARCHAR(20) NOT NULL,
  `repo_id`         INT UNSIGNED DEFAULT NULL,
  `project`         VARCHAR(100) DEFAULT NULL,
  `dataset_group`   VARCHAR(200) DEFAULT NULL COMMENT 'dataset group name, database name, etc',
  `owner_type`      VARCHAR(50) DEFAULT NULL,
  `owner_name`      VARCHAR(300) DEFAULT NULL COMMENT 'owner names in comma separated list',
  `multiproduct_name` VARCHAR(100) DEFAULT NULL,
  `product_type`    VARCHAR(100) DEFAULT NULL,
  `product_version` VARCHAR(50) DEFAULT NULL,
  `namespace`       VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`scm_repo_fullname`, `scm_type`, `app_id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE `stg_repo_owner` (
  `app_id`          SMALLINT(5) UNSIGNED NOT NULL,
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  `scm_repo_fullname` VARCHAR(100) NOT NULL,
  `scm_type`        VARCHAR(20) NOT NULL,
  `repo_id`         INT DEFAULT NULL,
  `dataset_group`   VARCHAR(200) DEFAULT NULL COMMENT 'dataset group name, database name, etc',
  `owner_type`      VARCHAR(50) NOT NULL COMMENT 'which acl file this owner is in',
  `owner_name`      VARCHAR(50) NOT NULL COMMENT 'one owner name',
  `sort_id`         INT UNSIGNED DEFAULT NULL,
  `is_active`       CHAR(1) COMMENT 'if owner is active',
  `paths`           TEXT CHAR SET utf8 DEFAULT NULL COMMENT 'covered paths by this acl',
  PRIMARY KEY (`scm_repo_fullname`, `scm_type`, `owner_type`, `owner_name`, `app_id`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

CREATE TABLE stg_database_scm_map (
  `database_name`   VARCHAR(100) NOT NULL COMMENT 'database name',
  `database_type`   VARCHAR(50) NOT NULL COMMENT 'database type',
  `app_name`        VARCHAR(127) NOT NULL COMMENT 'the name of application',
  `scm_type`        VARCHAR(50) NOT NULL COMMENT 'scm type',
  `scm_url`         VARCHAR(127) DEFAULT NULL COMMENT 'scm url',
  `committers`      VARCHAR(500) DEFAULT NULL COMMENT 'committers',
  `filepath`        VARCHAR(200) DEFAULT NULL COMMENT 'filepath',
  `app_id`          SMALLINT(5) UNSIGNED COMMENT 'application id of the namesapce',
  `wh_etl_exec_id`  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`database_type`,`database_name`,`scm_type`,`app_name`)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- created statements for lineage related tables
CREATE TABLE IF NOT EXISTS `stg_job_execution_data_lineage` (
  `app_id`                 SMALLINT(5) UNSIGNED                                ,
  `flow_exec_id`           BIGINT(20) UNSIGNED                                 ,
  `job_exec_id`            BIGINT(20) UNSIGNED                                 ,
  `job_exec_uuid`          VARCHAR(100)                                        NULL,
  `job_name`               VARCHAR(255)                                        NULL,
  `job_start_unixtime`     BIGINT(20)                                          NOT NULL,
  `job_finished_unixtime`  BIGINT(20)                                          NOT NULL,

  `db_id`                  SMALLINT(5) UNSIGNED                                NULL,
  `abstracted_object_name` VARCHAR(255)                                        NOT NULL,
  `full_object_name`       VARCHAR(1000)                                       NOT NULL,
  `partition_start`        VARCHAR(50)                                         NULL,
  `partition_end`          VARCHAR(50)                                         NULL,
  `partition_type`         VARCHAR(20)                                         NULL,
  `layout_id`              SMALLINT(5) UNSIGNED                                NULL,
  `storage_type`           VARCHAR(16)                                         NULL,

  `source_target_type`     ENUM('source', 'target', 'lookup', 'temp') NOT NULL,
  `srl_no`                 SMALLINT(5) UNSIGNED                       NOT NULL DEFAULT '1'
  COMMENT 'the sorted number of this record in all records of this job related operation',
  `source_srl_no`          SMALLINT(5) UNSIGNED                                NULL
  COMMENT 'the related record of this record',
  `operation`              VARCHAR(64)                                         NULL,
  `record_count`           BIGINT(20) UNSIGNED                                 NULL,
  `insert_count`           BIGINT(20) UNSIGNED                                 NULL,
  `delete_count`           BIGINT(20) UNSIGNED                                 NULL,
  `update_count`           BIGINT(20) UNSIGNED                                 NULL,
  `flow_path`              VARCHAR(1024)                                       NULL,
  `created_date`           INT UNSIGNED,
  `wh_etl_exec_id`              INT(11)                                        NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS `job_execution_data_lineage` (
  `app_id`                 SMALLINT(5) UNSIGNED                       NOT NULL,
  `flow_exec_id`           BIGINT(20) UNSIGNED                                 NOT NULL,
  `job_exec_id`            BIGINT(20) UNSIGNED                                 NOT NULL
  COMMENT 'in azkaban this is a smart key combined execution id and sort id of the job',
  `job_exec_uuid`          VARCHAR(100)                                        NULL
  COMMENT 'some scheduler do not have this value, e.g. Azkaban',
  `job_name`               VARCHAR(255)                                        NOT NULL,
  `job_start_unixtime`     BIGINT(20)                                          NOT NULL,
  `job_finished_unixtime`  BIGINT(20)                                          NOT NULL,

  `db_id`                  SMALLINT(5) UNSIGNED                                NULL,
  `abstracted_object_name` VARCHAR(255)                               NOT NULL,
  `full_object_name`       VARCHAR(1000)                                       NULL,
  `partition_start`        VARCHAR(50)                                         NULL,
  `partition_end`          VARCHAR(50)                                         NULL,
  `partition_type`         VARCHAR(20)                                         NULL,
  `layout_id`              SMALLINT(5) UNSIGNED                                NULL
  COMMENT 'layout of the dataset',
  `storage_type`           VARCHAR(16)                                         NULL,

  `source_target_type`     ENUM('source', 'target', 'lookup', 'temp') NOT NULL,
  `srl_no`                 SMALLINT(5) UNSIGNED                       NOT NULL DEFAULT '1'
  COMMENT 'the sorted number of this record in all records of this job related operation',
  `source_srl_no`          SMALLINT(5) UNSIGNED                                NULL
  COMMENT 'the related record of this record',
  `operation`              VARCHAR(64)                                         NULL,
  `record_count`           BIGINT(20) UNSIGNED                                 NULL,
  `insert_count`           BIGINT(20) UNSIGNED                                 NULL,
  `delete_count`           BIGINT(20) UNSIGNED                                 NULL,
  `update_count`           BIGINT(20) UNSIGNED                                 NULL,
  `flow_path`              VARCHAR(1024)                                       NULL,
  `created_date`           INT UNSIGNED,
  `wh_etl_exec_id`              INT(11)                                        NULL,

  PRIMARY KEY (`app_id`, `job_exec_id`, `srl_no`),
  KEY `idx_flow_path` (`app_id`, `flow_path`(300)),
  KEY `idx_job_execution_data_lineage__object_name` (`abstracted_object_name`, `source_target_type`) USING BTREE
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1
  COMMENT = 'Lineage table' PARTITION BY HASH (app_id) PARTITIONS 8;

CREATE TABLE job_attempt_source_code  (
	application_id	int(11) NOT NULL,
	job_id        	int(11) NOT NULL,
	attempt_number	tinyint(4) NOT NULL,
	script_name   	varchar(256) NULL,
	script_path   	varchar(128) NOT NULL,
	script_type   	varchar(16) NOT NULL,
	script_md5_sum	binary(16) NULL,
	created_date  	datetime NOT NULL,
	PRIMARY KEY(application_id,job_id,attempt_number)
)
ENGINE = InnoDB
DEFAULT CHARSET = utf8;

CREATE TABLE `job_execution_script` (
  `app_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `script_name` varchar(512) NOT NULL DEFAULT '',
  `script_path` varchar(128) DEFAULT NULL,
  `script_type` varchar(16) NOT NULL,
  `chain_name` varchar(30) DEFAULT NULL,
  `job_name` varchar(30) DEFAULT NULL,
  `committer_name` varchar(128) NOT NULL DEFAULT '',
  `committer_email` varchar(128) DEFAULT NULL,
  `committer_ldap` varchar(30) DEFAULT NULL,
  `commit_time` datetime DEFAULT NULL,
  `script_url` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`app_id`,`job_id`,`script_name`(100),`committer_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--


CREATE TABLE `log_jira__hdfs_directory_to_owner_map` (
  `hdfs_name` varchar(50) NOT NULL,
  `directory_path` varchar(500) NOT NULL,
  `ref_directory_path` varchar(50) DEFAULT NULL,
  `hdfs_owner_id` varchar(50) DEFAULT NULL,
  `total_size_mb` bigint(20) DEFAULT NULL,
  `num_of_files` bigint(20) DEFAULT NULL,
  `earliest_file_creation_date` date DEFAULT NULL,
  `lastest_file_creation_date` date DEFAULT NULL,
  `jira_key` varchar(50) DEFAULT NULL,
  `jira_status` varchar(50) DEFAULT NULL,
  `jira_last_updated_time` bigint(20) DEFAULT NULL,
  `jira_created_time` bigint(20) DEFAULT NULL,
  `prev_jira_status` varchar(50) DEFAULT NULL,
  `prev_jira_status_changed_time` bigint(20) DEFAULT NULL,
  `current_assignee_id` varchar(50) DEFAULT NULL,
  `original_assignee_id` varchar(50) DEFAULT NULL,
  `watcher_id` varchar(50) DEFAULT NULL,
  `ref_manager_ids` varchar(1000) DEFAULT NULL,
  `ref_user_ids` varchar(2000) DEFAULT NULL,
  `modified` timestamp NULL DEFAULT NULL,
  `jira_component` varchar(100) DEFAULT NULL,
  `jira_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`directory_path`,`hdfs_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- metrics table
CREATE TABLE dict_business_metric  (
  `metric_id`                	SMALLINT(6) UNSIGNED AUTO_INCREMENT NOT NULL,
  `metric_name`              	VARCHAR(200) NOT NULL,
  `metric_description`       	VARCHAR(500) NULL,
  `dashboard_name`           	VARCHAR(100) COMMENT 'Hierarchy Level 1'  NULL,
  `metric_group`             	VARCHAR(100) COMMENT 'Hierarchy Level 2'  NULL,
  `metric_category`          	VARCHAR(100) COMMENT 'Hierarchy Level 3'  NULL,
  `metric_sub_category`         VARCHAR(100) COMMENT 'Additional Classification, such as Product, Line of Business' NULL,
  `metric_level`		VARCHAR(50) COMMENT 'CORE, DEPARTMENT, TEAM, OPERATION, STRATEGIC, TIER1, TIER2' NULL,
  `metric_source_type`       	VARCHAR(50) COMMENT 'Table, Cube, File, Web Service'  NULL,
  `metric_source`            	VARCHAR(300) CHAR SET latin1 COMMENT 'Table Name, Cube Name, URL'  NULL,
  `metric_source_dataset_id`	INT(11) COMMENT 'If metric_source can be matched in dict_dataset' NULL,
  `metric_ref_id_type`       	VARCHAR(50) CHAR SET latin1 COMMENT 'DWH, ABTEST, FINANCE, SEGMENT, SALESAPP' NULL,
  `metric_ref_id`            	VARCHAR(100) CHAR SET latin1 COMMENT 'ID in the reference system' NULL,
  `metric_type`			VARCHAR(100) COMMENT 'NUMBER, BOOLEAN, LIST' NULL,
  `metric_additive_type`     	VARCHAR(100) COMMENT 'FULL, SEMI, NONE' NULL,
  `metric_grain`             	VARCHAR(100) COMMENT 'DAILY, WEEKLY, UNIQUE, ROLLING 7D, ROLLING 30D' NULL,
  `metric_display_factor`    	DECIMAL(10,4) COMMENT '0.01, 1000, 1000000, 1000000000' NULL,
  `metric_display_factor_sym`	VARCHAR(20) COMMENT '%, (K), (M), (B), (GB), (TB), (PB)' NULL,
  `metric_good_direction`	VARCHAR(20) COMMENT 'UP, DOWN, ZERO, FLAT' NULL,
  `metric_formula`           	TEXT COMMENT 'Expression, Code Snippet or Calculation Logic' NULL,
  `dimensions`			VARCHAR(800) CHAR SET latin1 NULL,
  `owners`                 	VARCHAR(300) NULL,
  `tags`			VARCHAR(300) NULL,
  `urn`                         VARCHAR(300) CHAR SET latin1 NOT NULL,
  `metric_url`			VARCHAR(300) CHAR SET latin1 NULL,
  `wiki_url`              	VARCHAR(300) CHAR SET latin1 NULL,
  `scm_url`               	VARCHAR(300) CHAR SET latin1 NULL,
  `wh_etl_exec_id`              BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY(metric_id),
  UNIQUE KEY `uq_dataset_urn` (`urn`),
  KEY `idx_dict_business_metric__ref_id` (`metric_ref_id`) USING BTREE,
  FULLTEXT KEY `fti_dict_business_metric_all` (`metric_name`, `metric_description`, `metric_category`, `metric_group`, `dashboard_name`)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
;

CREATE TABLE `stg_dict_business_metric` (
  `metric_name` varchar(200) NOT NULL,
  `metric_description` varchar(500) DEFAULT NULL,
  `dashboard_name` varchar(100) DEFAULT NULL COMMENT 'Hierarchy Level 1',
  `metric_group` varchar(100) DEFAULT NULL COMMENT 'Hierarchy Level 2',
  `metric_category` varchar(100) DEFAULT NULL COMMENT 'Hierarchy Level 3',
  `metric_sub_category` varchar(100) DEFAULT NULL COMMENT 'Additional Classification, such as Product, Line of Business',
  `metric_level` varchar(50) DEFAULT NULL COMMENT 'CORE, DEPARTMENT, TEAM, OPERATION, STRATEGIC, TIER1, TIER2',
  `metric_source_type` varchar(50) DEFAULT NULL COMMENT 'Table, Cube, File, Web Service',
  `metric_source` varchar(300) CHARACTER SET latin1 DEFAULT NULL COMMENT 'Table Name, Cube Name, URL',
  `metric_source_dataset_id` int(11) DEFAULT NULL COMMENT 'If metric_source can be matched in dict_dataset',
  `metric_ref_id_type` varchar(50) CHARACTER SET latin1 DEFAULT NULL COMMENT 'DWH, ABTEST, FINANCE, SEGMENT, SALESAPP',
  `metric_ref_id` varchar(100) CHARACTER SET latin1 DEFAULT NULL COMMENT 'ID in the reference system',
  `metric_type` varchar(100) DEFAULT NULL COMMENT 'NUMBER, BOOLEAN, LIST',
  `metric_additive_type` varchar(100) DEFAULT NULL COMMENT 'FULL, SEMI, NONE',
  `metric_grain` varchar(100) DEFAULT NULL COMMENT 'DAILY, WEEKLY, UNIQUE, ROLLING 7D, ROLLING 30D',
  `metric_display_factor` decimal(15,4) DEFAULT NULL,
  `metric_display_factor_sym` varchar(20) DEFAULT NULL COMMENT '%, (K), (M), (B), (GB), (TB), (PB)',
  `metric_good_direction` varchar(20) DEFAULT NULL COMMENT 'UP, DOWN, ZERO, FLAT',
  `metric_formula` text COMMENT 'Expression, Code Snippet or Calculation Logic',
  `dimensions` varchar(800) CHARACTER SET latin1 DEFAULT NULL,
  `owners` varchar(300) DEFAULT NULL,
  `tags` varchar(500) DEFAULT NULL,
  `urn` varchar(300) CHARACTER SET latin1 NOT NULL,
  `metric_url` varchar(300) CHARACTER SET latin1 DEFAULT NULL,
  `wiki_url` varchar(300) CHARACTER SET latin1 DEFAULT NULL,
  `scm_url` varchar(300) CHARACTER SET latin1 DEFAULT NULL,
  `wh_etl_exec_id`              BIGINT COMMENT 'wherehows etl execution id that modified this record',
   PRIMARY KEY(`urn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--


CREATE TABLE dataset_owner (
  `dataset_id`    INT UNSIGNED NOT NULL,
  `dataset_urn`   VARCHAR(500) NOT NULL,
  `owner_id`      VARCHAR(127) NOT NULL,
  `app_id`        SMALLINT NOT NULL COMMENT 'application id of the namespace',
  `namespace`     VARCHAR(127) COMMENT 'the namespace of the user',
  `owner_type`    VARCHAR(127) COMMENT 'Producer, Consumer, Stakeholder',
  `owner_sub_type`  VARCHAR(127) COMMENT 'DWH, UMP, BA, etc',
  `owner_id_type` VARCHAR(127) COMMENT 'user, group, service, or urn',
  `owner_source`  VARCHAR(30) NOT NULL COMMENT 'where the owner info is extracted: JIRA,RB,DB,FS,AUDIT',
  `db_ids`        VARCHAR(127) COMMENT 'comma separated database ids',
  `is_group`      CHAR(1) COMMENT 'if owner is a group',
  `is_active`     CHAR(1) COMMENT 'if owner is active',
  `is_deleted`    CHAR(1) COMMENT 'if owner has been removed from the dataset',
  `sort_id`       SMALLINT COMMENT '0 = primary owner, order by priority/importance',
  `source_time`   INT UNSIGNED COMMENT 'the source time in epoch',
  `created_time`  INT UNSIGNED COMMENT 'the create time in epoch',
  `modified_time` INT UNSIGNED COMMENT 'the modified time in epoch',
  `confirmed_by`  VARCHAR(127) NULL,
  `confirmed_on`  INT UNSIGNED,
  wh_etl_exec_id  BIGINT COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`dataset_id`, `owner_id`, `app_id`, `owner_source`),
  UNIQUE KEY `with_urn` (`dataset_urn`, `owner_id`, `app_id`, `owner_source`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE stg_dataset_owner (
  `dataset_id` INT COMMENT 'dataset_id',
  `dataset_urn` VARCHAR(500) NOT NULL,
  `owner_id` VARCHAR(127) NOT NULL,
  `sort_id` SMALLINT COMMENT '0 = primary owner, order by priority/importance',
  `app_id` INT COMMENT 'application id of the namesapce',
  `namespace` VARCHAR(127) COMMENT 'the namespace of the user',
  `owner_type` VARCHAR(127) COMMENT 'Producer, Consumer, Stakeholder',
  `owner_sub_type` VARCHAR(127) COMMENT 'DWH, UMP, BA, etc',
  `owner_id_type` VARCHAR(127) COMMENT 'user, group, service, or urn',
  `owner_source`  VARCHAR(127) COMMENT 'where the owner info is extracted: JIRA,RB,DB,FS,AUDIT',
  `is_group` CHAR(1) COMMENT 'if owner is a group',
  `db_name` VARCHAR(127) COMMENT 'database name',
  `db_id` INT COMMENT 'database id',
  `is_active` CHAR(1) COMMENT 'if owner is active',
  `source_time` INT UNSIGNED COMMENT 'the source event time in epoch',
  `is_parent_urn` CHAR(1) DEFAULT 'N' COMMENT 'if the urn is a directory for datasets',
  KEY (dataset_urn, owner_id, namespace, db_name),
  KEY dataset_index (dataset_urn),
  KEY db_name_index (db_name)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = latin1;

CREATE TABLE stg_dataset_owner_unmatched (
  `dataset_urn` VARCHAR(200) NOT NULL,
  `owner_id` VARCHAR(127) NOT NULL,
  `sort_id` SMALLINT COMMENT '0 = primary owner, order by priority/importance',
  `app_id` INT COMMENT 'application id of the namesapce',
  `namespace` VARCHAR(127) COMMENT 'the namespace of the user',
  `owner_type` VARCHAR(127) COMMENT 'Producer, Consumer, Stakeholder',
  `owner_sub_type` VARCHAR(127) COMMENT 'DWH, UMP, BA, etc',
  `owner_id_type` VARCHAR(127) COMMENT 'user, group, role, service, or urn',
  `owner_source`  VARCHAR(127) COMMENT 'where the owner info is extracted: JIRA,RB,DB,FS,AUDIT',
  `is_group` CHAR(1) COMMENT 'if owner is a group',
  `db_name` VARCHAR(127) COMMENT 'database name',
  `db_id` INT COMMENT 'database id',
  `is_active` CHAR(1) COMMENT 'if owner is active',
  `source_time` INT UNSIGNED COMMENT 'the source event time in epoch',
  KEY (dataset_urn, owner_id, namespace, db_name),
  KEY dataset_index (dataset_urn),
  KEY db_name_index (db_name)
);

CREATE TABLE `dir_external_user_info` (
  `app_id` smallint(5) unsigned NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `urn` varchar(200) DEFAULT NULL,
  `full_name` varchar(200) DEFAULT NULL,
  `display_name` varchar(200) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `employee_number` int(10) unsigned DEFAULT NULL,
  `manager_urn` varchar(200) DEFAULT NULL,
  `manager_user_id` varchar(50) DEFAULT NULL,
  `manager_employee_number` int(10) unsigned DEFAULT NULL,
  `default_group_name` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `department_id` int(10) unsigned DEFAULT '0',
  `department_name` varchar(200) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `mobile_phone` varchar(50) DEFAULT NULL,
  `is_active` char(1) DEFAULT 'Y',
  `org_hierarchy` varchar(500) DEFAULT NULL,
  `org_hierarchy_depth` tinyint(3) unsigned DEFAULT NULL,
  `created_time` int(10) unsigned DEFAULT NULL COMMENT 'the create time in epoch',
  `modified_time` int(10) unsigned DEFAULT NULL COMMENT 'the modified time in epoch',
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`user_id`,`app_id`),
  KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stg_dir_external_user_info` (
  `app_id` smallint(5) unsigned NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `urn` varchar(200) DEFAULT NULL,
  `full_name` varchar(200) DEFAULT NULL,
  `display_name` varchar(200) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `employee_number` int(10) unsigned DEFAULT NULL,
  `manager_urn` varchar(200) DEFAULT NULL,
  `manager_user_id` varchar(50) DEFAULT NULL,
  `manager_employee_number` int(10) unsigned DEFAULT NULL,
  `default_group_name` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `department_id` int(10) unsigned DEFAULT '0',
  `department_name` varchar(200) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `mobile_phone` varchar(50) DEFAULT NULL,
  `is_active` char(1) DEFAULT 'Y',
  `org_hierarchy` varchar(500) DEFAULT NULL,
  `org_hierarchy_depth` tinyint(3) unsigned DEFAULT NULL,
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`app_id`,`user_id`),
  KEY `email` (`email`),
  KEY `app_id` (`app_id`,`urn`),
  KEY `app_id_2` (`app_id`,`manager_urn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dir_external_group_user_map` (
  `app_id` smallint(5) unsigned NOT NULL,
  `group_id` varchar(50) NOT NULL,
  `sort_id` smallint(6) NOT NULL,
  `user_app_id` smallint(5) unsigned NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `created_time` int(10) unsigned DEFAULT NULL COMMENT 'the create time in epoch',
  `modified_time` int(10) unsigned DEFAULT NULL COMMENT 'the modified time in epoch',
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`app_id`,`group_id`,`user_app_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stg_dir_external_group_user_map` (
  `app_id` smallint(5) unsigned NOT NULL,
  `group_id` varchar(50) NOT NULL,
  `sort_id` smallint(6) NOT NULL,
  `user_app_id` smallint(5) unsigned NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`app_id`,`group_id`,`user_app_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dir_external_group_user_map_flatten` (
  `app_id` smallint(5) unsigned NOT NULL,
  `group_id` varchar(50) NOT NULL,
  `sort_id` smallint(6) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_app_id` smallint(5) unsigned NOT NULL,
  `created_time` int(10) unsigned DEFAULT NULL COMMENT 'the create time in epoch',
  `modified_time` int(10) unsigned DEFAULT NULL COMMENT 'the modified time in epoch',
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`app_id`,`group_id`,`user_app_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stg_dir_external_group_user_map_flatten` (
  `app_id` smallint(5) unsigned NOT NULL,
  `group_id` varchar(50) NOT NULL,
  `sort_id` smallint(6) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_app_id` smallint(5) unsigned NOT NULL,
  `wh_etl_exec_id` bigint(20) DEFAULT NULL COMMENT 'wherehows etl execution id that modified this record',
  PRIMARY KEY (`app_id`,`group_id`,`user_app_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--


-- file name pattern to abstract from file level to directory level
CREATE TABLE filename_pattern
(
  filename_pattern_id INT(11) NOT NULL AUTO_INCREMENT,
  regex               VARCHAR(100),
  PRIMARY KEY (filename_pattern_id)
);

-- partitions pattern to abstract from partition level to dataset level
CREATE TABLE `dataset_partition_layout_pattern` (
  `layout_id`               INT(11) NOT NULL AUTO_INCREMENT,
  `regex`                   VARCHAR(50)      DEFAULT NULL,
  `mask`                    VARCHAR(50)      DEFAULT NULL,
  `leading_path_index`      SMALLINT(6)      DEFAULT NULL,
  `partition_index`         SMALLINT(6)      DEFAULT NULL,
  `second_partition_index`  SMALLINT(6)      DEFAULT NULL,
  `sort_id`                 INT(11)          DEFAULT NULL,
  `comments`                VARCHAR(200)     DEFAULT NULL,
  `partition_pattern_group` VARCHAR(50)      DEFAULT NULL,
  PRIMARY KEY (`layout_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- log lineage pattern to extract lineage from logs
CREATE TABLE `log_lineage_pattern` (
  `pattern_id`          INT(11)      NOT NULL AUTO_INCREMENT,
  `pattern_type`        VARCHAR(20)              DEFAULT NULL
  COMMENT 'type of job that have this log pattern',
  `regex`               VARCHAR(200) NOT NULL,
  `database_type`       VARCHAR(20)              DEFAULT NULL
  COMMENT 'database type input by user, e.g. hdfs, voldermont...',
  `database_name_index` INT(11)                  DEFAULT NULL,
  `dataset_index`       INT(11)      NOT NULL
  COMMENT 'the group id of dataset part in the regex',
  `operation_type`      VARCHAR(20)              DEFAULT NULL
  COMMENT 'read/write, input by user',
  `record_count_index`  INT(20)                  DEFAULT NULL
  COMMENT 'all operations count',
  `record_byte_index`   INT(20)                  DEFAULT NULL,
  `insert_count_index`  INT(20)                  DEFAULT NULL,
  `insert_byte_index`   INT(20)                  DEFAULT NULL,
  `delete_count_index`  INT(20)                  DEFAULT NULL,
  `delete_byte_index`   INT(20)                  DEFAULT NULL,
  `update_count_index`  INT(20)                  DEFAULT NULL,
  `update_byte_index`   INT(20)                  DEFAULT NULL,
  `comments`            VARCHAR(200)             DEFAULT NULL,
  `source_target_type`  ENUM('source', 'target') DEFAULT NULL,
  PRIMARY KEY (`pattern_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- patterns used to discover the hadoop id inside log
CREATE TABLE `log_reference_job_id_pattern` (
  `pattern_id`             INT(11)      NOT NULL AUTO_INCREMENT,
  `pattern_type`           VARCHAR(20)  DEFAULT NULL
  COMMENT 'type of job that have this log pattern',
  `regex`                  VARCHAR(200) NOT NULL,
  `reference_job_id_index` INT(11)      NOT NULL,
  `is_active`              TINYINT(1)   DEFAULT '0',
  `comments`               VARCHAR(200) DEFAULT NULL,
  PRIMARY KEY (`pattern_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- tracking user access
CREATE TABLE track_object_access_log (
  `access_unixtime` BIGINT(20) UNSIGNED                                                                                                  NOT NULL,
  `login_id`        INT(10) UNSIGNED                                                                                                     NOT NULL,
  `object_type`     ENUM('dataset', 'metric', 'glossary', 'flow', 'lineage:data', 'lineage:flow', 'lineage:metric', 'lineage:metricJob') NOT NULL DEFAULT 'dataset',
  `object_id`       BIGINT(20)                                                                                                           NULL,
  `object_name`     VARCHAR(500)                                                                                                         NULL,
  `parameters`      VARCHAR(500)                                                                                                         NULL,
  PRIMARY KEY (access_unixtime, login_id, object_type)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0;
--
-- Copyright 2015 LinkedIn Corp. All rights reserved.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
-- http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--

-- create statement for users related tables :
-- users, user_settings, watch

CREATE TABLE users (
  id                       INT(11) AUTO_INCREMENT      NOT NULL,
  name                     VARCHAR(100)                NOT NULL,
  email                    VARCHAR(200)                NOT NULL,
  username                 VARCHAR(20)                 NOT NULL,
  department_number        INT(11)                     NULL,
  password_digest          VARCHAR(256)                NULL,
  password_digest_type     ENUM('SHA1', 'SHA2', 'MD5') NULL DEFAULT 'SHA1',
  ext_directory_ref_app_id SMALLINT UNSIGNED,
  authentication_type      VARCHAR(20),
  PRIMARY KEY (id)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
  DEFAULT CHARSET = utf8;

CREATE INDEX idx_users__username USING BTREE ON users(username);

CREATE TABLE user_settings (
  user_id             INT(11)                           NOT NULL,
  detail_default_view VARCHAR(20)                       NULL,
  default_watch       ENUM('monthly', 'weekly', 'daily', 'hourly') NULL DEFAULT 'weekly',
  PRIMARY KEY (user_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE watch (
  id                BIGINT(20) AUTO_INCREMENT                                 NOT NULL,
  user_id           INT(11)                                                   NOT NULL,
  item_id           INT(11)                                                   NULL,
  urn               VARCHAR(200)                                              NULL,
  item_type         ENUM('dataset', 'dataset_field', 'metric', 'flow', 'urn') NOT NULL DEFAULT 'dataset',
  notification_type ENUM('monthly', 'weekly', 'hourly', 'daily')              NULL     DEFAULT 'weekly',
  created           TIMESTAMP                                                 NULL     DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
)
  ENGINE = InnoDB
  AUTO_INCREMENT = 0
  DEFAULT CHARSET = utf8;

CREATE TABLE favorites (
  user_id    INT(11)   NOT NULL,
  dataset_id INT(11)   NOT NULL,
  created    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, dataset_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE user_login_history (
  log_id              INT(11) AUTO_INCREMENT NOT NULL,
  username            VARCHAR(20)            NOT NULL,
  authentication_type VARCHAR(20)            NOT NULL,
  `status`            VARCHAR(20)            NOT NULL,
  message             TEXT                            DEFAULT NULL,
  login_time          TIMESTAMP              NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (log_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;