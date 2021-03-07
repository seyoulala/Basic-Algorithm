评分卡

## 好坏样本定义

明确三个定义：观察期，表现期，观察点

![](https://pic1.zhimg.com/80/v2-a2688ab93ed5eeb364c967153708cb9c_hd.jpg)

- 观察期：就是观察点的左侧，主要是用来生成用户特征的时间区间，不宜太长也不能太短。我们是设定一年的时间.
- 观察点：这个点并不是一个具体的时间点，而是一个时间区间，表示的是客户申请贷款的时间，用来搜集用来建模的客户样本，在该时间段申请的客户会是我们用来建模的样本。
- 表现期：用来定义用户是否好坏的时间区段，一般是6个月到一年的时间。


举例说明

假如现在我们模型的表现期为6个月，观察期为一年。当一个客户在2019年-1月-1号来申请贷款的时候，我们需要用现在有的模型来对申请人进行一个申请评分，评估他未来表现期内是否为坏客户的概率，那么模型采用的训练样本应该是什么时候进件的呢？

答：因为表现期为6个月，那么往前推六个月，观察点大概是在2018年6月1号左右某段时间段，因为观察期是一年，所以在往前推一年，也就是在2017年6月到18年6月为观察期。利用在观察点内的申请人在这观察期这一年时间内的行为信息来构建特征。然后根据在表现期内申请人的表现情况来定义违约，然后训练出一个模型。所以评分卡有着天然的滞后性，需要不断对其模型进行监控.


## vintage分析

举个例子，今天是一月一号，我们取今天贷款第一期到期的用户作为观察群体，观察他们今后一个月的还款情况。然后到了二月一号，我们取2月一号第一期到期的客户作为观察群体，观察他们之后一个月的还款情况。这样就可以比较一月一号的群体和二月一号群体还款情况差异了。一般是观察M3+

![](https://pic1.zhimg.com/v2-8ba3e4c0b98572682c09d5f6e46a4c8c_b.jpg)

其中拖欠率为 未还金额/应还金额

按照账龄为经营时间减去发卡时间，可以得到不同发卡时间在发卡后几个月的逾期情况。

![](https://pic2.zhimg.com/v2-066a715935d2965189f794cc42504159_b.jpg)

### PSI

作用:衡量测试样本及模型开发样本评分的分布差异


公式: psi = sum((实际占比-预期占比)*ln(实际占比/预期占比))

举个例子,训练一个LR模型,把数据 喂到模型后会输出一个概率值叫做p1,将概率值从小到大排序后,等频分为10等分.然后计算每等分组的最大最小概率值.现在用这个模型去对新样本进行预测,输出概率值为p2.将P2根据P1的分组进行划分.

实际占比就是新样本通过p2落在p1划分出来的每组占比,预期占比就是测试集上各等分样本的占比.

![](https://images2018.cnblogs.com/blog/1102791/201805/1102791-20180522171535332-956416934.png)



> 目录
> Part 1. 借据与还款计划表
> Part 2. 账龄(MOB)的定义
> Part 3. 逾期天数的计算
> Part 4. 剩余本金的计算
> Part 5. vintage透视表呈现
> Part 6. 总结
> 致谢
> 版权声明
> 参考资料

## **Part 1.** 借据与还款计划表

如图1所示，客户在经过注册、实名认证、授信申请通过后，在可用额度内可以发起动支申请订单。当申贷订单被风控审批通过后，形成借据。对于分期产品，同时生成相应的还款计划表，相当于双方约定的履约合同。此后，客户的还款行为信息将会被记录在还款计划表中，每日更新。

![img](https://pic3.zhimg.com/80/v2-a6f30410c3be4983c8c667ab256e1cba_1440w.png)

​																				图 1 - 信贷产品基础表

现在假设我们借12,000元本金，选择分12期偿还，按等额本息的算法计算一年后需要还的利息，如图2所示。

![img](https://pic4.zhimg.com/80/v2-e998ae78382ed8485d9a179321b73837_1440w.jpg)图 2 - 贷款利息计算器

如图3所示，笔者总结了借据表和还款计划表的一些常见字段。现有一笔借据的放款日期为2019-06-27，每一期约定了还款日期、应还金额等信息。

![img](https://pic1.zhimg.com/80/v2-7d8cdbf8828a3d86379501fe76a3551c_1440w.jpg)图 3 - 客户借据表和还款计划表（非真实数据）

**客户借据表**：

```sql
create table if not exists dm_risk.fhj_loan_table (
 loan_no        string      comment '借据号（主键）'
,loan_term      int         comment '期限'
,prin_amt       double      comment '本金'
,inter_amt      double      comment '利息'
,remain_prin    double      comment '剩余本金'
,repay_type     string      comment '还款方式'
,loan_date      string      comment '放款日期'
,start_date     string      comment '贷款始期'
,end_date       string      comment '贷款止期'
,settle_date    string      comment '结清日期'
,repay_sts      string      comment '结清状态'
) comment '客户借据表';
```

**还款计划表**：

```sql
create table if not exists dm_risk.fhj_plan_table (
 plan_no        string      comment '计划号(主键)'
,loan_no        string      comment '借据号'
,term_no        int         comment '期序'
,due_date       string      comment '应还日'
,repay_date     string      comment '实还日'
,overdue_days   int         comment '逾期天数'
,amt            double      comment '应还金额'
,remain_amt     double      comment '剩余本金'
,prin_amt       double      comment '应还本金'
,inter_amt      double      comment '应还利息'
,penalty        double      comment '应还罚息'
,act_amt        double      comment '实还金额'
,act_prin_amt   double      comment '实还本金'
,act_inter_amt  double      comment '实还利息'
,act_penalty    double      comment '实还罚息'
,repay_sts      string      comment '结清状态'
) comment '还款计划表';
```

假设该信贷产品支持客户选择多种分期（3期、6期、9期、12期），但最长期限为12期。那么，我们只需要注册以下表就可以满足期序要求。

```sql
create table if not exists dm_risk.fhj_term_define as 
          select 1  as term_no 
union all select 2  as term_no 
union all select 3  as term_no 
union all select 4  as term_no 
union all select 5  as term_no 
union all select 6  as term_no 
union all select 7  as term_no 
union all select 8  as term_no 
union all select 9  as term_no 
union all select 10 as term_no 
union all select 11 as term_no
union all select 12 as term_no;
```

假设我们的还款计划表中，每一期的还款日就是每个月固定多少号。我们可以通过以下SQL，初始化生成这笔借据的还款计划表。由于月份存在30/31天（除2月份），或者28/29天（2月份），因此间隔日期不一定都是30天。

每一期的应还本金、本金、利息等数据，取决于具体算法。可参考：《[Vintage损失率转为年化损失率(名义利率/内部收益率/年化利率等概念)](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/dBHmBMCC3ro6AhuYUVHeOg)》

```sql
create table if not exists dm_risk.fhj_plan_table as
select concat(a.loan_no, b.term_no) as plan_no
      ,a.loan_no
      ,b.term_no
      ,add_months(a.loan_date, b.term_no) as due_date
      ,null as repay_date
      ,0 as overdue_days
      -- 以下字段根据实际计息算法得出
      ,prin_amt + inter_amt + penalty as amt  -- 应还金额
      ,0 as remain_amt  -- 剩余金额
      ,0 as prin_amt    -- 本金
      ,0 as inter_amt   -- 利息
      ,0 as penalty     -- 罚息
      -- 以下字段在生成还款计划表时无数据，根据客户还款结果更新
      ,act_prin_amt + act_inter_amt + act_penalty as act_amt  -- 实还金额
      ,null as act_prin_amt      -- 实还本金
      ,null as act_inter_amt     -- 实还利息
      ,null as act_penalty       -- 实还罚息
      ,'未结清' as repay_sts   -- 结清状态
from dm_risk.fhj_loan_table as a        -- 借据表
cross join dm_risk.fhj_term_define as b -- 期序定义
where a.term >= b.term_no;
```

结清状态始终以当前日期为准，在还款计划中T+1更新，其取值共有2种：已结清（提前结清、还款日当天结清、逾期结清）、未结清（未到还款日、还款日未还、逾期未还）。

若**不支持部分还款**，则只有当金额全部还清，repay_date才出现具体日期。因此，我们定义这一期是否还款的依据如下：

```sql
when repay_date is null or repay_date in ('NULL','Null','null') then '未结清' else '已结清'
```

若**支持部分还款**，则当未还清本期金额时，repay_date也会出现具体日期。因此，我们定义这一期是否还款的依据如下：

```sql
case when repay_date is null or repay_date in ('NULL','Null','null') then '未结清'
     when act_amt >= amt then '已结清' -- 实还金额 >= 应还金额
else '未结清'
```

为了后续使用方便，我们将loan和plan表中与vintage计算相关字段摘选出来，并合成一张表。

```sql
create table dm_risk.fhj_vintage_loan_plan as
select distinct 
       l.loan_no
      ,l.loan_date             -- 放款日期
      ,l.loan_term             -- 借款期数
      ,l.prin_amt as loan_amt  -- 借款金额

      ,p.plan_no               -- 还款计划号
      ,p.term_no               -- 期序
      ,p.due_date              -- 应还日期
      ,p.repay_date            -- 结清日期
      ,p.prin_amt              -- 应还本金
      ,p.act_prin_amt          -- 实还本金
      ,p.repay_sts             -- 结清状态
from dm_risk.fhj_loan_table l
left join dm_risk.fhj_plan_table p on l.loan_no = p.loan_no;
```

## **Part 2. 账龄(MOB)的定义**

MOB的英文全称是Month on Book，其含义是这笔资金在账本上记录的月份数。类似于婴孩一出生就有了年龄，一旦申贷订单形成借据，也便拥有了账龄和生命周期。

选取切片数据的时间为每个自然月的最后一天，所有借据都是在同一天统计。我们站在自然月的月末这个时间点，观测这笔借据的逾期状态，并记录下来。

- MOB0：放款日至当月月底
- MOB1：放款后第二个完整的自然月
- MOB2：放款后第三个完整的自然月

![img](https://pic4.zhimg.com/80/v2-25f64871cd21edc034d857a38fd37403_1440w.jpg)图 4 - 月末时点（Month End）定义的MOB

MOB的最大值取决于该笔借据的期数。如果是12期，那么MOB最大到MOB12。例如，放款日期为2019年6月27日的借据，2019年6月是MOB0，2019年7月是MOB1，2019年8月是MOB2，以此类推。

由于是月末时点，因此对于该月所有的借据而言，观察点都是固定的。因此，我们可以将其注册为一张表备用。但是，这种定义的MOB存在的问题是不同时间点的借据，其表现期长度是不同的。例如，以下两笔借据：

- 6月03号：第一个还款日为7月03号，mob1_date为7月31号，逾期表现期有28天。
- 6月27号：第一个还款日为7月27号，mob1_date为7月31号，逾期表现期只有4天。

```sql
create table if not exists dm_risk.fhj_mob_month_end as 
          select '2019-06-30' as mob_date 
union all select '2019-07-31' as mob_date 
union all select '2019-08-31' as mob_date 
union all select '2019-09-30' as mob_date 
union all select '2019-10-31' as mob_date 
union all select '2019-11-30' as mob_date 
union all select '2019-12-31' as mob_date
union all select '2020-01-31' as mob_date
union all select '2020-02-29' as mob_date
union all select '2020-03-31' as mob_date
union all select '2020-04-30' as mob_date
union all select '2020-05-31' as mob_date
union all select '2020-06-30' as mob_date
union all select '2020-07-31' as mob_date
union all select '2020-08-31' as mob_date
union all select '2020-09-30' as mob_date
union all select '2020-10-31' as mob_date
union all select '2020-11-30' as mob_date
union all select '2020-12-31' as mob_date;
```

为解决表现期长短不一的问题，可以采取期末（cycle end）时点作为观察点来统计。但由于月末（month end）时点更容易理解，本文接下来就以月末时点来举例说明。在理解月末时点后，只需要改动下SQL逻辑，就能推广至期末时点。

## **Part 3. 逾期天数的计算**

首先，我们定义3个时间点，后面将会围绕这三者来分情形计算逾期天数。

- **应还日**：due_date，约定应还日期，在生成还款计划表时就已经固定。
- **实还日**：repay_date，实际还款日期，若截止到当前日还未还清，则取值为null。
- **观察日**：mob_date，用以观察逾期状态的时间点。

另外，我们再定义2种逾期观测口径：

**曾经（ever）逾期**：截止到观察点，只要用户曾经发生过逾期（如M1、M2、M3等），不管观察点是否结清，都认为该笔借据处于逾期。因此，该口径下的逾期率能保证vintage曲线单调不减。

**当前（current）逾期**：用户在观察点上当前是否处于逾期状态（如M1、M2、M3等）。哪怕借据在该周期内是否曾经逾期，但在观察点上已经结清，则仍认为该借据正常。《[大数据风控的MOB、Vintage是什么？](https://zhuanlan.zhihu.com/p/192879721)》一文所介绍的就是这种口径。可以看到该口径下的vintage曲线并非单调上升，而可能下降。

如图5所示，对于这种还款表现，**在ever口径下则为逾期，但在current口径下则为正常**。

![img](https://pic4.zhimg.com/80/v2-da1147bbcf588d59a266a413d87de99f_1440w.jpg)图 5 - ever和current口径的对比

现详细介绍如何计算ever口径下的逾期天数。

我们是站在观察日（mob_date）这个时点上去还原统计逾期天数，因此可分为以下几种情况讨论：

**1. 未到应还日，不予考虑**

截止到观察日，有些期序还未到还款日，也就还没产生还款行为。这些期序的逾期天数可直接置为0，或者直接不予考虑。

![img](https://pic4.zhimg.com/80/v2-ab2d3387aabfcccbfc327343ce68e17f_1440w.jpg)图 6 - 情形一（未到还款日）

```sql
when due_date >= mob_date then 0 
```

**2. 已到应还日，但未还清**

这一期，客户截止到当前日一直处于“未结清”状态，而观察日在当前日之前。因此，在ever和current口径下，这一期逾期天数都为：观察日 - 应还日。

![img](https://pic2.zhimg.com/80/v2-2548a084de7cb1bffb9df2a623617775_1440w.jpg)图 7 - 情形二（红色代表逾期中）

```sql
when due_date < mob_date and repay_sts = '未结清' then datediff(mob_date, due_date)
```

**3. 到观察日已还，实还日在观察日之后**

某一期截止到当前日已经处于“已结清”状态，而观察日在实还日之前。因此，在ever和current口径下，这一期逾期天数都为：观察日 - 应还日。

![img](https://pic2.zhimg.com/80/v2-3b4ac1b04dfa7effae142b2279a1543d_1440w.jpg)图 8 - 情形三（红色代表逾期中，绿色代表已还清）

```sql
when due_date < mob_date and repay_sts = '已结清' and repay_date >= mob_date 
then datediff(mob_date, due_date) 
```

**4. 到观察日已还，实还日在观察日之前**

某一期截止到当前日已经处于“已结清”状态，而实还日在观察日之前。因此，逾期天数在两种口径下分别为：

- ever口径：实还日 - 应还日
- current口径：0

![img](https://pic1.zhimg.com/80/v2-5a607b185f99475dad2ef3155889ad68_1440w.jpg)图 9 - 情形四（红色代表逾期中，绿色代表已还清）

```sql
when due_date < mob_date and repay_sts = '已结清' and repay_date <  mob_date 
then datediff(repay_date, due_date)  -- ever口径
```

综上所述，我们生成2张plan_no为主键的逾期天数统计表：

- 在ever口径下，逾期天数计算逻辑如下：

```sql
create table dm_risk.fhj_mob_ever_overduedays_stat as
select a.plan_no, a.term_no, a.due_date, a.repay_date, a.prin_amt, a.act_prin_amt
     , a.loan_no, a.loan_term, a.loan_date, a.loan_amt
     , b.mob_date
     , months_between(mob_date, last_day(loan_date)) as mob,  
case 
when due_date >= mob_date then 0
when due_date <  mob_date and repay_sts = '未结清' then datediff(mob_date, due_date)
when due_date <  mob_date and repay_sts = '已结清' and repay_date >= mob_date then datediff(mob_date, due_date) 
when due_date <  mob_date and repay_sts = '已结清' and repay_date <  mob_date then datediff(repay_date, due_date) 
else 0 end as ever_overdue_days

from dm_risk.fhj_vintage_loan_plan as a  -- 还款计划表
cross join dm_risk.fhj_mob_month_end as b   -- 月末时点
where mob_date <= '2020-10-25'
```

- 在current口径下，逾期天数计算逻辑为：

```sql
create table dm_risk.fhj_mob_curr_overduedays_stat as
select a.plan_no, a.term_no, a.due_date, a.repay_date, a.prin_amt, a.act_prin_amt
     , a.loan_no, a.loan_term, a.loan_date, a.loan_amt
     , b.mob_date
     , months_between(mob_date, last_day(loan_date)) as mob,  
case 
when due_date >= mob_date then 0
when due_date <  mob_date and repay_sts = '未结清' then datediff(mob_date, due_date)
when due_date <  mob_date and repay_sts = '已结清' and repay_date >= mob_date then datediff(mob_date, due_date) 
when due_date <  mob_date and repay_sts = '已结清' and repay_date <  mob_date then 0 
else 0 end as curr_overdue_days

from dm_risk.fhj_vintage_loan_plan as a  -- 还款计划表
cross join dm_risk.fhj_mob_month_end as b   -- 月末时点
where mob_date <= '2020-10-25'
```

## **Part 4. 剩余本金的计算**

如图10所示，这笔借据从第三期开始逾期，截止到观察日时点，该期已经逾期41天，因此这笔借据将被打上“M1+”标记（逾期30天以上）。同时，截止到该观察点的剩余未还本金（balance），我们计入损失金额，也就是逾期率的分子。

> 逾期率 = 第N个MOB月逾期M1+的剩余本金 / 基准月放款额

![img](https://pic4.zhimg.com/80/v2-b5e790281d9895377f75fda66963cdc7_1440w.jpg)图 10 - 剩余本金的计算

此时，我们从loan_no维度来计算逾期信息（以ever口径为例）：

```sql
create table if not exists dm_risk.fhj_loan_ever_m1_stat as
select a.loan_no         -- 借据号
      ,a.loan_term       -- 借款期限
      ,a.loan_amt        -- 借款本金
      ,a.loan_date       -- 借款日期
      ,a.mob             -- 账龄
      ,a.mob_date        -- 观察点
      
      ,sum(if(due_date < mob_date, prin_amt, 0)) as due_prin_amt -- 到期应还本金
      ,sum(if(due_date < mob_date and ever_overdue_days > 30, prin_amt, 0)) as ovd_prin_amt_ever  -- 逾期本金

      ,max(if(due_date < mob_date and ever_overdue_days > 30, 1, 0)) as ovd_flag_ever
      ,if(max(if(due_date < mob_date and ever_overdue_days > 30, 1, 0)) = 1 -- 在观察点前，只要任意一期满足m1+标记，则该借据为m1+
         ,loan_amt - sum(if(repay_date <= mob_date, act_prin_amt, 0)) -- 借款本金 - 已还本金
         ,0
       ) as ovd_loan_bal_ever -- 剩余本金
     
from dm_risk.fhj_mob_ever_overduedays_stat as a
group by a.loan_no  
      ,a.loan_term
      ,a.loan_amt 
      ,a.loan_date
      ,a.mob      
      ,a.mob_date ;
```

## **Part 5. vintage透视表呈现**

本金余额计算口径：放款后在每个自然月的月末，当月总放款额中有多少的本金余额是处于逾期M1+的状态，并观测其变化趋势。

```sql
create table if not exists dm_risk.fhj_vintage_m1_plus_stat as 
select substr(loan_date, 1 ,7) as loan_month -- 放款月份，即vintage
,mob, loan_term -- MOB、期限（之后作为透视表筛选维度）

,count(loan_no) as cnt  -- 放款订单量#
,sum(loan_amt) as amt   -- 放款金额量¥

,sum(ovd_flag_ever) as m1_plus_cnt      -- 逾期M1+放款订单量#
,sum(ovd_loan_bal_ever) as m1_plus_amt  -- 逾期M1+剩余金额量¥

from dm_risk.fhj_loan_ever_m1_stat
where mob_date <= '2020-10-25'
group by substr(loan_date, 1, 7), mob, loan_term;
```

我们将上述结果在Excel中拉出透视表，即可得到vintage曲线。图11为虚构数据。为突出新冠疫情的影响，将2020年1月和2月的曲线有意调高。

![img](https://pic1.zhimg.com/80/v2-70b4cca0c4cbac843ad43030e3972938_1440w.jpg)图 11 - vintage曲线（虚构）

## **Part 5. 总结**

本文主要介绍了以下内容：

1. 借据表和还款计划表的生成和更新逻辑。
2. mob的口径定义和计算方法
3. 逾期天数和剩余本金的计算方法
4. vintage口径的计算方法。