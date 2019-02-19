# Mongodb数据导入HIve方案

## 方案一 
[Hive连接MongoDB](http://blog.csdn.net/thriving_fcl/article/details/51471248)这篇讲了怎么连接
好处在于，直接创建一个Hive的表，用于映射MongoDB里的数据。也就是数据仍然还在MongoDB内，创建映射表的时间非常短。

但是坏处也同样在这，如果要把数据ETL到Hive表，这种方式必须执行map reduce，一直从MongoDB里面取数据，连接的稳定性受到网络环境影响。

在用这种方式导数据的时候遇到过两个坑。


执行map reduce耗时太长，这里一部分是网络原因，还有一部分是起了太多的map 任务，也就是将任务切分的过细，每个map只处理很少的任务，耗费太多资源，坑在于设置map数的参数不同于hive默认的参数。要在执行HQL前输入set mongo.input.split_size=n，这个n就是将mongo collection切分成若干份，每份的大小，单位是MB。默认的设置是8，将它改成128以后，mapper的数量明显减少了，总的执行时间也提高了。还有一种设置方法， 是修改hadoop的yarn-site.xml配置文件，添加

```
    <property>
     <name>mongo.input.split_size</name>
      <value>128</value>
    </property>
```

第二个坑是，MongoDB与Hadoop部署在不同的服务器上，服务器的带宽变改变了，经常在map reduce执行的过程中中断，报SocketTimeout错误，把timeout的时间从30s改成300s了，还是偶尔会出现错误，这对Data pipeline的稳定性影响就特别大。


考虑到data pipeline稳定性第一，只好采用稍微麻烦的第二种方法

---------------------
## 方案二

**mongodump -> BSON -> HDFS**

mongodump 是MongoDB备份的一种方式，可以dump下整个数据库，也可以指定dump某个collection。dump下来的每个collection 都是BSON文件，也就是binary json 的意思。

关于mongodump详细的内容，可以看官方文档 
https://docs.mongodb.com/manual/reference/program/mongodump/

mongodump 的过程比较稳定，效率也比较高。



`mongodump -h $host -u $user -p $password -d $db -c $collection -o $output `

使用上述命令就可以将指定的`collection dump`到`$output`目录了。

然后再将bson文件放入hdfs内。

首先创建一个目录



### 创建HDFS目录
`hdfs dfs -mkdir $hdfs_dir`

### 将文件放入该目录下,$file_path为dump出的bson文件的路径
`hdfs dfs -put $file_path $hdfs_dir`

这时候已经将数据都存放到hdfs内了。要想使用Hive查询数据，再创建相应的表即可，建表的方式与直接连接MongoDB创建映射表类似，不过要修改一些参数，下面给出一个例子。
```bash
create table if not exists ${table_name}
(
 ...
)
comment '...'
row format serde 'com.mongodb.hadoop.hive.BSONSerDe'
with serdeproperties('mongo.columns.mapping'='{hive字段与mongo字段的映射关系}')
stored as inputformat 'com.mongodb.hadoop.mapred.BSONFileInputFormat'
outputformat 'com.mongodb.hadoop.hive.output.HiveBSONFileOutputFormat'
location '{hdfs_dir}'
```

与直接连接mongo创建映射表相同的部分是with serdeproperties，不同的是serde 为com.mongodb.hadoop.hive.BSONSerde 
存储的输入输出控件也不同，并且多了location参数，location指示的是bson文件所在的HDFS目录，也就是先前创建的那个目录。



总结

如果为了方便，偶尔使用Hive访问MongoDB，使用第一种方式较为方便。如果需要定时导数据，保证稳定性，则第二种方式更优。



------------------- 