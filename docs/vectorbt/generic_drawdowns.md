# drawdowns - VectorBT

> **Source:** https://vectorbt.dev/api/generic/drawdowns/

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
      * drawdowns  [ drawdowns  ](https://vectorbt.dev/api/generic/drawdowns/) Table of contents 
        * From accessors 
        * Stats 
        * Plots 
        * dd_attach_field_config 
        * dd_field_config 
        * Drawdowns() 
          * active 
          * active_drawdown() 
          * active_duration() 
          * active_recovery() 
          * active_recovery_duration() 
          * active_recovery_return() 
          * avg_drawdown() 
          * avg_recovery_return() 
          * decline_duration 
          * drawdown 
          * end_val 
          * field_config 
          * from_ts() 
          * indexing_func() 
          * max_drawdown() 
          * max_recovery_return() 
          * metrics 
          * peak_idx 
          * peak_val 
          * plot() 
          * plots_defaults 
          * recovered 
          * recovery_duration 
          * recovery_duration_ratio 
          * recovery_return 
          * stats_defaults 
          * subplots 
          * valley_idx 
          * valley_val 
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
      * [ orders  ](https://vectorbt.dev/api/portfolio/orders/)
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

  * From accessors 
  * Stats 
  * Plots 
  * dd_attach_field_config 
  * dd_field_config 
  * Drawdowns() 
    * active 
    * active_drawdown() 
    * active_duration() 
    * active_recovery() 
    * active_recovery_duration() 
    * active_recovery_return() 
    * avg_drawdown() 
    * avg_recovery_return() 
    * decline_duration 
    * drawdown 
    * end_val 
    * field_config 
    * from_ts() 
    * indexing_func() 
    * max_drawdown() 
    * max_recovery_return() 
    * metrics 
    * peak_idx 
    * peak_val 
    * plot() 
    * plots_defaults 
    * recovered 
    * recovery_duration 
    * recovery_duration_ratio 
    * recovery_return 
    * stats_defaults 
    * subplots 
    * valley_idx 
    * valley_val 



# drawdowns module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Base class for working with drawdown records.

Drawdown records capture information on drawdowns. Since drawdowns are ranges, they subclass [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges").

Warning

[Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns") return both recovered AND active drawdowns, which may skew your performance results. To only consider recovered drawdowns, you should explicitly query `recovered` attribute.

Using [Drawdowns.from_ts()](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.from_ts "vectorbt.generic.drawdowns.Drawdowns.from_ts"), you can generate drawdown records for any time series and analyze them right away.
    
    
    >>> import vectorbt as vbt
    >>> import numpy as np
    >>> import pandas as pd
    
    >>> start = '2019-10-01 UTC'  # crypto is in UTC
    >>> end = '2020-01-01 UTC'
    >>> price = vbt.YFData.download('BTC-USD', start=start, end=end).get('Close')
    >>> price = price.rename(None)
    
    >>> drawdowns = vbt.Drawdowns.from_ts(price, wrapper_kwargs=dict(freq='d'))
    
    >>> drawdowns.records_readable
       Drawdown Id  Column            Peak Timestamp           Start Timestamp  \
    0            0       0 2019-10-02 00:00:00+00:00 2019-10-03 00:00:00+00:00
    1            1       0 2019-10-09 00:00:00+00:00 2019-10-10 00:00:00+00:00
    2            2       0 2019-10-27 00:00:00+00:00 2019-10-28 00:00:00+00:00
    
               Valley Timestamp             End Timestamp   Peak Value  \
    0 2019-10-06 00:00:00+00:00 2019-10-09 00:00:00+00:00  8393.041992
    1 2019-10-24 00:00:00+00:00 2019-10-25 00:00:00+00:00  8595.740234
    2 2019-12-17 00:00:00+00:00 2020-01-01 00:00:00+00:00  9551.714844
    
       Valley Value    End Value     Status
    0   7988.155762  8595.740234  Recovered
    1   7493.488770  8660.700195  Recovered
    2   6640.515137  7200.174316     Active
    
    >>> drawdowns.duration.max(wrap_kwargs=dict(to_timedelta=True))
    Timedelta('66 days 00:00:00')
    

## From accessors¶

Moreover, all generic accessors have a property `drawdowns` and a method `get_drawdowns`:
    
    
    >>> # vectorbt.generic.accessors.GenericAccessor.drawdowns.coverage
    >>> price.vbt.drawdowns.coverage()
    0.9354838709677419
    

## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [Drawdowns.metrics](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.metrics "vectorbt.generic.drawdowns.Drawdowns.metrics").
    
    
    >>> df = pd.DataFrame({
    ...     'a': [1, 2, 1, 3, 2],
    ...     'b': [2, 3, 1, 2, 1]
    ... })
    
    >>> drawdowns = df.vbt(freq='d').drawdowns
    
    >>> drawdowns['a'].stats()
    Start                                        0
    End                                          4
    Period                         5 days 00:00:00
    Coverage [%]                              40.0
    Total Records                                2
    Total Recovered Drawdowns                    1
    Total Active Drawdowns                       1
    Active Drawdown [%]                  33.333333
    Active Duration                1 days 00:00:00
    Active Recovery [%]                        0.0
    Active Recovery Return [%]                 0.0
    Active Recovery Duration       0 days 00:00:00
    Max Drawdown [%]                          50.0
    Avg Drawdown [%]                          50.0
    Max Drawdown Duration          1 days 00:00:00
    Avg Drawdown Duration          1 days 00:00:00
    Max Recovery Return [%]                  200.0
    Avg Recovery Return [%]                  200.0
    Max Recovery Duration          1 days 00:00:00
    Avg Recovery Duration          1 days 00:00:00
    Avg Recovery Duration Ratio                1.0
    Name: a, dtype: object
    

By default, the metrics `max_dd`, `avg_dd`, `max_dd_duration`, and `avg_dd_duration` do not include active drawdowns. To change that, pass `incl_active=True`:
    
    
    >>> drawdowns['a'].stats(settings=dict(incl_active=True))
    Start                                        0
    End                                          4
    Period                         5 days 00:00:00
    Coverage [%]                              40.0
    Total Records                                2
    Total Recovered Drawdowns                    1
    Total Active Drawdowns                       1
    Active Drawdown [%]                  33.333333
    Active Duration                1 days 00:00:00
    Active Recovery [%]                        0.0
    Active Recovery Return [%]                 0.0
    Active Recovery Duration       0 days 00:00:00
    Max Drawdown [%]                          50.0
    Avg Drawdown [%]                     41.666667
    Max Drawdown Duration          1 days 00:00:00
    Avg Drawdown Duration          1 days 00:00:00
    Max Recovery Return [%]                  200.0
    Avg Recovery Return [%]                  200.0
    Max Recovery Duration          1 days 00:00:00
    Avg Recovery Duration          1 days 00:00:00
    Avg Recovery Duration Ratio                1.0
    Name: a, dtype: object
    

[StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.drawdowns.Drawdowns.stats") also supports (re-)grouping:
    
    
    >>> drawdowns['a'].stats(group_by=True)
    UserWarning: Metric 'active_dd' does not support grouped data
    UserWarning: Metric 'active_duration' does not support grouped data
    UserWarning: Metric 'active_recovery' does not support grouped data
    UserWarning: Metric 'active_recovery_return' does not support grouped data
    UserWarning: Metric 'active_recovery_duration' does not support grouped data
    
    Start                                        0
    End                                          4
    Period                         5 days 00:00:00
    Coverage [%]                              40.0
    Total Records                                2
    Total Recovered Drawdowns                    1
    Total Active Drawdowns                       1
    Max Drawdown [%]                          50.0
    Avg Drawdown [%]                          50.0
    Max Drawdown Duration          1 days 00:00:00
    Avg Drawdown Duration          1 days 00:00:00
    Max Recovery Return [%]                  200.0
    Avg Recovery Return [%]                  200.0
    Max Recovery Duration          1 days 00:00:00
    Avg Recovery Duration          1 days 00:00:00
    Avg Recovery Duration Ratio                1.0
    Name: group, dtype: object
    

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [Drawdowns.subplots](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.subplots "vectorbt.generic.drawdowns.Drawdowns.subplots").

[Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns") class has a single subplot based on [Drawdowns.plot()](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.plot "vectorbt.generic.drawdowns.Drawdowns.plot"):
    
    
    >>> drawdowns['a'].plots()
    

* * *

## dd_attach_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Config of fields to be attached to [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").
    
    
    Config({
        "status": {
            "attach_filters": true
        }
    })
    

* * *

## dd_field_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Field config for [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "peak_idx": "int64",
            "start_idx": "int64",
            "valley_idx": "int64",
            "end_idx": "int64",
            "peak_val": "float64",
            "valley_val": "float64",
            "end_val": "float64",
            "status": "int64"
        },
        "settings": {
            "id": {
                "title": "Drawdown Id"
            },
            "peak_idx": {
                "title": "Peak Timestamp",
                "mapping": "index"
            },
            "valley_idx": {
                "title": "Valley Timestamp",
                "mapping": "index"
            },
            "peak_val": {
                "title": "Peak Value"
            },
            "valley_val": {
                "title": "Valley Value"
            },
            "end_val": {
                "title": "End Value"
            },
            "status": {
                "mapping": {
                    "Active": 0,
                    "Recovered": 1
                }
            }
        }
    })
    

* * *

## Drawdowns class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L249-L963 "Jump to source")¶
    
    
    Drawdowns(
        wrapper,
        records_arr,
        ts=None,
        **kwargs
    )
    

Extends [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges") for working with drawdown records.

Requires `records_arr` to have all fields defined in [drawdown_dt](https://vectorbt.dev/api/generic/enums/#vectorbt.generic.enums.drawdown_dt "vectorbt.generic.enums.drawdown_dt").

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges")
  * [Records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records "vectorbt.records.base.Records")
  * [RecordsWithFields](https://vectorbt.dev/api/records/base/#vectorbt.records.base.RecordsWithFields "vectorbt.records.base.RecordsWithFields")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.generic.ranges.Ranges.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.generic.ranges.Ranges.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.generic.ranges.Ranges.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.generic.ranges.Ranges.resolve_attr")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.generic.ranges.Ranges.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.generic.ranges.Ranges.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.generic.ranges.Ranges.loads")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.generic.ranges.Ranges.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.generic.ranges.Ranges.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.generic.ranges.Ranges.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.generic.ranges.Ranges.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.generic.ranges.Ranges.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.generic.ranges.Ranges.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.generic.ranges.Ranges.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.ranges.Ranges.plots")
  * [Ranges.avg_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.avg_duration "vectorbt.generic.ranges.Ranges.avg_duration")
  * [Ranges.closed](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.closed "vectorbt.generic.ranges.Ranges.closed")
  * [Ranges.col](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.col "vectorbt.generic.ranges.Ranges.col")
  * [Ranges.col_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_arr "vectorbt.generic.ranges.Ranges.col_arr")
  * [Ranges.col_mapper](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.col_mapper "vectorbt.generic.ranges.Ranges.col_mapper")
  * [Ranges.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.generic.ranges.Ranges.config")
  * [Ranges.coverage()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage "vectorbt.generic.ranges.Ranges.coverage")
  * [Ranges.duration](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.duration "vectorbt.generic.ranges.Ranges.duration")
  * [Ranges.end_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.end_idx "vectorbt.generic.ranges.Ranges.end_idx")
  * [Ranges.id](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.id "vectorbt.generic.ranges.Ranges.id")
  * [Ranges.id_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.id_arr "vectorbt.generic.ranges.Ranges.id_arr")
  * [Ranges.idx_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.idx_arr "vectorbt.generic.ranges.Ranges.idx_arr")
  * [Ranges.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.generic.ranges.Ranges.iloc")
  * [Ranges.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.generic.ranges.Ranges.indexing_kwargs")
  * [Ranges.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.generic.ranges.Ranges.loc")
  * [Ranges.max_duration()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.max_duration "vectorbt.generic.ranges.Ranges.max_duration")
  * [Ranges.open](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.open "vectorbt.generic.ranges.Ranges.open")
  * [Ranges.records](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records "vectorbt.generic.ranges.Ranges.records")
  * [Ranges.records_arr](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_arr "vectorbt.generic.ranges.Ranges.records_arr")
  * [Ranges.records_readable](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.records_readable "vectorbt.generic.ranges.Ranges.records_readable")
  * [Ranges.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.generic.ranges.Ranges.self_aliases")
  * [Ranges.start_idx](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.start_idx "vectorbt.generic.ranges.Ranges.start_idx")
  * [Ranges.status](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.status "vectorbt.generic.ranges.Ranges.status")
  * [Ranges.to_mask()](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.to_mask "vectorbt.generic.ranges.Ranges.to_mask")
  * [Ranges.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.generic.ranges.Ranges.ts")
  * [Ranges.values](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.values "vectorbt.generic.ranges.Ranges.values")
  * [Ranges.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.generic.ranges.Ranges.wrapper")
  * [Ranges.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.generic.ranges.Ranges.writeable_attrs")
  * [Records.apply()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply "vectorbt.generic.ranges.Ranges.apply")
  * [Records.apply_mask()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.apply_mask "vectorbt.generic.ranges.Ranges.apply_mask")
  * [Records.build_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.build_field_config_doc "vectorbt.generic.ranges.Ranges.build_field_config_doc")
  * [Records.count()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.count "vectorbt.generic.ranges.Ranges.count")
  * [Records.get_apply_mapping_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_apply_mapping_arr "vectorbt.generic.ranges.Ranges.get_apply_mapping_arr")
  * [Records.get_by_col_idxs()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_by_col_idxs "vectorbt.generic.ranges.Ranges.get_by_col_idxs")
  * [Records.get_field_arr()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_arr "vectorbt.generic.ranges.Ranges.get_field_arr")
  * [Records.get_field_mapping()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_mapping "vectorbt.generic.ranges.Ranges.get_field_mapping")
  * [Records.get_field_name()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_name "vectorbt.generic.ranges.Ranges.get_field_name")
  * [Records.get_field_setting()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_setting "vectorbt.generic.ranges.Ranges.get_field_setting")
  * [Records.get_field_title()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_field_title "vectorbt.generic.ranges.Ranges.get_field_title")
  * [Records.get_map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field "vectorbt.generic.ranges.Ranges.get_map_field")
  * [Records.get_map_field_to_index()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.get_map_field_to_index "vectorbt.generic.ranges.Ranges.get_map_field_to_index")
  * [Records.indexing_func_meta()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.indexing_func_meta "vectorbt.generic.ranges.Ranges.indexing_func_meta")
  * [Records.is_sorted()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.is_sorted "vectorbt.generic.ranges.Ranges.is_sorted")
  * [Records.map()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map "vectorbt.generic.ranges.Ranges.map")
  * [Records.map_array()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_array "vectorbt.generic.ranges.Ranges.map_array")
  * [Records.map_field()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.map_field "vectorbt.generic.ranges.Ranges.map_field")
  * [Records.override_field_config_doc()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.override_field_config_doc "vectorbt.generic.ranges.Ranges.override_field_config_doc")
  * [Records.replace()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.replace "vectorbt.generic.ranges.Ranges.replace")
  * [Records.sort()](https://vectorbt.dev/api/records/base/#vectorbt.records.base.Records.sort "vectorbt.generic.ranges.Ranges.sort")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.generic.ranges.Ranges.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.generic.ranges.Ranges.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.ranges.Ranges.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.generic.ranges.Ranges.regroup")
  * [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.generic.ranges.Ranges.resolve_self")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.generic.ranges.Ranges.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.generic.ranges.Ranges.select_one_from_obj")



* * *

### active method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `status == 0`.

* * *

### active_drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L409-L422 "Jump to source")¶
    
    
    Drawdowns.active_drawdown(
        group_by=None,
        wrap_kwargs=None
    )
    

Drawdown of the last active drawdown only.

Does not support grouping.

* * *

### active_duration method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L424-L433 "Jump to source")¶
    
    
    Drawdowns.active_duration(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Duration of the last active drawdown only.

Does not support grouping.

* * *

### active_recovery method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L435-L449 "Jump to source")¶
    
    
    Drawdowns.active_recovery(
        group_by=None,
        wrap_kwargs=None
    )
    

Recovery of the last active drawdown only.

Does not support grouping.

* * *

### active_recovery_duration method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L462-L471 "Jump to source")¶
    
    
    Drawdowns.active_recovery_duration(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Recovery duration of the last active drawdown only.

Does not support grouping.

* * *

### active_recovery_return method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L451-L460 "Jump to source")¶
    
    
    Drawdowns.active_recovery_return(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Recovery return of the last active drawdown only.

Does not support grouping.

* * *

### avg_drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L320-L327 "Jump to source")¶
    
    
    Drawdowns.avg_drawdown(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Average drawdown (ADD).

Based on [Drawdowns.drawdown](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.drawdown "vectorbt.generic.drawdowns.Drawdowns.drawdown").

* * *

### avg_recovery_return method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L351-L358 "Jump to source")¶
    
    
    Drawdowns.avg_recovery_return(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Average recovery return.

Based on [Drawdowns.recovery_return](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.recovery_return "vectorbt.generic.drawdowns.Drawdowns.recovery_return").

* * *

### decline_duration method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

See [dd_decline_duration_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.dd_decline_duration_nb "vectorbt.generic.nb.dd_decline_duration_nb").

Takes into account both recovered and active drawdowns.

* * *

### drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

See [dd_drawdown_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.dd_drawdown_nb "vectorbt.generic.nb.dd_drawdown_nb").

Takes into account both recovered and active drawdowns.

* * *

### end_val method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `end_val`.

* * *

### field_config class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Field config of [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").
    
    
    Config({
        "dtype": {
            "id": "int64",
            "col": "int64",
            "peak_idx": "int64",
            "start_idx": "int64",
            "valley_idx": "int64",
            "end_idx": "int64",
            "peak_val": "float64",
            "valley_val": "float64",
            "end_val": "float64",
            "status": "int64"
        },
        "settings": {
            "id": {
                "name": "id",
                "title": "Drawdown Id"
            },
            "col": {
                "name": "col",
                "title": "Column",
                "mapping": "columns"
            },
            "idx": {
                "name": "end_idx",
                "title": "Timestamp",
                "mapping": "index"
            },
            "start_idx": {
                "title": "Start Timestamp",
                "mapping": "index"
            },
            "end_idx": {
                "title": "End Timestamp",
                "mapping": "index"
            },
            "status": {
                "title": "Status",
                "mapping": {
                    "Active": 0,
                    "Recovered": 1
                }
            },
            "peak_idx": {
                "title": "Peak Timestamp",
                "mapping": "index"
            },
            "valley_idx": {
                "title": "Valley Timestamp",
                "mapping": "index"
            },
            "peak_val": {
                "title": "Peak Value"
            },
            "valley_val": {
                "title": "Valley Value"
            },
            "end_val": {
                "title": "End Value"
            }
        }
    })
    

* * *

### from_ts class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L288-L300 "Jump to source")¶
    
    
    Drawdowns.from_ts(
        ts,
        attach_ts=True,
        wrapper_kwargs=None,
        **kwargs
    )
    

Build [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns") from time series `ts`.

`**kwargs` will be passed to [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L274-L286 "Jump to source")¶
    
    
    Drawdowns.indexing_func(
        pd_indexing_func,
        **kwargs
    )
    

Perform indexing on [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").

* * *

### max_drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L329-L336 "Jump to source")¶
    
    
    Drawdowns.max_drawdown(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Maximum drawdown (MDD).

Based on [Drawdowns.drawdown](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.drawdown "vectorbt.generic.drawdowns.Drawdowns.drawdown").

* * *

### max_recovery_return method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L360-L367 "Jump to source")¶
    
    
    Drawdowns.max_recovery_return(
        group_by=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Maximum recovery return.

Based on [Drawdowns.recovery_return](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns.recovery_return "vectorbt.generic.drawdowns.Drawdowns.recovery_return").

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Metrics supported by [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01620>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function Drawdowns.<lambda> at 0x7f9596c016c0>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01760>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "tags": "wrapper"
        },
        "coverage": {
            "title": "Coverage [%]",
            "calc_func": "coverage",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01800>",
            "tags": [
                "ranges",
                "duration"
            ]
        },
        "total_records": {
            "title": "Total Records",
            "calc_func": "count",
            "tags": "records"
        },
        "total_recovered": {
            "title": "Total Recovered Drawdowns",
            "calc_func": "recovered.count",
            "tags": "drawdowns"
        },
        "total_active": {
            "title": "Total Active Drawdowns",
            "calc_func": "active.count",
            "tags": "drawdowns"
        },
        "active_dd": {
            "title": "Active Drawdown [%]",
            "calc_func": "active_drawdown",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c018a0>",
            "check_is_not_grouped": true,
            "tags": [
                "drawdowns",
                "active"
            ]
        },
        "active_duration": {
            "title": "Active Duration",
            "calc_func": "active_duration",
            "fill_wrap_kwargs": true,
            "check_is_not_grouped": true,
            "tags": [
                "drawdowns",
                "active",
                "duration"
            ]
        },
        "active_recovery": {
            "title": "Active Recovery [%]",
            "calc_func": "active_recovery",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01940>",
            "check_is_not_grouped": true,
            "tags": [
                "drawdowns",
                "active"
            ]
        },
        "active_recovery_return": {
            "title": "Active Recovery Return [%]",
            "calc_func": "active_recovery_return",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c019e0>",
            "check_is_not_grouped": true,
            "tags": [
                "drawdowns",
                "active"
            ]
        },
        "active_recovery_duration": {
            "title": "Active Recovery Duration",
            "calc_func": "active_recovery_duration",
            "fill_wrap_kwargs": true,
            "check_is_not_grouped": true,
            "tags": [
                "drawdowns",
                "active",
                "duration"
            ]
        },
        "max_dd": {
            "title": "Max Drawdown [%]",
            "calc_func": "RepEval(expression=\"'max_drawdown' if incl_active else 'recovered.max_drawdown'\", mapping={})",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01a80>",
            "tags": "RepEval(expression=\"['drawdowns'] if incl_active else ['drawdowns', 'recovered']\", mapping={})"
        },
        "avg_dd": {
            "title": "Avg Drawdown [%]",
            "calc_func": "RepEval(expression=\"'avg_drawdown' if incl_active else 'recovered.avg_drawdown'\", mapping={})",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01b20>",
            "tags": "RepEval(expression=\"['drawdowns'] if incl_active else ['drawdowns', 'recovered']\", mapping={})"
        },
        "max_dd_duration": {
            "title": "Max Drawdown Duration",
            "calc_func": "RepEval(expression=\"'max_duration' if incl_active else 'recovered.max_duration'\", mapping={})",
            "fill_wrap_kwargs": true,
            "tags": "RepEval(expression=\"['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']\", mapping={})"
        },
        "avg_dd_duration": {
            "title": "Avg Drawdown Duration",
            "calc_func": "RepEval(expression=\"'avg_duration' if incl_active else 'recovered.avg_duration'\", mapping={})",
            "fill_wrap_kwargs": true,
            "tags": "RepEval(expression=\"['drawdowns', 'duration'] if incl_active else ['drawdowns', 'recovered', 'duration']\", mapping={})"
        },
        "max_return": {
            "title": "Max Recovery Return [%]",
            "calc_func": "recovered.recovery_return.max",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01bc0>",
            "tags": [
                "drawdowns",
                "recovered"
            ]
        },
        "avg_return": {
            "title": "Avg Recovery Return [%]",
            "calc_func": "recovered.recovery_return.mean",
            "post_calc_func": "<function Drawdowns.<lambda> at 0x7f9596c01c60>",
            "tags": [
                "drawdowns",
                "recovered"
            ]
        },
        "max_recovery_duration": {
            "title": "Max Recovery Duration",
            "calc_func": "recovered.recovery_duration.max",
            "apply_to_timedelta": true,
            "tags": [
                "drawdowns",
                "recovered",
                "duration"
            ]
        },
        "avg_recovery_duration": {
            "title": "Avg Recovery Duration",
            "calc_func": "recovered.recovery_duration.mean",
            "apply_to_timedelta": true,
            "tags": [
                "drawdowns",
                "recovered",
                "duration"
            ]
        },
        "recovery_duration_ratio": {
            "title": "Avg Recovery Duration Ratio",
            "calc_func": "recovered.recovery_duration_ratio.mean",
            "tags": [
                "drawdowns",
                "recovered"
            ]
        }
    })
    

Returns `Drawdowns._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `Drawdowns._metrics`.

* * *

### peak_idx method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `peak_idx`.

* * *

### peak_val method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `peak_val`.

* * *

### plot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L629-L933 "Jump to source")¶
    
    
    Drawdowns.plot(
        column=None,
        top_n=5,
        plot_zones=True,
        ts_trace_kwargs=None,
        peak_trace_kwargs=None,
        valley_trace_kwargs=None,
        recovery_trace_kwargs=None,
        active_trace_kwargs=None,
        decline_shape_kwargs=None,
        recovery_shape_kwargs=None,
        active_shape_kwargs=None,
        add_trace_kwargs=None,
        xref='x',
        yref='y',
        fig=None,
        **layout_kwargs
    )
    

Plot drawdowns.

**Args**

**`column`** : `str`
    Name of the column to plot.
**`top_n`** : `int`
    Filter top N drawdown records by maximum drawdown.
**`plot_zones`** : `bool`
    Whether to plot zones.
**`ts_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for [Drawdowns.ts](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.ts "vectorbt.generic.drawdowns.Drawdowns.ts").
**`peak_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for peak values.
**`valley_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for valley values.
**`recovery_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for recovery values.
**`active_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for active recovery values.
**`decline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for decline zones.
**`recovery_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for recovery zones.
**`active_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for active recovery zones.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`xref`** : `str`
    X coordinate axis.
**`yref`** : `str`
    Y coordinate axis.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> import vectorbt as vbt
    >>> from datetime import datetime, timedelta
    >>> import pandas as pd
    
    >>> price = pd.Series([1, 2, 1, 2, 3, 2, 1, 2], name='Price')
    >>> price.index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(price))]
    >>> vbt.Drawdowns.from_ts(price, wrapper_kwargs=dict(freq='1 day')).plot()
    

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L935-L947 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.drawdowns.Drawdowns.plots").

Merges [Ranges.plots_defaults](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.plots_defaults "vectorbt.generic.ranges.Ranges.plots_defaults") and `drawdowns.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### recovered method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Records filtered by `status == 1`.

* * *

### recovery_duration method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

See [dd_recovery_duration_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.dd_recovery_duration_nb "vectorbt.generic.nb.dd_recovery_duration_nb").

A value higher than 1 means the recovery was slower than the decline.

Takes into account both recovered and active drawdowns.

* * *

### recovery_duration_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

See [dd_recovery_duration_ratio_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.dd_recovery_duration_ratio_nb "vectorbt.generic.nb.dd_recovery_duration_ratio_nb").

Takes into account both recovered and active drawdowns.

* * *

### recovery_return method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

See [dd_recovery_return_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.dd_recovery_return_nb "vectorbt.generic.nb.dd_recovery_return_nb").

Takes into account both recovered and active drawdowns.

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py#L475-L487 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.drawdowns.Drawdowns.stats").

Merges [Ranges.stats_defaults](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.stats_defaults "vectorbt.generic.ranges.Ranges.stats_defaults") and `drawdowns.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/drawdowns.py "Jump to source")¶

Subplots supported by [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").
    
    
    Config({
        "plot": {
            "title": "Drawdowns",
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "tags": "drawdowns"
        }
    })
    

Returns `Drawdowns._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `Drawdowns._subplots`.

* * *

### valley_idx method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `valley_idx`.

* * *

### valley_val method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/utils/decorators.py#L325-L339 "Jump to source")¶

Mapped array of the field `valley_val`.

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
