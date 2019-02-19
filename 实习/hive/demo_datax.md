### Datax 的简单使用



### 1. 登入服务器
```bash
xyh@xyh:~$ ssh hdfs@192.192.0.27
hdfs@192.192.0.27's password:
```
#### 2.安装位置

```bash
(ml_plat) [hdfs@cdhagent2 deploy]$ pwd
/data0/deploy

(ml_plat) [hdfs@cdhagent2 deploy]$ ll datax/
总用量 4
drwxrwxr-x 2 hdfs hdfs   59 9月   5 13:56 bin
drwxrwxr-x 2 hdfs hdfs   68 9月   4 16:47 conf
drwxrwxr-x 2 hdfs hdfs   74 9月   5 16:37 job
drwxrwxr-x 2 hdfs hdfs 4096 9月   4 16:47 lib
drwxrwxr-x 3 hdfs hdfs   24 9月   5 14:17 log
drwxrwxr-x 3 hdfs hdfs   24 9月   5 14:17 log_perf
drwxrwxr-x 4 hdfs hdfs   34 9月   4 16:48 plugin
drwxrwxr-x 2 hdfs hdfs   23 9月   4 16:47 script
drwxrwxr-x 2 hdfs hdfs   24 9月   4 16:47 tmp

```

### 3. 配置job.json 文件

```json
{
    "job": {
        "setting": {
            "speed": {
                 "channel":1
            }
        },
        "content": [
            {
                "reader": {
                    "name": "mysqlreader",
                    "parameter": {
                        "username": mysql用户名,
                        "password": 密码,
                        "connection": [
                            {
                                "querySql": [
                                    "select BANK_ID,BANK_NAME,THIRD_BANK_NO,IS_SUPPORT from dim_bank;"
                                ],
                                "jdbcUrl": [
                                    "jdbc:mysql://192.192.0.27:3306/WKL?autoReconnect=true"
                                               ]
                            }
                        ]
                    }
                },
                "writer": {
                    "name": "hdfswriter",
                    "parameter": {
                        "defaultFS": "hdfs://192.192.0.26:8020",
                        "fileType": "text",
                        "path":"/ext_dc/dm/tmp/datax_bank/",
                        "fileName":"daata_x_bank",
                        "fieldDelimiter":"/001",
                        "writeMode":"append",
                        "column":[
                        {
                            "name":"BANK_ID",
                            "type":"String"
                        },
                        {
                            "name":"BANK_NAME",
                            "type":"String"
                        },
                        {
                            "name":"THIRD_BANK_NO",
                            "type":"String"
                        },
                        {
                            "name":"IS_SUPPORT",
                            "type":"String"
                        }
                                ]
                    }
                }
            }
        ]
    }
}
```
### 4. 环境配置文件

环境配置文件统一放在 util/env 中

```bash
(ml_plat) [hdfs@cdhagent2 xu_user_datax]$ ll
总用量 0
drwxr-xr-x 2 hdfs hdfs  63 9月   5 11:00 alert
drwxr-xr-x 2 hdfs hdfs  61 9月   6 11:03 conf
drwxr-xr-x 2 hdfs hdfs  88 9月   6 11:12 create_table
drwxr-xr-x 2 hdfs hdfs  41 9月   5 11:00 crontab_job
drwxrwxr-x 2 hdfs hdfs  46 9月  13 10:25 data
drwxr-xr-x 2 hdfs hdfs   6 9月   5 11:00 flag
drwxrwxr-x 2 hdfs hdfs 120 9月   6 10:07 log
drwxr-xr-x 3 hdfs hdfs  83 9月  13 10:31 script
drwxr-xr-x 2 hdfs hdfs 122 9月  13 10:28 util
```

<!--```bash-->
<!--#!/bin/sh-->
<!--cd `dirname $0`/..-->
<!--wk_dir=`pwd`-->
<!--script_dir=${wk_dir}/script-->
<!--cd ${script_dir}-->
<!--script_name=`basename $0`-->
<!--job_name="`basename $0 .sh`"-->
<!--script_path=${script_dir}/${script_name}-->
<!--bin_dir=${wk_dir}/bin-->
<!--conf_dir=${wk_dir}/conf-->
<!--util_dir=${wk_dir}/util-->
<!--jar_dir=${wk_dir}/jar-->
<!--flag_dir=${wk_dir}/flag-->
<!--alert_dir=${wk_dir}/alert-->
<!--log_dir=${wk_dir}/log-->
<!--data_dir=${wk_dir}/data-->
<!--```-->

### 5. 写入数据之间要在hive中先建立表

**建表脚本**

```bash
#!/bin/sh
cd `dirname $0`/.. && wk_dir=`pwd` && cd -
source ${wk_dir}/util/env

###### create ods_dim_bank ##########
table_name="${table_ods_dim_bank}"
hql="create external table if not exists ${table_name}
(
    bank_id string COMMENT '银行ID',
    bank_name string COMMENT '银行名称',
    third_bank_no string ,
    is_support string
) COMMENT 'dim_bank(银行名列表)'
row format delimited fields terminated by '\t' collection items terminated by ',' map keys terminated by ':' lines terminated by '\n'
stored as textfile
location '${ods_hive_dir}${table_name}';
"
echo "$hql"
${HIVE} -e "$hql"
###### create tmp_ods_dim_bank ##########
table_name="${table_tmp_ods_dim_bank}"
hql="create external table if not exists ${table_name}
(
    bank_id string COMMENT '银行ID',
    bank_name string COMMENT '银行名称',
    third_bank_no string ,
    is_support string
	) COMMENT 'dim_bank(银行名列表)'
row format delimited fields terminated by '\t' collection items terminated by ',' map keys terminated by ':' lines terminated by '\n'
stored as textfile
location '${tmp_hive_dir}${table_name}';
"
echo "$hql"
${HIVE} -e "$hql"

```
### 6. 脚本启动文件
启动脚本统一放在script目录中
```bash

(ml_plat) [hdfs@cdhagent2 script]$ vim ods_dm_bank_by_datax.sh
```


```bash
#!/bin/bash
cd `dirname $0`/.. && wk_dir=`pwd` && cd -
source ${wk_dir}/util/env

python2 ${DATAX_HOME}/bin/datax.py ${data_dir}/bank_mysqlreader_hdfswriter.json
check_success

hql="insert overwrite talble ${table_ods_dm}
     select * from ${table_tmp_dm}"

echo_ex "${hql}"
${HIVE} -e "${hql}"

check_success
exit 0

```


**写入成功**

```log
DataX (DATAX-OPENSOURCE-3.0), From Alibaba !
Copyright (C) 2010-2017, Alibaba Group. All Rights Reserved.


2018-09-13 10:36:14.669 [main] INFO  VMInfo - VMInfo# operatingSystem class => sun.management.OperatingSystemImpl
2018-09-13 10:36:14.677 [main] INFO  Engine - the machine info  =>

        osInfo: Oracle Corporation 1.8 25.171-b11
        jvmInfo:        Linux amd64 3.10.0-862.el7.x86_64
        cpu num:        8

        totalPhysicalMemory:    -0.00G
        freePhysicalMemory:     -0.00G
        maxFileDescriptorCount: -1
        currentOpenFileDescriptorCount: -1

        GC Names        [PS MarkSweep, PS Scavenge]

        MEMORY_NAME                    | allocation_size                | init_size          
        PS Eden Space                  | 256.00MB                       | 256.00MB           
        Code Cache                     | 240.00MB                       | 2.44MB             
        Compressed Class Space         | 1,024.00MB                     | 0.00MB             
        PS Survivor Space              | 42.50MB                        | 42.50MB            
        PS Old Gen                     | 683.00MB                       | 683.00MB           
        Metaspace                      | -0.00MB                        | 0.00MB             


2018-09-13 10:36:26.465 [job-0] INFO  JobContainer - PerfTrace not enable!
2018-09-13 10:36:26.466 [job-0] INFO  StandAloneJobContainerCommunicator - Total 22 records, 413 bytes | Speed 41B/s, 2 records/s | Error 0 records, 0 bytes |  All Task WaitWriterTime 0.000s |  All Task WaitReaderTime 0.000s | Percentage 100.00%
2018-09-13 10:36:26.467 [job-0] INFO  JobContainer -
任务启动时刻                    : 2018-09-13 10:36:14
任务结束时刻                    : 2018-09-13 10:36:26
任务总计耗时                    :                 11s
任务平均流量                    :               41B/s
记录写入速度                    :              2rec/s
读出记录总数                    :                  22
读写失败总数                    :                   0

2018-09-13 10:36:26 Last shell sentence or jobTask run successful!
```

