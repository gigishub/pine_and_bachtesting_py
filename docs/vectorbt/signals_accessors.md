# accessors - VectorBT

> **Source:** https://vectorbt.dev/api/signals/accessors/

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
      * accessors  [ accessors  ](https://vectorbt.dev/api/signals/accessors/) Table of contents 
        * Stats 
        * Plots 
        * SignalsAccessor() 
          * AND() 
          * OR() 
          * XOR() 
          * between_partition_ranges() 
          * between_ranges() 
          * bshift() 
          * clean() 
          * empty() 
          * empty_like() 
          * first() 
          * from_nth() 
          * fshift() 
          * generate() 
          * generate_both() 
          * generate_exits() 
          * generate_ohlc_stop_exits() 
          * generate_random() 
          * generate_random_both() 
          * generate_random_exits() 
          * generate_stop_exits() 
          * index_mapped() 
          * metrics 
          * norm_avg_index() 
          * nth() 
          * nth_index() 
          * partition_pos_rank() 
          * partition_pos_rank_mapped() 
          * partition_ranges() 
          * partition_rate() 
          * plot() 
          * plots_defaults 
          * pos_rank() 
          * pos_rank_mapped() 
          * rank() 
          * rate() 
          * stats_defaults 
          * subplots 
          * total() 
          * total_partitions() 
        * SignalsDFAccessor() 
        * SignalsSRAccessor() 
          * plot_as_entry_markers() 
          * plot_as_exit_markers() 
          * plot_as_markers() 
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
  * SignalsAccessor() 
    * AND() 
    * OR() 
    * XOR() 
    * between_partition_ranges() 
    * between_ranges() 
    * bshift() 
    * clean() 
    * empty() 
    * empty_like() 
    * first() 
    * from_nth() 
    * fshift() 
    * generate() 
    * generate_both() 
    * generate_exits() 
    * generate_ohlc_stop_exits() 
    * generate_random() 
    * generate_random_both() 
    * generate_random_exits() 
    * generate_stop_exits() 
    * index_mapped() 
    * metrics 
    * norm_avg_index() 
    * nth() 
    * nth_index() 
    * partition_pos_rank() 
    * partition_pos_rank_mapped() 
    * partition_ranges() 
    * partition_rate() 
    * plot() 
    * plots_defaults 
    * pos_rank() 
    * pos_rank_mapped() 
    * rank() 
    * rate() 
    * stats_defaults 
    * subplots 
    * total() 
    * total_partitions() 
  * SignalsDFAccessor() 
  * SignalsSRAccessor() 
    * plot_as_entry_markers() 
    * plot_as_exit_markers() 
    * plot_as_markers() 



# accessors module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py "Jump to source")¶

Custom pandas accessors for signals data.

Methods can be accessed as follows:

  * [SignalsSRAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsSRAccessor "vectorbt.signals.accessors.SignalsSRAccessor") -> `pd.Series.vbt.signals.*`
  * [SignalsDFAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsDFAccessor "vectorbt.signals.accessors.SignalsDFAccessor") -> `pd.DataFrame.vbt.signals.*`


    
    
    >>> import pandas as pd
    >>> import vectorbt as vbt
    
    >>> # vectorbt.signals.accessors.SignalsAccessor.pos_rank
    >>> pd.Series([False, True, True, True, False]).vbt.signals.pos_rank()
    0    0
    1    1
    2    2
    3    3
    4    0
    dtype: int64
    

The accessors extend [vectorbt.generic.accessors](https://vectorbt.dev/api/generic/accessors/ "vectorbt.generic.accessors").

Note

The underlying Series/DataFrame should already be a signal series.

Input arrays should be `np.bool_`.

Grouping is only supported by the methods that accept the `group_by` argument.

Accessors do not utilize caching.

**Run for the examples below**
    
    
    >>> import vectorbt as vbt
    >>> import numpy as np
    >>> import pandas as pd
    >>> from numba import njit
    >>> from datetime import datetime
    
    >>> mask = pd.DataFrame({
    ...     'a': [True, False, False, False, False],
    ...     'b': [True, False, True, False, True],
    ...     'c': [True, True, True, False, False]
    ... }, index=pd.Index([
    ...     datetime(2020, 1, 1),
    ...     datetime(2020, 1, 2),
    ...     datetime(2020, 1, 3),
    ...     datetime(2020, 1, 4),
    ...     datetime(2020, 1, 5)
    ... ]))
    >>> mask
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False  False   True
    2020-01-03  False   True   True
    2020-01-04  False  False  False
    2020-01-05  False   True  False
    

## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [SignalsAccessor.metrics](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.metrics "vectorbt.signals.accessors.SignalsAccessor.metrics").
    
    
    >>> mask.vbt.signals.stats(column='a')
    Start                       2020-01-01 00:00:00
    End                         2020-01-05 00:00:00
    Period                          5 days 00:00:00
    Total                                         1
    Rate [%]                                     20
    First Index                 2020-01-01 00:00:00
    Last Index                  2020-01-01 00:00:00
    Norm Avg Index [-1, 1]                       -1
    Distance: Min                               NaT
    Distance: Max                               NaT
    Distance: Mean                              NaT
    Distance: Std                               NaT
    Total Partitions                              1
    Partition Rate [%]                          100
    Partition Length: Min           1 days 00:00:00
    Partition Length: Max           1 days 00:00:00
    Partition Length: Mean          1 days 00:00:00
    Partition Length: Std                       NaT
    Partition Distance: Min                     NaT
    Partition Distance: Max                     NaT
    Partition Distance: Mean                    NaT
    Partition Distance: Std                     NaT
    Name: a, dtype: object
    

We can pass another signal array to compare this array with:
    
    
    >>> mask.vbt.signals.stats(column='a', settings=dict(other=mask['b']))
    Start                       2020-01-01 00:00:00
    End                         2020-01-05 00:00:00
    Period                          5 days 00:00:00
    Total                                         1
    Rate [%]                                     20
    Total Overlapping                             1
    Overlapping Rate [%]                    33.3333
    First Index                 2020-01-01 00:00:00
    Last Index                  2020-01-01 00:00:00
    Norm Avg Index [-1, 1]                       -1
    Distance -> Other: Min          0 days 00:00:00
    Distance -> Other: Max          0 days 00:00:00
    Distance -> Other: Mean         0 days 00:00:00
    Distance -> Other: Std                      NaT
    Total Partitions                              1
    Partition Rate [%]                          100
    Partition Length: Min           1 days 00:00:00
    Partition Length: Max           1 days 00:00:00
    Partition Length: Mean          1 days 00:00:00
    Partition Length: Std                       NaT
    Partition Distance: Min                     NaT
    Partition Distance: Max                     NaT
    Partition Distance: Mean                    NaT
    Partition Distance: Std                     NaT
    Name: a, dtype: object
    

We can also return duration as a floating number rather than a timedelta:
    
    
    >>> mask.vbt.signals.stats(column='a', settings=dict(to_timedelta=False))
    Start                       2020-01-01 00:00:00
    End                         2020-01-05 00:00:00
    Period                                        5
    Total                                         1
    Rate [%]                                     20
    First Index                 2020-01-01 00:00:00
    Last Index                  2020-01-01 00:00:00
    Norm Avg Index [-1, 1]                       -1
    Distance: Min                               NaN
    Distance: Max                               NaN
    Distance: Mean                              NaN
    Distance: Std                               NaN
    Total Partitions                              1
    Partition Rate [%]                          100
    Partition Length: Min                         1
    Partition Length: Max                         1
    Partition Length: Mean                        1
    Partition Length: Std                       NaN
    Partition Distance: Min                     NaN
    Partition Distance: Max                     NaN
    Partition Distance: Mean                    NaN
    Partition Distance: Std                     NaN
    Name: a, dtype: object
    

[StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.signals.accessors.SignalsAccessor.stats") also supports (re-)grouping:
    
    
    >>> mask.vbt.signals.stats(column=0, group_by=[0, 0, 1])
    Start                       2020-01-01 00:00:00
    End                         2020-01-05 00:00:00
    Period                          5 days 00:00:00
    Total                                         4
    Rate [%]                                     40
    First Index                 2020-01-01 00:00:00
    Last Index                  2020-01-05 00:00:00
    Norm Avg Index [-1, 1]                    -0.25
    Distance: Min                   2 days 00:00:00
    Distance: Max                   2 days 00:00:00
    Distance: Mean                  2 days 00:00:00
    Distance: Std                   0 days 00:00:00
    Total Partitions                              4
    Partition Rate [%]                          100
    Partition Length: Min           1 days 00:00:00
    Partition Length: Max           1 days 00:00:00
    Partition Length: Mean          1 days 00:00:00
    Partition Length: Std           0 days 00:00:00
    Partition Distance: Min         2 days 00:00:00
    Partition Distance: Max         2 days 00:00:00
    Partition Distance: Mean        2 days 00:00:00
    Partition Distance: Std         0 days 00:00:00
    Name: 0, dtype: object
    

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [SignalsAccessor.subplots](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.subplots "vectorbt.signals.accessors.SignalsAccessor.subplots").

This class inherits subplots from [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").

* * *

## SignalsAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L218-L1702 "Jump to source")¶
    
    
    SignalsAccessor(
        obj,
        **kwargs
    )
    

Accessor on top of signal series. For both, Series and DataFrames.

Accessible through `pd.Series.vbt.signals` and `pd.DataFrame.vbt.signals`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.generic.accessors.GenericAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.generic.accessors.GenericAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.generic.accessors.GenericAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.generic.accessors.GenericAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.generic.accessors.GenericAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.generic.accessors.GenericAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.generic.accessors.GenericAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.generic.accessors.GenericAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.generic.accessors.GenericAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.generic.accessors.GenericAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.generic.accessors.GenericAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.generic.accessors.GenericAccessor.concat")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.generic.accessors.GenericAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.generic.accessors.GenericAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.generic.accessors.GenericAccessor.drop_redundant_levels")
  * [BaseAccessor.indexing_func()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.indexing_func "vectorbt.generic.accessors.GenericAccessor.indexing_func")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.generic.accessors.GenericAccessor.make_symmetric")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.generic.accessors.GenericAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.generic.accessors.GenericAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.generic.accessors.GenericAccessor.select_levels")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.generic.accessors.GenericAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.generic.accessors.GenericAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.generic.accessors.GenericAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.generic.accessors.GenericAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.generic.accessors.GenericAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.generic.accessors.GenericAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.generic.accessors.GenericAccessor.unstack_to_df")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.generic.accessors.GenericAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.generic.accessors.GenericAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.generic.accessors.GenericAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.generic.accessors.GenericAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.generic.accessors.GenericAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.generic.accessors.GenericAccessor.update_config")
  * [GenericAccessor.apply_along_axis()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_along_axis "vectorbt.generic.accessors.GenericAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_and_reduce "vectorbt.generic.accessors.GenericAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_mapping "vectorbt.generic.accessors.GenericAccessor.apply_mapping")
  * [GenericAccessor.applymap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.applymap "vectorbt.generic.accessors.GenericAccessor.applymap")
  * [GenericAccessor.barplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.barplot "vectorbt.generic.accessors.GenericAccessor.barplot")
  * [GenericAccessor.bfill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bfill "vectorbt.generic.accessors.GenericAccessor.bfill")
  * [GenericAccessor.binarize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.binarize "vectorbt.generic.accessors.GenericAccessor.binarize")
  * [GenericAccessor.boxplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.boxplot "vectorbt.generic.accessors.GenericAccessor.boxplot")
  * [GenericAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.generic.accessors.GenericAccessor.config")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.generic.accessors.GenericAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.generic.accessors.GenericAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.generic.accessors.GenericAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.generic.accessors.GenericAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.generic.accessors.GenericAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.generic.accessors.GenericAccessor.describe")
  * [GenericAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.generic.accessors.GenericAccessor.df_accessor_cls")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.generic.accessors.GenericAccessor.diff")
  * [GenericAccessor.drawdown()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdown "vectorbt.generic.accessors.GenericAccessor.drawdown")
  * [GenericAccessor.drawdowns](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdowns "vectorbt.generic.accessors.GenericAccessor.drawdowns")
  * [GenericAccessor.ewm_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_mean "vectorbt.generic.accessors.GenericAccessor.ewm_mean")
  * [GenericAccessor.ewm_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_std "vectorbt.generic.accessors.GenericAccessor.ewm_std")
  * [GenericAccessor.expanding_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_apply "vectorbt.generic.accessors.GenericAccessor.expanding_apply")
  * [GenericAccessor.expanding_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_max "vectorbt.generic.accessors.GenericAccessor.expanding_max")
  * [GenericAccessor.expanding_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_mean "vectorbt.generic.accessors.GenericAccessor.expanding_mean")
  * [GenericAccessor.expanding_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_min "vectorbt.generic.accessors.GenericAccessor.expanding_min")
  * [GenericAccessor.expanding_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_split "vectorbt.generic.accessors.GenericAccessor.expanding_split")
  * [GenericAccessor.expanding_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_std "vectorbt.generic.accessors.GenericAccessor.expanding_std")
  * [GenericAccessor.ffill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ffill "vectorbt.generic.accessors.GenericAccessor.ffill")
  * [GenericAccessor.fillna()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fillna "vectorbt.generic.accessors.GenericAccessor.fillna")
  * [GenericAccessor.filter()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.filter "vectorbt.generic.accessors.GenericAccessor.filter")
  * [GenericAccessor.get_drawdowns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_drawdowns "vectorbt.generic.accessors.GenericAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.generic.accessors.GenericAccessor.get_ranges")
  * [GenericAccessor.groupby_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.groupby_apply "vectorbt.generic.accessors.GenericAccessor.groupby_apply")
  * [GenericAccessor.histplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.histplot "vectorbt.generic.accessors.GenericAccessor.histplot")
  * [GenericAccessor.idxmax()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmax "vectorbt.generic.accessors.GenericAccessor.idxmax")
  * [GenericAccessor.idxmin()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmin "vectorbt.generic.accessors.GenericAccessor.idxmin")
  * [GenericAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.generic.accessors.GenericAccessor.iloc")
  * [GenericAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.generic.accessors.GenericAccessor.indexing_kwargs")
  * [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.generic.accessors.GenericAccessor.lineplot")
  * [GenericAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.generic.accessors.GenericAccessor.loc")
  * [GenericAccessor.mapping](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mapping "vectorbt.generic.accessors.GenericAccessor.mapping")
  * [GenericAccessor.max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.max "vectorbt.generic.accessors.GenericAccessor.max")
  * [GenericAccessor.maxabs_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.maxabs_scale "vectorbt.generic.accessors.GenericAccessor.maxabs_scale")
  * [GenericAccessor.mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mean "vectorbt.generic.accessors.GenericAccessor.mean")
  * [GenericAccessor.median()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.median "vectorbt.generic.accessors.GenericAccessor.median")
  * [GenericAccessor.min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.min "vectorbt.generic.accessors.GenericAccessor.min")
  * [GenericAccessor.minmax_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.minmax_scale "vectorbt.generic.accessors.GenericAccessor.minmax_scale")
  * [GenericAccessor.normalize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.normalize "vectorbt.generic.accessors.GenericAccessor.normalize")
  * [GenericAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.generic.accessors.GenericAccessor.obj")
  * [GenericAccessor.pct_change()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.pct_change "vectorbt.generic.accessors.GenericAccessor.pct_change")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.generic.accessors.GenericAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.generic.accessors.GenericAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.generic.accessors.GenericAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.generic.accessors.GenericAccessor.range_split")
  * [GenericAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.generic.accessors.GenericAccessor.ranges")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.generic.accessors.GenericAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.generic.accessors.GenericAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.generic.accessors.GenericAccessor.resample_apply")
  * [GenericAccessor.resolve_self()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resolve_self "vectorbt.generic.accessors.GenericAccessor.resolve_self")
  * [GenericAccessor.robust_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.robust_scale "vectorbt.generic.accessors.GenericAccessor.robust_scale")
  * [GenericAccessor.rolling_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_apply "vectorbt.generic.accessors.GenericAccessor.rolling_apply")
  * [GenericAccessor.rolling_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_max "vectorbt.generic.accessors.GenericAccessor.rolling_max")
  * [GenericAccessor.rolling_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_mean "vectorbt.generic.accessors.GenericAccessor.rolling_mean")
  * [GenericAccessor.rolling_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_min "vectorbt.generic.accessors.GenericAccessor.rolling_min")
  * [GenericAccessor.rolling_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_split "vectorbt.generic.accessors.GenericAccessor.rolling_split")
  * [GenericAccessor.rolling_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_std "vectorbt.generic.accessors.GenericAccessor.rolling_std")
  * [GenericAccessor.scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scale "vectorbt.generic.accessors.GenericAccessor.scale")
  * [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.generic.accessors.GenericAccessor.scatterplot")
  * [GenericAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.generic.accessors.GenericAccessor.self_aliases")
  * [GenericAccessor.shuffle()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.shuffle "vectorbt.generic.accessors.GenericAccessor.shuffle")
  * [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.generic.accessors.GenericAccessor.split")
  * [GenericAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.generic.accessors.GenericAccessor.sr_accessor_cls")
  * [GenericAccessor.std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.std "vectorbt.generic.accessors.GenericAccessor.std")
  * [GenericAccessor.sum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.sum "vectorbt.generic.accessors.GenericAccessor.sum")
  * [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.generic.accessors.GenericAccessor.to_mapped")
  * [GenericAccessor.to_returns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_returns "vectorbt.generic.accessors.GenericAccessor.to_returns")
  * [GenericAccessor.transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.transform "vectorbt.generic.accessors.GenericAccessor.transform")
  * [GenericAccessor.value_counts()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.value_counts "vectorbt.generic.accessors.GenericAccessor.value_counts")
  * [GenericAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.generic.accessors.GenericAccessor.wrapper")
  * [GenericAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.generic.accessors.GenericAccessor.writeable_attrs")
  * [GenericAccessor.zscore()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.zscore "vectorbt.generic.accessors.GenericAccessor.zscore")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.generic.accessors.GenericAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.generic.accessors.GenericAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.generic.accessors.GenericAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.generic.accessors.GenericAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.generic.accessors.GenericAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.accessors.GenericAccessor.plots")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.generic.accessors.GenericAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.generic.accessors.GenericAccessor.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.accessors.GenericAccessor.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.generic.accessors.GenericAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.generic.accessors.GenericAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.generic.accessors.GenericAccessor.select_one_from_obj")



**Subclasses**

  * [SignalsDFAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsDFAccessor "vectorbt.signals.accessors.SignalsDFAccessor")
  * [SignalsSRAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsSRAccessor "vectorbt.signals.accessors.SignalsSRAccessor")



* * *

### AND method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1487-L1493 "Jump to source")¶
    
    
    SignalsAccessor.AND(
        other,
        **kwargs
    )
    

Combine with `other` using logical AND.

See [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.base.accessors.BaseAccessor.combine").

* * *

### OR method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1495-L1515 "Jump to source")¶
    
    
    SignalsAccessor.OR(
        other,
        **kwargs
    )
    

Combine with `other` using logical OR.

See [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.base.accessors.BaseAccessor.combine").

**Usage**

  * Perform two OR operations and concatenate them:


    
    
    >>> ts = pd.Series([1, 2, 3, 2, 1])
    >>> mask.vbt.signals.OR([ts > 1, ts > 2], concat=True, keys=['>1', '>2'])
                                >1                   >2
                    a     b      c      a      b      c
    2020-01-01   True  True   True   True   True   True
    2020-01-02   True  True   True  False  False   True
    2020-01-03   True  True   True   True   True   True
    2020-01-04   True  True   True  False  False  False
    2020-01-05  False  True  False  False   True  False
    

* * *

### XOR method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1517-L1521 "Jump to source")¶
    
    
    SignalsAccessor.XOR(
        other,
        **kwargs
    )
    

Combine with `other` using logical XOR.

See [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.base.accessors.BaseAccessor.combine").

* * *

### between_partition_ranges method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1163-L1182 "Jump to source")¶
    
    
    SignalsAccessor.between_partition_ranges(
        group_by=None,
        attach_ts=True,
        **kwargs
    )
    

Wrap the result of [between_partition_ranges_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.between_partition_ranges_nb "vectorbt.signals.nb.between_partition_ranges_nb") with [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges").

**Usage**
    
    
    >>> mask_sr = pd.Series([True, False, False, True, False, True, True])
    >>> mask_sr.vbt.signals.between_partition_ranges().records_readable
       Range Id  Column  Start Timestamp  End Timestamp  Status
    0         0       0                0              3  Closed
    1         1       0                3              5  Closed
    

* * *

### between_ranges method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1046-L1137 "Jump to source")¶
    
    
    SignalsAccessor.between_ranges(
        other=None,
        from_other=False,
        broadcast_kwargs=None,
        group_by=None,
        attach_ts=True,
        attach_other=False,
        **kwargs
    )
    

Wrap the result of [between_ranges_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.between_ranges_nb "vectorbt.signals.nb.between_ranges_nb") with [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges").

If `other` specified, see [between_two_ranges_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.between_two_ranges_nb "vectorbt.signals.nb.between_two_ranges_nb"). Both will broadcast using [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast") and `broadcast_kwargs`.

**Usage**

  * One array:


    
    
    >>> mask_sr = pd.Series([True, False, False, True, False, True, True])
    >>> ranges = mask_sr.vbt.signals.between_ranges()
    >>> ranges
    <vectorbt.generic.ranges.Ranges at 0x7ff29ea7c7b8>
    
    >>> ranges.records_readable
       Range Id  Column  Start Timestamp  End Timestamp  Status
    0         0       0                0              3  Closed
    1         1       0                3              5  Closed
    2         2       0                5              6  Closed
    
    >>> ranges.duration.values
    array([3, 2, 1])
    

  * Two arrays, traversing the signals of the first array:


    
    
    >>> mask_sr = pd.Series([True, True, True, False, False])
    >>> mask_sr2 = pd.Series([False, False, True, False, True])
    >>> ranges = mask_sr.vbt.signals.between_ranges(other=mask_sr2)
    >>> ranges
    <vectorbt.generic.ranges.Ranges at 0x7ff29e3b80f0>
    
    >>> ranges.records_readable
       Range Id  Column  Start Timestamp  End Timestamp  Status
    0         0       0                0              2  Closed
    1         1       0                1              2  Closed
    2         2       0                2              2  Closed
    
    >>> ranges.duration.values
    array([2, 1, 0])
    

  * Two arrays, traversing the signals of the second array:


    
    
    >>> ranges = mask_sr.vbt.signals.between_ranges(other=mask_sr2, from_other=True)
    >>> ranges
    <vectorbt.generic.ranges.Ranges at 0x7ff29eccbd68>
    
    >>> ranges.records_readable
       Range Id  Column  Start Timestamp  End Timestamp  Status
    0         0       0                2              2  Closed
    1         1       0                2              4  Closed
    
    >>> ranges.duration.values
    array([0, 2])
    

* * *

### bshift method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L240-L242 "Jump to source")¶
    
    
    SignalsAccessor.bshift(
        *args,
        fill_value=False,
        **kwargs
    )
    

[GenericAccessor.bshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bshift "vectorbt.generic.accessors.GenericAccessor.bshift") with `fill_value=False`.

* * *

### clean class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L430-L462 "Jump to source")¶
    
    
    SignalsAccessor.clean(
        *args,
        entry_first=True,
        broadcast_kwargs=None,
        wrap_kwargs=None
    )
    

Clean signals.

If one array passed, see [SignalsAccessor.first()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.first "vectorbt.signals.accessors.SignalsAccessor.first"). If two arrays passed, entries and exits, see [clean_enex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.clean_enex_nb "vectorbt.signals.nb.clean_enex_nb").

* * *

### empty class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L248-L251 "Jump to source")¶
    
    
    SignalsAccessor.empty(
        *args,
        fill_value=False,
        **kwargs
    )
    

[BaseAccessor.empty()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty "vectorbt.base.accessors.BaseAccessor.empty") with `fill_value=False`.

* * *

### empty_like class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L253-L256 "Jump to source")¶
    
    
    SignalsAccessor.empty_like(
        *args,
        fill_value=False,
        **kwargs
    )
    

[BaseAccessor.empty_like()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty_like "vectorbt.base.accessors.BaseAccessor.empty_like") with `fill_value=False`.

* * *

### first method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1327-L1330 "Jump to source")¶
    
    
    SignalsAccessor.first(
        wrap_kwargs=None,
        **kwargs
    )
    

Select signals that satisfy the condition `pos_rank == 0`.

* * *

### from_nth method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1337-L1340 "Jump to source")¶
    
    
    SignalsAccessor.from_nth(
        n,
        wrap_kwargs=None,
        **kwargs
    )
    

Select signals that satisfy the condition `pos_rank >= n`.

* * *

### fshift method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L244-L246 "Jump to source")¶
    
    
    SignalsAccessor.fshift(
        *args,
        fill_value=False,
        **kwargs
    )
    

[GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.generic.accessors.GenericAccessor.fshift") with `fill_value=False`.

* * *

### generate class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L260-L301 "Jump to source")¶
    
    
    SignalsAccessor.generate(
        shape,
        choice_func_nb,
        *args,
        pick_first=False,
        **kwargs
    )
    

See [generate_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_nb "vectorbt.signals.nb.generate_nb").

`**kwargs` will be passed to pandas constructor.

**Usage**

  * Generate random signals manually:


    
    
    >>> @njit
    ... def choice_func_nb(from_i, to_i, col):
    ...     return col + from_i
    
    >>> pd.DataFrame.vbt.signals.generate((5, 3),
    ...     choice_func_nb, index=mask.index, columns=mask.columns)
                    a      b      c
    2020-01-01   True  False  False
    2020-01-02  False   True  False
    2020-01-03  False  False   True
    2020-01-04  False  False  False
    2020-01-05  False  False  False
    

* * *

### generate_both class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L303-L386 "Jump to source")¶
    
    
    SignalsAccessor.generate_both(
        shape,
        entry_choice_func_nb=None,
        entry_args=None,
        exit_choice_func_nb=None,
        exit_args=None,
        entry_wait=1,
        exit_wait=1,
        entry_pick_first=True,
        exit_pick_first=True,
        **kwargs
    )
    

See [generate_enex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_enex_nb "vectorbt.signals.nb.generate_enex_nb").

`**kwargs` will be passed to pandas constructor.

**Usage**

  * Generate entry and exit signals one after another. Each column increment the number of ticks to wait before placing the exit signal.


    
    
    >>> @njit
    ... def entry_choice_func_nb(from_i, to_i, col, temp_idx_arr):
    ...     temp_idx_arr[0] = from_i
    ...     return temp_idx_arr[:1]  # array with one signal
    
    >>> @njit
    ... def exit_choice_func_nb(from_i, to_i, col, temp_idx_arr):
    ...     wait = col
    ...     temp_idx_arr[0] = from_i + wait
    ...     if temp_idx_arr[0] < to_i:
    ...         return temp_idx_arr[:1]  # array with one signal
    ...     return temp_idx_arr[:0]  # empty array
    
    >>> temp_idx_arr = np.empty((1,), dtype=np.int64)  # reuse memory
    >>> en, ex = pd.DataFrame.vbt.signals.generate_both(
    ...     (5, 3),
    ...     entry_choice_func_nb, (temp_idx_arr,),
    ...     exit_choice_func_nb, (temp_idx_arr,),
    ...     index=mask.index, columns=mask.columns)
    >>> en
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False  False  False
    2020-01-03   True  False  False
    2020-01-04  False   True  False
    2020-01-05   True  False   True
    >>> ex
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True  False  False
    2020-01-03  False   True  False
    2020-01-04   True  False   True
    2020-01-05  False  False  False
    

* * *

### generate_exits method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L388-L426 "Jump to source")¶
    
    
    SignalsAccessor.generate_exits(
        exit_choice_func_nb,
        *args,
        wait=1,
        until_next=True,
        skip_until_exit=False,
        pick_first=False,
        wrap_kwargs=None
    )
    

See [generate_ex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_ex_nb "vectorbt.signals.nb.generate_ex_nb").

**Usage**

  * Fill all space after signals in `mask`:


    
    
    >>> @njit
    ... def exit_choice_func_nb(from_i, to_i, col, temp_range):
    ...     return temp_range[from_i:to_i]
    
    >>> temp_range = np.arange(mask.shape[0])  # reuse memory
    >>> mask.vbt.signals.generate_exits(exit_choice_func_nb, temp_range)
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True  False
    2020-01-03   True  False  False
    2020-01-04   True   True   True
    2020-01-05   True  False   True
    

* * *

### generate_ohlc_stop_exits method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L789-L1042 "Jump to source")¶
    
    
    SignalsAccessor.generate_ohlc_stop_exits(
        open,
        high=None,
        low=None,
        close=None,
        is_open_safe=True,
        out_dict=None,
        sl_stop=nan,
        sl_trail=False,
        tp_stop=nan,
        reverse=False,
        entry_wait=1,
        exit_wait=1,
        until_next=True,
        skip_until_exit=False,
        pick_first=True,
        chain=False,
        broadcast_kwargs=None,
        wrap_kwargs=None
    )
    

Generate exits based on when the price hits (trailing) stop loss or take profit.

Hint

This function is meant for signal analysis. For backtesting, consider using the stop logic integrated into [Portfolio.from_signals()](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.from_signals "vectorbt.portfolio.base.Portfolio.from_signals").

If any of `high`, `low` or `close` is None, it will be set to `open`.

Use `out_dict` as a dict to pass `stop_price` and `stop_type` arrays. You can also set `out_dict` to {} to produce these arrays automatically and still have access to them.

For arguments, see [ohlc_stop_choice_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.ohlc_stop_choice_nb "vectorbt.signals.nb.ohlc_stop_choice_nb"). If `chain` is True, see [generate_ohlc_stop_enex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_ohlc_stop_enex_nb "vectorbt.signals.nb.generate_ohlc_stop_enex_nb"). Otherwise, see [generate_ohlc_stop_ex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_ohlc_stop_ex_nb "vectorbt.signals.nb.generate_ohlc_stop_ex_nb").

All array-like arguments including stops and `out_dict` will broadcast using [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast") and `broadcast_kwargs`.

For arguments, see [ohlc_stop_choice_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.ohlc_stop_choice_nb "vectorbt.signals.nb.ohlc_stop_choice_nb").

Note

`open` isn't necessarily open price, but can be any entry price (even previous close). Stop price is calculated based solely on the entry price.

Hint

Default arguments will generate an exit signal strictly between two entry signals. If both entry signals are too close to each other, no exit will be generated.

To ignore all entries that come between an entry and its exit, set `until_next` to False and `skip_until_exit` to True.

To remove all entries that come between an entry and its exit, set `chain` to True. This will return two arrays: new entries and exits.

**Usage**

  * The same example as under [generate_ohlc_stop_ex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_ohlc_stop_ex_nb "vectorbt.signals.nb.generate_ohlc_stop_ex_nb"):


    
    
    >>> from vectorbt.signals.enums import StopType
    
    >>> price = pd.DataFrame({
    ...     'open': [10, 11, 12, 11, 10],
    ...     'high': [11, 12, 13, 12, 11],
    ...     'low': [9, 10, 11, 10, 9],
    ...     'close': [10, 11, 12, 11, 10]
    ... })
    >>> out_dict = {}
    >>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
    ...     price['open'], price['high'], price['low'], price['close'],
    ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict)
    >>> exits
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True  False
    2020-01-03  False  False  False
    2020-01-04  False   True   True
    2020-01-05  False  False  False
    
    >>> out_dict['stop_price']
                   a     b     c
    2020-01-01   NaN   NaN   NaN
    2020-01-02  11.0  11.0   NaN
    2020-01-03   NaN   NaN   NaN
    2020-01-04   NaN  10.8  10.8
    2020-01-05   NaN   NaN   NaN
    
    >>> out_dict['stop_type'].vbt(mapping=StopType).apply_mapping()
                         a           b          c
    2020-01-01        None        None       None
    2020-01-02  TakeProfit  TakeProfit       None
    2020-01-03        None        None       None
    2020-01-04        None   TrailStop  TrailStop
    2020-01-05        None        None       None
    

Notice how the first two entry signals in the third column have no exit signal - there is no room between them for an exit signal.

  * To find an exit for the first entry and ignore all entries that are in-between them, we can pass `until_next=False` and `skip_until_exit=True`:


    
    
    >>> out_dict = {}
    >>> exits = mask.vbt.signals.generate_ohlc_stop_exits(
    ...     price['open'], price['high'], price['low'], price['close'],
    ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict,
    ...     until_next=False, skip_until_exit=True)
    >>> exits
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True   True
    2020-01-03  False  False  False
    2020-01-04  False   True   True
    2020-01-05  False  False  False
    
    >>> out_dict['stop_price']
    2020-01-01   NaN   NaN   NaN
    2020-01-02  11.0  11.0  11.0
    2020-01-03   NaN   NaN   NaN
    2020-01-04   NaN  10.8  10.8
    2020-01-05   NaN   NaN   NaN
    
    >>> out_dict['stop_type'].vbt(mapping=StopType).apply_mapping()
                         a           b           c
    2020-01-01        None        None        None
    2020-01-02  TakeProfit  TakeProfit  TakeProfit
    2020-01-03        None        None        None
    2020-01-04        None   TrailStop   TrailStop
    2020-01-05        None        None        None
    

Now, the first signal in the third column gets executed regardless of the entries that come next, which is very similar to the logic that is implemented in [Portfolio.from_signals()](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.from_signals "vectorbt.portfolio.base.Portfolio.from_signals").

  * To automatically remove all ignored entry signals, pass `chain=True`. This will return a new entries array:


    
    
    >>> out_dict = {}
    >>> new_entries, exits = mask.vbt.signals.generate_ohlc_stop_exits(
    ...     price['open'], price['high'], price['low'], price['close'],
    ...     sl_stop=0.1, sl_trail=True, tp_stop=0.1, out_dict=out_dict,
    ...     chain=True)
    >>> new_entries
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False  False  False  << removed entry in the third column
    2020-01-03  False   True   True
    2020-01-04  False  False  False
    2020-01-05  False   True  False
    >>> exits
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True   True
    2020-01-03  False  False  False
    2020-01-04  False   True   True
    2020-01-05  False  False  False
    

Warning

The last two examples above make entries dependent upon exits - this makes only sense if you have no other exit arrays to combine this stop exit array with.

* * *

### generate_random class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L466-L533 "Jump to source")¶
    
    
    SignalsAccessor.generate_random(
        shape,
        n=None,
        prob=None,
        pick_first=False,
        seed=None,
        **kwargs
    )
    

Generate signals randomly.

If `n` is set, see [generate_rand_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_nb "vectorbt.signals.nb.generate_rand_nb"). If `prob` is set, see [generate_rand_by_prob_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_by_prob_nb "vectorbt.signals.nb.generate_rand_by_prob_nb").

`n` should be either a scalar or an array that will broadcast to the number of columns. `prob` should be either a single number or an array that will broadcast to match `shape`. `**kwargs` will be passed to pandas constructor.

**Usage**

  * For each column, generate a variable number of signals:


    
    
    >>> pd.DataFrame.vbt.signals.generate_random((5, 3), n=[0, 1, 2],
    ...     seed=42, index=mask.index, columns=mask.columns)
                    a      b      c
    2020-01-01  False  False   True
    2020-01-02  False  False   True
    2020-01-03  False  False  False
    2020-01-04  False   True  False
    2020-01-05  False  False  False
    

  * For each column and time step, pick a signal with 50% probability:


    
    
    >>> pd.DataFrame.vbt.signals.generate_random((5, 3), prob=0.5,
    ...     seed=42, index=mask.index, columns=mask.columns)
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False   True  False
    2020-01-03  False  False  False
    2020-01-04  False  False   True
    2020-01-05   True  False   True
    

* * *

### generate_random_both class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L537-L634 "Jump to source")¶
    
    
    SignalsAccessor.generate_random_both(
        shape,
        n=None,
        entry_prob=None,
        exit_prob=None,
        seed=None,
        entry_wait=1,
        exit_wait=1,
        entry_pick_first=True,
        exit_pick_first=True,
        **kwargs
    )
    

Generate chain of entry and exit signals randomly.

If `n` is set, see [generate_rand_enex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_enex_nb "vectorbt.signals.nb.generate_rand_enex_nb"). If `entry_prob` and `exit_prob` are set, see [generate_rand_enex_by_prob_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_enex_by_prob_nb "vectorbt.signals.nb.generate_rand_enex_by_prob_nb").

For arguments, see [SignalsAccessor.generate_random()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random "vectorbt.signals.accessors.SignalsAccessor.generate_random").

**Usage**

  * For each column, generate two entries and exits randomly:


    
    
    >>> en, ex = pd.DataFrame.vbt.signals.generate_random_both(
    ...     (5, 3), n=2, seed=42, index=mask.index, columns=mask.columns)
    >>> en
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False  False  False
    2020-01-03   True   True  False
    2020-01-04  False  False   True
    2020-01-05  False  False  False
    >>> ex
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True   True
    2020-01-03  False  False  False
    2020-01-04  False   True  False
    2020-01-05   True  False   True
    

  * For each column and time step, pick entry with 50% probability and exit right after:


    
    
    >>> en, ex = pd.DataFrame.vbt.signals.generate_random_both(
    ...     (5, 3), entry_prob=0.5, exit_prob=1.,
    ...     seed=42, index=mask.index, columns=mask.columns)
    >>> en
                    a      b      c
    2020-01-01   True   True   True
    2020-01-02  False  False  False
    2020-01-03  False  False  False
    2020-01-04  False  False   True
    2020-01-05   True  False  False
    >>> ex
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True   True  False
    2020-01-03  False  False   True
    2020-01-04  False   True  False
    2020-01-05   True  False   True
    

* * *

### generate_random_exits method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L636-L692 "Jump to source")¶
    
    
    SignalsAccessor.generate_random_exits(
        prob=None,
        seed=None,
        wait=1,
        until_next=True,
        skip_until_exit=False,
        wrap_kwargs=None
    )
    

Generate exit signals randomly.

If `prob` is None, see [generate_rand_ex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_ex_nb "vectorbt.signals.nb.generate_rand_ex_nb"). Otherwise, see [generate_rand_ex_by_prob_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_rand_ex_by_prob_nb "vectorbt.signals.nb.generate_rand_ex_by_prob_nb").

**Usage**

  * After each entry in `mask`, generate exactly one exit:


    
    
    >>> mask.vbt.signals.generate_random_exits(seed=42)
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02  False   True  False
    2020-01-03   True  False  False
    2020-01-04  False   True  False
    2020-01-05  False  False   True
    

  * After each entry in `mask` and at each time step, generate exit with 50% probability:


    
    
    >>> mask.vbt.signals.generate_random_exits(prob=0.5, seed=42)
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02   True  False  False
    2020-01-03  False  False  False
    2020-01-04  False  False  False
    2020-01-05  False  False   True
    

* * *

### generate_stop_exits method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L694-L787 "Jump to source")¶
    
    
    SignalsAccessor.generate_stop_exits(
        ts,
        stop,
        trailing=False,
        entry_wait=1,
        exit_wait=1,
        until_next=True,
        skip_until_exit=False,
        pick_first=True,
        chain=False,
        broadcast_kwargs=None,
        wrap_kwargs=None
    )
    

Generate exits based on when `ts` hits the stop.

For arguments, see [stop_choice_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.stop_choice_nb "vectorbt.signals.nb.stop_choice_nb"). If `chain` is True, see [generate_stop_enex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_stop_enex_nb "vectorbt.signals.nb.generate_stop_enex_nb"). Otherwise, see [generate_stop_ex_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.generate_stop_ex_nb "vectorbt.signals.nb.generate_stop_ex_nb").

Arguments `entries`, `ts` and `stop` will broadcast using [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast") and `broadcast_kwargs`.

For arguments, see [stop_choice_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.stop_choice_nb "vectorbt.signals.nb.stop_choice_nb").

Hint

Default arguments will generate an exit signal strictly between two entry signals. If both entry signals are too close to each other, no exit will be generated.

To ignore all entries that come between an entry and its exit, set `until_next` to False and `skip_until_exit` to True.

To remove all entries that come between an entry and its exit, set `chain` to True. This will return two arrays: new entries and exits.

**Usage**
    
    
    >>> ts = pd.Series([1, 2, 3, 2, 1])
    
    >>> # stop loss
    >>> mask.vbt.signals.generate_stop_exits(ts, -0.1)
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02  False  False  False
    2020-01-03  False  False  False
    2020-01-04  False   True   True
    2020-01-05  False  False  False
    
    >>> # trailing stop loss
    >>> mask.vbt.signals.generate_stop_exits(ts, -0.1, trailing=True)
                    a      b      c
    2020-01-01  False  False  False
    2020-01-02  False  False  False
    2020-01-03  False  False  False
    2020-01-04   True   True   True
    2020-01-05  False  False  False
    

* * *

### index_mapped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1440-L1455 "Jump to source")¶
    
    
    SignalsAccessor.index_mapped(
        group_by=None,
        **kwargs
    )
    

Get a mapped array of indices.

See [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.generic.accessors.GenericAccessor.to_mapped").

Only True values will be considered.

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py "Jump to source")¶

Metrics supported by [SignalsAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor "vectorbt.signals.accessors.SignalsAccessor").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3eb60>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3ec00>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3eca0>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "tags": "wrapper"
        },
        "total": {
            "title": "Total",
            "calc_func": "total",
            "tags": "signals"
        },
        "rate": {
            "title": "Rate [%]",
            "calc_func": "rate",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3ed40>",
            "tags": "signals"
        },
        "total_overlapping": {
            "title": "Total Overlapping",
            "calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3ede0>",
            "check_silent_has_other": true,
            "tags": [
                "signals",
                "other"
            ]
        },
        "overlapping_rate": {
            "title": "Overlapping Rate [%]",
            "calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3ee80>",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3ef20>",
            "check_silent_has_other": true,
            "tags": [
                "signals",
                "other"
            ]
        },
        "first_index": {
            "title": "First Index",
            "calc_func": "nth_index",
            "n": 0,
            "return_labels": true,
            "tags": [
                "signals",
                "index"
            ]
        },
        "last_index": {
            "title": "Last Index",
            "calc_func": "nth_index",
            "n": -1,
            "return_labels": true,
            "tags": [
                "signals",
                "index"
            ]
        },
        "norm_avg_index": {
            "title": "Norm Avg Index [-1, 1]",
            "calc_func": "norm_avg_index",
            "tags": [
                "signals",
                "index"
            ]
        },
        "distance": {
            "title": "RepEval(expression=\"f'Distance {\"<-\" if from_other else \"->\"} {other_name}' if other is not None else 'Distance'\", mapping={})",
            "calc_func": "between_ranges.duration",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3efc0>",
            "apply_to_timedelta": true,
            "tags": "RepEval(expression=\"['signals', 'distance', 'other'] if other is not None else ['signals', 'distance']\", mapping={})"
        },
        "total_partitions": {
            "title": "Total Partitions",
            "calc_func": "total_partitions",
            "tags": [
                "signals",
                "partitions"
            ]
        },
        "partition_rate": {
            "title": "Partition Rate [%]",
            "calc_func": "partition_rate",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3f060>",
            "tags": [
                "signals",
                "partitions"
            ]
        },
        "partition_len": {
            "title": "Partition Length",
            "calc_func": "partition_ranges.duration",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3f100>",
            "apply_to_timedelta": true,
            "tags": [
                "signals",
                "partitions",
                "distance"
            ]
        },
        "partition_distance": {
            "title": "Partition Distance",
            "calc_func": "between_partition_ranges.duration",
            "post_calc_func": "<function SignalsAccessor.<lambda> at 0x7f957ed3f1a0>",
            "apply_to_timedelta": true,
            "tags": [
                "signals",
                "partitions",
                "distance"
            ]
        }
    })
    

Returns `SignalsAccessor._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `SignalsAccessor._metrics`.

* * *

### norm_avg_index method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1398-L1438 "Jump to source")¶
    
    
    SignalsAccessor.norm_avg_index(
        group_by=None,
        wrap_kwargs=None
    )
    

See [norm_avg_index_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.norm_avg_index_nb "vectorbt.signals.nb.norm_avg_index_nb").

Normalized average index measures the average signal location relative to the middle of the column. This way, we can quickly see where the majority of signals are located.

Common values are:

  * -1.0: only the first signal is set
  * 1.0: only the last signal is set
  * 0.0: symmetric distribution around the middle
  * [-1.0, 0.0): average signal is on the left
  * (0.0, 1.0]: average signal is on the right



**Usage**
    
    
    >>> pd.Series([True, False, False, False]).vbt.signals.norm_avg_index()
    -1.0
    
    >>> pd.Series([False, False, False, True]).vbt.signals.norm_avg_index()
    1.0
    
    >>> pd.Series([True, False, False, True]).vbt.signals.norm_avg_index()
    0.0
    

* * *

### nth method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1332-L1335 "Jump to source")¶
    
    
    SignalsAccessor.nth(
        n,
        wrap_kwargs=None,
        **kwargs
    )
    

Select signals that satisfy the condition `pos_rank == n`.

* * *

### nth_index method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1356-L1396 "Jump to source")¶
    
    
    SignalsAccessor.nth_index(
        n,
        return_labels=True,
        group_by=None,
        wrap_kwargs=None
    )
    

See [nth_index_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.nth_index_nb "vectorbt.signals.nb.nth_index_nb").

**Usage**
    
    
    >>> mask.vbt.signals.nth_index(0)
    a   2020-01-01
    b   2020-01-01
    c   2020-01-01
    Name: nth_index, dtype: datetime64[ns]
    
    >>> mask.vbt.signals.nth_index(2)
    a          NaT
    b   2020-01-05
    c   2020-01-03
    Name: nth_index, dtype: datetime64[ns]
    
    >>> mask.vbt.signals.nth_index(-1)
    a   2020-01-01
    b   2020-01-05
    c   2020-01-03
    Name: nth_index, dtype: datetime64[ns]
    
    >>> mask.vbt.signals.nth_index(-1, group_by=True)
    Timestamp('2020-01-05 00:00:00')
    

* * *

### partition_pos_rank method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1286-L1325 "Jump to source")¶
    
    
    SignalsAccessor.partition_pos_rank(
        **kwargs
    )
    

Get partition position ranks.

Uses [SignalsAccessor.rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rank "vectorbt.signals.accessors.SignalsAccessor.rank") with [part_pos_rank_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.part_pos_rank_nb "vectorbt.signals.nb.part_pos_rank_nb").

**Usage**

  * Rank each partition of True values in `mask`:


    
    
    >>> mask.vbt.signals.partition_pos_rank()
                a  b  c
    2020-01-01  0  0  0
    2020-01-02 -1 -1  0
    2020-01-03 -1  1  0
    2020-01-04 -1 -1 -1
    2020-01-05 -1  2 -1
    
    >>> mask.vbt.signals.partition_pos_rank(after_false=True)
                a  b  c
    2020-01-01 -1 -1 -1
    2020-01-02 -1 -1 -1
    2020-01-03 -1  0 -1
    2020-01-04 -1 -1 -1
    2020-01-05 -1  1 -1
    
    >>> mask.vbt.signals.partition_pos_rank(reset_by=mask)
                a  b  c
    2020-01-01  0  0  0
    2020-01-02 -1 -1  0
    2020-01-03 -1  0  0
    2020-01-04 -1 -1 -1
    2020-01-05 -1  0 -1
    

* * *

### partition_pos_rank_mapped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1348-L1352 "Jump to source")¶
    
    
    SignalsAccessor.partition_pos_rank_mapped(
        group_by=None,
        **kwargs
    )
    

Get a mapped array of partition position ranks.

See [SignalsAccessor.partition_pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank").

* * *

### partition_ranges method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1139-L1161 "Jump to source")¶
    
    
    SignalsAccessor.partition_ranges(
        group_by=None,
        attach_ts=True,
        **kwargs
    )
    

Wrap the result of [partition_ranges_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.partition_ranges_nb "vectorbt.signals.nb.partition_ranges_nb") with [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges").

If `use_end_idxs` is True, uses the index of the last signal in each partition as `idx_arr`. Otherwise, uses the index of the first signal.

**Usage**
    
    
    >>> mask_sr = pd.Series([True, True, True, False, True, True])
    >>> mask_sr.vbt.signals.partition_ranges().records_readable
       Range Id  Column  Start Timestamp  End Timestamp  Status
    0         0       0                0              3  Closed
    1         1       0                4              5    Open
    

* * *

### partition_rate method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1477-L1483 "Jump to source")¶
    
    
    SignalsAccessor.partition_rate(
        wrap_kwargs=None,
        group_by=None,
        **kwargs
    )
    

[SignalsAccessor.total_partitions()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total_partitions "vectorbt.signals.accessors.SignalsAccessor.total_partitions") divided by [SignalsAccessor.total()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total "vectorbt.signals.accessors.SignalsAccessor.total") in each column/group.

* * *

### plot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1664-L1684 "Jump to source")¶
    
    
    SignalsAccessor.plot(
        yref='y',
        **kwargs
    )
    

Plot signals.

**Args**

**`yref`** : `str`
    Y coordinate axis.
**`**kwargs`**
    Keyword arguments passed to [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.generic.accessors.GenericAccessor.lineplot").

**Usage**
    
    
    >>> mask[['a', 'c']].vbt.signals.plot()
    

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1686-L1698 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.signals.accessors.SignalsAccessor.plots").

Merges [GenericAccessor.plots_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plots_defaults "vectorbt.generic.accessors.GenericAccessor.plots_defaults") and `signals.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### pos_rank method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1236-L1284 "Jump to source")¶
    
    
    SignalsAccessor.pos_rank(
        allow_gaps=False,
        **kwargs
    )
    

Get signal position ranks.

Uses [SignalsAccessor.rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rank "vectorbt.signals.accessors.SignalsAccessor.rank") with [sig_pos_rank_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.sig_pos_rank_nb "vectorbt.signals.nb.sig_pos_rank_nb").

**Usage**

  * Rank each True value in each partition in `mask`:


    
    
    >>> mask.vbt.signals.pos_rank()
                a  b  c
    2020-01-01  0  0  0
    2020-01-02 -1 -1  1
    2020-01-03 -1  0  2
    2020-01-04 -1 -1 -1
    2020-01-05 -1  0 -1
    
    >>> mask.vbt.signals.pos_rank(after_false=True)
                a  b  c
    2020-01-01 -1 -1 -1
    2020-01-02 -1 -1 -1
    2020-01-03 -1  0 -1
    2020-01-04 -1 -1 -1
    2020-01-05 -1  0 -1
    
    >>> mask.vbt.signals.pos_rank(allow_gaps=True)
                a  b  c
    2020-01-01  0  0  0
    2020-01-02 -1 -1  1
    2020-01-03 -1  1  2
    2020-01-04 -1 -1 -1
    2020-01-05 -1  2 -1
    
    >>> mask.vbt.signals.pos_rank(reset_by=~mask, allow_gaps=True)
                a  b  c
    2020-01-01  0  0  0
    2020-01-02 -1 -1  1
    2020-01-03 -1  0  2
    2020-01-04 -1 -1 -1
    2020-01-05 -1  0 -1
    

* * *

### pos_rank_mapped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1342-L1346 "Jump to source")¶
    
    
    SignalsAccessor.pos_rank_mapped(
        group_by=None,
        **kwargs
    )
    

Get a mapped array of signal position ranks.

See [SignalsAccessor.pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.pos_rank "vectorbt.signals.accessors.SignalsAccessor.pos_rank").

* * *

### rank method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1186-L1234 "Jump to source")¶
    
    
    SignalsAccessor.rank(
        rank_func_nb,
        *args,
        prepare_func=None,
        reset_by=None,
        after_false=False,
        broadcast_kwargs=None,
        wrap_kwargs=None,
        as_mapped=False,
        **kwargs
    )
    

See [rank_nb()](https://vectorbt.dev/api/signals/nb/#vectorbt.signals.nb.rank_nb "vectorbt.signals.nb.rank_nb").

Will broadcast with `reset_by` using [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast") and `broadcast_kwargs`.

Use `prepare_func` to prepare further arguments to be passed before `*args`, such as temporary arrays. It should take both broadcasted arrays (`reset_by` can be None) and return a tuple.

Set `as_mapped` to True to return an instance of [MappedArray](https://vectorbt.dev/api/records/mapped_array/#vectorbt.records.mapped_array.MappedArray "vectorbt.records.mapped_array.MappedArray").

* * *

### rate method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1463-L1469 "Jump to source")¶
    
    
    SignalsAccessor.rate(
        wrap_kwargs=None,
        group_by=None,
        **kwargs
    )
    

[SignalsAccessor.total()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total "vectorbt.signals.accessors.SignalsAccessor.total") divided by the total index length in each column/group.

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1525-L1537 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.signals.accessors.SignalsAccessor.stats").

Merges [GenericAccessor.stats_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.stats_defaults "vectorbt.generic.accessors.GenericAccessor.stats_defaults") and `signals.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py "Jump to source")¶

Subplots supported by [SignalsAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor "vectorbt.signals.accessors.SignalsAccessor").
    
    
    Config({
        "plot": {
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "pass_trace_names": false,
            "tags": "generic"
        }
    })
    

Returns `SignalsAccessor._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `SignalsAccessor._subplots`.

* * *

### total method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1457-L1461 "Jump to source")¶
    
    
    SignalsAccessor.total(
        wrap_kwargs=None,
        group_by=None
    )
    

Total number of True values in each column/group.

* * *

### total_partitions method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1471-L1475 "Jump to source")¶
    
    
    SignalsAccessor.total_partitions(
        wrap_kwargs=None,
        group_by=None,
        **kwargs
    )
    

Total number of partitions of True values in each column/group.

* * *

## SignalsDFAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1806-L1814 "Jump to source")¶
    
    
    SignalsDFAccessor(
        obj,
        **kwargs
    )
    

Accessor on top of signal series. For DataFrames only.

Accessible through `pd.DataFrame.vbt.signals`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [BaseDFAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseDFAccessor "vectorbt.base.accessors.BaseDFAccessor")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor")
  * [GenericDFAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor "vectorbt.generic.accessors.GenericDFAccessor")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [SignalsAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor "vectorbt.signals.accessors.SignalsAccessor")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.signals.accessors.SignalsAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.signals.accessors.SignalsAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.signals.accessors.SignalsAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.signals.accessors.SignalsAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.signals.accessors.SignalsAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.signals.accessors.SignalsAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.signals.accessors.SignalsAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.signals.accessors.SignalsAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.signals.accessors.SignalsAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.signals.accessors.SignalsAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.signals.accessors.SignalsAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.signals.accessors.SignalsAccessor.concat")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.signals.accessors.SignalsAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.signals.accessors.SignalsAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.signals.accessors.SignalsAccessor.drop_redundant_levels")
  * [BaseAccessor.indexing_func()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.indexing_func "vectorbt.signals.accessors.SignalsAccessor.indexing_func")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.signals.accessors.SignalsAccessor.make_symmetric")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.signals.accessors.SignalsAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.signals.accessors.SignalsAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.signals.accessors.SignalsAccessor.select_levels")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.signals.accessors.SignalsAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.signals.accessors.SignalsAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.signals.accessors.SignalsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.signals.accessors.SignalsAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.signals.accessors.SignalsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.signals.accessors.SignalsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.signals.accessors.SignalsAccessor.unstack_to_df")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.signals.accessors.SignalsAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.signals.accessors.SignalsAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.signals.accessors.SignalsAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.signals.accessors.SignalsAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.signals.accessors.SignalsAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.signals.accessors.SignalsAccessor.update_config")
  * [GenericAccessor.apply_along_axis()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_along_axis "vectorbt.signals.accessors.SignalsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_and_reduce "vectorbt.signals.accessors.SignalsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_mapping "vectorbt.signals.accessors.SignalsAccessor.apply_mapping")
  * [GenericAccessor.applymap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.applymap "vectorbt.signals.accessors.SignalsAccessor.applymap")
  * [GenericAccessor.barplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.barplot "vectorbt.signals.accessors.SignalsAccessor.barplot")
  * [GenericAccessor.bfill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bfill "vectorbt.signals.accessors.SignalsAccessor.bfill")
  * [GenericAccessor.binarize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.binarize "vectorbt.signals.accessors.SignalsAccessor.binarize")
  * [GenericAccessor.boxplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.boxplot "vectorbt.signals.accessors.SignalsAccessor.boxplot")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.signals.accessors.SignalsAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.signals.accessors.SignalsAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.signals.accessors.SignalsAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.signals.accessors.SignalsAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.signals.accessors.SignalsAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.signals.accessors.SignalsAccessor.describe")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.signals.accessors.SignalsAccessor.diff")
  * [GenericAccessor.drawdown()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdown "vectorbt.signals.accessors.SignalsAccessor.drawdown")
  * [GenericAccessor.ewm_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_mean "vectorbt.signals.accessors.SignalsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_std "vectorbt.signals.accessors.SignalsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_apply "vectorbt.signals.accessors.SignalsAccessor.expanding_apply")
  * [GenericAccessor.expanding_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_max "vectorbt.signals.accessors.SignalsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_mean "vectorbt.signals.accessors.SignalsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_min "vectorbt.signals.accessors.SignalsAccessor.expanding_min")
  * [GenericAccessor.expanding_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_split "vectorbt.signals.accessors.SignalsAccessor.expanding_split")
  * [GenericAccessor.expanding_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_std "vectorbt.signals.accessors.SignalsAccessor.expanding_std")
  * [GenericAccessor.ffill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ffill "vectorbt.signals.accessors.SignalsAccessor.ffill")
  * [GenericAccessor.fillna()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fillna "vectorbt.signals.accessors.SignalsAccessor.fillna")
  * [GenericAccessor.filter()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.filter "vectorbt.signals.accessors.SignalsAccessor.filter")
  * [GenericAccessor.get_drawdowns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_drawdowns "vectorbt.signals.accessors.SignalsAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.signals.accessors.SignalsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.groupby_apply "vectorbt.signals.accessors.SignalsAccessor.groupby_apply")
  * [GenericAccessor.histplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.histplot "vectorbt.signals.accessors.SignalsAccessor.histplot")
  * [GenericAccessor.idxmax()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmax "vectorbt.signals.accessors.SignalsAccessor.idxmax")
  * [GenericAccessor.idxmin()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmin "vectorbt.signals.accessors.SignalsAccessor.idxmin")
  * [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.signals.accessors.SignalsAccessor.lineplot")
  * [GenericAccessor.max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.max "vectorbt.signals.accessors.SignalsAccessor.max")
  * [GenericAccessor.maxabs_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.maxabs_scale "vectorbt.signals.accessors.SignalsAccessor.maxabs_scale")
  * [GenericAccessor.mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mean "vectorbt.signals.accessors.SignalsAccessor.mean")
  * [GenericAccessor.median()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.median "vectorbt.signals.accessors.SignalsAccessor.median")
  * [GenericAccessor.min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.min "vectorbt.signals.accessors.SignalsAccessor.min")
  * [GenericAccessor.minmax_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.minmax_scale "vectorbt.signals.accessors.SignalsAccessor.minmax_scale")
  * [GenericAccessor.normalize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.normalize "vectorbt.signals.accessors.SignalsAccessor.normalize")
  * [GenericAccessor.pct_change()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.pct_change "vectorbt.signals.accessors.SignalsAccessor.pct_change")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.signals.accessors.SignalsAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.signals.accessors.SignalsAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.signals.accessors.SignalsAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.signals.accessors.SignalsAccessor.range_split")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.signals.accessors.SignalsAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.signals.accessors.SignalsAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.signals.accessors.SignalsAccessor.resample_apply")
  * [GenericAccessor.resolve_self()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resolve_self "vectorbt.signals.accessors.SignalsAccessor.resolve_self")
  * [GenericAccessor.robust_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.robust_scale "vectorbt.signals.accessors.SignalsAccessor.robust_scale")
  * [GenericAccessor.rolling_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_apply "vectorbt.signals.accessors.SignalsAccessor.rolling_apply")
  * [GenericAccessor.rolling_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_max "vectorbt.signals.accessors.SignalsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_mean "vectorbt.signals.accessors.SignalsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_min "vectorbt.signals.accessors.SignalsAccessor.rolling_min")
  * [GenericAccessor.rolling_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_split "vectorbt.signals.accessors.SignalsAccessor.rolling_split")
  * [GenericAccessor.rolling_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_std "vectorbt.signals.accessors.SignalsAccessor.rolling_std")
  * [GenericAccessor.scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scale "vectorbt.signals.accessors.SignalsAccessor.scale")
  * [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.signals.accessors.SignalsAccessor.scatterplot")
  * [GenericAccessor.shuffle()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.shuffle "vectorbt.signals.accessors.SignalsAccessor.shuffle")
  * [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.signals.accessors.SignalsAccessor.split")
  * [GenericAccessor.std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.std "vectorbt.signals.accessors.SignalsAccessor.std")
  * [GenericAccessor.sum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.sum "vectorbt.signals.accessors.SignalsAccessor.sum")
  * [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.signals.accessors.SignalsAccessor.to_mapped")
  * [GenericAccessor.to_returns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_returns "vectorbt.signals.accessors.SignalsAccessor.to_returns")
  * [GenericAccessor.transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.transform "vectorbt.signals.accessors.SignalsAccessor.transform")
  * [GenericAccessor.value_counts()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.value_counts "vectorbt.signals.accessors.SignalsAccessor.value_counts")
  * [GenericAccessor.zscore()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.zscore "vectorbt.signals.accessors.SignalsAccessor.zscore")
  * [GenericDFAccessor.flatten_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped "vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped")
  * [GenericDFAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.heatmap "vectorbt.generic.accessors.GenericDFAccessor.heatmap")
  * [GenericDFAccessor.squeeze_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped "vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped")
  * [GenericDFAccessor.ts_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.ts_heatmap "vectorbt.generic.accessors.GenericDFAccessor.ts_heatmap")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.signals.accessors.SignalsAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.signals.accessors.SignalsAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.signals.accessors.SignalsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.signals.accessors.SignalsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.signals.accessors.SignalsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.signals.accessors.SignalsAccessor.plots")
  * [SignalsAccessor.AND()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.AND "vectorbt.signals.accessors.SignalsAccessor.AND")
  * [SignalsAccessor.OR()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.OR "vectorbt.signals.accessors.SignalsAccessor.OR")
  * [SignalsAccessor.XOR()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.XOR "vectorbt.signals.accessors.SignalsAccessor.XOR")
  * [SignalsAccessor.between_partition_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.between_partition_ranges "vectorbt.signals.accessors.SignalsAccessor.between_partition_ranges")
  * [SignalsAccessor.between_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.between_ranges "vectorbt.signals.accessors.SignalsAccessor.between_ranges")
  * [SignalsAccessor.bshift()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.bshift "vectorbt.signals.accessors.SignalsAccessor.bshift")
  * [SignalsAccessor.clean()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.clean "vectorbt.signals.accessors.SignalsAccessor.clean")
  * [SignalsAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.signals.accessors.SignalsAccessor.config")
  * [SignalsAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.signals.accessors.SignalsAccessor.df_accessor_cls")
  * [SignalsAccessor.drawdowns](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdowns "vectorbt.signals.accessors.SignalsAccessor.drawdowns")
  * [SignalsAccessor.empty()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.empty "vectorbt.signals.accessors.SignalsAccessor.empty")
  * [SignalsAccessor.empty_like()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.empty_like "vectorbt.signals.accessors.SignalsAccessor.empty_like")
  * [SignalsAccessor.first()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.first "vectorbt.signals.accessors.SignalsAccessor.first")
  * [SignalsAccessor.from_nth()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.from_nth "vectorbt.signals.accessors.SignalsAccessor.from_nth")
  * [SignalsAccessor.fshift()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.fshift "vectorbt.signals.accessors.SignalsAccessor.fshift")
  * [SignalsAccessor.generate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate "vectorbt.signals.accessors.SignalsAccessor.generate")
  * [SignalsAccessor.generate_both()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_both "vectorbt.signals.accessors.SignalsAccessor.generate_both")
  * [SignalsAccessor.generate_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_exits "vectorbt.signals.accessors.SignalsAccessor.generate_exits")
  * [SignalsAccessor.generate_ohlc_stop_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits "vectorbt.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits")
  * [SignalsAccessor.generate_random()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random "vectorbt.signals.accessors.SignalsAccessor.generate_random")
  * [SignalsAccessor.generate_random_both()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random_both "vectorbt.signals.accessors.SignalsAccessor.generate_random_both")
  * [SignalsAccessor.generate_random_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random_exits "vectorbt.signals.accessors.SignalsAccessor.generate_random_exits")
  * [SignalsAccessor.generate_stop_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_stop_exits "vectorbt.signals.accessors.SignalsAccessor.generate_stop_exits")
  * [SignalsAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.signals.accessors.SignalsAccessor.iloc")
  * [SignalsAccessor.index_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.index_mapped "vectorbt.signals.accessors.SignalsAccessor.index_mapped")
  * [SignalsAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.signals.accessors.SignalsAccessor.indexing_kwargs")
  * [SignalsAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.signals.accessors.SignalsAccessor.loc")
  * [SignalsAccessor.mapping](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mapping "vectorbt.signals.accessors.SignalsAccessor.mapping")
  * [SignalsAccessor.norm_avg_index()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.norm_avg_index "vectorbt.signals.accessors.SignalsAccessor.norm_avg_index")
  * [SignalsAccessor.nth()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.nth "vectorbt.signals.accessors.SignalsAccessor.nth")
  * [SignalsAccessor.nth_index()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.nth_index "vectorbt.signals.accessors.SignalsAccessor.nth_index")
  * [SignalsAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.signals.accessors.SignalsAccessor.obj")
  * [SignalsAccessor.partition_pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank")
  * [SignalsAccessor.partition_pos_rank_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank_mapped "vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank_mapped")
  * [SignalsAccessor.partition_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_ranges "vectorbt.signals.accessors.SignalsAccessor.partition_ranges")
  * [SignalsAccessor.partition_rate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_rate "vectorbt.signals.accessors.SignalsAccessor.partition_rate")
  * [SignalsAccessor.plot()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.plot "vectorbt.signals.accessors.SignalsAccessor.plot")
  * [SignalsAccessor.plots_defaults](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.plots_defaults "vectorbt.signals.accessors.SignalsAccessor.plots_defaults")
  * [SignalsAccessor.pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.pos_rank "vectorbt.signals.accessors.SignalsAccessor.pos_rank")
  * [SignalsAccessor.pos_rank_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.pos_rank_mapped "vectorbt.signals.accessors.SignalsAccessor.pos_rank_mapped")
  * [SignalsAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.signals.accessors.SignalsAccessor.ranges")
  * [SignalsAccessor.rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rank "vectorbt.signals.accessors.SignalsAccessor.rank")
  * [SignalsAccessor.rate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rate "vectorbt.signals.accessors.SignalsAccessor.rate")
  * [SignalsAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.signals.accessors.SignalsAccessor.self_aliases")
  * [SignalsAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.signals.accessors.SignalsAccessor.sr_accessor_cls")
  * [SignalsAccessor.stats_defaults](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.stats_defaults "vectorbt.signals.accessors.SignalsAccessor.stats_defaults")
  * [SignalsAccessor.total()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total "vectorbt.signals.accessors.SignalsAccessor.total")
  * [SignalsAccessor.total_partitions()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total_partitions "vectorbt.signals.accessors.SignalsAccessor.total_partitions")
  * [SignalsAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.signals.accessors.SignalsAccessor.wrapper")
  * [SignalsAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.signals.accessors.SignalsAccessor.writeable_attrs")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.signals.accessors.SignalsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.signals.accessors.SignalsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.signals.accessors.SignalsAccessor.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.signals.accessors.SignalsAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.signals.accessors.SignalsAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.signals.accessors.SignalsAccessor.select_one_from_obj")



* * *

## SignalsSRAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1709-L1803 "Jump to source")¶
    
    
    SignalsSRAccessor(
        obj,
        **kwargs
    )
    

Accessor on top of signal series. For Series only.

Accessible through `pd.Series.vbt.signals`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [BaseSRAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseSRAccessor "vectorbt.base.accessors.BaseSRAccessor")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor")
  * [GenericSRAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor "vectorbt.generic.accessors.GenericSRAccessor")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [SignalsAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor "vectorbt.signals.accessors.SignalsAccessor")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.signals.accessors.SignalsAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.signals.accessors.SignalsAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.signals.accessors.SignalsAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.signals.accessors.SignalsAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.signals.accessors.SignalsAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.signals.accessors.SignalsAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.signals.accessors.SignalsAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.signals.accessors.SignalsAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.signals.accessors.SignalsAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.signals.accessors.SignalsAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.signals.accessors.SignalsAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.signals.accessors.SignalsAccessor.concat")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.signals.accessors.SignalsAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.signals.accessors.SignalsAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.signals.accessors.SignalsAccessor.drop_redundant_levels")
  * [BaseAccessor.indexing_func()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.indexing_func "vectorbt.signals.accessors.SignalsAccessor.indexing_func")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.signals.accessors.SignalsAccessor.make_symmetric")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.signals.accessors.SignalsAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.signals.accessors.SignalsAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.signals.accessors.SignalsAccessor.select_levels")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.signals.accessors.SignalsAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.signals.accessors.SignalsAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.signals.accessors.SignalsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.signals.accessors.SignalsAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.signals.accessors.SignalsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.signals.accessors.SignalsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.signals.accessors.SignalsAccessor.unstack_to_df")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.signals.accessors.SignalsAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.signals.accessors.SignalsAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.signals.accessors.SignalsAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.signals.accessors.SignalsAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.signals.accessors.SignalsAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.signals.accessors.SignalsAccessor.update_config")
  * [GenericAccessor.apply_along_axis()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_along_axis "vectorbt.signals.accessors.SignalsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_and_reduce "vectorbt.signals.accessors.SignalsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_mapping "vectorbt.signals.accessors.SignalsAccessor.apply_mapping")
  * [GenericAccessor.applymap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.applymap "vectorbt.signals.accessors.SignalsAccessor.applymap")
  * [GenericAccessor.barplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.barplot "vectorbt.signals.accessors.SignalsAccessor.barplot")
  * [GenericAccessor.bfill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bfill "vectorbt.signals.accessors.SignalsAccessor.bfill")
  * [GenericAccessor.binarize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.binarize "vectorbt.signals.accessors.SignalsAccessor.binarize")
  * [GenericAccessor.boxplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.boxplot "vectorbt.signals.accessors.SignalsAccessor.boxplot")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.signals.accessors.SignalsAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.signals.accessors.SignalsAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.signals.accessors.SignalsAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.signals.accessors.SignalsAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.signals.accessors.SignalsAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.signals.accessors.SignalsAccessor.describe")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.signals.accessors.SignalsAccessor.diff")
  * [GenericAccessor.drawdown()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdown "vectorbt.signals.accessors.SignalsAccessor.drawdown")
  * [GenericAccessor.ewm_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_mean "vectorbt.signals.accessors.SignalsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_std "vectorbt.signals.accessors.SignalsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_apply "vectorbt.signals.accessors.SignalsAccessor.expanding_apply")
  * [GenericAccessor.expanding_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_max "vectorbt.signals.accessors.SignalsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_mean "vectorbt.signals.accessors.SignalsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_min "vectorbt.signals.accessors.SignalsAccessor.expanding_min")
  * [GenericAccessor.expanding_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_split "vectorbt.signals.accessors.SignalsAccessor.expanding_split")
  * [GenericAccessor.expanding_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_std "vectorbt.signals.accessors.SignalsAccessor.expanding_std")
  * [GenericAccessor.ffill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ffill "vectorbt.signals.accessors.SignalsAccessor.ffill")
  * [GenericAccessor.fillna()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fillna "vectorbt.signals.accessors.SignalsAccessor.fillna")
  * [GenericAccessor.filter()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.filter "vectorbt.signals.accessors.SignalsAccessor.filter")
  * [GenericAccessor.get_drawdowns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_drawdowns "vectorbt.signals.accessors.SignalsAccessor.get_drawdowns")
  * [GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.signals.accessors.SignalsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.groupby_apply "vectorbt.signals.accessors.SignalsAccessor.groupby_apply")
  * [GenericAccessor.histplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.histplot "vectorbt.signals.accessors.SignalsAccessor.histplot")
  * [GenericAccessor.idxmax()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmax "vectorbt.signals.accessors.SignalsAccessor.idxmax")
  * [GenericAccessor.idxmin()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmin "vectorbt.signals.accessors.SignalsAccessor.idxmin")
  * [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.signals.accessors.SignalsAccessor.lineplot")
  * [GenericAccessor.max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.max "vectorbt.signals.accessors.SignalsAccessor.max")
  * [GenericAccessor.maxabs_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.maxabs_scale "vectorbt.signals.accessors.SignalsAccessor.maxabs_scale")
  * [GenericAccessor.mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mean "vectorbt.signals.accessors.SignalsAccessor.mean")
  * [GenericAccessor.median()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.median "vectorbt.signals.accessors.SignalsAccessor.median")
  * [GenericAccessor.min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.min "vectorbt.signals.accessors.SignalsAccessor.min")
  * [GenericAccessor.minmax_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.minmax_scale "vectorbt.signals.accessors.SignalsAccessor.minmax_scale")
  * [GenericAccessor.normalize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.normalize "vectorbt.signals.accessors.SignalsAccessor.normalize")
  * [GenericAccessor.pct_change()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.pct_change "vectorbt.signals.accessors.SignalsAccessor.pct_change")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.signals.accessors.SignalsAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.signals.accessors.SignalsAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.signals.accessors.SignalsAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.signals.accessors.SignalsAccessor.range_split")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.signals.accessors.SignalsAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.signals.accessors.SignalsAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.signals.accessors.SignalsAccessor.resample_apply")
  * [GenericAccessor.resolve_self()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resolve_self "vectorbt.signals.accessors.SignalsAccessor.resolve_self")
  * [GenericAccessor.robust_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.robust_scale "vectorbt.signals.accessors.SignalsAccessor.robust_scale")
  * [GenericAccessor.rolling_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_apply "vectorbt.signals.accessors.SignalsAccessor.rolling_apply")
  * [GenericAccessor.rolling_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_max "vectorbt.signals.accessors.SignalsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_mean "vectorbt.signals.accessors.SignalsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_min "vectorbt.signals.accessors.SignalsAccessor.rolling_min")
  * [GenericAccessor.rolling_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_split "vectorbt.signals.accessors.SignalsAccessor.rolling_split")
  * [GenericAccessor.rolling_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_std "vectorbt.signals.accessors.SignalsAccessor.rolling_std")
  * [GenericAccessor.scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scale "vectorbt.signals.accessors.SignalsAccessor.scale")
  * [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.signals.accessors.SignalsAccessor.scatterplot")
  * [GenericAccessor.shuffle()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.shuffle "vectorbt.signals.accessors.SignalsAccessor.shuffle")
  * [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.signals.accessors.SignalsAccessor.split")
  * [GenericAccessor.std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.std "vectorbt.signals.accessors.SignalsAccessor.std")
  * [GenericAccessor.sum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.sum "vectorbt.signals.accessors.SignalsAccessor.sum")
  * [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.signals.accessors.SignalsAccessor.to_mapped")
  * [GenericAccessor.to_returns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_returns "vectorbt.signals.accessors.SignalsAccessor.to_returns")
  * [GenericAccessor.transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.transform "vectorbt.signals.accessors.SignalsAccessor.transform")
  * [GenericAccessor.value_counts()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.value_counts "vectorbt.signals.accessors.SignalsAccessor.value_counts")
  * [GenericAccessor.zscore()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.zscore "vectorbt.signals.accessors.SignalsAccessor.zscore")
  * [GenericSRAccessor.flatten_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.flatten_grouped "vectorbt.generic.accessors.GenericSRAccessor.flatten_grouped")
  * [GenericSRAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.heatmap "vectorbt.generic.accessors.GenericSRAccessor.heatmap")
  * [GenericSRAccessor.overlay_with_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.overlay_with_heatmap "vectorbt.generic.accessors.GenericSRAccessor.overlay_with_heatmap")
  * [GenericSRAccessor.plot_against()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.plot_against "vectorbt.generic.accessors.GenericSRAccessor.plot_against")
  * [GenericSRAccessor.qqplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.qqplot "vectorbt.generic.accessors.GenericSRAccessor.qqplot")
  * [GenericSRAccessor.squeeze_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.squeeze_grouped "vectorbt.generic.accessors.GenericSRAccessor.squeeze_grouped")
  * [GenericSRAccessor.ts_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.ts_heatmap "vectorbt.generic.accessors.GenericSRAccessor.ts_heatmap")
  * [GenericSRAccessor.volume()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.volume "vectorbt.generic.accessors.GenericSRAccessor.volume")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.signals.accessors.SignalsAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.signals.accessors.SignalsAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.signals.accessors.SignalsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.signals.accessors.SignalsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.signals.accessors.SignalsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.signals.accessors.SignalsAccessor.plots")
  * [SignalsAccessor.AND()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.AND "vectorbt.signals.accessors.SignalsAccessor.AND")
  * [SignalsAccessor.OR()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.OR "vectorbt.signals.accessors.SignalsAccessor.OR")
  * [SignalsAccessor.XOR()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.XOR "vectorbt.signals.accessors.SignalsAccessor.XOR")
  * [SignalsAccessor.between_partition_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.between_partition_ranges "vectorbt.signals.accessors.SignalsAccessor.between_partition_ranges")
  * [SignalsAccessor.between_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.between_ranges "vectorbt.signals.accessors.SignalsAccessor.between_ranges")
  * [SignalsAccessor.bshift()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.bshift "vectorbt.signals.accessors.SignalsAccessor.bshift")
  * [SignalsAccessor.clean()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.clean "vectorbt.signals.accessors.SignalsAccessor.clean")
  * [SignalsAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.signals.accessors.SignalsAccessor.config")
  * [SignalsAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.signals.accessors.SignalsAccessor.df_accessor_cls")
  * [SignalsAccessor.drawdowns](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.drawdowns "vectorbt.signals.accessors.SignalsAccessor.drawdowns")
  * [SignalsAccessor.empty()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.empty "vectorbt.signals.accessors.SignalsAccessor.empty")
  * [SignalsAccessor.empty_like()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.empty_like "vectorbt.signals.accessors.SignalsAccessor.empty_like")
  * [SignalsAccessor.first()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.first "vectorbt.signals.accessors.SignalsAccessor.first")
  * [SignalsAccessor.from_nth()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.from_nth "vectorbt.signals.accessors.SignalsAccessor.from_nth")
  * [SignalsAccessor.fshift()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.fshift "vectorbt.signals.accessors.SignalsAccessor.fshift")
  * [SignalsAccessor.generate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate "vectorbt.signals.accessors.SignalsAccessor.generate")
  * [SignalsAccessor.generate_both()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_both "vectorbt.signals.accessors.SignalsAccessor.generate_both")
  * [SignalsAccessor.generate_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_exits "vectorbt.signals.accessors.SignalsAccessor.generate_exits")
  * [SignalsAccessor.generate_ohlc_stop_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits "vectorbt.signals.accessors.SignalsAccessor.generate_ohlc_stop_exits")
  * [SignalsAccessor.generate_random()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random "vectorbt.signals.accessors.SignalsAccessor.generate_random")
  * [SignalsAccessor.generate_random_both()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random_both "vectorbt.signals.accessors.SignalsAccessor.generate_random_both")
  * [SignalsAccessor.generate_random_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_random_exits "vectorbt.signals.accessors.SignalsAccessor.generate_random_exits")
  * [SignalsAccessor.generate_stop_exits()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.generate_stop_exits "vectorbt.signals.accessors.SignalsAccessor.generate_stop_exits")
  * [SignalsAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.signals.accessors.SignalsAccessor.iloc")
  * [SignalsAccessor.index_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.index_mapped "vectorbt.signals.accessors.SignalsAccessor.index_mapped")
  * [SignalsAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.signals.accessors.SignalsAccessor.indexing_kwargs")
  * [SignalsAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.signals.accessors.SignalsAccessor.loc")
  * [SignalsAccessor.mapping](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mapping "vectorbt.signals.accessors.SignalsAccessor.mapping")
  * [SignalsAccessor.norm_avg_index()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.norm_avg_index "vectorbt.signals.accessors.SignalsAccessor.norm_avg_index")
  * [SignalsAccessor.nth()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.nth "vectorbt.signals.accessors.SignalsAccessor.nth")
  * [SignalsAccessor.nth_index()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.nth_index "vectorbt.signals.accessors.SignalsAccessor.nth_index")
  * [SignalsAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.signals.accessors.SignalsAccessor.obj")
  * [SignalsAccessor.partition_pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank "vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank")
  * [SignalsAccessor.partition_pos_rank_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank_mapped "vectorbt.signals.accessors.SignalsAccessor.partition_pos_rank_mapped")
  * [SignalsAccessor.partition_ranges()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_ranges "vectorbt.signals.accessors.SignalsAccessor.partition_ranges")
  * [SignalsAccessor.partition_rate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.partition_rate "vectorbt.signals.accessors.SignalsAccessor.partition_rate")
  * [SignalsAccessor.plot()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.plot "vectorbt.signals.accessors.SignalsAccessor.plot")
  * [SignalsAccessor.plots_defaults](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.plots_defaults "vectorbt.signals.accessors.SignalsAccessor.plots_defaults")
  * [SignalsAccessor.pos_rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.pos_rank "vectorbt.signals.accessors.SignalsAccessor.pos_rank")
  * [SignalsAccessor.pos_rank_mapped()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.pos_rank_mapped "vectorbt.signals.accessors.SignalsAccessor.pos_rank_mapped")
  * [SignalsAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.signals.accessors.SignalsAccessor.ranges")
  * [SignalsAccessor.rank()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rank "vectorbt.signals.accessors.SignalsAccessor.rank")
  * [SignalsAccessor.rate()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.rate "vectorbt.signals.accessors.SignalsAccessor.rate")
  * [SignalsAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.signals.accessors.SignalsAccessor.self_aliases")
  * [SignalsAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.signals.accessors.SignalsAccessor.sr_accessor_cls")
  * [SignalsAccessor.stats_defaults](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.stats_defaults "vectorbt.signals.accessors.SignalsAccessor.stats_defaults")
  * [SignalsAccessor.total()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total "vectorbt.signals.accessors.SignalsAccessor.total")
  * [SignalsAccessor.total_partitions()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor.total_partitions "vectorbt.signals.accessors.SignalsAccessor.total_partitions")
  * [SignalsAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.signals.accessors.SignalsAccessor.wrapper")
  * [SignalsAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.signals.accessors.SignalsAccessor.writeable_attrs")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.signals.accessors.SignalsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.signals.accessors.SignalsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.signals.accessors.SignalsAccessor.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.signals.accessors.SignalsAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.signals.accessors.SignalsAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.signals.accessors.SignalsAccessor.select_one_from_obj")



* * *

### plot_as_entry_markers method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1759-L1780 "Jump to source")¶
    
    
    SignalsSRAccessor.plot_as_entry_markers(
        y=None,
        **kwargs
    )
    

Plot signals as entry markers.

See [SignalsSRAccessor.plot_as_markers()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsSRAccessor.plot_as_markers "vectorbt.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_exit_markers method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1782-L1803 "Jump to source")¶
    
    
    SignalsSRAccessor.plot_as_exit_markers(
        y=None,
        **kwargs
    )
    

Plot signals as exit markers.

See [SignalsSRAccessor.plot_as_markers()](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsSRAccessor.plot_as_markers "vectorbt.signals.accessors.SignalsSRAccessor.plot_as_markers").

* * *

### plot_as_markers method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/signals/accessors.py#L1719-L1757 "Jump to source")¶
    
    
    SignalsSRAccessor.plot_as_markers(
        y=None,
        **kwargs
    )
    

Plot Series as markers.

**Args**

**`y`** : `array_like`
    Y-axis values to plot markers on.
**`**kwargs`**
    Keyword arguments passed to [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.generic.accessors.GenericAccessor.scatterplot").

**Usage**
    
    
    >>> ts = pd.Series([1, 2, 3, 2, 1], index=mask.index)
    >>> fig = ts.vbt.lineplot()
    >>> mask['b'].vbt.signals.plot_as_entry_markers(y=ts, fig=fig)
    >>> (~mask['b']).vbt.signals.plot_as_exit_markers(y=ts, fig=fig)
    

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
