# orders - VectorBT

> **Source:** https://vectorbt.dev/api/portfolio/orders/

---

[ ](https://vectorbt.dev/ "VectorBT") VectorBT 

[ vectorbt  ](https://github.com/polakowo/vectorbt "Go to repository")

  * [ Getting started  ](https://vectorbt.dev/)

Getting started 
    * [ Features  ](https://vectorbt.dev/getting-started/features/)
    * [ Installation  ](https://vectorbt.dev/getting-started/installation/)
    * [ Usage  ](https://vectorbt.dev/getting-started/usage/)
    * [ Resources  ](https://vectorbt.dev/getting-started/resources/)
    * [ Contributing  ](https://vectorbt.dev/getting-started/contributing/)
  * [ API  ](https://vectorbt.dev/api/)

API 
    * [ _settings  ](https://vectorbt.dev/api/_settings/)
    * [ base  ](https://vectorbt.dev/api/base/)

base 
      * [ accessors  ](https://vectorbt.dev/api/base/accessors/)
      * [ array_wrapper  ](https://vectorbt.dev/api/base/array_wrapper/)
      * [ column_grouper  ](https://vectorbt.dev/api/base/column_grouper/)
      * [ combine_fns  ](https://vectorbt.dev/api/base/combine_fns/)
      * [ index_fns  ](https://vectorbt.dev/api/base/index_fns/)
      * [ indexing  ](https://vectorbt.dev/api/base/indexing/)
      * [ reshape_fns  ](https://vectorbt.dev/api/base/reshape_fns/)
    * [ data  ](https://vectorbt.dev/api/data/)

data 
      * [ base  ](https://vectorbt.dev/api/data/base/)
      * [ custom  ](https://vectorbt.dev/api/data/custom/)
      * [ updater  ](https://vectorbt.dev/api/data/updater/)
    * [ generic  ](https://vectorbt.dev/api/generic/)

generic 
      * [ accessors  ](https://vectorbt.dev/api/generic/accessors/)
      * [ decorators  ](https://vectorbt.dev/api/generic/decorators/)
      * [ drawdowns  ](https://vectorbt.dev/api/generic/drawdowns/)
      * [ enums  ](https://vectorbt.dev/api/generic/enums/)
      * [ nb  ](https://vectorbt.dev/api/generic/nb/)
      * [ plots_builder  ](https://vectorbt.dev/api/generic/plots_builder/)
      * [ plotting  ](https://vectorbt.dev/api/generic/plotting/)
      * [ ranges  ](https://vectorbt.dev/api/generic/ranges/)
      * [ splitters  ](https://vectorbt.dev/api/generic/splitters/)
      * [ stats_builder  ](https://vectorbt.dev/api/generic/stats_builder/)
    * [ indicators  ](https://vectorbt.dev/api/indicators/)

indicators 
      * [ basic  ](https://vectorbt.dev/api/indicators/basic/)
      * [ configs  ](https://vectorbt.dev/api/indicators/configs/)
      * [ factory  ](https://vectorbt.dev/api/indicators/factory/)
      * [ nb  ](https://vectorbt.dev/api/indicators/nb/)
    * [ labels  ](https://vectorbt.dev/api/labels/)

labels 
      * [ enums  ](https://vectorbt.dev/api/labels/enums/)
      * [ generators  ](https://vectorbt.dev/api/labels/generators/)
      * [ nb  ](https://vectorbt.dev/api/labels/nb/)
    * [ messaging  ](https://vectorbt.dev/api/messaging/)

messaging 
      * [ telegram  ](https://vectorbt.dev/api/messaging/telegram/)
    * [ ohlcv_accessors  ](https://vectorbt.dev/api/ohlcv_accessors/)
    * [ portfolio  ](https://vectorbt.dev/api/portfolio/)

portfolio 
      * [ base  ](https://vectorbt.dev/api/portfolio/base/)
      * [ decorators  ](https://vectorbt.dev/api/portfolio/decorators/)
      * [ enums  ](https://vectorbt.dev/api/portfolio/enums/)
      * [ logs  ](https://vectorbt.dev/api/portfolio/logs/)
      * [ nb  ](https://vectorbt.dev/api/portfolio/nb/)
      * orders  [ orders  ](https://vectorbt.dev/api/portfolio/orders/) Table of contents 
        * Stats 
        * Plots 
        * orders_attach_field_config 
        * orders_field_config 
        * Orders() 
          * buy 
          * close 
          * col 
          * fees 
          * field_config 
          * id 
          * idx 
          * indexing_func() 
          * metrics 
          * plot() 
          * plots_defaults 
          * price 
          * sell 
          * side 
          * size 
          * stats_defaults 
          * subplots 
      * [ trades  ](https://vectorbt.dev/api/portfolio/trades/)
    * [ px_accessors  ](https://vectorbt.dev/api/px_accessors/)
    * [ records  ](https://vectorbt.dev/api/records/)

records 
      * [ base  ](https://vectorbt.dev/api/records/base/)
      * [ col_mapper  ](https://vectorbt.dev/api/records/col_mapper/)
      * [ decorators  ](https://vectorbt.dev/api/records/decorators/)
      * [ mapped_array  ](https://vectorbt.dev/api/records/mapped_array/)
      * [ nb  ](https://vectorbt.dev/api/records/nb/)
    * [ returns  ](https://vectorbt.dev/api/returns/)

returns 
      * [ accessors  ](https://vectorbt.dev/api/returns/accessors/)
      * [ metrics  ](https://vectorbt.dev/api/returns/metrics/)
      * [ nb  ](https://vectorbt.dev/api/returns/nb/)
      * [ qs_adapter  ](https://vectorbt.dev/api/returns/qs_adapter/)
    * [ root_accessors  ](https://vectorbt.dev/api/root_accessors/)
    * [ signals  ](https://vectorbt.dev/api/signals/)

signals 
      * [ accessors  ](https://vectorbt.dev/api/signals/accessors/)
      * [ enums  ](https://vectorbt.dev/api/signals/enums/)
      * [ factory  ](https://vectorbt.dev/api/signals/factory/)
      * [ generators  ](https://vectorbt.dev/api/signals/generators/)
      * [ nb  ](https://vectorbt.dev/api/signals/nb/)
    * [ utils  ](https://vectorbt.dev/api/utils/)

utils 
      * [ array_  ](https://vectorbt.dev/api/utils/array_/)
      * [ attr_  ](https://vectorbt.dev/api/utils/attr_/)
      * [ checks  ](https://vectorbt.dev/api/utils/checks/)
      * [ colors  ](https://vectorbt.dev/api/utils/colors/)
      * [ config  ](https://vectorbt.dev/api/utils/config/)
      * [ datetime_  ](https://vectorbt.dev/api/utils/datetime_/)
      * [ decorators  ](https://vectorbt.dev/api/utils/decorators/)
      * [ docs  ](https://vectorbt.dev/api/utils/docs/)
      * [ enum_  ](https://vectorbt.dev/api/utils/enum_/)
      * [ figure  ](https://vectorbt.dev/api/utils/figure/)
      * [ image_  ](https://vectorbt.dev/api/utils/image_/)
      * [ mapping  ](https://vectorbt.dev/api/utils/mapping/)
      * [ math_  ](https://vectorbt.dev/api/utils/math_/)
      * [ module_  ](https://vectorbt.dev/api/utils/module_/)
      * [ params  ](https://vectorbt.dev/api/utils/params/)
      * [ random_  ](https://vectorbt.dev/api/utils/random_/)
      * [ requests_  ](https://vectorbt.dev/api/utils/requests_/)
      * [ schedule_  ](https://vectorbt.dev/api/utils/schedule_/)
      * [ tags  ](https://vectorbt.dev/api/utils/tags/)
      * [ template  ](https://vectorbt.dev/api/utils/template/)
  * [ Terms  ](https://vectorbt.dev/terms/)

Terms 
    * [ License  ](https://vectorbt.dev/terms/license/)



Table of contents 

  * Stats 
  * Plots 
  * orders_attach_field_config 
  * orders_field_config 
  * Orders() 
    * buy 
    * close 
    * col 
    * fees 
    * field_config 
    * id 
    * idx 
    * indexing_func() 
    * metrics 
    * plot() 
    * plots_defaults 
    * price 
    * sell 
    * side 
    * size 
    * stats_defaults 
    * subplots 



# orders module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Base class for working with order records.

Order records capture information on filled orders. Orders are mainly populated when simulating a portfolio and can be accessed as [Portfolio.orders](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.orders "vectorbt.portfolio.base.Portfolio.orders").
    
    
    >>> import pandas as pd
    >>> import numpy as np
    >>> from datetime import datetime, timedelta
    >>> import vectorbt as vbt
    
    >>> np.random.seed(42)
    >>> price = pd.DataFrame({
    ...     'a': np.random.uniform(1, 2, size=100),
    ...     'b': np.random.uniform(1, 2, size=100)
    ... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    >>> size = pd.DataFrame({
    ...     'a': np.random.uniform(-1, 1, size=100),
    ...     'b': np.random.uniform(-1, 1, size=100),
    ... }, index=[datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)])
    >>> pf = vbt.Portfolio.from_orders(price, size, fees=0.01, freq='d')
    >>> orders = pf.orders
    
    >>> orders.buy.count()
    a    58
    b    51
    Name: count, dtype: int64
    
    >>> orders.sell.count()
    a    42
    b    49
    Name: count, dtype: int64
    

## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [Orders.metrics](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders.metrics "vectorbt.portfolio.orders.Orders.metrics").
    
    
    >>> orders['a'].stats()
    Start                2020-01-01 00:00:00
    End                  2020-04-09 00:00:00
    Period                 100 days 00:00:00
    Total Records                        100
    Total Buy Orders                      58
    Total Sell Orders                     42
    Min Size                        0.003033
    Max Size                        0.989877
    Avg Size                        0.508608
    Avg Buy Size                    0.468802
    Avg Sell Size                   0.563577
    Avg Buy Price                   1.437037
    Avg Sell Price                  1.515951
    Total Fees                      0.740177
    Min Fees                        0.000052
    Max Fees                        0.016224
    Avg Fees                        0.007402
    Avg Buy Fees                    0.006771
    Avg Sell Fees                   0.008273
    Name: a, dtype: object
    

[StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.orders.Orders.stats") also supports (re-)grouping:
    
    
    >>> orders.stats(group_by=True)
    Start                2020-01-01 00:00:00
    End                  2020-04-09 00:00:00
    Period                 100 days 00:00:00
    Total Records                        200
    Total Buy Orders                     109
    Total Sell Orders                     91
    Min Size                        0.003033
    Max Size                        0.989877
    Avg Size                        0.506279
    Avg Buy Size                    0.472504
    Avg Sell Size                   0.546735
    Avg Buy Price                    1.47336
    Avg Sell Price                  1.496759
    Total Fees                      1.483343
    Min Fees                        0.000052
    Max Fees                        0.018319
    Avg Fees                        0.007417
    Avg Buy Fees                    0.006881
    Avg Sell Fees                   0.008058
    Name: group, dtype: object
    

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [Orders.subplots](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders.subplots "vectorbt.portfolio.orders.Orders.subplots").

[Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders") class has a single subplot based on [Orders.plot()](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders.plot "vectorbt.portfolio.orders.Orders.plot"):
    
    
    >>> orders['a'].plots()
    

* * *

## orders_attach_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Config of fields to be attached to [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").
    
    
    Config({
        "side": {
            "attach_filters": true
        }
    })
    

* * *

## orders_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Field config for [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "idx": "int64",
            "size": "float64",
            "price": "float64",
            "fees": "float64",
            "side": "int64"
        },
        "settings": {
            "id": {
                "title": "Order Id"
            },
            "size": {
                "title": "Size"
            },
            "price": {
                "title": "Price"
            },
            "fees": {
                "title": "Fees"
            },
            "side": {
                "title": "Side",
                "mapping": {
                    "Buy": 0,
                    "Sell": 1
                }
            }
        }
    })
    

* * *

## Orders class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L178-L524 "Jump to source")¶
    
    
    Orders(
        wrapper,
        records_arr,
        close=None,
        **kwargs
    )
    

Extends `Records` for working with order records.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.records.base.Records.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.records.base.Records.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.records.base.Records.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.records.base.Records.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.records.base.Records.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.records.base.Records.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.records.base.Records.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.records.base.Records.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.records.base.Records.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.records.base.Records.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.records.base.Records.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.records.base.Records.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.records.base.Records.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.records.base.Records.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.records.base.Records.plots")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.records.base.Records.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.records.base.Records.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.records.base.Records.build_field_config_doc")
  * [Records.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.records.base.Records.col_arr")
  * [Records.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.records.base.Records.col_mapper")
  * [Records.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.records.base.Records.config")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.records.base.Records.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.records.base.Records.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.records.base.Records.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.records.base.Records.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.records.base.Records.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.records.base.Records.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.records.base.Records.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.records.base.Records.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.records.base.Records.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.records.base.Records.get_map_field_to_index")
  * [Records.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.records.base.Records.id_arr")
  * [Records.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.records.base.Records.idx_arr")
  * [Records.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.records.base.Records.iloc")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.records.base.Records.indexing_func_meta")
  * [Records.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.records.base.Records.indexing_kwargs")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.records.base.Records.is_sorted")
  * [Records.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.records.base.Records.loc")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.records.base.Records.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.records.base.Records.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.records.base.Records.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.records.base.Records.override_field_config_doc")
  * [Records.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.records.base.Records.records")
  * [Records.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.records.base.Records.records_arr")
  * [Records.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.records.base.Records.records_readable")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.records.base.Records.replace")
  * [Records.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.records.base.Records.self_aliases")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.records.base.Records.sort")
  * [Records.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.records.base.Records.values")
  * [Records.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.records.base.Records.wrapper")
  * [Records.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.records.base.Records.writeable_attrs")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.records.base.Records.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.records.base.Records.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.records.base.Records.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.records.base.Records.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.records.base.Records.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.records.base.Records.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.records.base.Records.select_one_from_obj")



* * *

### buy method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `side == 0`.

* * *

### close property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L215-L218 "Jump to source")¶

Reference price such as close (optional).

* * *

### col method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `col`.

* * *

### fees method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `fees`.

* * *

### field_config class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Field config of [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "idx": "int64",
            "size": "float64",
            "price": "float64",
            "fees": "float64",
            "side": "int64"
        },
        "settings": {
            "id": {
                "name": "id",
                "title": "Order Id"
            },
            "col": {
                "name": "col",
                "title": "Column",
                "mapping": "columns"
            },
            "idx": {
                "name": "idx",
                "title": "Timestamp",
                "mapping": "index"
            },
            "size": {
                "title": "Size"
            },
            "price": {
                "title": "Price"
            },
            "fees": {
                "title": "Fees"
            },
            "side": {
                "title": "Side",
                "mapping": {
                    "Buy": 0,
                    "Sell": 1
                }
            }
        }
    })
    

* * *

### id method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `id`.

* * *

### idx method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `idx`.

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L201-L213 "Jump to source")¶
    
    
    Orders.indexing_func(
        pd_indexing_func,
        **kwargs
    )
    

Perform indexing on [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Metrics supported by [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function Orders.<lambda> at 0x7f957f5d59e0>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function Orders.<lambda> at 0x7f957f5d5800>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function Orders.<lambda> at 0x7f957f5d5760>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "tags": "wrapper"
        },
        "total_records": {
            "title": "Total Records",
            "calc_func": "count",
            "tags": "records"
        },
        "total_buy_orders": {
            "title": "Total Buy Orders",
            "calc_func": "buy.count",
            "tags": [
                "orders",
                "buy"
            ]
        },
        "total_sell_orders": {
            "title": "Total Sell Orders",
            "calc_func": "sell.count",
            "tags": [
                "orders",
                "sell"
            ]
        },
        "min_size": {
            "title": "Min Size",
            "calc_func": "size.min",
            "tags": [
                "orders",
                "size"
            ]
        },
        "max_size": {
            "title": "Max Size",
            "calc_func": "size.max",
            "tags": [
                "orders",
                "size"
            ]
        },
        "avg_size": {
            "title": "Avg Size",
            "calc_func": "size.mean",
            "tags": [
                "orders",
                "size"
            ]
        },
        "avg_buy_size": {
            "title": "Avg Buy Size",
            "calc_func": "buy.size.mean",
            "tags": [
                "orders",
                "buy",
                "size"
            ]
        },
        "avg_sell_size": {
            "title": "Avg Sell Size",
            "calc_func": "sell.size.mean",
            "tags": [
                "orders",
                "sell",
                "size"
            ]
        },
        "avg_buy_price": {
            "title": "Avg Buy Price",
            "calc_func": "buy.price.mean",
            "tags": [
                "orders",
                "buy",
                "price"
            ]
        },
        "avg_sell_price": {
            "title": "Avg Sell Price",
            "calc_func": "sell.price.mean",
            "tags": [
                "orders",
                "sell",
                "price"
            ]
        },
        "total_fees": {
            "title": "Total Fees",
            "calc_func": "fees.sum",
            "tags": [
                "orders",
                "fees"
            ]
        },
        "min_fees": {
            "title": "Min Fees",
            "calc_func": "fees.min",
            "tags": [
                "orders",
                "fees"
            ]
        },
        "max_fees": {
            "title": "Max Fees",
            "calc_func": "fees.max",
            "tags": [
                "orders",
                "fees"
            ]
        },
        "avg_fees": {
            "title": "Avg Fees",
            "calc_func": "fees.mean",
            "tags": [
                "orders",
                "fees"
            ]
        },
        "avg_buy_fees": {
            "title": "Avg Buy Fees",
            "calc_func": "buy.fees.mean",
            "tags": [
                "orders",
                "buy",
                "fees"
            ]
        },
        "avg_sell_fees": {
            "title": "Avg Sell Fees",
            "calc_func": "sell.fees.mean",
            "tags": [
                "orders",
                "sell",
                "fees"
            ]
        }
    })
    

Returns `Orders._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Orders._metrics`.

* * *

### plot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L347-L493 "Jump to source")¶
    
    
    Orders.plot(
        column=None,
        close_trace_kwargs=None,
        buy_trace_kwargs=None,
        sell_trace_kwargs=None,
        add_trace_kwargs=None,
        fig=None,
        **layout_kwargs
    )
    

Plot orders.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`close_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Orders.close](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders.close "vectorbt.portfolio.orders.Orders.close").
**`buy_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Buy" markers.
**`sell_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for "Sell" markers.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> import pandas as pd
    >>> from datetime import datetime, timedelta
    >>> import vectorbt as vbt
    
    >>> price = pd.Series([1., 2., 3., 2., 1.], name='Price')
    >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
    >>> size = pd.Series([1., 1., 1., 1., -1.])
    >>> orders = vbt.Portfolio.from_orders(price, size).orders
    
    >>> orders.plot()
    

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L495-L507 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.portfolio.orders.Orders.plots").

Merges [Records.plots_defaults](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.plots_defaults "vectorbt.records.base.Records.plots_defaults") and `orders.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### price method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `price`.

* * *

### sell method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `side == 1`.

* * *

### side method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `side`.

* * *

### size method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `size`.

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py#L222-L234 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.portfolio.orders.Orders.stats").

Merges [Records.stats_defaults](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.stats_defaults "vectorbt.records.base.Records.stats_defaults") and `orders.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/orders.py "Jump to source")¶

Subplots supported by [Orders](https://vectorbt.dev/api/portfolio/orders/#vectorbt.portfolio.orders.Orders "vectorbt.portfolio.orders.Orders").
    
    
    Config({
        "plot": {
            "title": "Orders",
            "yaxis_kwargs": {
                "title": "Price"
            },
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "tags": "orders"
        }
    })
    

Returns `Orders._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Orders._subplots`.

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
