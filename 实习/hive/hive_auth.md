# Hive遇到的问题汇总

Date | Title | Author |  Confirmer  |
-------  | ------- | ------- | ------- | 
2018-07-25 | Spark+Ipython+notebook搭建 | yaojinquan |  Blair |


### hive的权限问题

    初次使用hive输入类似show databases;出现无权访问的报错
```
org.apache.hadoop.hive.ql.metadata.HiveException: java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
```
    根据实际情况，最初只有root用户具有再服务器上操作/var/lib/hive/metastore文件夹的权限因此普通用户无法进行操作，需要登录root用户或者其他有权限的用户建立数据库后分配对应权限

#### 开启权限管理

```
1.在hive-site.xml文件中配置参数开启权限认证，开启启身份认证后，任何用户必须被grant privilege才能对实体进行操作：
hive.security.authorization.enabled = true
```

```
2.表示创建表时自动赋予一些用户或角色相应的权限：
hive.security.authorization.createtable.owner.grants = ALL
hive.security.authorization.createtable.role.grants = admin_role:ALL
hive.security.authorization.createtable.user.grants = user1,user2:select;user3:create

```

```
3.假如出现以下错误： Error while compiling statement: FAILED: SemanticException The current builtin authorization in Hive is incomplete and disabled. 需要配置下面的属性：
hive.security.authorization.task.factory = org.apache.hadoop.hive.ql.parse.authorization.HiveAuthorizationTaskFactoryImpl
```

```
4.属性赋值采用xml，格式如下：
<property> 
    <name>key</name> 
    <value>value</value> 
</property> 
```

```
5.成功后需要将/var/lib/hive/metastore/metastore_db目录下部分文件的写权限开启，否则普通用户无法对root用户创建的文件进行操作
至少需要开启其中tmp/ db.lck 的写权限 如果失败，通过日志查看还需要什么文件的权限，开启后继续尝试
chmod -R o+w ...
chmod -R 777 ... (注意虽然成功率很高但谨慎使用)
```
>**成功后不要再使用root账户对hive进行操作，这会导致db.lck文件和tmp文件夹被root重写，权限会被更改导致普通用户无法访问**

### 连接数据库

```
ERROR sqoop.Sqoop: Got exception running Sqoop: java.lang.RuntimeException: Could not load db driver class: com.mysql.jdbc.Driver
java.lang.RuntimeException: Could not load db driver class: com.mysql.jdbc.Driver
```

    成功建表之后，使用shell连接mysql导入数据时可能遇到缺少驱动包的问题，只需将mysql-connector-java-5.xx.x.jar 复制到sqoop安装目录的lib目录中即可！
    
>**如果导入还依然报如下错误，请尝试导入不同的版本的包**


### 实例操作

使用数据库：192.192.0.201下的WKL

```
表结构： id            bigint
        name          varchar
        age           int
        create_time   timestamp
```

