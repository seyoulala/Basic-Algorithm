### hive left semi join

`left semi join`(左半连接)是exists/in的一种更高效的实现

```sql
select A.key,A.value 
from table1
where A.key in (select B.key from table2)
```

可以改写为

```sql
select A.key,B.value
from table1
left semi join table2
on A.key=B.key
```

特点:

（1）Semi Join，也叫半连接，是从分布式数据库中借鉴过来的方法。它的产生动机是：对于reduce side join，跨机器的数据传输量非常大，这成了join操作的一个瓶颈，如果能够在map端过滤掉不会参加join操作的数据，则可以大大节省网络IO，提升执行效率。
实现方法很简单：选取一个小表，假设是File1，将其参与join的key抽取出来，保存到文件File3中，File3文件一般很小，可以放到内存中。在map阶段，使用DistributedCache将File3复制到各个TaskTracker上，然后将File2中不在File3中的key对应的记录过滤掉，剩下的reduce阶段的工作与reduce side join相同。
由于 hive 中没有 in/exist 这样的子句（新版将支持），所以需要将这种类型的子句转成 left semi join。left semi join 是只传递表的 join key 给 map 阶段 , 如果 key 足够小还是执行 map join, 如果不是则还是 common join。关于 common join（shuffle join/reduce join）的原理请参考文末 refer。

（2）left semi join 子句中右边的表只能在 ON 子句中设置过滤条件，在 WHERE 子句、SELECT 子句或其他地方过滤都不行。

（3）对待右表中重复key的处理方式差异：因为 left semi join 是 in(keySet) 的关系，遇到右表重复记录，左表会跳过，而 join on 则会一直遍历。

最后的结果是这会造成性能，以及 join 结果上的差异。

（4）left semi join 中最后 select 的结果只许出现左表，因为右表只有 join key 参与关联计算了，而 join on 默认是整个关系模型都参与计算了。

