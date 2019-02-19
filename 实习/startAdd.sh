#!/bin/sh
#使环境变量生效
#source ~/.bash_profile
#获取目录
basepath=$(cd `dirname $0`; pwd)
export kettlepath=/opt/soft/kettle/data-integration
export JAVA_HOME=/opt/soft/jdk
export JRE_HOME=/opt/soft/jdk/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
#kettlepath=$(cd `$KETTLE_HOME`;pwd)
#删除PUBLIC历史日志
DIRECTORY_PUBLIC=$basepath/public/log
#if [ "`ls -A $DIRECTORY_PUBLIC`" = "" ]; then
#  echo "$DIRECTORY_PUBLIC 不存在文件"
#else
  rm $DIRECTORY_PUBLIC/*
#fi
#运行public kjb
$kettlepath/kitchen.sh -file=$basepath/public/jobs/report_public.kjb >>$basepath/log/publicadd.log
echo "public增量作业完成"
#删除CORE历史日志
DIRECTORY_CORE=$basepath/core/log
#if [ "`ls -A $DIRECTORY_CORE`" = "" ]; then
#  echo "$DIRECTORY_CORE 不存在文件"
#else
  rm $DIRECTORY_CORE/*
#fi
#运行core kjb 依赖public和dim
# 无限循环直到找到public和dim完成的文件
while [ 1=1 ]
do
   if [  -f "$basepath/public/files/publicaddend" ] && [  -f "$basepath/dim/files/dimaddend" ];then
     $kettlepath/kitchen.sh -file=$basepath/core/jobs/report_core.kjb >>$basepath/log/coreadd.log
     break
   fi
   echo "正在运行public作业或者dim作业"
   sleep 1m
done
