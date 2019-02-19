# 阿里DataX概述

## 1. 什么是 DataX


DataX 是阿里巴巴集团内被广泛使用的离线数据同步工具/平台，实现包括 MySQL、SQL Server、Oracle、PostgreSQL、HDFS、Hive、HBase、OTS、ODPS 等各种异构数据源之间高效的数据同步功能

### 1.1 DataX 的 Feature

DataX本身作为数据同步框架，将不同数据源的同步抽象为从源头数据源读取数据的Reader插件，以及向目标端写入数据的Writer插件，理论上DataX框架可以支持任意数据源类型的数据同步工作。同时DataX插件体系作为一套生态系统, 每接入一套新数据源该新加入的数据源即可实现和现有的数据源互通。

## 2. DataX 解决的问题

实现**跨平台的、跨数据库、不同系统之间的数据同步及交互**。

如果我们拥有很多不同类型的数据库/文件系统(Mysql/Oracle/Rac/Hive/Other…),并且经常需要在它们之间导入导出数据,那么我们可能需要开发/维护/学习使用一批这样的工具(jdbcdump/dbloader/multithread/getmerge+sqlloader/mysqldumper…)。而且以后每增加一种库类型,我们需要的工具数目将线性增长。
 这些工具有些使用文件中转数据,有些使用管道,不同程度的为数据中转带来额外开销,效率差别很非常大。

很多工具也无法满足ETL任务中常见的需求,比如日期格式转化,特性字符的转化,编码转换。另外,有些时候,我们希望在一个很短的时间窗口内,将一份数据从一个数据库同时导出到多个不同类型的数据库。 DataX正是为了解决这些问题而生。
以往，增加一类型的数据对接，我们可能为此增加一个接口或者特意开发兼容数据的系统，如下图:

<img src="http://aliyunzixunbucket.oss-cn-beijing.aliyuncs.com/jpg/d8781923aa9082d8e52542c352a6e94e.jpg?x-oss-process=image/resize,p_100/auto-orient,1/quality,q_90/format,jpg/watermark,image_eXVuY2VzaGk=,t_100,g_se,x_0,y_0" width="600" />

倘若我们要增加一个数据源和目标源，就得从新开发一套新的同步工具，如下图

<img src="http://aliyunzixunbucket.oss-cn-beijing.aliyuncs.com/jpg/14864d274a8e6aaa4fe9e9ee3d3babec.jpg?x-oss-process=image/resize,p_100/auto-orient,1/quality,q_90/format,jpg/watermark,image_eXVuY2VzaGk=,t_100,g_se,x_0,y_0" width="600" />


**DataX 结构模型(框架+插架)**

<img src="http://aliyunzixunbucket.oss-cn-beijing.aliyuncs.com/jpg/c4073b139a6623303613005c30c06039.jpg?x-oss-process=image/resize,p_100/auto-orient,1/quality,q_90/format,jpg/watermark,image_eXVuY2VzaGk=,t_100,g_se,x_0,y_0" width="700" />

| column | 作用 |
|:--------:|:--------:|
| Job      | 数据同步作业         |
|Spliter   |作业切分模块，将一个大任务与分解成多个可以并发的小任务
|sub-job   |数据同步作业切分后的小任务
|Reader    |数据读入模块，负责将数据从源头载入DataxStorage
|Storage|Reader和Writer通过Storage交换数据
|Writer|数据写出模块，负责将数据从Datax导入至目的数据地

DataX框架内部通过双缓冲队列、线程池封装等技术,集中处理了高速数据交换遇到的问题,提供简单的接口与插件交互	,插件分为Reader和Writer两类,基于框架提供的插件接口,可以十分便捷的开发出需要的插件。比如想要从oracle导出数据到mysql,那么需要做的就是开发出OracleReader和MysqlWriter插件,装配到框架上即可。

## 3. DataX 体验

### 3.1 Datax 安装

安装 Datax 有好几种方法，这里这讲述工具包的下载解压，具体可以到查看github上的详细文档 [Datax](https://github.com/alibaba/DataX/blob/master/userGuid.md)

- 直接下载Datax工具包:[Datax下载地址](http://datax-opensource.oss-cn-hangzhou.aliyuncs.com/datax.tar.gz)

下载后解压至本地某个目录，进入bin目录，即可运行同步作业:
```bash
$ cd /data0/deploy/datax/bin
python datax.py {YOUR_JOB.json}

```
### 3.2 导入数据

本次实验是将数据从 mysql导入到hdfs中，所以需要MysqlReader插件实现了从Mysql读取数据，hdfsWriter写插件将数据写入到hdfs中，详细的参数配置请看github文档

[MysqlReader](https://github.com/alibaba/DataX/blob/master/mysqlreader/doc/mysqlreader.md)

[HDFSWriter](https://github.com/alibaba/DataX/blob/master/hdfswriter/doc/hdfswriter.md)

参数配置完之后就可以 通过脚本来导入数据

 ```bash
 python {YOUR_DATAX_HOME}/bin/datax.py {YOUR_DATAX_HOME}/job/job.json
 ```
 YOUR_DATAX_HOME 为datax安装目录，job.json 为配置的读写参数