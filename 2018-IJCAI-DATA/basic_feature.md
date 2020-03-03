`从广告角度`

- Item_hour_cnt:每一个item_id在每个时刻被点击的次数：groupby(item_id,hour).nunique(instance_id)
- Item_hour_cnt_ratio:每一个item_id在每个时刻被点击的次数比例
- Item_maphour_cnt:每个item_id在每个时间段被点击的次数
- item_maphour_cnt_ratio:每个item_id在每个时间段被点击的次数比率

`从用户角度`

- User_hour_cnt：每个用户在每个时刻点击广告的数量
- user_hour_cnt_ratio
- user_hourmap_cnt:每个用户在每个时间段点击广告的数量
- User_hourmap_cnt_ratio
- Same_time_expo_cnt:每个user在广告展示时间点击广告的情况。

`活跃时间特征`

- User_active_hour:每个用户一天内活跃的次数
- User_active_city:每个用户一天内活跃的城市数
- Category_day_active_item:每个类别商品在每天活跃的广告数
- User_hour_active_city:每个用户在每个每个时刻点击的广告数量
- 从Item_id,shop_id,item_brand_id,item_category_list的角度统计每天活跃的用户数(item_day_active_user,shop_day_active_user,brand_day_active_user,category_day_active_user)
- 从user角度去看每个user在每个shop，brand中活跃的次数(user_day_active_shop,user_day_active_brand)

`广告商品是展示在shop中，从shop_id角度去统计该店商品的一些统计值`

- 

### 点击特征

- 从用户角度看

  - u_day_diffTime_first:当前点击时间和第一次点击的时间差
  - u_day_diffTime_last:当前点击时间和最后一次点击的时间差
  - 前后点击时间的时间差值特征:time_diff

  - user_Time_diff_mean:时间差值的mean
  - user_time_diff_std:时间差值的std

- 从广告角度看

  - item_day_diffTime_first:当前点击时间和第一次点击的时间差
  - item_day_diffTime_last:当前点击时间和最后一次点击的时间差
  - 前后点击时间的时间差值特征:time_diff

  - item_Time_diff_mean:时间差值的mean
  - item_time_diff_std:时间差值的std

- 从商品品牌角度看

  - b_day_diffTime_first:当前点击时间和第一次点击的时间差
  - b_day_diffTime_last:当前点击时间和最后一次点击的时间差
  - 前后点击时间的时间差值特征:time_diff

  - brand_Time_diff_mean:时间差值的mean
  - brand_time_diff_std:时间差值的std

- 从商店角度去看

  - shop_day_diffTime_first:当前点击时间和第一次点击的时间差
  - shop_day_diffTime_last:当前点击时间和最后一次点击的时间差
  - 前后点击时间的时间差值特征:time_diff

  - shop_Time_diff_mean:时间差值的mean
  - shop_time_diff_std:时间差值的std



### 组合特征

`对于category feature的组合特征，变为str然后进行拼接`

Item_sales_level,item_price_level,item_collected_level两两之间进行组合特征

User_gender_id,user_age_level,user_occupation_id,user_star_level两两之间进行特征的组合等。

`item,shop,user之间也可以进行特征的交叉`

### 多维度groupby进行统计构造特征

如：一个user_id,item_id下有多少点击样本等等。



