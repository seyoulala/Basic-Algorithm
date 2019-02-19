#!/bin/sh
cd `dirname $0`/.. && wk_dir=`pwd` && cd -
source ${wk_dir}/util/env

###### create ods_dm_user1 ##########
table_name="${table_ods_user1}"
hql="create external table if not exists ${table_name}
(
    id bigint COMMENT '序号',
    gerder string COMMENT '性别',
    age int COMMENT '年龄'，
    name string COMMET '姓名'
) COMMENT 'persion(练习)'
partitioned by (dt string)
row format delimited fields terminated by '\001' collection items terminated by ',' map keys terminated by ':' lines terminated by '\n'
stored as textfile
location '${ods_hive_dir}${table_name}';
"
echo "$hql"
${HIVE} -e "$hql"
###### create tmp_ods_dm_user1 ##########
table_name="${table_tmp_ods_user1}"
hql="create external table if not exists ${table_name}
(
    id bigint COMMENT '序号',
    gerder string COMMENT '性别',
    age int COMMENT '年龄'，
    name string COMMET '姓名'
) COMMENT 'persion(练习)'
row format delimited fields terminated by '\001' collection items terminated by ',' map keys terminated by ':' lines terminated by '\n'
stored as textfile
location '${tmp_hive_dir}/${table_name}';
"
echo "$hql"
${HIVE} -e "$hql"
