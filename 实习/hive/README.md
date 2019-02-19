# 大数据时代下的Hive技术简单介绍

Date | Title | Desc | Author |  Confirmer  | Version
-------  | ------- | :-------: | ------- | ------- | -------
2018-08-30 | Hive 相关组件和执行过程，内外部表等 | - | Xu | Blair |  1.0

### 什么是Hive

1. hive是基于Hadoop的一个数据仓库工具，可以将结构化的数据文件映射为一张数据库表，并提供完整的sql查询功能，可以将sql语句装换成MapReduce任务进行运行。`优点`是学习成本低，可以通过类SQL语句快速实现简单的MapReduce统计，不必开发专门的MapReduce应用，十分适合数据仓库的统计分析。

2. Hive是建立在 Hadoop 上的数据仓库基础构架。它提供了一系列的工具，可以用来进行数据提取转化加载（ETL），这是一种可以存储、查询和分析存储在 Hadoop 中的大规模数据的机制。Hive 定义了简单的类 SQL 查询语言，称为 HQL，它允许熟悉 SQL 的用户查询数据。同时，这个语言也允许熟悉 MapReduce 开发者的开发自定义的 mapper 和 reducer 来处理内建的 mapper 和 reducer 无法完成的复杂的分析工作。


### 1. 架构

<img src = "real_time_flow/images/hive.png" width='600'high="300"/>


#### 1.1 组件
| 组成	 | 作用 |
|:-------:|:--------:|
|   Metastore     	|   存储所有关于表，表的分区、模式、列及其类型、表地址等表的元数据
|Driver				|	控制HIVEQL生命周期的组件，当有HiveQL查询穿过Hive时，该驱动管理着回话句柄以及任何回话的统计
|Query Compiler		|将HiveQL编译成DAG形式的MR任务
|Execution Engine	|执行由编译器产生的任务
|HiveServer			|一个提供“健壮的接口（thrift interface ）、JDBC/ODBC 服务器以及提供一种整合 Hive 和其它应用的”组件。

### 2.执行的过程

HiveQL通过CLI/web UI或者thrift、odbc、或jdbc接口外部接口提交，进过Query compiler ,运用metastore中的元数据进行类型检测会语法分析，生成一个逻辑方案(logical plan),然后通过简单的优化处理，产生一个以有向无环图DAG数据结构形式展现的map-reduce任务

#### 2.1 执行流程图
<img src="real_time_flow/images/hive2.png" width="600">



### 3 Hive 内部表和外部表区别详解

1. 创建内部表与外部表的区别是什么？
2. external关键字的作用是什么？
3. 外部表与内部表的区别是什么？
4. 删除表的时候，内部表与外部表有什么区别？
5. load data local inpath '/home/wyp/data/wyp.txt' into table wyp;的过程是什么样子的？
6. 磁盘，hdfs,hive表他们之间的过程是什么样子的？

#### 创建一个外部表
```hive
hive> create table wyp(id int,
    > name string,
    > age int,
    > tele string)
    > ROW FORMAT DELIMITED
    > FIELDS TERMINATED BY '\t'
    > STORED AS TEXTFILE;
OK
Time taken: 0.759 seconds

```
**在hive中创建数据后给这个表导入数据**

```hive
hive> load data local inpath '/home/wyp/data/wyp.txt' into table wyp;
Copying data from file:/home/wyp/data/wyp.txt
Copying file: file:/home/hdfs/wyp.txt
Loading data to table default.wyp
Table default.wyp stats: [num_partitions: 0, num_files: 1, 
           num_rows: 0, total_size: 67, raw_data_size: 0]
OK
Time taken: 3.289 seconds
hive> select * from wyp;
OK
1       wyp     25      13188888888888
2       test    30      13888888888888
3       zs      34      899314121
Time taken: 0.41 seconds, Fetched: 3 row(s)
```

**导入过程**

指定Linux本地文件路径，数据先从本地文件夹下复制到HDFS上，最后HIve将数据从hdfs上将数据移动到表里面，hdfs中会以表名创建一个文件夹，所有属于这个表的数据都会放在这里面，

**删除过程**
```hive
hive> drop table wyp;
Moved: 'hdfs://mycluster/user/hive/warehouse/wyp' to 
        trash at: hdfs://mycluster/user/hdfs/.Trash/Current
OK
Time taken: 2.503 seconds
```
**从中看出，如果hadoop取用垃圾回收机制，删除表后，删除的数据会被放在hdfs中的一个Trash/current文件下，如果没有启用这个机制，那么删除表后，表的所有数据都没了**


#### 创建一个外部表

```hive
hive> create external table exter_table(
    > id int,
    > name string,
    > age int,
    > tel string)
    > location '/home/wyp/external';
OK
Time taken: 0.098 seconds
```

**外部表的创建多了一个external关键字，同时指定外部表存放数据的路径，如果不指定路径，那么会子hdfs上以外部表的表面建立一个文件夹，并将属于这个表的数据存在里面**

**最后归纳一下Hive中表与外部表的区别:**

1. 在导入数据到外部表，数据并没有移动到自己的数据仓库目录下，也就是说外部表中的数据并不是由它自己来管理的！而表则不一样；

2. 在删除表的时候，Hive将会把属于表的元数据和数据全部删掉；而删除外部表的时候，Hive仅仅删除外部表的元数据，数据是不会删除的！
那么，应该如何选择使用哪种表呢？在大多数情况没有太多的区别，因此选择只是个人喜好的问题。但是作为一个经验，如果所有处理都需要由Hive完成，那么你应该创建表，否则使用外部表！

### 4 Reference

[大数据时代的Hive技术][1]

[Hive组件和执行过程][2]

[内部表和外部表的区别][3]

[1]:http://www.cnblogs.com/sharpxiajun/archive/2013/06/02/3114180.html
[2]:https://blog.csdn.net/youzhouliu/article/details/60581414
[3]:http://www.aboutyun.com/thread-7458-1-1.html


