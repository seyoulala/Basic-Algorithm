#!/bin/bash
###############################################################################
#                                                                             
# @date:   2017-12-12
# @desc:   ods_dm_e_coupon
#                                                                            
############################################################################### 

cd `dirname $0`/.. && wk_dir=`pwd` && cd -
source ${wk_dir}/util/env
source ${util_dir}/my_functions

python3 ${script_dir}/python.py ${argu1} ${argu2}
check_success

local_dir="/extc/mg/"
hql="load data local inpath ${local_dir} overwrite into table into ${table_name} partition by(dt='2019-9-25')"

echo_ex "${hql}"
${HIVE} -e "${hql}"

check_success
exit 0
