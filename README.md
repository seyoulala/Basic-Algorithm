## Project Service

No. | Date | Title | Content |  部署启动位置  | 访问地址  | Author  | Version
-------  | -------  | ------- | ------- | ------- | ------ | ------- | -------
0 | ..  | CDH 集群 | CDH & [CM][0]  | Clouder Manager | [http://192.192.0.25:7180/cmf/login][l0] | Zhou、Blair、Yao | 1.0
1 | 2018-08-20  | 算法小平台 | ipython+Jupyter+Spark | 27:/etc/jupyterhub/jupyterhub_spark.sh | [192.192.0.27:8000][l1] | Yao | 1.0
2 | 2018-09-08  | 多维分析（OLAP） | Kylin | 27:/data0/deploy/apache-kylin-2.3.2-bin/| [192.192.0.27:7070/kylin][l2] | Yao | 1.0
3 | -  | 爬虫平台 | Pyspider | - | [http://192.192.0.18:5000/][l2] | Zhou、Yao | 1.0
4 | - | 图数据库 | neo4j | 27:/etc/data0/neo4j<br>25、26:/etc/neo4j | [http://192.192.0.27:7474][l4] | Yao、Blair | 1.0
5 | - | Elasticsearch | - | - | [http://192.192.0.18:9100/][l5] | Zhou、Blair、Yao | 1.0

[l0]: http://192.192.0.25:7180/cmf/login
[l1]: http://192.192.0.27:8000
[l2]: http://192.192.0.27:7070/kylin
[l3]: http://192.192.0.18:5000/
[l4]: http://192.192.0.27:7474
[l5]: http://192.192.0.18:9100/

## Skill & Project

No. | Date | Title | Content |  Status  | Author  | Version
-------  | -------  | ------- | ------- | ------- | ------ | -------
| | | | | |
1 | 2018-06-20  | 大数据搜索引擎 | ElasticSreach & Kibana | Python 增删改查 掌握 | Yao、Xu、Blair | 1.0
2 | 2018-09-01  | 大数据仓库工具 | Hive | Hive SQL 操作  | Yao、Xu、Blair | 1.0
3 | - | ETL离线数据同步工具/平台 | DataX & Sqoop | Mysql 导入 Hdfs、Hive 掌握   | Xu、Yao、Blair | 1.0
4 | ..  | 分布式列数据库 | Hbase | 未操作 |  |  | 1.0
5 | 2018-09-13 | 大数据 多维分析（OLAP）| Kylin | Hive/Hbase/Cube/Tableau demo操作 | Yao | 1.0
 |  | 多维分析大数据平台数据流程图 | [文档链接][10] | |  Yao、Blair | 1.0
6 | 2018-09-13 | 实时流 | Spark Streaming 等[文档链接][6] | Python 代码 未实操 | Xu、Yao | 1.0
 |  | 规则引擎+实时流 数据流图 | [文档链接][6.1] | 假定预期 | Yao、Blair | 1.0
7 | 2018-09-13 | 机器学习算法平台 | 小平台多用户ipython+Jupyter+Spark | [业界的通用大平台调研文档][9] | Yao、Xu、Blair | 1.0
8 | 2018-07-21 | 评分卡 | A卡技术调研 与 Python实操 [文档链接][8] | 通用 LR 评分卡技术 掌握 |  Xu | 1.0
9 |  | 图数据库  | neo4j |  | Yao、Blair | 1.0
10 |  | 知识图谱  | KG在反欺诈中的应用调研报告 |  | Xu、Blair |  1.0

[0]: http://192.192.0.25:7180/cmf/login
[6.1]: http://192.168.0.12/data/data-team-doc/tree/master/decision_engine#4预期规则引擎实时流应用流程
[6]: http://192.168.0.12/data/data-team-doc/tree/master/real_time_flow
[8]: http://192.168.0.12/data/data-team-doc/tree/master/scoring_card
[9]: http://192.168.0.12/data/data-team-doc/blob/master/ml_platform/ml_platform_report_2.0.md
[10]: http://192.168.0.12/data/data-team-doc/blob/master/kylin/Kylin_Tableau.md

## Some Problem

kylin 使用 与 Hive 同时使用，阻塞等
...
