CREATE DATABASE azkaban;

CREATE TABLE active_executing_flows (
  exec_id     INT,
  update_time BIGINT,
  PRIMARY KEY (exec_id)
);
CREATE TABLE active_sla (
  exec_id    INT          NOT NULL,
  job_name   VARCHAR(128) NOT NULL,
  check_time BIGINT       NOT NULL,
  rule       TINYINT      NOT NULL,
  enc_type   TINYINT,
  options    LONGBLOB     NOT NULL,
  PRIMARY KEY (exec_id, job_name)
);
CREATE TABLE execution_dependencies(
  trigger_instance_id varchar(64),
  dep_name varchar(128),
  starttime bigint(20) not null,
  endtime bigint(20),
  dep_status tinyint not null,
  cancelleation_cause tinyint not null,

  project_id INT not null,
  project_version INT not null,
  flow_id varchar(128) not null,
  flow_version INT not null,
  flow_exec_id INT not null,
  primary key(trigger_instance_id, dep_name)
);

CREATE INDEX ex_end_time
  ON execution_dependencies (endtime);
CREATE TABLE execution_flows (
  exec_id     INT          NOT NULL AUTO_INCREMENT,
  project_id  INT          NOT NULL,
  version     INT          NOT NULL,
  flow_id     VARCHAR(128) NOT NULL,
  status      TINYINT,
  submit_user VARCHAR(64),
  submit_time BIGINT,
  update_time BIGINT,
  start_time  BIGINT,
  end_time    BIGINT,
  enc_type    TINYINT,
  flow_data   LONGBLOB,
  executor_id INT                   DEFAULT NULL,
  PRIMARY KEY (exec_id)
);

CREATE INDEX ex_flows_start_time
  ON execution_flows (start_time);
CREATE INDEX ex_flows_end_time
  ON execution_flows (end_time);
CREATE INDEX ex_flows_time_range
  ON execution_flows (start_time, end_time);
CREATE INDEX ex_flows_flows
  ON execution_flows (project_id, flow_id);
CREATE INDEX executor_id
  ON execution_flows (executor_id);
CREATE INDEX ex_flows_staus
  ON execution_flows (status);
CREATE TABLE execution_jobs (
  exec_id       INT          NOT NULL,
  project_id    INT          NOT NULL,
  version       INT          NOT NULL,
  flow_id       VARCHAR(128) NOT NULL,
  job_id        VARCHAR(512) NOT NULL,
  attempt       INT,
  start_time    BIGINT,
  end_time      BIGINT,
  status        TINYINT,
  input_params  LONGBLOB,
  output_params LONGBLOB,
  attachments   LONGBLOB,
  PRIMARY KEY (exec_id, job_id, flow_id, attempt)
);

CREATE INDEX ex_job_id
  ON execution_jobs (project_id, job_id);
-- In table execution_logs, name is the combination of flow_id and job_id
--
-- prefix support and lengths of prefixes (where supported) are storage engine dependent.
-- By default, the index key prefix length limit is 767 bytes for innoDB.
-- from: https://dev.mysql.com/doc/refman/5.7/en/create-index.html

CREATE TABLE execution_logs (
  exec_id     INT NOT NULL,
  name        VARCHAR(640),
  attempt     INT,
  enc_type    TINYINT,
  start_byte  INT,
  end_byte    INT,
  log         LONGBLOB,
  upload_time BIGINT,
  PRIMARY KEY (exec_id, name, attempt, start_byte)
);

CREATE INDEX ex_log_attempt
  ON execution_logs (exec_id, name, attempt);
CREATE INDEX ex_log_index
  ON execution_logs (exec_id, name);
CREATE INDEX ex_log_upload_time
  ON execution_logs (upload_time);
CREATE TABLE executor_events (
  executor_id INT      NOT NULL,
  event_type  TINYINT  NOT NULL,
  event_time  DATETIME NOT NULL,
  username    VARCHAR(64),
  message     VARCHAR(512)
);

CREATE INDEX executor_log
  ON executor_events (executor_id, event_time);
CREATE TABLE executors (
  id     INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
  host   VARCHAR(64) NOT NULL,
  port   INT         NOT NULL,
  active BOOLEAN                          DEFAULT FALSE,
  UNIQUE (host, port),
  UNIQUE INDEX executor_id (id)
);

CREATE INDEX executor_connection
  ON executors (host, port);
CREATE TABLE project_events (
  project_id INT     NOT NULL,
  event_type TINYINT NOT NULL,
  event_time BIGINT  NOT NULL,
  username   VARCHAR(64),
  message    VARCHAR(512)
);

CREATE INDEX log
  ON project_events (project_id, event_time);
CREATE TABLE project_files (
  project_id INT NOT NULL,
  version    INT NOT NULL,
  chunk      INT,
  size       INT,
  file       LONGBLOB,
  PRIMARY KEY (project_id, version, chunk)
);

CREATE INDEX file_version
  ON project_files (project_id, version);
CREATE TABLE project_flow_files (
  project_id        INT          NOT NULL,
  project_version   INT          NOT NULL,
  flow_name         VARCHAR(128) NOT NULL,
  flow_version      INT          NOT NULL,
  modified_time     BIGINT       NOT NULL,
  flow_file         LONGBLOB,
  PRIMARY KEY (project_id, project_version, flow_name, flow_version)
);
CREATE TABLE project_flows (
  project_id    INT    NOT NULL,
  version       INT    NOT NULL,
  flow_id       VARCHAR(128),
  modified_time BIGINT NOT NULL,
  encoding_type TINYINT,
  json          BLOB,
  PRIMARY KEY (project_id, version, flow_id)
);

CREATE INDEX flow_index
  ON project_flows (project_id, version);
CREATE TABLE project_permissions (
  project_id    VARCHAR(64) NOT NULL,
  modified_time BIGINT      NOT NULL,
  name          VARCHAR(64) NOT NULL,
  permissions   INT         NOT NULL,
  isGroup       BOOLEAN     NOT NULL,
  PRIMARY KEY (project_id, name)
);

CREATE INDEX permission_index
  ON project_permissions (project_id);
CREATE TABLE project_properties (
  project_id    INT    NOT NULL,
  version       INT    NOT NULL,
  name          VARCHAR(255),
  modified_time BIGINT NOT NULL,
  encoding_type TINYINT,
  property      BLOB,
  PRIMARY KEY (project_id, version, name)
);

CREATE INDEX properties_index
  ON project_properties (project_id, version);
CREATE TABLE project_versions (
  project_id  INT         NOT NULL,
  version     INT         NOT NULL,
  upload_time BIGINT      NOT NULL,
  uploader    VARCHAR(64) NOT NULL,
  file_type   VARCHAR(16),
  file_name   VARCHAR(128),
  md5         BINARY(16),
  num_chunks  INT,
  resource_id VARCHAR(512) DEFAULT NULL,
  PRIMARY KEY (project_id, version)
);

CREATE INDEX version_index
  ON project_versions (project_id);
CREATE TABLE projects (
  id               INT         NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name             VARCHAR(64) NOT NULL,
  active           BOOLEAN,
  modified_time    BIGINT      NOT NULL,
  create_time      BIGINT      NOT NULL,
  version          INT,
  last_modified_by VARCHAR(64) NOT NULL,
  description      VARCHAR(2048),
  enc_type         TINYINT,
  settings_blob    LONGBLOB,
  UNIQUE INDEX project_id (id)
);

CREATE INDEX project_name
  ON projects (name);
CREATE TABLE properties (
  name          VARCHAR(64) NOT NULL,
  type          INT         NOT NULL,
  modified_time BIGINT      NOT NULL,
  value         VARCHAR(256),
  PRIMARY KEY (name, type)
);
-- This file collects all quartz table create statement required for quartz 2.2.1
--
-- We are using Quartz 2.2.1 tables, the original place of which can be found at
-- https://github.com/quartz-scheduler/quartz/blob/quartz-2.2.1/distribution/src/main/assembly/root/docs/dbTables/tables_mysql.sql


DROP TABLE IF EXISTS QRTZ_FIRED_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_PAUSED_TRIGGER_GRPS;
DROP TABLE IF EXISTS QRTZ_SCHEDULER_STATE;
DROP TABLE IF EXISTS QRTZ_LOCKS;
DROP TABLE IF EXISTS QRTZ_SIMPLE_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_SIMPROP_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_CRON_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_BLOB_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_JOB_DETAILS;
DROP TABLE IF EXISTS QRTZ_CALENDARS;


CREATE TABLE QRTZ_JOB_DETAILS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    JOB_NAME  VARCHAR(200) NOT NULL,
    JOB_GROUP VARCHAR(200) NOT NULL,
    DESCRIPTION VARCHAR(250) NULL,
    JOB_CLASS_NAME   VARCHAR(250) NOT NULL,
    IS_DURABLE VARCHAR(1) NOT NULL,
    IS_NONCONCURRENT VARCHAR(1) NOT NULL,
    IS_UPDATE_DATA VARCHAR(1) NOT NULL,
    REQUESTS_RECOVERY VARCHAR(1) NOT NULL,
    JOB_DATA BLOB NULL,
    PRIMARY KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
);

CREATE TABLE QRTZ_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    JOB_NAME  VARCHAR(200) NOT NULL,
    JOB_GROUP VARCHAR(200) NOT NULL,
    DESCRIPTION VARCHAR(250) NULL,
    NEXT_FIRE_TIME BIGINT(13) NULL,
    PREV_FIRE_TIME BIGINT(13) NULL,
    PRIORITY INTEGER NULL,
    TRIGGER_STATE VARCHAR(16) NOT NULL,
    TRIGGER_TYPE VARCHAR(8) NOT NULL,
    START_TIME BIGINT(13) NOT NULL,
    END_TIME BIGINT(13) NULL,
    CALENDAR_NAME VARCHAR(200) NULL,
    MISFIRE_INSTR SMALLINT(2) NULL,
    JOB_DATA BLOB NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
        REFERENCES QRTZ_JOB_DETAILS(SCHED_NAME,JOB_NAME,JOB_GROUP)
);

CREATE TABLE QRTZ_SIMPLE_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    REPEAT_COUNT BIGINT(7) NOT NULL,
    REPEAT_INTERVAL BIGINT(12) NOT NULL,
    TIMES_TRIGGERED BIGINT(10) NOT NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
        REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
);

CREATE TABLE QRTZ_CRON_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    CRON_EXPRESSION VARCHAR(200) NOT NULL,
    TIME_ZONE_ID VARCHAR(80),
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
        REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
);

CREATE TABLE QRTZ_SIMPROP_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    STR_PROP_1 VARCHAR(512) NULL,
    STR_PROP_2 VARCHAR(512) NULL,
    STR_PROP_3 VARCHAR(512) NULL,
    INT_PROP_1 INT NULL,
    INT_PROP_2 INT NULL,
    LONG_PROP_1 BIGINT NULL,
    LONG_PROP_2 BIGINT NULL,
    DEC_PROP_1 NUMERIC(13,4) NULL,
    DEC_PROP_2 NUMERIC(13,4) NULL,
    BOOL_PROP_1 VARCHAR(1) NULL,
    BOOL_PROP_2 VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
    REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
);

CREATE TABLE QRTZ_BLOB_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    BLOB_DATA BLOB NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
        REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
);

CREATE TABLE QRTZ_CALENDARS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    CALENDAR_NAME  VARCHAR(200) NOT NULL,
    CALENDAR BLOB NOT NULL,
    PRIMARY KEY (SCHED_NAME,CALENDAR_NAME)
);

CREATE TABLE QRTZ_PAUSED_TRIGGER_GRPS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_GROUP  VARCHAR(200) NOT NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_GROUP)
);

CREATE TABLE QRTZ_FIRED_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    ENTRY_ID VARCHAR(95) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    INSTANCE_NAME VARCHAR(200) NOT NULL,
    FIRED_TIME BIGINT(13) NOT NULL,
    SCHED_TIME BIGINT(13) NOT NULL,
    PRIORITY INTEGER NOT NULL,
    STATE VARCHAR(16) NOT NULL,
    JOB_NAME VARCHAR(200) NULL,
    JOB_GROUP VARCHAR(200) NULL,
    IS_NONCONCURRENT VARCHAR(1) NULL,
    REQUESTS_RECOVERY VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,ENTRY_ID)
);

CREATE TABLE QRTZ_SCHEDULER_STATE
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    INSTANCE_NAME VARCHAR(200) NOT NULL,
    LAST_CHECKIN_TIME BIGINT(13) NOT NULL,
    CHECKIN_INTERVAL BIGINT(13) NOT NULL,
    PRIMARY KEY (SCHED_NAME,INSTANCE_NAME)
);

CREATE TABLE QRTZ_LOCKS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    LOCK_NAME  VARCHAR(40) NOT NULL,
    PRIMARY KEY (SCHED_NAME,LOCK_NAME)
);


commit;
CREATE TABLE triggers (
  trigger_id     INT    NOT NULL AUTO_INCREMENT,
  trigger_source VARCHAR(128),
  modify_time    BIGINT NOT NULL,
  enc_type       TINYINT,
  data           LONGBLOB,
  PRIMARY KEY (trigger_id)
);
version=3.10.1
-- DB Migration from release 3.20.0 to 3.22.0
--
-- Release 3.21.0 is broken
-- PR #1024 introduces a new column to 'project_versions' table.
--
ALTER TABLE project_versions
  ADD resource_id VARCHAR(512);
-- DB Migration from release 3.42.0 to 3.43.0
-- PR #1657 changes project cache to case insensitive.
-- Below queries are DB specific and only apply to MySQL DB.
--
-- 1. When creating new DB in MySQL,
-- use below query to explicitly set the COLLATION to case insensitive for the entire DB:
--
ALTER DATABASE <database_name> CHARACTER SET utf8 COLLATE utf8_general_ci;
--
-- 2. For existing MySQL DB,
-- use below query to explicitly set the COLLATION to case insensitive for "name" column in
-- "projects" table:
--
ALTER TABLE projects MODIFY name VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci;



--
-- Table structure for table `kk_jobs`
--

DROP TABLE IF EXISTS `kk_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kk_jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '任务名，不能重复',
  `project_name` varchar(64) NOT NULL COMMENT '项目名，一个任务只能属于一个项目，防止多次运行',
  `flow_name` varchar(64) DEFAULT '' COMMENT '流程中的最后的节点任务名，空为节点，非空为子流程',
  `server_host` varchar(30) DEFAULT '' COMMENT '任务所在服务器域名，或IP',
  `server_user` varchar(30) DEFAULT '' COMMENT '执行任务的服务器用户',
  `server_dir` varchar(200) DEFAULT '' COMMENT '执行任务的服务器目录，有的话自动执行cd',
  `server_script` varchar(500) NOT NULL COMMENT '执行任务的脚本命令',
  `dependencies` varchar(2000) DEFAULT '' COMMENT '依赖的任务，多个则以逗号分隔',
  `success_email` varchar(2000) DEFAULT '' COMMENT '执行成功时的邮件接收人',
  `failure_email` varchar(2000) DEFAULT '' COMMENT '执行成功时的邮件接收人',
  `success_sms` varchar(2000) DEFAULT '' COMMENT '执行成功时的短信接收人',
  `failure_sms` varchar(2000) DEFAULT '' COMMENT '执行失败时的短信接收人',
  `retries` tinyint(2) DEFAULT '0' COMMENT '失败后的重试次数',
  `creator` varchar(30) DEFAULT '' COMMENT '任务创建人',
  `updater` varchar(30) DEFAULT '' COMMENT '修改人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `loc` varchar(50) DEFAULT '' COMMENT 'DAG中的位置',
  `ext_dependencies` varchar(4000) DEFAULT '' COMMENT '外部依赖，针对跨任务及跨时间维度的任务',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `project_name` (`project_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='自定义任务配置';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kk_jobs_status`
--

DROP TABLE IF EXISTS `kk_jobs_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kk_jobs_status` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `job_name` varchar(200) NOT NULL COMMENT '任务名称',
  `execute_time` bigint(20) NOT NULL COMMENT '执行时间参数,只支持天级、小时级',
  `exec_id` bigint(20) DEFAULT '0' COMMENT 'azkaban任务ID',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '任务创建时间',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '任务实际开始时间，所有依赖完成',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '任务更新时间',
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '任务状态,0执行中，1成功，-1失败',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_job_exec` (`job_name`,`execute_time`),
  KEY `idx_job` (`job_name`),
  KEY `idx_execute_time` (`execute_time`),
  KEY `idx_status` (`status`),
  KEY `idx_exec_id` (`exec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;