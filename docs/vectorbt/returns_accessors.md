# accessors - VectorBT

> **Source:** https://vectorbt.dev/api/returns/accessors/

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
      * accessors  [ accessors  ](https://vectorbt.dev/api/returns/accessors/) Table of contents 
        * Defaults 
        * Stats 
        * Plots 
        * ReturnsAccessor() 
          * alpha() 
          * ann_factor 
          * annual() 
          * annualized() 
          * annualized_volatility() 
          * benchmark_rets 
          * beta() 
          * calmar_ratio() 
          * capture() 
          * common_sense_ratio() 
          * cond_value_at_risk() 
          * cumulative() 
          * daily() 
          * defaults 
          * deflated_sharpe_ratio() 
          * down_capture() 
          * downside_risk() 
          * drawdown() 
          * drawdowns 
          * from_value() 
          * get_drawdowns() 
          * indexing_func() 
          * information_ratio() 
          * max_drawdown() 
          * metrics 
          * omega_ratio() 
          * plots_defaults 
          * qs 
          * resolve_self() 
          * rolling_alpha() 
          * rolling_annualized() 
          * rolling_annualized_volatility() 
          * rolling_beta() 
          * rolling_calmar_ratio() 
          * rolling_capture() 
          * rolling_common_sense_ratio() 
          * rolling_cond_value_at_risk() 
          * rolling_down_capture() 
          * rolling_downside_risk() 
          * rolling_information_ratio() 
          * rolling_max_drawdown() 
          * rolling_omega_ratio() 
          * rolling_sharpe_ratio() 
          * rolling_sortino_ratio() 
          * rolling_tail_ratio() 
          * rolling_total() 
          * rolling_up_capture() 
          * rolling_value_at_risk() 
          * sharpe_ratio() 
          * sortino_ratio() 
          * stats_defaults 
          * subplots 
          * tail_ratio() 
          * total() 
          * up_capture() 
          * value_at_risk() 
          * year_freq 
        * ReturnsDFAccessor() 
        * ReturnsSRAccessor() 
          * plot_cumulative() 
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

  * Defaults 
  * Stats 
  * Plots 
  * ReturnsAccessor() 
    * alpha() 
    * ann_factor 
    * annual() 
    * annualized() 
    * annualized_volatility() 
    * benchmark_rets 
    * beta() 
    * calmar_ratio() 
    * capture() 
    * common_sense_ratio() 
    * cond_value_at_risk() 
    * cumulative() 
    * daily() 
    * defaults 
    * deflated_sharpe_ratio() 
    * down_capture() 
    * downside_risk() 
    * drawdown() 
    * drawdowns 
    * from_value() 
    * get_drawdowns() 
    * indexing_func() 
    * information_ratio() 
    * max_drawdown() 
    * metrics 
    * omega_ratio() 
    * plots_defaults 
    * qs 
    * resolve_self() 
    * rolling_alpha() 
    * rolling_annualized() 
    * rolling_annualized_volatility() 
    * rolling_beta() 
    * rolling_calmar_ratio() 
    * rolling_capture() 
    * rolling_common_sense_ratio() 
    * rolling_cond_value_at_risk() 
    * rolling_down_capture() 
    * rolling_downside_risk() 
    * rolling_information_ratio() 
    * rolling_max_drawdown() 
    * rolling_omega_ratio() 
    * rolling_sharpe_ratio() 
    * rolling_sortino_ratio() 
    * rolling_tail_ratio() 
    * rolling_total() 
    * rolling_up_capture() 
    * rolling_value_at_risk() 
    * sharpe_ratio() 
    * sortino_ratio() 
    * stats_defaults 
    * subplots 
    * tail_ratio() 
    * total() 
    * up_capture() 
    * value_at_risk() 
    * year_freq 
  * ReturnsDFAccessor() 
  * ReturnsSRAccessor() 
    * plot_cumulative() 



# accessors module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py "Jump to source")¶

Custom pandas accessors for returns data.

Methods can be accessed as follows:

  * [ReturnsSRAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsSRAccessor "vectorbt.returns.accessors.ReturnsSRAccessor") -> `pd.Series.vbt.returns.*`
  * [ReturnsDFAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsDFAccessor "vectorbt.returns.accessors.ReturnsDFAccessor") -> `pd.DataFrame.vbt.returns.*`



Note

The underlying Series/DataFrame must already be a return series. To convert price to returns, use [ReturnsAccessor.from_value()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.from_value "vectorbt.returns.accessors.ReturnsAccessor.from_value").

Grouping is only supported by the methods that accept the `group_by` argument.

Accessors do not utilize caching.

There are three options to compute returns and get the accessor:
    
    
    >>> import numpy as np
    >>> import pandas as pd
    >>> import vectorbt as vbt
    
    >>> price = pd.Series([1.1, 1.2, 1.3, 1.2, 1.1])
    
    >>> # 1. pd.Series.pct_change
    >>> rets = price.pct_change()
    >>> ret_acc = rets.vbt.returns(freq='d')
    
    >>> # 2. vectorbt.generic.accessors.GenericAccessor.to_returns
    >>> rets = price.vbt.to_returns()
    >>> ret_acc = rets.vbt.returns(freq='d')
    
    >>> # 3. vectorbt.returns.accessors.ReturnsAccessor.from_value
    >>> ret_acc = pd.Series.vbt.returns.from_value(price, freq='d')
    
    >>> # vectorbt.returns.accessors.ReturnsAccessor.total
    >>> ret_acc.total()
    0.0
    

The accessors extend [vectorbt.generic.accessors](https://vectorbt.dev/api/generic/accessors/ "vectorbt.generic.accessors").
    
    
    >>> # inherited from GenericAccessor
    >>> ret_acc.max()
    0.09090909090909083
    

## Defaults¶

[ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor") accepts `defaults` dictionary where you can pass defaults for arguments used throughout the accessor, such as

  * `start_value`: The starting value.
  * `window`: Window length.
  * `minp`: Minimum number of observations in a window required to have a value.
  * `ddof`: Delta Degrees of Freedom.
  * `risk_free`: Constant risk-free return throughout the period.
  * `levy_alpha`: Scaling relation (Levy stability exponent).
  * `required_return`: Minimum acceptance return of the investor.
  * `cutoff`: Decimal representing the percentage cutoff for the bottom percentile of returns.



## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [ReturnsAccessor.metrics](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.metrics "vectorbt.returns.accessors.ReturnsAccessor.metrics").
    
    
    >>> ret_acc.stats()
    UserWarning: Metric 'benchmark_return' requires benchmark_rets to be set
    UserWarning: Metric 'alpha' requires benchmark_rets to be set
    UserWarning: Metric 'beta' requires benchmark_rets to be set
    
    Start                                      0
    End                                        4
    Duration                     5 days 00:00:00
    Total Return [%]                           0
    Annualized Return [%]                      0
    Annualized Volatility [%]            184.643
    Sharpe Ratio                        0.691185
    Calmar Ratio                               0
    Max Drawdown [%]                     15.3846
    Omega Ratio                          1.08727
    Sortino Ratio                        1.17805
    Skew                              0.00151002
    Kurtosis                            -5.94737
    Tail Ratio                           1.08985
    Common Sense Ratio                   1.08985
    Value at Risk                     -0.0823718
    dtype: object
    

The missing `benchmark_rets` can be either passed to the contrustor of the accessor or as a setting to [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.returns.accessors.ReturnsAccessor.stats"):
    
    
    >>> benchmark = pd.Series([1.05, 1.1, 1.15, 1.1, 1.05])
    >>> benchmark_rets = benchmark.vbt.to_returns()
    
    >>> ret_acc.stats(settings=dict(benchmark_rets=benchmark_rets))
    Start                                      0
    End                                        4
    Duration                     5 days 00:00:00
    Total Return [%]                           0
    Benchmark Return [%]                       0
    Annualized Return [%]                      0
    Annualized Volatility [%]            184.643
    Sharpe Ratio                        0.691185
    Calmar Ratio                               0
    Max Drawdown [%]                     15.3846
    Omega Ratio                          1.08727
    Sortino Ratio                        1.17805
    Skew                              0.00151002
    Kurtosis                            -5.94737
    Tail Ratio                           1.08985
    Common Sense Ratio                   1.08985
    Value at Risk                     -0.0823718
    Alpha                                0.78789
    Beta                                 1.83864
    dtype: object
    

Note

[StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.returns.accessors.ReturnsAccessor.stats") does not support grouping.

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [ReturnsAccessor.subplots](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.subplots "vectorbt.returns.accessors.ReturnsAccessor.subplots").

This class inherits subplots from [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").

* * *

## ReturnsAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L164-L1107 "Jump to source")¶
    
    
    ReturnsAccessor(
        obj,
        benchmark_rets=None,
        year_freq=None,
        defaults=None,
        **kwargs
    )
    

Accessor on top of return series. For both, Series and DataFrames.

Accessible through `pd.Series.vbt.returns` and `pd.DataFrame.vbt.returns`.

**Args**

**`obj`** : `pd.Series` or `pd.DataFrame`
    Pandas object representing returns.
**`benchmark_rets`** : `array_like`
    Pandas object representing benchmark returns.
**`year_freq`** : `any`
    Year frequency for annualization purposes.
**`defaults`** : `dict`
    Defaults that override `returns.defaults` in [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").
**`**kwargs`**
    Keyword arguments that are passed down to [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").

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
  * [BaseAccessor.empty()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty "vectorbt.generic.accessors.GenericAccessor.empty")
  * [BaseAccessor.empty_like()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty_like "vectorbt.generic.accessors.GenericAccessor.empty_like")
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
  * [GenericAccessor.bshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bshift "vectorbt.generic.accessors.GenericAccessor.bshift")
  * [GenericAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.generic.accessors.GenericAccessor.config")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.generic.accessors.GenericAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.generic.accessors.GenericAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.generic.accessors.GenericAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.generic.accessors.GenericAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.generic.accessors.GenericAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.generic.accessors.GenericAccessor.describe")
  * [GenericAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.generic.accessors.GenericAccessor.df_accessor_cls")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.generic.accessors.GenericAccessor.diff")
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
  * [GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.generic.accessors.GenericAccessor.fshift")
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
  * [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.generic.accessors.GenericAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.generic.accessors.GenericAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.generic.accessors.GenericAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.generic.accessors.GenericAccessor.range_split")
  * [GenericAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.generic.accessors.GenericAccessor.ranges")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.generic.accessors.GenericAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.generic.accessors.GenericAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.generic.accessors.GenericAccessor.resample_apply")
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

  * [ReturnsDFAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsDFAccessor "vectorbt.returns.accessors.ReturnsDFAccessor")
  * [ReturnsSRAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsSRAccessor "vectorbt.returns.accessors.ReturnsSRAccessor")



* * *

### alpha method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L629-L641 "Jump to source")¶
    
    
    ReturnsAccessor.alpha(
        benchmark_rets=None,
        risk_free=None,
        wrap_kwargs=None
    )
    

See [alpha_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.alpha_nb "vectorbt.returns.nb.alpha_nb").

* * *

### ann_factor property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L271-L280 "Jump to source")¶

Get annualization factor.

* * *

### annual method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L304-L310 "Jump to source")¶
    
    
    ReturnsAccessor.annual(
        **kwargs
    )
    

Annual returns.

* * *

### annualized method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L341-L345 "Jump to source")¶
    
    
    ReturnsAccessor.annualized(
        wrap_kwargs=None
    )
    

See [annualized_return_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.annualized_return_nb "vectorbt.returns.nb.annualized_return_nb").

* * *

### annualized_volatility method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L360-L371 "Jump to source")¶
    
    
    ReturnsAccessor.annualized_volatility(
        levy_alpha=None,
        ddof=None,
        wrap_kwargs=None
    )
    

See [annualized_volatility_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.annualized_volatility_nb "vectorbt.returns.nb.annualized_volatility_nb").

* * *

### benchmark_rets property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L253-L256 "Jump to source")¶

Benchmark returns.

* * *

### beta method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L601-L610 "Jump to source")¶
    
    
    ReturnsAccessor.beta(
        benchmark_rets=None,
        wrap_kwargs=None
    )
    

See [beta_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.beta_nb "vectorbt.returns.nb.beta_nb").

* * *

### calmar_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L393-L397 "Jump to source")¶
    
    
    ReturnsAccessor.calmar_ratio(
        wrap_kwargs=None
    )
    

See [calmar_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.calmar_ratio_nb "vectorbt.returns.nb.calmar_ratio_nb").

* * *

### capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L755-L764 "Jump to source")¶
    
    
    ReturnsAccessor.capture(
        benchmark_rets=None,
        wrap_kwargs=None
    )
    

See [capture_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.capture_nb "vectorbt.returns.nb.capture_nb").

* * *

### common_sense_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L682-L686 "Jump to source")¶
    
    
    ReturnsAccessor.common_sense_ratio(
        wrap_kwargs=None
    )
    

Common Sense Ratio.

* * *

### cond_value_at_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L729-L737 "Jump to source")¶
    
    
    ReturnsAccessor.cond_value_at_risk(
        cutoff=None,
        wrap_kwargs=None
    )
    

See [cond_value_at_risk_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.cond_value_at_risk_nb "vectorbt.returns.nb.cond_value_at_risk_nb").

* * *

### cumulative method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L312-L320 "Jump to source")¶
    
    
    ReturnsAccessor.cumulative(
        start_value=None,
        wrap_kwargs=None
    )
    

See [cum_returns_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.cum_returns_nb "vectorbt.returns.nb.cum_returns_nb").

* * *

### daily method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L296-L302 "Jump to source")¶
    
    
    ReturnsAccessor.daily(
        **kwargs
    )
    

Daily returns.

* * *

### defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L282-L294 "Jump to source")¶

Defaults for [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor").

Merges `returns.defaults` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings") with `defaults` from [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor").

* * *

### deflated_sharpe_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L477-L513 "Jump to source")¶
    
    
    ReturnsAccessor.deflated_sharpe_ratio(
        risk_free=None,
        ddof=None,
        var_sharpe=None,
        nb_trials=None,
        bias=True,
        wrap_kwargs=None
    )
    

Deflated Sharpe Ratio (DSR).

Expresses the chance that the advertised strategy has a positive Sharpe ratio.

If `var_sharpe` is None, is calculated based on all columns. If `nb_trials` is None, is set to the number of columns.

* * *

### down_capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L811-L820 "Jump to source")¶
    
    
    ReturnsAccessor.down_capture(
        benchmark_rets=None,
        wrap_kwargs=None
    )
    

See [down_capture_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.down_capture_nb "vectorbt.returns.nb.down_capture_nb").

* * *

### downside_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L515-L523 "Jump to source")¶
    
    
    ReturnsAccessor.downside_risk(
        required_return=None,
        wrap_kwargs=None
    )
    

See [downside_risk_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.downside_risk_nb "vectorbt.returns.nb.downside_risk_nb").

* * *

### drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L839-L843 "Jump to source")¶
    
    
    ReturnsAccessor.drawdown(
        wrap_kwargs=None
    )
    

Relative decline from a peak.

* * *

### drawdowns property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L866-L869 "Jump to source")¶

[ReturnsAccessor.get_drawdowns()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns "vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns") with default arguments.

* * *

### from_value class method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L232-L251 "Jump to source")¶
    
    
    ReturnsAccessor.from_value(
        value,
        init_value=nan,
        broadcast_kwargs=None,
        wrap_kwargs=None,
        **kwargs
    )
    

Returns a new [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor") instance with returns calculated from `value`.

* * *

### get_drawdowns method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L871-L876 "Jump to source")¶
    
    
    ReturnsAccessor.get_drawdowns(
        wrapper_kwargs=None,
        **kwargs
    )
    

Generate drawdown records of cumulative returns.

See [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").

* * *

### indexing_func method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L207-L230 "Jump to source")¶
    
    
    ReturnsAccessor.indexing_func(
        pd_indexing_func,
        **kwargs
    )
    

Perform indexing on [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor").

* * *

### information_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L567-L579 "Jump to source")¶
    
    
    ReturnsAccessor.information_ratio(
        benchmark_rets=None,
        ddof=None,
        wrap_kwargs=None
    )
    

See [information_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.information_ratio_nb "vectorbt.returns.nb.information_ratio_nb").

* * *

### max_drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L845-L851 "Jump to source")¶
    
    
    ReturnsAccessor.max_drawdown(
        wrap_kwargs=None
    )
    

See [max_drawdown_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.max_drawdown_nb "vectorbt.returns.nb.max_drawdown_nb").

Yields the same result as `max_drawdown` of [ReturnsAccessor.drawdowns](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.drawdowns "vectorbt.returns.accessors.ReturnsAccessor.drawdowns").

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py "Jump to source")¶

Metrics supported by [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c040>",
            "agg_func": null,
            "check_is_not_grouped": false,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c0e0>",
            "agg_func": null,
            "check_is_not_grouped": false,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c180>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "check_is_not_grouped": false,
            "tags": "wrapper"
        },
        "total_return": {
            "title": "Total Return [%]",
            "calc_func": "total",
            "post_calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c220>",
            "tags": "returns"
        },
        "benchmark_return": {
            "title": "Benchmark Return [%]",
            "calc_func": "benchmark_rets.vbt.returns.total",
            "post_calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c2c0>",
            "check_has_benchmark_rets": true,
            "tags": "returns"
        },
        "ann_return": {
            "title": "Annualized Return [%]",
            "calc_func": "annualized",
            "post_calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c360>",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "ann_volatility": {
            "title": "Annualized Volatility [%]",
            "calc_func": "annualized_volatility",
            "post_calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c400>",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "max_dd": {
            "title": "Max Drawdown [%]",
            "calc_func": "drawdowns.max_drawdown",
            "post_calc_func": "<function ReturnsAccessor.<lambda> at 0x7f957f64c4a0>",
            "tags": [
                "returns",
                "drawdowns"
            ]
        },
        "max_dd_duration": {
            "title": "Max Drawdown Duration",
            "calc_func": "drawdowns.max_duration",
            "fill_wrap_kwargs": true,
            "tags": [
                "returns",
                "drawdowns",
                "duration"
            ]
        },
        "sharpe_ratio": {
            "title": "Sharpe Ratio",
            "calc_func": "sharpe_ratio",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "calmar_ratio": {
            "title": "Calmar Ratio",
            "calc_func": "calmar_ratio",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "omega_ratio": {
            "title": "Omega Ratio",
            "calc_func": "omega_ratio",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "sortino_ratio": {
            "title": "Sortino Ratio",
            "calc_func": "sortino_ratio",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "skew": {
            "title": "Skew",
            "calc_func": "obj.skew",
            "tags": "returns"
        },
        "kurtosis": {
            "title": "Kurtosis",
            "calc_func": "obj.kurtosis",
            "tags": "returns"
        },
        "tail_ratio": {
            "title": "Tail Ratio",
            "calc_func": "tail_ratio",
            "tags": "returns"
        },
        "common_sense_ratio": {
            "title": "Common Sense Ratio",
            "calc_func": "common_sense_ratio",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "tags": "returns"
        },
        "value_at_risk": {
            "title": "Value at Risk",
            "calc_func": "value_at_risk",
            "tags": "returns"
        },
        "alpha": {
            "title": "Alpha",
            "calc_func": "alpha",
            "check_has_freq": true,
            "check_has_year_freq": true,
            "check_has_benchmark_rets": true,
            "tags": "returns"
        },
        "beta": {
            "title": "Beta",
            "calc_func": "beta",
            "check_has_benchmark_rets": true,
            "tags": "returns"
        }
    })
    

Returns `ReturnsAccessor._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `ReturnsAccessor._metrics`.

* * *

### omega_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L412-L423 "Jump to source")¶
    
    
    ReturnsAccessor.omega_ratio(
        risk_free=None,
        required_return=None,
        wrap_kwargs=None
    )
    

See [omega_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.omega_ratio_nb "vectorbt.returns.nb.omega_ratio_nb").

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L1088-L1103 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.returns.accessors.ReturnsAccessor.plots").

Merges [GenericAccessor.plots_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plots_defaults "vectorbt.generic.accessors.GenericAccessor.plots_defaults"), defaults from [ReturnsAccessor.defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.defaults "vectorbt.returns.accessors.ReturnsAccessor.defaults") (acting as `settings`), and `returns.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings")

* * *

### qs property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L878-L883 "Jump to source")¶

Quantstats adapter.

* * *

### resolve_self method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L887-L923 "Jump to source")¶
    
    
    ReturnsAccessor.resolve_self(
        cond_kwargs=None,
        custom_arg_names=None,
        impacts_caching=True,
        silence_warnings=False
    )
    

Resolve self.

See [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.base.array_wrapper.Wrapping.resolve_self").

Creates a copy of this instance `year_freq` is different in `cond_kwargs`.

* * *

### rolling_alpha method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L643-L661 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_alpha(
        benchmark_rets=None,
        window=None,
        minp=None,
        risk_free=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.alpha()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.alpha "vectorbt.returns.accessors.ReturnsAccessor.alpha").

* * *

### rolling_annualized method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L347-L358 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_annualized(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.annualized()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized "vectorbt.returns.accessors.ReturnsAccessor.annualized").

* * *

### rolling_annualized_volatility method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L373-L391 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_annualized_volatility(
        window=None,
        minp=None,
        levy_alpha=None,
        ddof=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.annualized_volatility()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility "vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility").

* * *

### rolling_beta method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L612-L627 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_beta(
        benchmark_rets=None,
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.beta()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.beta "vectorbt.returns.accessors.ReturnsAccessor.beta").

* * *

### rolling_calmar_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L399-L410 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_calmar_ratio(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.calmar_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio "vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio").

* * *

### rolling_capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L766-L781 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_capture(
        benchmark_rets=None,
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.capture "vectorbt.returns.accessors.ReturnsAccessor.capture").

* * *

### rolling_common_sense_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L688-L701 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_common_sense_ratio(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.common_sense_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio "vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio").

* * *

### rolling_cond_value_at_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L739-L753 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_cond_value_at_risk(
        window=None,
        minp=None,
        cutoff=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.cond_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk").

* * *

### rolling_down_capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L822-L837 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_down_capture(
        benchmark_rets=None,
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.down_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.down_capture "vectorbt.returns.accessors.ReturnsAccessor.down_capture").

* * *

### rolling_downside_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L525-L539 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_downside_risk(
        window=None,
        minp=None,
        required_return=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.downside_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.downside_risk "vectorbt.returns.accessors.ReturnsAccessor.downside_risk").

* * *

### rolling_information_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L581-L599 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_information_ratio(
        benchmark_rets=None,
        window=None,
        minp=None,
        ddof=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.information_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.information_ratio "vectorbt.returns.accessors.ReturnsAccessor.information_ratio").

* * *

### rolling_max_drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L853-L864 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_max_drawdown(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.max_drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.max_drawdown "vectorbt.returns.accessors.ReturnsAccessor.max_drawdown").

* * *

### rolling_omega_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L425-L443 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_omega_ratio(
        window=None,
        minp=None,
        risk_free=None,
        required_return=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.omega_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.omega_ratio "vectorbt.returns.accessors.ReturnsAccessor.omega_ratio").

* * *

### rolling_sharpe_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L458-L475 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_sharpe_ratio(
        window=None,
        minp=None,
        risk_free=None,
        ddof=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio").

* * *

### rolling_sortino_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L551-L565 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_sortino_ratio(
        window=None,
        minp=None,
        required_return=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.sortino_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio "vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio").

* * *

### rolling_tail_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L669-L680 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_tail_ratio(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.tail_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.tail_ratio "vectorbt.returns.accessors.ReturnsAccessor.tail_ratio").

* * *

### rolling_total method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L328-L339 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_total(
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.total()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.total "vectorbt.returns.accessors.ReturnsAccessor.total").

* * *

### rolling_up_capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L794-L809 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_up_capture(
        benchmark_rets=None,
        window=None,
        minp=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.up_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.up_capture "vectorbt.returns.accessors.ReturnsAccessor.up_capture").

* * *

### rolling_value_at_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L713-L727 "Jump to source")¶
    
    
    ReturnsAccessor.rolling_value_at_risk(
        window=None,
        minp=None,
        cutoff=None,
        wrap_kwargs=None
    )
    

Rolling version of [ReturnsAccessor.value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.value_at_risk").

* * *

### sharpe_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L445-L456 "Jump to source")¶
    
    
    ReturnsAccessor.sharpe_ratio(
        risk_free=None,
        ddof=None,
        wrap_kwargs=None
    )
    

See [sharpe_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.sharpe_ratio_nb "vectorbt.returns.nb.sharpe_ratio_nb").

* * *

### sortino_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L541-L549 "Jump to source")¶
    
    
    ReturnsAccessor.sortino_ratio(
        required_return=None,
        wrap_kwargs=None
    )
    

See [sortino_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.sortino_ratio_nb "vectorbt.returns.nb.sortino_ratio_nb").

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L927-L942 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.returns.accessors.ReturnsAccessor.stats").

Merges [GenericAccessor.stats_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.stats_defaults "vectorbt.generic.accessors.GenericAccessor.stats_defaults"), defaults from [ReturnsAccessor.defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.defaults "vectorbt.returns.accessors.ReturnsAccessor.defaults") (acting as `settings`), and `returns.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings")

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py "Jump to source")¶

Subplots supported by [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor").
    
    
    Config({
        "plot": {
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "pass_trace_names": false,
            "tags": "generic"
        }
    })
    

Returns `ReturnsAccessor._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `ReturnsAccessor._subplots`.

* * *

### tail_ratio method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L663-L667 "Jump to source")¶
    
    
    ReturnsAccessor.tail_ratio(
        wrap_kwargs=None
    )
    

See [tail_ratio_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.tail_ratio_nb "vectorbt.returns.nb.tail_ratio_nb").

* * *

### total method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L322-L326 "Jump to source")¶
    
    
    ReturnsAccessor.total(
        wrap_kwargs=None
    )
    

See [cum_returns_final_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.cum_returns_final_nb "vectorbt.returns.nb.cum_returns_final_nb").

* * *

### up_capture method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L783-L792 "Jump to source")¶
    
    
    ReturnsAccessor.up_capture(
        benchmark_rets=None,
        wrap_kwargs=None
    )
    

See [up_capture_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.up_capture_nb "vectorbt.returns.nb.up_capture_nb").

* * *

### value_at_risk method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L703-L711 "Jump to source")¶
    
    
    ReturnsAccessor.value_at_risk(
        cutoff=None,
        wrap_kwargs=None
    )
    

See [value_at_risk_nb()](https://vectorbt.dev/api/returns/nb/#vectorbt.returns.nb.value_at_risk_nb "vectorbt.returns.nb.value_at_risk_nb").

* * *

### year_freq property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L258-L269 "Jump to source")¶

Year frequency for annualization purposes.

* * *

## ReturnsDFAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L1243-L1263 "Jump to source")¶
    
    
    ReturnsDFAccessor(
        obj,
        benchmark_rets=None,
        year_freq=None,
        defaults=None,
        **kwargs
    )
    

Accessor on top of return series. For DataFrames only.

Accessible through `pd.DataFrame.vbt.returns`.

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
  * [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.returns.accessors.ReturnsAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.returns.accessors.ReturnsAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.returns.accessors.ReturnsAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.returns.accessors.ReturnsAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.returns.accessors.ReturnsAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.returns.accessors.ReturnsAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.returns.accessors.ReturnsAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.returns.accessors.ReturnsAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.returns.accessors.ReturnsAccessor.concat")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_redundant_levels")
  * [BaseAccessor.empty()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty "vectorbt.returns.accessors.ReturnsAccessor.empty")
  * [BaseAccessor.empty_like()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty_like "vectorbt.returns.accessors.ReturnsAccessor.empty_like")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.returns.accessors.ReturnsAccessor.make_symmetric")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.returns.accessors.ReturnsAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.returns.accessors.ReturnsAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.returns.accessors.ReturnsAccessor.select_levels")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.returns.accessors.ReturnsAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.returns.accessors.ReturnsAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.returns.accessors.ReturnsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.returns.accessors.ReturnsAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.returns.accessors.ReturnsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.returns.accessors.ReturnsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.returns.accessors.ReturnsAccessor.unstack_to_df")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.returns.accessors.ReturnsAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.returns.accessors.ReturnsAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.returns.accessors.ReturnsAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.returns.accessors.ReturnsAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.returns.accessors.ReturnsAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.returns.accessors.ReturnsAccessor.update_config")
  * [GenericAccessor.apply_along_axis()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_along_axis "vectorbt.returns.accessors.ReturnsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_and_reduce "vectorbt.returns.accessors.ReturnsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_mapping "vectorbt.returns.accessors.ReturnsAccessor.apply_mapping")
  * [GenericAccessor.applymap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.applymap "vectorbt.returns.accessors.ReturnsAccessor.applymap")
  * [GenericAccessor.barplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.barplot "vectorbt.returns.accessors.ReturnsAccessor.barplot")
  * [GenericAccessor.bfill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bfill "vectorbt.returns.accessors.ReturnsAccessor.bfill")
  * [GenericAccessor.binarize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.binarize "vectorbt.returns.accessors.ReturnsAccessor.binarize")
  * [GenericAccessor.boxplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.boxplot "vectorbt.returns.accessors.ReturnsAccessor.boxplot")
  * [GenericAccessor.bshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bshift "vectorbt.returns.accessors.ReturnsAccessor.bshift")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.returns.accessors.ReturnsAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.returns.accessors.ReturnsAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.returns.accessors.ReturnsAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.returns.accessors.ReturnsAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.returns.accessors.ReturnsAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.returns.accessors.ReturnsAccessor.describe")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.returns.accessors.ReturnsAccessor.diff")
  * [GenericAccessor.ewm_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_mean "vectorbt.returns.accessors.ReturnsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_std "vectorbt.returns.accessors.ReturnsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_apply "vectorbt.returns.accessors.ReturnsAccessor.expanding_apply")
  * [GenericAccessor.expanding_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_max "vectorbt.returns.accessors.ReturnsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_mean "vectorbt.returns.accessors.ReturnsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_min "vectorbt.returns.accessors.ReturnsAccessor.expanding_min")
  * [GenericAccessor.expanding_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_split "vectorbt.returns.accessors.ReturnsAccessor.expanding_split")
  * [GenericAccessor.expanding_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_std "vectorbt.returns.accessors.ReturnsAccessor.expanding_std")
  * [GenericAccessor.ffill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ffill "vectorbt.returns.accessors.ReturnsAccessor.ffill")
  * [GenericAccessor.fillna()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fillna "vectorbt.returns.accessors.ReturnsAccessor.fillna")
  * [GenericAccessor.filter()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.filter "vectorbt.returns.accessors.ReturnsAccessor.filter")
  * [GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.returns.accessors.ReturnsAccessor.fshift")
  * [GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.returns.accessors.ReturnsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.groupby_apply "vectorbt.returns.accessors.ReturnsAccessor.groupby_apply")
  * [GenericAccessor.histplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.histplot "vectorbt.returns.accessors.ReturnsAccessor.histplot")
  * [GenericAccessor.idxmax()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmax "vectorbt.returns.accessors.ReturnsAccessor.idxmax")
  * [GenericAccessor.idxmin()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmin "vectorbt.returns.accessors.ReturnsAccessor.idxmin")
  * [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.returns.accessors.ReturnsAccessor.lineplot")
  * [GenericAccessor.max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.max "vectorbt.returns.accessors.ReturnsAccessor.max")
  * [GenericAccessor.maxabs_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.maxabs_scale "vectorbt.returns.accessors.ReturnsAccessor.maxabs_scale")
  * [GenericAccessor.mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mean "vectorbt.returns.accessors.ReturnsAccessor.mean")
  * [GenericAccessor.median()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.median "vectorbt.returns.accessors.ReturnsAccessor.median")
  * [GenericAccessor.min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.min "vectorbt.returns.accessors.ReturnsAccessor.min")
  * [GenericAccessor.minmax_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.minmax_scale "vectorbt.returns.accessors.ReturnsAccessor.minmax_scale")
  * [GenericAccessor.normalize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.normalize "vectorbt.returns.accessors.ReturnsAccessor.normalize")
  * [GenericAccessor.pct_change()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.pct_change "vectorbt.returns.accessors.ReturnsAccessor.pct_change")
  * [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.returns.accessors.ReturnsAccessor.plot")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.returns.accessors.ReturnsAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.returns.accessors.ReturnsAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.returns.accessors.ReturnsAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.returns.accessors.ReturnsAccessor.range_split")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.returns.accessors.ReturnsAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.returns.accessors.ReturnsAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.returns.accessors.ReturnsAccessor.resample_apply")
  * [GenericAccessor.robust_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.robust_scale "vectorbt.returns.accessors.ReturnsAccessor.robust_scale")
  * [GenericAccessor.rolling_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_apply "vectorbt.returns.accessors.ReturnsAccessor.rolling_apply")
  * [GenericAccessor.rolling_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_max "vectorbt.returns.accessors.ReturnsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_mean "vectorbt.returns.accessors.ReturnsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_min "vectorbt.returns.accessors.ReturnsAccessor.rolling_min")
  * [GenericAccessor.rolling_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_split "vectorbt.returns.accessors.ReturnsAccessor.rolling_split")
  * [GenericAccessor.rolling_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_std "vectorbt.returns.accessors.ReturnsAccessor.rolling_std")
  * [GenericAccessor.scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scale "vectorbt.returns.accessors.ReturnsAccessor.scale")
  * [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.returns.accessors.ReturnsAccessor.scatterplot")
  * [GenericAccessor.shuffle()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.shuffle "vectorbt.returns.accessors.ReturnsAccessor.shuffle")
  * [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.returns.accessors.ReturnsAccessor.split")
  * [GenericAccessor.std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.std "vectorbt.returns.accessors.ReturnsAccessor.std")
  * [GenericAccessor.sum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.sum "vectorbt.returns.accessors.ReturnsAccessor.sum")
  * [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.returns.accessors.ReturnsAccessor.to_mapped")
  * [GenericAccessor.to_returns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_returns "vectorbt.returns.accessors.ReturnsAccessor.to_returns")
  * [GenericAccessor.transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.transform "vectorbt.returns.accessors.ReturnsAccessor.transform")
  * [GenericAccessor.value_counts()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.value_counts "vectorbt.returns.accessors.ReturnsAccessor.value_counts")
  * [GenericAccessor.zscore()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.zscore "vectorbt.returns.accessors.ReturnsAccessor.zscore")
  * [GenericDFAccessor.flatten_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped "vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped")
  * [GenericDFAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.heatmap "vectorbt.generic.accessors.GenericDFAccessor.heatmap")
  * [GenericDFAccessor.squeeze_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped "vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped")
  * [GenericDFAccessor.ts_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.ts_heatmap "vectorbt.generic.accessors.GenericDFAccessor.ts_heatmap")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.returns.accessors.ReturnsAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.returns.accessors.ReturnsAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.returns.accessors.ReturnsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.returns.accessors.ReturnsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.returns.accessors.ReturnsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.returns.accessors.ReturnsAccessor.plots")
  * [ReturnsAccessor.alpha()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.alpha "vectorbt.returns.accessors.ReturnsAccessor.alpha")
  * [ReturnsAccessor.ann_factor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.ann_factor "vectorbt.returns.accessors.ReturnsAccessor.ann_factor")
  * [ReturnsAccessor.annual()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annual "vectorbt.returns.accessors.ReturnsAccessor.annual")
  * [ReturnsAccessor.annualized()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized "vectorbt.returns.accessors.ReturnsAccessor.annualized")
  * [ReturnsAccessor.annualized_volatility()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility "vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility")
  * [ReturnsAccessor.benchmark_rets](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.benchmark_rets "vectorbt.returns.accessors.ReturnsAccessor.benchmark_rets")
  * [ReturnsAccessor.beta()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.beta "vectorbt.returns.accessors.ReturnsAccessor.beta")
  * [ReturnsAccessor.calmar_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio "vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio")
  * [ReturnsAccessor.capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.capture "vectorbt.returns.accessors.ReturnsAccessor.capture")
  * [ReturnsAccessor.common_sense_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio "vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio")
  * [ReturnsAccessor.cond_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk")
  * [ReturnsAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.returns.accessors.ReturnsAccessor.config")
  * [ReturnsAccessor.cumulative()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.cumulative "vectorbt.returns.accessors.ReturnsAccessor.cumulative")
  * [ReturnsAccessor.daily()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.daily "vectorbt.returns.accessors.ReturnsAccessor.daily")
  * [ReturnsAccessor.defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.defaults "vectorbt.returns.accessors.ReturnsAccessor.defaults")
  * [ReturnsAccessor.deflated_sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.deflated_sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.deflated_sharpe_ratio")
  * [ReturnsAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.returns.accessors.ReturnsAccessor.df_accessor_cls")
  * [ReturnsAccessor.down_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.down_capture "vectorbt.returns.accessors.ReturnsAccessor.down_capture")
  * [ReturnsAccessor.downside_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.downside_risk "vectorbt.returns.accessors.ReturnsAccessor.downside_risk")
  * [ReturnsAccessor.drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.drawdown "vectorbt.returns.accessors.ReturnsAccessor.drawdown")
  * [ReturnsAccessor.drawdowns](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.drawdowns "vectorbt.returns.accessors.ReturnsAccessor.drawdowns")
  * [ReturnsAccessor.from_value()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.from_value "vectorbt.returns.accessors.ReturnsAccessor.from_value")
  * [ReturnsAccessor.get_drawdowns()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns "vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns")
  * [ReturnsAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.returns.accessors.ReturnsAccessor.iloc")
  * [ReturnsAccessor.indexing_func()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.indexing_func "vectorbt.returns.accessors.ReturnsAccessor.indexing_func")
  * [ReturnsAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.returns.accessors.ReturnsAccessor.indexing_kwargs")
  * [ReturnsAccessor.information_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.information_ratio "vectorbt.returns.accessors.ReturnsAccessor.information_ratio")
  * [ReturnsAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.returns.accessors.ReturnsAccessor.loc")
  * [ReturnsAccessor.mapping](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mapping "vectorbt.returns.accessors.ReturnsAccessor.mapping")
  * [ReturnsAccessor.max_drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.max_drawdown "vectorbt.returns.accessors.ReturnsAccessor.max_drawdown")
  * [ReturnsAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.returns.accessors.ReturnsAccessor.obj")
  * [ReturnsAccessor.omega_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.omega_ratio "vectorbt.returns.accessors.ReturnsAccessor.omega_ratio")
  * [ReturnsAccessor.plots_defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.plots_defaults "vectorbt.returns.accessors.ReturnsAccessor.plots_defaults")
  * [ReturnsAccessor.qs](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.qs "vectorbt.returns.accessors.ReturnsAccessor.qs")
  * [ReturnsAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.returns.accessors.ReturnsAccessor.ranges")
  * [ReturnsAccessor.resolve_self()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.resolve_self "vectorbt.returns.accessors.ReturnsAccessor.resolve_self")
  * [ReturnsAccessor.rolling_alpha()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_alpha "vectorbt.returns.accessors.ReturnsAccessor.rolling_alpha")
  * [ReturnsAccessor.rolling_annualized()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized "vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized")
  * [ReturnsAccessor.rolling_annualized_volatility()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized_volatility "vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized_volatility")
  * [ReturnsAccessor.rolling_beta()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_beta "vectorbt.returns.accessors.ReturnsAccessor.rolling_beta")
  * [ReturnsAccessor.rolling_calmar_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_calmar_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_calmar_ratio")
  * [ReturnsAccessor.rolling_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_capture")
  * [ReturnsAccessor.rolling_common_sense_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_common_sense_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_common_sense_ratio")
  * [ReturnsAccessor.rolling_cond_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_cond_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_cond_value_at_risk")
  * [ReturnsAccessor.rolling_down_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_down_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_down_capture")
  * [ReturnsAccessor.rolling_downside_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_downside_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_downside_risk")
  * [ReturnsAccessor.rolling_information_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_information_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_information_ratio")
  * [ReturnsAccessor.rolling_max_drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_max_drawdown "vectorbt.returns.accessors.ReturnsAccessor.rolling_max_drawdown")
  * [ReturnsAccessor.rolling_omega_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_omega_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_omega_ratio")
  * [ReturnsAccessor.rolling_sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio")
  * [ReturnsAccessor.rolling_sortino_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_sortino_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_sortino_ratio")
  * [ReturnsAccessor.rolling_tail_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_tail_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_tail_ratio")
  * [ReturnsAccessor.rolling_total()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_total "vectorbt.returns.accessors.ReturnsAccessor.rolling_total")
  * [ReturnsAccessor.rolling_up_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_up_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_up_capture")
  * [ReturnsAccessor.rolling_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_value_at_risk")
  * [ReturnsAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.returns.accessors.ReturnsAccessor.self_aliases")
  * [ReturnsAccessor.sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio")
  * [ReturnsAccessor.sortino_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio "vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio")
  * [ReturnsAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.returns.accessors.ReturnsAccessor.sr_accessor_cls")
  * [ReturnsAccessor.stats_defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.stats_defaults "vectorbt.returns.accessors.ReturnsAccessor.stats_defaults")
  * [ReturnsAccessor.tail_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.tail_ratio "vectorbt.returns.accessors.ReturnsAccessor.tail_ratio")
  * [ReturnsAccessor.total()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.total "vectorbt.returns.accessors.ReturnsAccessor.total")
  * [ReturnsAccessor.up_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.up_capture "vectorbt.returns.accessors.ReturnsAccessor.up_capture")
  * [ReturnsAccessor.value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.value_at_risk")
  * [ReturnsAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.returns.accessors.ReturnsAccessor.wrapper")
  * [ReturnsAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.returns.accessors.ReturnsAccessor.writeable_attrs")
  * [ReturnsAccessor.year_freq](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.year_freq "vectorbt.returns.accessors.ReturnsAccessor.year_freq")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.returns.accessors.ReturnsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.returns.accessors.ReturnsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.returns.accessors.ReturnsAccessor.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.returns.accessors.ReturnsAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.returns.accessors.ReturnsAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.returns.accessors.ReturnsAccessor.select_one_from_obj")



* * *

## ReturnsSRAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L1114-L1240 "Jump to source")¶
    
    
    ReturnsSRAccessor(
        obj,
        benchmark_rets=None,
        year_freq=None,
        defaults=None,
        **kwargs
    )
    

Accessor on top of return series. For Series only.

Accessible through `pd.Series.vbt.returns`.

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
  * [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.returns.accessors.ReturnsAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.returns.accessors.ReturnsAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.returns.accessors.ReturnsAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.returns.accessors.ReturnsAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.returns.accessors.ReturnsAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.returns.accessors.ReturnsAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.returns.accessors.ReturnsAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.returns.accessors.ReturnsAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.returns.accessors.ReturnsAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.returns.accessors.ReturnsAccessor.concat")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.returns.accessors.ReturnsAccessor.drop_redundant_levels")
  * [BaseAccessor.empty()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty "vectorbt.returns.accessors.ReturnsAccessor.empty")
  * [BaseAccessor.empty_like()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty_like "vectorbt.returns.accessors.ReturnsAccessor.empty_like")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.returns.accessors.ReturnsAccessor.make_symmetric")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.returns.accessors.ReturnsAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.returns.accessors.ReturnsAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.returns.accessors.ReturnsAccessor.select_levels")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.returns.accessors.ReturnsAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.returns.accessors.ReturnsAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.returns.accessors.ReturnsAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.returns.accessors.ReturnsAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.returns.accessors.ReturnsAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.returns.accessors.ReturnsAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.returns.accessors.ReturnsAccessor.unstack_to_df")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.returns.accessors.ReturnsAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.returns.accessors.ReturnsAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.returns.accessors.ReturnsAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.returns.accessors.ReturnsAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.returns.accessors.ReturnsAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.returns.accessors.ReturnsAccessor.update_config")
  * [GenericAccessor.apply_along_axis()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_along_axis "vectorbt.returns.accessors.ReturnsAccessor.apply_along_axis")
  * [GenericAccessor.apply_and_reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_and_reduce "vectorbt.returns.accessors.ReturnsAccessor.apply_and_reduce")
  * [GenericAccessor.apply_mapping()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.apply_mapping "vectorbt.returns.accessors.ReturnsAccessor.apply_mapping")
  * [GenericAccessor.applymap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.applymap "vectorbt.returns.accessors.ReturnsAccessor.applymap")
  * [GenericAccessor.barplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.barplot "vectorbt.returns.accessors.ReturnsAccessor.barplot")
  * [GenericAccessor.bfill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bfill "vectorbt.returns.accessors.ReturnsAccessor.bfill")
  * [GenericAccessor.binarize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.binarize "vectorbt.returns.accessors.ReturnsAccessor.binarize")
  * [GenericAccessor.boxplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.boxplot "vectorbt.returns.accessors.ReturnsAccessor.boxplot")
  * [GenericAccessor.bshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.bshift "vectorbt.returns.accessors.ReturnsAccessor.bshift")
  * [GenericAccessor.count()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.count "vectorbt.returns.accessors.ReturnsAccessor.count")
  * [GenericAccessor.crossed_above()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_above "vectorbt.returns.accessors.ReturnsAccessor.crossed_above")
  * [GenericAccessor.crossed_below()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.crossed_below "vectorbt.returns.accessors.ReturnsAccessor.crossed_below")
  * [GenericAccessor.cumprod()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumprod "vectorbt.returns.accessors.ReturnsAccessor.cumprod")
  * [GenericAccessor.cumsum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.cumsum "vectorbt.returns.accessors.ReturnsAccessor.cumsum")
  * [GenericAccessor.describe()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.describe "vectorbt.returns.accessors.ReturnsAccessor.describe")
  * [GenericAccessor.diff()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.diff "vectorbt.returns.accessors.ReturnsAccessor.diff")
  * [GenericAccessor.ewm_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_mean "vectorbt.returns.accessors.ReturnsAccessor.ewm_mean")
  * [GenericAccessor.ewm_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ewm_std "vectorbt.returns.accessors.ReturnsAccessor.ewm_std")
  * [GenericAccessor.expanding_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_apply "vectorbt.returns.accessors.ReturnsAccessor.expanding_apply")
  * [GenericAccessor.expanding_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_max "vectorbt.returns.accessors.ReturnsAccessor.expanding_max")
  * [GenericAccessor.expanding_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_mean "vectorbt.returns.accessors.ReturnsAccessor.expanding_mean")
  * [GenericAccessor.expanding_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_min "vectorbt.returns.accessors.ReturnsAccessor.expanding_min")
  * [GenericAccessor.expanding_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_split "vectorbt.returns.accessors.ReturnsAccessor.expanding_split")
  * [GenericAccessor.expanding_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.expanding_std "vectorbt.returns.accessors.ReturnsAccessor.expanding_std")
  * [GenericAccessor.ffill()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ffill "vectorbt.returns.accessors.ReturnsAccessor.ffill")
  * [GenericAccessor.fillna()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fillna "vectorbt.returns.accessors.ReturnsAccessor.fillna")
  * [GenericAccessor.filter()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.filter "vectorbt.returns.accessors.ReturnsAccessor.filter")
  * [GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.returns.accessors.ReturnsAccessor.fshift")
  * [GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.returns.accessors.ReturnsAccessor.get_ranges")
  * [GenericAccessor.groupby_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.groupby_apply "vectorbt.returns.accessors.ReturnsAccessor.groupby_apply")
  * [GenericAccessor.histplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.histplot "vectorbt.returns.accessors.ReturnsAccessor.histplot")
  * [GenericAccessor.idxmax()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmax "vectorbt.returns.accessors.ReturnsAccessor.idxmax")
  * [GenericAccessor.idxmin()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.idxmin "vectorbt.returns.accessors.ReturnsAccessor.idxmin")
  * [GenericAccessor.lineplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.lineplot "vectorbt.returns.accessors.ReturnsAccessor.lineplot")
  * [GenericAccessor.max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.max "vectorbt.returns.accessors.ReturnsAccessor.max")
  * [GenericAccessor.maxabs_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.maxabs_scale "vectorbt.returns.accessors.ReturnsAccessor.maxabs_scale")
  * [GenericAccessor.mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mean "vectorbt.returns.accessors.ReturnsAccessor.mean")
  * [GenericAccessor.median()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.median "vectorbt.returns.accessors.ReturnsAccessor.median")
  * [GenericAccessor.min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.min "vectorbt.returns.accessors.ReturnsAccessor.min")
  * [GenericAccessor.minmax_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.minmax_scale "vectorbt.returns.accessors.ReturnsAccessor.minmax_scale")
  * [GenericAccessor.normalize()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.normalize "vectorbt.returns.accessors.ReturnsAccessor.normalize")
  * [GenericAccessor.pct_change()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.pct_change "vectorbt.returns.accessors.ReturnsAccessor.pct_change")
  * [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.returns.accessors.ReturnsAccessor.plot")
  * [GenericAccessor.power_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.power_transform "vectorbt.returns.accessors.ReturnsAccessor.power_transform")
  * [GenericAccessor.product()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.product "vectorbt.returns.accessors.ReturnsAccessor.product")
  * [GenericAccessor.quantile_transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.quantile_transform "vectorbt.returns.accessors.ReturnsAccessor.quantile_transform")
  * [GenericAccessor.range_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.range_split "vectorbt.returns.accessors.ReturnsAccessor.range_split")
  * [GenericAccessor.rebase()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rebase "vectorbt.returns.accessors.ReturnsAccessor.rebase")
  * [GenericAccessor.reduce()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.reduce "vectorbt.returns.accessors.ReturnsAccessor.reduce")
  * [GenericAccessor.resample_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.resample_apply "vectorbt.returns.accessors.ReturnsAccessor.resample_apply")
  * [GenericAccessor.robust_scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.robust_scale "vectorbt.returns.accessors.ReturnsAccessor.robust_scale")
  * [GenericAccessor.rolling_apply()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_apply "vectorbt.returns.accessors.ReturnsAccessor.rolling_apply")
  * [GenericAccessor.rolling_max()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_max "vectorbt.returns.accessors.ReturnsAccessor.rolling_max")
  * [GenericAccessor.rolling_mean()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_mean "vectorbt.returns.accessors.ReturnsAccessor.rolling_mean")
  * [GenericAccessor.rolling_min()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_min "vectorbt.returns.accessors.ReturnsAccessor.rolling_min")
  * [GenericAccessor.rolling_split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_split "vectorbt.returns.accessors.ReturnsAccessor.rolling_split")
  * [GenericAccessor.rolling_std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.rolling_std "vectorbt.returns.accessors.ReturnsAccessor.rolling_std")
  * [GenericAccessor.scale()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scale "vectorbt.returns.accessors.ReturnsAccessor.scale")
  * [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.returns.accessors.ReturnsAccessor.scatterplot")
  * [GenericAccessor.shuffle()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.shuffle "vectorbt.returns.accessors.ReturnsAccessor.shuffle")
  * [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.returns.accessors.ReturnsAccessor.split")
  * [GenericAccessor.std()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.std "vectorbt.returns.accessors.ReturnsAccessor.std")
  * [GenericAccessor.sum()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.sum "vectorbt.returns.accessors.ReturnsAccessor.sum")
  * [GenericAccessor.to_mapped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_mapped "vectorbt.returns.accessors.ReturnsAccessor.to_mapped")
  * [GenericAccessor.to_returns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.to_returns "vectorbt.returns.accessors.ReturnsAccessor.to_returns")
  * [GenericAccessor.transform()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.transform "vectorbt.returns.accessors.ReturnsAccessor.transform")
  * [GenericAccessor.value_counts()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.value_counts "vectorbt.returns.accessors.ReturnsAccessor.value_counts")
  * [GenericAccessor.zscore()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.zscore "vectorbt.returns.accessors.ReturnsAccessor.zscore")
  * [GenericSRAccessor.flatten_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.flatten_grouped "vectorbt.generic.accessors.GenericSRAccessor.flatten_grouped")
  * [GenericSRAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.heatmap "vectorbt.generic.accessors.GenericSRAccessor.heatmap")
  * [GenericSRAccessor.overlay_with_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.overlay_with_heatmap "vectorbt.generic.accessors.GenericSRAccessor.overlay_with_heatmap")
  * [GenericSRAccessor.plot_against()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.plot_against "vectorbt.generic.accessors.GenericSRAccessor.plot_against")
  * [GenericSRAccessor.qqplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.qqplot "vectorbt.generic.accessors.GenericSRAccessor.qqplot")
  * [GenericSRAccessor.squeeze_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.squeeze_grouped "vectorbt.generic.accessors.GenericSRAccessor.squeeze_grouped")
  * [GenericSRAccessor.ts_heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.ts_heatmap "vectorbt.generic.accessors.GenericSRAccessor.ts_heatmap")
  * [GenericSRAccessor.volume()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor.volume "vectorbt.generic.accessors.GenericSRAccessor.volume")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.returns.accessors.ReturnsAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.returns.accessors.ReturnsAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.returns.accessors.ReturnsAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.returns.accessors.ReturnsAccessor.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.returns.accessors.ReturnsAccessor.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.returns.accessors.ReturnsAccessor.plots")
  * [ReturnsAccessor.alpha()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.alpha "vectorbt.returns.accessors.ReturnsAccessor.alpha")
  * [ReturnsAccessor.ann_factor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.ann_factor "vectorbt.returns.accessors.ReturnsAccessor.ann_factor")
  * [ReturnsAccessor.annual()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annual "vectorbt.returns.accessors.ReturnsAccessor.annual")
  * [ReturnsAccessor.annualized()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized "vectorbt.returns.accessors.ReturnsAccessor.annualized")
  * [ReturnsAccessor.annualized_volatility()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility "vectorbt.returns.accessors.ReturnsAccessor.annualized_volatility")
  * [ReturnsAccessor.benchmark_rets](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.benchmark_rets "vectorbt.returns.accessors.ReturnsAccessor.benchmark_rets")
  * [ReturnsAccessor.beta()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.beta "vectorbt.returns.accessors.ReturnsAccessor.beta")
  * [ReturnsAccessor.calmar_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio "vectorbt.returns.accessors.ReturnsAccessor.calmar_ratio")
  * [ReturnsAccessor.capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.capture "vectorbt.returns.accessors.ReturnsAccessor.capture")
  * [ReturnsAccessor.common_sense_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio "vectorbt.returns.accessors.ReturnsAccessor.common_sense_ratio")
  * [ReturnsAccessor.cond_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.cond_value_at_risk")
  * [ReturnsAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.returns.accessors.ReturnsAccessor.config")
  * [ReturnsAccessor.cumulative()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.cumulative "vectorbt.returns.accessors.ReturnsAccessor.cumulative")
  * [ReturnsAccessor.daily()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.daily "vectorbt.returns.accessors.ReturnsAccessor.daily")
  * [ReturnsAccessor.defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.defaults "vectorbt.returns.accessors.ReturnsAccessor.defaults")
  * [ReturnsAccessor.deflated_sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.deflated_sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.deflated_sharpe_ratio")
  * [ReturnsAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.returns.accessors.ReturnsAccessor.df_accessor_cls")
  * [ReturnsAccessor.down_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.down_capture "vectorbt.returns.accessors.ReturnsAccessor.down_capture")
  * [ReturnsAccessor.downside_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.downside_risk "vectorbt.returns.accessors.ReturnsAccessor.downside_risk")
  * [ReturnsAccessor.drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.drawdown "vectorbt.returns.accessors.ReturnsAccessor.drawdown")
  * [ReturnsAccessor.drawdowns](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.drawdowns "vectorbt.returns.accessors.ReturnsAccessor.drawdowns")
  * [ReturnsAccessor.from_value()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.from_value "vectorbt.returns.accessors.ReturnsAccessor.from_value")
  * [ReturnsAccessor.get_drawdowns()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns "vectorbt.returns.accessors.ReturnsAccessor.get_drawdowns")
  * [ReturnsAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.returns.accessors.ReturnsAccessor.iloc")
  * [ReturnsAccessor.indexing_func()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.indexing_func "vectorbt.returns.accessors.ReturnsAccessor.indexing_func")
  * [ReturnsAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.returns.accessors.ReturnsAccessor.indexing_kwargs")
  * [ReturnsAccessor.information_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.information_ratio "vectorbt.returns.accessors.ReturnsAccessor.information_ratio")
  * [ReturnsAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.returns.accessors.ReturnsAccessor.loc")
  * [ReturnsAccessor.mapping](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.mapping "vectorbt.returns.accessors.ReturnsAccessor.mapping")
  * [ReturnsAccessor.max_drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.max_drawdown "vectorbt.returns.accessors.ReturnsAccessor.max_drawdown")
  * [ReturnsAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.returns.accessors.ReturnsAccessor.obj")
  * [ReturnsAccessor.omega_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.omega_ratio "vectorbt.returns.accessors.ReturnsAccessor.omega_ratio")
  * [ReturnsAccessor.plots_defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.plots_defaults "vectorbt.returns.accessors.ReturnsAccessor.plots_defaults")
  * [ReturnsAccessor.qs](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.qs "vectorbt.returns.accessors.ReturnsAccessor.qs")
  * [ReturnsAccessor.ranges](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.ranges "vectorbt.returns.accessors.ReturnsAccessor.ranges")
  * [ReturnsAccessor.resolve_self()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.resolve_self "vectorbt.returns.accessors.ReturnsAccessor.resolve_self")
  * [ReturnsAccessor.rolling_alpha()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_alpha "vectorbt.returns.accessors.ReturnsAccessor.rolling_alpha")
  * [ReturnsAccessor.rolling_annualized()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized "vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized")
  * [ReturnsAccessor.rolling_annualized_volatility()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized_volatility "vectorbt.returns.accessors.ReturnsAccessor.rolling_annualized_volatility")
  * [ReturnsAccessor.rolling_beta()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_beta "vectorbt.returns.accessors.ReturnsAccessor.rolling_beta")
  * [ReturnsAccessor.rolling_calmar_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_calmar_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_calmar_ratio")
  * [ReturnsAccessor.rolling_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_capture")
  * [ReturnsAccessor.rolling_common_sense_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_common_sense_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_common_sense_ratio")
  * [ReturnsAccessor.rolling_cond_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_cond_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_cond_value_at_risk")
  * [ReturnsAccessor.rolling_down_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_down_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_down_capture")
  * [ReturnsAccessor.rolling_downside_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_downside_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_downside_risk")
  * [ReturnsAccessor.rolling_information_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_information_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_information_ratio")
  * [ReturnsAccessor.rolling_max_drawdown()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_max_drawdown "vectorbt.returns.accessors.ReturnsAccessor.rolling_max_drawdown")
  * [ReturnsAccessor.rolling_omega_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_omega_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_omega_ratio")
  * [ReturnsAccessor.rolling_sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_sharpe_ratio")
  * [ReturnsAccessor.rolling_sortino_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_sortino_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_sortino_ratio")
  * [ReturnsAccessor.rolling_tail_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_tail_ratio "vectorbt.returns.accessors.ReturnsAccessor.rolling_tail_ratio")
  * [ReturnsAccessor.rolling_total()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_total "vectorbt.returns.accessors.ReturnsAccessor.rolling_total")
  * [ReturnsAccessor.rolling_up_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_up_capture "vectorbt.returns.accessors.ReturnsAccessor.rolling_up_capture")
  * [ReturnsAccessor.rolling_value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.rolling_value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.rolling_value_at_risk")
  * [ReturnsAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.returns.accessors.ReturnsAccessor.self_aliases")
  * [ReturnsAccessor.sharpe_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio "vectorbt.returns.accessors.ReturnsAccessor.sharpe_ratio")
  * [ReturnsAccessor.sortino_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio "vectorbt.returns.accessors.ReturnsAccessor.sortino_ratio")
  * [ReturnsAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.returns.accessors.ReturnsAccessor.sr_accessor_cls")
  * [ReturnsAccessor.stats_defaults](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.stats_defaults "vectorbt.returns.accessors.ReturnsAccessor.stats_defaults")
  * [ReturnsAccessor.tail_ratio()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.tail_ratio "vectorbt.returns.accessors.ReturnsAccessor.tail_ratio")
  * [ReturnsAccessor.total()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.total "vectorbt.returns.accessors.ReturnsAccessor.total")
  * [ReturnsAccessor.up_capture()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.up_capture "vectorbt.returns.accessors.ReturnsAccessor.up_capture")
  * [ReturnsAccessor.value_at_risk()](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.value_at_risk "vectorbt.returns.accessors.ReturnsAccessor.value_at_risk")
  * [ReturnsAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.returns.accessors.ReturnsAccessor.wrapper")
  * [ReturnsAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.returns.accessors.ReturnsAccessor.writeable_attrs")
  * [ReturnsAccessor.year_freq](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor.year_freq "vectorbt.returns.accessors.ReturnsAccessor.year_freq")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.returns.accessors.ReturnsAccessor.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.returns.accessors.ReturnsAccessor.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.returns.accessors.ReturnsAccessor.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.returns.accessors.ReturnsAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.returns.accessors.ReturnsAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.returns.accessors.ReturnsAccessor.select_one_from_obj")



* * *

### plot_cumulative method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/returns/accessors.py#L1136-L1240 "Jump to source")¶
    
    
    ReturnsSRAccessor.plot_cumulative(
        benchmark_rets=None,
        start_value=1,
        fill_to_benchmark=False,
        main_kwargs=None,
        benchmark_kwargs=None,
        hline_shape_kwargs=None,
        add_trace_kwargs=None,
        xref='x',
        yref='y',
        fig=None,
        **layout_kwargs
    )
    

Plot cumulative returns.

**Args**

**`benchmark_rets`** : `array_like`
    Benchmark return to compare returns against. Will broadcast per element.
**`start_value`** : `float`
    The starting returns.
**`fill_to_benchmark`** : `bool`
    Whether to fill between main and benchmark, or between main and `start_value`.
**`main_kwargs`** : `dict`
    Keyword arguments passed to [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericSRAccessor.plot") for main.
**`benchmark_kwargs`** : `dict`
    Keyword arguments passed to [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericSRAccessor.plot") for benchmark.
**`hline_shape_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Figure.add_shape` for `start_value` line.
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
    
    
    >>> import pandas as pd
    >>> import numpy as np
    
    >>> np.random.seed(0)
    >>> rets = pd.Series(np.random.uniform(-0.05, 0.05, size=100))
    >>> benchmark_rets = pd.Series(np.random.uniform(-0.05, 0.05, size=100))
    >>> rets.vbt.returns.plot_cumulative(benchmark_rets=benchmark_rets)
    

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
