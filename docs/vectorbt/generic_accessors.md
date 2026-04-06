# accessors - VectorBT

> **Source:** https://vectorbt.dev/api/generic/accessors/

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
      * accessors  [ accessors  ](https://vectorbt.dev/api/generic/accessors/) Table of contents 
        * Stats 
          * Mapping 
        * Plots 
        * nb_config 
        * transform_config 
        * GenericAccessor() 
          * apply_along_axis() 
          * apply_and_reduce() 
          * apply_mapping() 
          * applymap() 
          * barplot() 
          * bfill() 
          * binarize() 
          * boxplot() 
          * bshift() 
          * count() 
          * crossed_above() 
          * crossed_below() 
          * cumprod() 
          * cumsum() 
          * describe() 
          * diff() 
          * drawdown() 
          * drawdowns 
          * ewm_mean() 
          * ewm_std() 
          * expanding_apply() 
          * expanding_max() 
          * expanding_mean() 
          * expanding_min() 
          * expanding_split() 
          * expanding_std() 
          * ffill() 
          * fillna() 
          * filter() 
          * fshift() 
          * get_drawdowns() 
          * get_ranges() 
          * groupby_apply() 
          * histplot() 
          * idxmax() 
          * idxmin() 
          * lineplot() 
          * mapping 
          * max() 
          * maxabs_scale() 
          * mean() 
          * median() 
          * metrics 
          * min() 
          * minmax_scale() 
          * normalize() 
          * pct_change() 
          * plot() 
          * plots_defaults 
          * power_transform() 
          * product() 
          * quantile_transform() 
          * range_split() 
          * ranges 
          * rebase() 
          * reduce() 
          * resample_apply() 
          * resolve_self() 
          * robust_scale() 
          * rolling_apply() 
          * rolling_max() 
          * rolling_mean() 
          * rolling_min() 
          * rolling_split() 
          * rolling_std() 
          * scale() 
          * scatterplot() 
          * shuffle() 
          * split() 
          * stats_defaults 
          * std() 
          * subplots 
          * sum() 
          * to_mapped() 
          * to_returns() 
          * transform() 
          * value_counts() 
          * zscore() 
        * GenericDFAccessor() 
          * flatten_grouped() 
          * heatmap() 
          * squeeze_grouped() 
          * ts_heatmap() 
        * GenericSRAccessor() 
          * flatten_grouped() 
          * heatmap() 
          * overlay_with_heatmap() 
          * plot_against() 
          * qqplot() 
          * squeeze_grouped() 
          * ts_heatmap() 
          * volume() 
        * MetaGenericAccessor() 
        * TransformerT() 
          * fit_transform() 
          * transform() 
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
    * Mapping 
  * Plots 
  * nb_config 
  * transform_config 
  * GenericAccessor() 
    * apply_along_axis() 
    * apply_and_reduce() 
    * apply_mapping() 
    * applymap() 
    * barplot() 
    * bfill() 
    * binarize() 
    * boxplot() 
    * bshift() 
    * count() 
    * crossed_above() 
    * crossed_below() 
    * cumprod() 
    * cumsum() 
    * describe() 
    * diff() 
    * drawdown() 
    * drawdowns 
    * ewm_mean() 
    * ewm_std() 
    * expanding_apply() 
    * expanding_max() 
    * expanding_mean() 
    * expanding_min() 
    * expanding_split() 
    * expanding_std() 
    * ffill() 
    * fillna() 
    * filter() 
    * fshift() 
    * get_drawdowns() 
    * get_ranges() 
    * groupby_apply() 
    * histplot() 
    * idxmax() 
    * idxmin() 
    * lineplot() 
    * mapping 
    * max() 
    * maxabs_scale() 
    * mean() 
    * median() 
    * metrics 
    * min() 
    * minmax_scale() 
    * normalize() 
    * pct_change() 
    * plot() 
    * plots_defaults 
    * power_transform() 
    * product() 
    * quantile_transform() 
    * range_split() 
    * ranges 
    * rebase() 
    * reduce() 
    * resample_apply() 
    * resolve_self() 
    * robust_scale() 
    * rolling_apply() 
    * rolling_max() 
    * rolling_mean() 
    * rolling_min() 
    * rolling_split() 
    * rolling_std() 
    * scale() 
    * scatterplot() 
    * shuffle() 
    * split() 
    * stats_defaults 
    * std() 
    * subplots 
    * sum() 
    * to_mapped() 
    * to_returns() 
    * transform() 
    * value_counts() 
    * zscore() 
  * GenericDFAccessor() 
    * flatten_grouped() 
    * heatmap() 
    * squeeze_grouped() 
    * ts_heatmap() 
  * GenericSRAccessor() 
    * flatten_grouped() 
    * heatmap() 
    * overlay_with_heatmap() 
    * plot_against() 
    * qqplot() 
    * squeeze_grouped() 
    * ts_heatmap() 
    * volume() 
  * MetaGenericAccessor() 
  * TransformerT() 
    * fit_transform() 
    * transform() 



# accessors module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py "Jump to source")¶

Custom pandas accessors for generic data.

Methods can be accessed as follows:

  * [GenericSRAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor "vectorbt.generic.accessors.GenericSRAccessor") -> `pd.Series.vbt.*`
  * [GenericDFAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor "vectorbt.generic.accessors.GenericDFAccessor") -> `pd.DataFrame.vbt.*`


    
    
    >>> import pandas as pd
    >>> import vectorbt as vbt
    
    >>> # vectorbt.generic.accessors.GenericAccessor.rolling_mean
    >>> pd.Series([1, 2, 3, 4]).vbt.rolling_mean(2)
    0    NaN
    1    1.5
    2    2.5
    3    3.5
    dtype: float64
    

The accessors inherit [vectorbt.base.accessors](https://vectorbt.dev/api/base/accessors/ "vectorbt.base.accessors") and are inherited by more specialized accessors, such as [vectorbt.signals.accessors](https://vectorbt.dev/api/signals/accessors/ "vectorbt.signals.accessors") and [vectorbt.returns.accessors](https://vectorbt.dev/api/returns/accessors/ "vectorbt.returns.accessors").

Note

Grouping is only supported by the methods that accept the `group_by` argument.

Accessors do not utilize caching.

**Run for the examples below**
    
    
    >>> import vectorbt as vbt
    >>> import numpy as np
    >>> import pandas as pd
    >>> from numba import njit
    >>> from datetime import datetime, timedelta
    
    >>> df = pd.DataFrame({
    ...     'a': [1, 2, 3, 4, 5],
    ...     'b': [5, 4, 3, 2, 1],
    ...     'c': [1, 2, 3, 2, 1]
    ... }, index=pd.Index([
    ...     datetime(2020, 1, 1),
    ...     datetime(2020, 1, 2),
    ...     datetime(2020, 1, 3),
    ...     datetime(2020, 1, 4),
    ...     datetime(2020, 1, 5)
    ... ]))
    >>> df
                a  b  c
    2020-01-01  1  5  1
    2020-01-02  2  4  2
    2020-01-03  3  3  3
    2020-01-04  4  2  2
    2020-01-05  5  1  1
    
    >>> index = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(10)]
    >>> sr = pd.Series(np.arange(len(index)), index=index)
    >>> sr
    2020-01-01    0
    2020-01-02    1
    2020-01-03    2
    2020-01-04    3
    2020-01-05    4
    2020-01-06    5
    2020-01-07    6
    2020-01-08    7
    2020-01-09    8
    2020-01-10    9
    dtype: int64
    

## Stats¶

Hint

See [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats") and [GenericAccessor.metrics](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.metrics "vectorbt.generic.accessors.GenericAccessor.metrics").
    
    
    >>> df2 = pd.DataFrame({
    ...     'a': [np.nan, 2, 3],
    ...     'b': [4, np.nan, 5],
    ...     'c': [6, 7, np.nan]
    ... }, index=['x', 'y', 'z'])
    
    >>> df2.vbt(freq='d').stats(column='a')
    Start                      x
    End                        z
    Period       3 days 00:00:00
    Count                      2
    Mean                     2.5
    Std                 0.707107
    Min                      2.0
    Median                   2.5
    Max                      3.0
    Min Index                  y
    Max Index                  z
    Name: a, dtype: object
    

### Mapping¶

Mapping can be set both in [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor") (preferred) and [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.accessors.GenericAccessor.stats"):
    
    
    >>> mapping = {x: 'test_' + str(x) for x in pd.unique(df2.values.flatten())}
    >>> df2.vbt(freq='d', mapping=mapping).stats(column='a')
    Start                                   x
    End                                     z
    Period                    3 days 00:00:00
    Count                                   2
    Value Counts: test_2.0                  1
    Value Counts: test_3.0                  1
    Value Counts: test_4.0                  0
    Value Counts: test_5.0                  0
    Value Counts: test_6.0                  0
    Value Counts: test_7.0                  0
    Value Counts: test_nan                  1
    Name: a, dtype: object
    
    >>> df2.vbt(freq='d').stats(column='a', settings=dict(mapping=mapping))
    UserWarning: Changing the mapping will create a copy of this object.
    Consider setting it upon object creation to re-use existing cache.
    
    Start                                   x
    End                                     z
    Period                    3 days 00:00:00
    Count                                   2
    Value Counts: test_2.0                  1
    Value Counts: test_3.0                  1
    Value Counts: test_4.0                  0
    Value Counts: test_5.0                  0
    Value Counts: test_6.0                  0
    Value Counts: test_7.0                  0
    Value Counts: test_nan                  1
    Name: a, dtype: object
    

Selecting a column before calling `stats` will consider uniques from this column only:
    
    
    >>> df2['a'].vbt(freq='d', mapping=mapping).stats()
    Start                                   x
    End                                     z
    Period                    3 days 00:00:00
    Count                                   2
    Value Counts: test_2.0                  1
    Value Counts: test_3.0                  1
    Value Counts: test_nan                  1
    Name: a, dtype: object
    

To include all keys from `mapping`, pass `incl_all_keys=True`:

> > > df2['a'].vbt(freq='d', mapping=mapping).stats(settings=dict(incl_all_keys=True)) Start x End z Period 3 days 00:00:00 Count 2 Value Counts: test_2.0 1 Value Counts: test_3.0 1 Value Counts: test_4.0 0 Value Counts: test_5.0 0 Value Counts: test_6.0 0 Value Counts: test_7.0 0 Value Counts: test_nan 1 Name: a, dtype: object 
>>>     
>>>     
>>>     `GenericAccessor.stats` also supports (re-)grouping:
>>>     
>>>     ```pycon
>>>     >>> df2.vbt(freq='d').stats(column=0, group_by=[0, 0, 1])
>>>     Start                      x
>>>     End                        z
>>>     Period       3 days 00:00:00
>>>     Count                      4
>>>     Mean                     3.5
>>>     Std                 1.290994
>>>     Min                      2.0
>>>     Median                   3.5
>>>     Max                      5.0
>>>     Min Index                  y
>>>     Max Index                  z
>>>     Name: 0, dtype: object
>>>     

## Plots¶

Hint

See [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots") and [GenericAccessor.subplots](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.subplots "vectorbt.generic.accessors.GenericAccessor.subplots").

[GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor") class has a single subplot based on [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot"):
    
    
    >>> df2.vbt.plots()
    

* * *

## nb_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py "Jump to source")¶

Config of Numba methods to be added to [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").
    
    
    Config({
        "shuffle": {
            "func": "CPUDispatcher(<function shuffle_nb at 0x7f959807ad40>)",
            "path": "vectorbt.generic.nb.shuffle_nb"
        },
        "fillna": {
            "func": "CPUDispatcher(<function fillna_nb at 0x7f95980ec720>)",
            "path": "vectorbt.generic.nb.fillna_nb"
        },
        "bshift": {
            "func": "CPUDispatcher(<function bshift_nb at 0x7f95980ecea0>)",
            "path": "vectorbt.generic.nb.bshift_nb"
        },
        "fshift": {
            "func": "CPUDispatcher(<function fshift_nb at 0x7f959807a3e0>)",
            "path": "vectorbt.generic.nb.fshift_nb"
        },
        "diff": {
            "func": "CPUDispatcher(<function diff_nb at 0x7f9598079e40>)",
            "path": "vectorbt.generic.nb.diff_nb"
        },
        "pct_change": {
            "func": "CPUDispatcher(<function pct_change_nb at 0x7f95980ed440>)",
            "path": "vectorbt.generic.nb.pct_change_nb"
        },
        "bfill": {
            "func": "CPUDispatcher(<function bfill_nb at 0x7f95980ed800>)",
            "path": "vectorbt.generic.nb.bfill_nb"
        },
        "ffill": {
            "func": "CPUDispatcher(<function ffill_nb at 0x7f95980edd00>)",
            "path": "vectorbt.generic.nb.ffill_nb"
        },
        "cumsum": {
            "func": "CPUDispatcher(<function nancumsum_nb at 0x7f95980ee480>)",
            "path": "vectorbt.generic.nb.nancumsum_nb"
        },
        "cumprod": {
            "func": "CPUDispatcher(<function nancumprod_nb at 0x7f95980ee7a0>)",
            "path": "vectorbt.generic.nb.nancumprod_nb"
        },
        "rolling_min": {
            "func": "CPUDispatcher(<function rolling_min_nb at 0x7f95980f8220>)",
            "path": "vectorbt.generic.nb.rolling_min_nb"
        },
        "rolling_max": {
            "func": "CPUDispatcher(<function rolling_max_nb at 0x7f95980f8860>)",
            "path": "vectorbt.generic.nb.rolling_max_nb"
        },
        "rolling_mean": {
            "func": "CPUDispatcher(<function rolling_mean_nb at 0x7f95980f8ea0>)",
            "path": "vectorbt.generic.nb.rolling_mean_nb"
        },
        "expanding_min": {
            "func": "CPUDispatcher(<function expanding_min_nb at 0x7f95980fa5c0>)",
            "path": "vectorbt.generic.nb.expanding_min_nb"
        },
        "expanding_max": {
            "func": "CPUDispatcher(<function expanding_max_nb at 0x7f95980fac00>)",
            "path": "vectorbt.generic.nb.expanding_max_nb"
        },
        "expanding_mean": {
            "func": "CPUDispatcher(<function expanding_mean_nb at 0x7f95980fb240>)",
            "path": "vectorbt.generic.nb.expanding_mean_nb"
        },
        "product": {
            "func": "CPUDispatcher(<function nanprod_nb at 0x7f95980ee160>)",
            "is_reducing": true,
            "path": "vectorbt.generic.nb.nanprod_nb"
        }
    })
    

* * *

## transform_config Config[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py "Jump to source")¶

Config of transform methods to be added to [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").
    
    
    Config({
        "binarize": {
            "transformer": "<class 'sklearn.preprocessing._data.Binarizer'>",
            "docstring": "See `sklearn.preprocessing.Binarizer`."
        },
        "minmax_scale": {
            "transformer": "<class 'sklearn.preprocessing._data.MinMaxScaler'>",
            "docstring": "See `sklearn.preprocessing.MinMaxScaler`."
        },
        "maxabs_scale": {
            "transformer": "<class 'sklearn.preprocessing._data.MaxAbsScaler'>",
            "docstring": "See `sklearn.preprocessing.MaxAbsScaler`."
        },
        "normalize": {
            "transformer": "<class 'sklearn.preprocessing._data.Normalizer'>",
            "docstring": "See `sklearn.preprocessing.Normalizer`."
        },
        "robust_scale": {
            "transformer": "<class 'sklearn.preprocessing._data.RobustScaler'>",
            "docstring": "See `sklearn.preprocessing.RobustScaler`."
        },
        "scale": {
            "transformer": "<class 'sklearn.preprocessing._data.StandardScaler'>",
            "docstring": "See `sklearn.preprocessing.StandardScaler`."
        },
        "quantile_transform": {
            "transformer": "<class 'sklearn.preprocessing._data.QuantileTransformer'>",
            "docstring": "See `sklearn.preprocessing.QuantileTransformer`."
        },
        "power_transform": {
            "transformer": "<class 'sklearn.preprocessing._data.PowerTransformer'>",
            "docstring": "See `sklearn.preprocessing.PowerTransformer`."
        }
    })
    

* * *

## GenericAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L364-L1769 "Jump to source")¶
    
    
    GenericAccessor(
        obj,
        mapping=None,
        **kwargs
    )
    

Accessor on top of data of any type. For both, Series and DataFrames.

Accessible through `pd.Series.vbt` and `pd.DataFrame.vbt`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [Configured](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured "vectorbt.utils.config.Configured")
  * [Documented](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented "vectorbt.utils.docs.Documented")
  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")
  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * [Pickleable](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable "vectorbt.utils.config.Pickleable")
  * [PlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin "vectorbt.generic.plots_builder.PlotsBuilderMixin")
  * [StatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin "vectorbt.generic.stats_builder.StatsBuilderMixin")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



**Inherited members**

  * [AttrResolver.deep_getattr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.deep_getattr "vectorbt.base.accessors.BaseAccessor.deep_getattr")
  * [AttrResolver.post_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.post_resolve_attr "vectorbt.base.accessors.BaseAccessor.post_resolve_attr")
  * [AttrResolver.pre_resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.pre_resolve_attr "vectorbt.base.accessors.BaseAccessor.pre_resolve_attr")
  * [AttrResolver.resolve_attr()](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.resolve_attr "vectorbt.base.accessors.BaseAccessor.resolve_attr")
  * [BaseAccessor.align_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.align_to "vectorbt.base.accessors.BaseAccessor.align_to")
  * [BaseAccessor.apply()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply "vectorbt.base.accessors.BaseAccessor.apply")
  * [BaseAccessor.apply_and_concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_and_concat "vectorbt.base.accessors.BaseAccessor.apply_and_concat")
  * [BaseAccessor.apply_on_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.apply_on_index "vectorbt.base.accessors.BaseAccessor.apply_on_index")
  * [BaseAccessor.broadcast()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast "vectorbt.base.accessors.BaseAccessor.broadcast")
  * [BaseAccessor.broadcast_to()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.broadcast_to "vectorbt.base.accessors.BaseAccessor.broadcast_to")
  * [BaseAccessor.combine()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.combine "vectorbt.base.accessors.BaseAccessor.combine")
  * [BaseAccessor.concat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.concat "vectorbt.base.accessors.BaseAccessor.concat")
  * [BaseAccessor.config](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.config "vectorbt.base.accessors.BaseAccessor.config")
  * [BaseAccessor.df_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.df_accessor_cls "vectorbt.base.accessors.BaseAccessor.df_accessor_cls")
  * [BaseAccessor.drop_duplicate_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels "vectorbt.base.accessors.BaseAccessor.drop_duplicate_levels")
  * [BaseAccessor.drop_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_levels "vectorbt.base.accessors.BaseAccessor.drop_levels")
  * [BaseAccessor.drop_redundant_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.drop_redundant_levels "vectorbt.base.accessors.BaseAccessor.drop_redundant_levels")
  * [BaseAccessor.empty()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty "vectorbt.base.accessors.BaseAccessor.empty")
  * [BaseAccessor.empty_like()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.empty_like "vectorbt.base.accessors.BaseAccessor.empty_like")
  * [BaseAccessor.iloc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.iloc "vectorbt.base.accessors.BaseAccessor.iloc")
  * [BaseAccessor.indexing_func()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.indexing_func "vectorbt.base.accessors.BaseAccessor.indexing_func")
  * [BaseAccessor.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.indexing_kwargs "vectorbt.base.accessors.BaseAccessor.indexing_kwargs")
  * [BaseAccessor.loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.loc "vectorbt.base.accessors.BaseAccessor.loc")
  * [BaseAccessor.make_symmetric()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.make_symmetric "vectorbt.base.accessors.BaseAccessor.make_symmetric")
  * [BaseAccessor.obj](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.obj "vectorbt.base.accessors.BaseAccessor.obj")
  * [BaseAccessor.rename_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.rename_levels "vectorbt.base.accessors.BaseAccessor.rename_levels")
  * [BaseAccessor.repeat()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.repeat "vectorbt.base.accessors.BaseAccessor.repeat")
  * [BaseAccessor.select_levels()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.select_levels "vectorbt.base.accessors.BaseAccessor.select_levels")
  * [BaseAccessor.self_aliases](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver.self_aliases "vectorbt.base.accessors.BaseAccessor.self_aliases")
  * [BaseAccessor.sr_accessor_cls](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.sr_accessor_cls "vectorbt.base.accessors.BaseAccessor.sr_accessor_cls")
  * [BaseAccessor.stack_index()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.stack_index "vectorbt.base.accessors.BaseAccessor.stack_index")
  * [BaseAccessor.tile()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.tile "vectorbt.base.accessors.BaseAccessor.tile")
  * [BaseAccessor.to_1d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_1d_array "vectorbt.base.accessors.BaseAccessor.to_1d_array")
  * [BaseAccessor.to_2d_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_2d_array "vectorbt.base.accessors.BaseAccessor.to_2d_array")
  * [BaseAccessor.to_dict()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.to_dict "vectorbt.base.accessors.BaseAccessor.to_dict")
  * [BaseAccessor.unstack_to_array()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_array "vectorbt.base.accessors.BaseAccessor.unstack_to_array")
  * [BaseAccessor.unstack_to_df()](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor.unstack_to_df "vectorbt.base.accessors.BaseAccessor.unstack_to_df")
  * [BaseAccessor.wrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.wrapper "vectorbt.base.accessors.BaseAccessor.wrapper")
  * [BaseAccessor.writeable_attrs](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.writeable_attrs "vectorbt.base.accessors.BaseAccessor.writeable_attrs")
  * [Configured.copy()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.copy "vectorbt.base.accessors.BaseAccessor.copy")
  * [Configured.dumps()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.dumps "vectorbt.base.accessors.BaseAccessor.dumps")
  * [Configured.loads()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.loads "vectorbt.base.accessors.BaseAccessor.loads")
  * [Configured.replace()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.replace "vectorbt.base.accessors.BaseAccessor.replace")
  * [Configured.to_doc()](https://vectorbt.dev/api/utils/docs/#vectorbt.utils.docs.Documented.to_doc "vectorbt.base.accessors.BaseAccessor.to_doc")
  * [Configured.update_config()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Configured.update_config "vectorbt.base.accessors.BaseAccessor.update_config")
  * [PandasIndexer.xs()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer.xs "vectorbt.base.accessors.BaseAccessor.xs")
  * [Pickleable.load()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.load "vectorbt.base.accessors.BaseAccessor.load")
  * [Pickleable.save()](https://vectorbt.dev/api/utils/config/#vectorbt.utils.config.Pickleable.save "vectorbt.base.accessors.BaseAccessor.save")
  * [PlotsBuilderMixin.build_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc "vectorbt.generic.plots_builder.PlotsBuilderMixin.build_subplots_doc")
  * [PlotsBuilderMixin.override_subplots_doc()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc "vectorbt.generic.plots_builder.PlotsBuilderMixin.override_subplots_doc")
  * [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots")
  * [StatsBuilderMixin.build_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc "vectorbt.generic.stats_builder.StatsBuilderMixin.build_metrics_doc")
  * [StatsBuilderMixin.override_metrics_doc()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc "vectorbt.generic.stats_builder.StatsBuilderMixin.override_metrics_doc")
  * [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.stats_builder.StatsBuilderMixin.stats")
  * [Wrapping.regroup()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.regroup "vectorbt.base.accessors.BaseAccessor.regroup")
  * [Wrapping.select_one()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one "vectorbt.base.accessors.BaseAccessor.select_one")
  * [Wrapping.select_one_from_obj()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.select_one_from_obj "vectorbt.base.accessors.BaseAccessor.select_one_from_obj")



**Subclasses**

  * [GenericDFAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor "vectorbt.generic.accessors.GenericDFAccessor")
  * [GenericSRAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericSRAccessor "vectorbt.generic.accessors.GenericSRAccessor")
  * [ReturnsAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsAccessor "vectorbt.returns.accessors.ReturnsAccessor")
  * [SignalsAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsAccessor "vectorbt.signals.accessors.SignalsAccessor")



* * *

### apply_along_axis method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L428-L439 "Jump to source")¶
    
    
    GenericAccessor.apply_along_axis(
        apply_func_nb,
        *args,
        axis=0,
        wrap_kwargs=None
    )
    

Apply a function `apply_func_nb` along an axis.

* * *

### apply_and_reduce method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L639-L664 "Jump to source")¶
    
    
    GenericAccessor.apply_and_reduce(
        apply_func_nb,
        reduce_func_nb,
        apply_args=None,
        reduce_args=None,
        wrap_kwargs=None
    )
    

See [apply_and_reduce_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.apply_and_reduce_nb "vectorbt.generic.nb.apply_and_reduce_nb").

**Usage**
    
    
    >>> greater_nb = njit(lambda col, a: a[a > 2])
    >>> mean_nb = njit(lambda col, a: np.nanmean(a))
    >>> df.vbt.apply_and_reduce(greater_nb, mean_nb)
    a    4.0
    b    4.0
    c    3.0
    dtype: float64
    

* * *

### apply_mapping method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L400-L402 "Jump to source")¶
    
    
    GenericAccessor.apply_mapping(
        **kwargs
    )
    

See [apply_mapping()](https://vectorbt.dev/api/utils/mapping/#vectorbt.utils.mapping.apply_mapping "vectorbt.utils.mapping.apply_mapping").

* * *

### applymap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L597-L616 "Jump to source")¶
    
    
    GenericAccessor.applymap(
        apply_func_nb,
        *args,
        wrap_kwargs=None
    )
    

See [applymap_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.applymap_nb "vectorbt.generic.nb.applymap_nb").

**Usage**
    
    
    >>> multiply_nb = njit(lambda i, col, a: a ** 2)
    >>> df.vbt.applymap(multiply_nb)
                   a     b    c
    2020-01-01   1.0  25.0  1.0
    2020-01-02   4.0  16.0  4.0
    2020-01-03   9.0   9.0  9.0
    2020-01-04  16.0   4.0  4.0
    2020-01-05  25.0   1.0  1.0
    

* * *

### barplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1654-L1681 "Jump to source")¶
    
    
    GenericAccessor.barplot(
        trace_names=None,
        x_labels=None,
        return_fig=True,
        **kwargs
    )
    

Create [Bar](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Bar "vectorbt.generic.plotting.Bar") and return the figure.

**Usage**
    
    
    >>> df.vbt.barplot()
    

* * *

### bfill method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.bfill(
        *,
        wrap_kwargs=None
    )
    

See [bfill_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.bfill_nb "vectorbt.generic.nb.bfill_nb").

* * *

### binarize method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.binarize(
        *,
        threshold=0.0,
        copy=True,
        **kwargs
    )
    

See `sklearn.preprocessing.Binarizer`.

* * *

### boxplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1712-L1739 "Jump to source")¶
    
    
    GenericAccessor.boxplot(
        trace_names=None,
        group_by=None,
        return_fig=True,
        **kwargs
    )
    

Create [Box](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Box "vectorbt.generic.plotting.Box") and return the figure.

**Usage**
    
    
    >>> df.vbt.boxplot()
    

* * *

### bshift method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.bshift(
        n=1,
        fill_value=nan,
        *,
        wrap_kwargs=None
    )
    

See [bshift_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.bshift_nb "vectorbt.generic.nb.bshift_nb").

* * *

### count method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L866-L872 "Jump to source")¶
    
    
    GenericAccessor.count(
        group_by=None,
        wrap_kwargs=None
    )
    

Return count of non-NaN elements.

* * *

### crossed_above method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1225-L1261 "Jump to source")¶
    
    
    GenericAccessor.crossed_above(
        other,
        wait=0,
        broadcast_kwargs=None,
        wrap_kwargs=None
    )
    

Generate crossover above another array.

See [crossed_above_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.crossed_above_nb "vectorbt.generic.nb.crossed_above_nb").

**Usage**
    
    
    >>> df['b'].vbt.crossed_above(df['c'])
    2020-01-01    False
    2020-01-02    False
    2020-01-03    False
    2020-01-04    False
    2020-01-05    False
    dtype: bool
    >>> df['a'].vbt.crossed_above(df['b'])
    2020-01-01    False
    2020-01-02    False
    2020-01-03    False
    2020-01-04     True
    2020-01-05    False
    dtype: bool
    >>> df['a'].vbt.crossed_above(df['b'], wait=1)
    2020-01-01    False
    2020-01-02    False
    2020-01-03    False
    2020-01-04    False
    2020-01-05     True
    dtype: bool
    

* * *

### crossed_below method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1263-L1273 "Jump to source")¶
    
    
    GenericAccessor.crossed_below(
        other,
        wait=0,
        broadcast_kwargs=None,
        wrap_kwargs=None
    )
    

Generate crossover below another array.

See [crossed_above_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.crossed_above_nb "vectorbt.generic.nb.crossed_above_nb") but in reversed order.

* * *

### cumprod method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.cumprod(
        *,
        wrap_kwargs=None
    )
    

See [nancumprod_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.nancumprod_nb "vectorbt.generic.nb.nancumprod_nb").

* * *

### cumsum method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.cumsum(
        *,
        wrap_kwargs=None
    )
    

See [nancumsum_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.nancumsum_nb "vectorbt.generic.nb.nancumsum_nb").

* * *

### describe method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L914-L952 "Jump to source")¶
    
    
    GenericAccessor.describe(
        percentiles=None,
        ddof=1,
        group_by=None,
        wrap_kwargs=None
    )
    

See [describe_reduce_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.describe_reduce_nb "vectorbt.generic.nb.describe_reduce_nb").

For `percentiles`, see `pd.DataFrame.describe`.

**Usage**
    
    
    >>> df.vbt.describe()
                  a         b        c
    count  5.000000  5.000000  5.00000
    mean   3.000000  3.000000  1.80000
    std    1.581139  1.581139  0.83666
    min    1.000000  1.000000  1.00000
    25%    2.000000  2.000000  1.00000
    50%    3.000000  3.000000  2.00000
    75%    4.000000  4.000000  2.00000
    max    5.000000  5.000000  3.00000
    

* * *

### diff method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.diff(
        n=1,
        *,
        wrap_kwargs=None
    )
    

See [diff_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.diff_nb "vectorbt.generic.nb.diff_nb").

* * *

### drawdown method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1168-L1171 "Jump to source")¶
    
    
    GenericAccessor.drawdown(
        wrap_kwargs=None
    )
    

Drawdown series.

* * *

### drawdowns property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1185-L1188 "Jump to source")¶

[GenericAccessor.get_drawdowns()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_drawdowns "vectorbt.generic.accessors.GenericAccessor.get_drawdowns") with default arguments.

* * *

### ewm_mean method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L416-L420 "Jump to source")¶
    
    
    GenericAccessor.ewm_mean(
        span,
        minp=0,
        adjust=True,
        wrap_kwargs=None
    )
    

See [ewm_mean_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.ewm_mean_nb "vectorbt.generic.nb.ewm_mean_nb").

* * *

### ewm_std method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L422-L426 "Jump to source")¶
    
    
    GenericAccessor.ewm_std(
        span,
        minp=0,
        adjust=True,
        ddof=1,
        wrap_kwargs=None
    )
    

See [ewm_std_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.ewm_std_nb "vectorbt.generic.nb.ewm_std_nb").

* * *

### expanding_apply method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L476-L509 "Jump to source")¶
    
    
    GenericAccessor.expanding_apply(
        apply_func_nb,
        *args,
        minp=1,
        on_matrix=False,
        wrap_kwargs=None
    )
    

See [expanding_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_apply_nb "vectorbt.generic.nb.expanding_apply_nb") and [expanding_matrix_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_matrix_apply_nb "vectorbt.generic.nb.expanding_matrix_apply_nb") for `on_matrix=True`.

**Usage**
    
    
    >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
    >>> df.vbt.expanding_apply(mean_nb)
                  a    b    c
    2020-01-01  1.0  5.0  1.0
    2020-01-02  1.5  4.5  1.5
    2020-01-03  2.0  4.0  2.0
    2020-01-04  2.5  3.5  2.0
    2020-01-05  3.0  3.0  1.8
    
    >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
    >>> df.vbt.expanding_apply(mean_matrix_nb, on_matrix=True)
                       a         b         c
    2020-01-01  2.333333  2.333333  2.333333
    2020-01-02  2.500000  2.500000  2.500000
    2020-01-03  2.666667  2.666667  2.666667
    2020-01-04  2.666667  2.666667  2.666667
    2020-01-05  2.600000  2.600000  2.600000
    

* * *

### expanding_max method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.expanding_max(
        minp=1,
        *,
        wrap_kwargs=None
    )
    

See [expanding_max_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_max_nb "vectorbt.generic.nb.expanding_max_nb").

* * *

### expanding_mean method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.expanding_mean(
        minp=1,
        *,
        wrap_kwargs=None
    )
    

See [expanding_mean_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_mean_nb "vectorbt.generic.nb.expanding_mean_nb").

* * *

### expanding_min method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.expanding_min(
        minp=1,
        *,
        wrap_kwargs=None
    )
    

See [expanding_min_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_min_nb "vectorbt.generic.nb.expanding_min_nb").

* * *

### expanding_split method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1566-L1597 "Jump to source")¶
    
    
    GenericAccessor.expanding_split(
        **kwargs
    )
    

Split using [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.generic.accessors.GenericAccessor.split") on [ExpandingSplitter](https://vectorbt.dev/api/generic/splitters/#vectorbt.generic.splitters.ExpandingSplitter "vectorbt.generic.splitters.ExpandingSplitter").

**Usage**
    
    
    >>> train_set, valid_set, test_set = sr.vbt.expanding_split(
    ...     n=5, set_lens=(1, 1), min_len=3, left_to_right=False)
    >>> train_set[0]
    split_idx    0    1    2    3    4    5    6  7
    0          0.0  0.0  0.0  0.0  0.0  0.0  0.0  0
    1          NaN  1.0  1.0  1.0  1.0  1.0  1.0  1
    2          NaN  NaN  2.0  2.0  2.0  2.0  2.0  2
    3          NaN  NaN  NaN  3.0  3.0  3.0  3.0  3
    4          NaN  NaN  NaN  NaN  4.0  4.0  4.0  4
    5          NaN  NaN  NaN  NaN  NaN  5.0  5.0  5
    6          NaN  NaN  NaN  NaN  NaN  NaN  6.0  6
    7          NaN  NaN  NaN  NaN  NaN  NaN  NaN  7
    >>> valid_set[0]
    split_idx  0  1  2  3  4  5  6  7
    0          1  2  3  4  5  6  7  8
    >>> test_set[0]
    split_idx  0  1  2  3  4  5  6  7
    0          2  3  4  5  6  7  8  9
    
    >>> sr.vbt.expanding_split(
    ...     set_lens=(1, 1), min_len=3, left_to_right=False,
    ...     plot=True, trace_names=['train', 'valid', 'test'])
    

* * *

### expanding_std method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L410-L414 "Jump to source")¶
    
    
    GenericAccessor.expanding_std(
        minp=1,
        ddof=1,
        wrap_kwargs=None
    )
    

See [expanding_std_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.expanding_std_nb "vectorbt.generic.nb.expanding_std_nb").

* * *

### ffill method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.ffill(
        *,
        wrap_kwargs=None
    )
    

See [ffill_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.ffill_nb "vectorbt.generic.nb.ffill_nb").

* * *

### fillna method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.fillna(
        value,
        *,
        wrap_kwargs=None
    )
    

See [fillna_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.fillna_nb "vectorbt.generic.nb.fillna_nb").

* * *

### filter method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L618-L637 "Jump to source")¶
    
    
    GenericAccessor.filter(
        filter_func_nb,
        *args,
        wrap_kwargs=None
    )
    

See [filter_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.filter_nb "vectorbt.generic.nb.filter_nb").

**Usage**
    
    
    >>> greater_nb = njit(lambda i, col, a: a > 2)
    >>> df.vbt.filter(greater_nb)
                  a    b    c
    2020-01-01  NaN  5.0  NaN
    2020-01-02  NaN  4.0  NaN
    2020-01-03  3.0  3.0  3.0
    2020-01-04  4.0  NaN  NaN
    2020-01-05  5.0  NaN  NaN
    

* * *

### fshift method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.fshift(
        n=1,
        fill_value=nan,
        *,
        wrap_kwargs=None
    )
    

See [fshift_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.fshift_nb "vectorbt.generic.nb.fshift_nb").

* * *

### get_drawdowns method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1190-L1195 "Jump to source")¶
    
    
    GenericAccessor.get_drawdowns(
        wrapper_kwargs=None,
        **kwargs
    )
    

Generate drawdown records.

See [Drawdowns](https://vectorbt.dev/api/generic/drawdowns/#vectorbt.generic.drawdowns.Drawdowns "vectorbt.generic.drawdowns.Drawdowns").

* * *

### get_ranges method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1178-L1183 "Jump to source")¶
    
    
    GenericAccessor.get_ranges(
        wrapper_kwargs=None,
        **kwargs
    )
    

Generate range records.

See [Ranges](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges "vectorbt.generic.ranges.Ranges").

* * *

### groupby_apply method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L511-L548 "Jump to source")¶
    
    
    GenericAccessor.groupby_apply(
        by,
        apply_func_nb,
        *args,
        on_matrix=False,
        wrap_kwargs=None,
        **kwargs
    )
    

See [groupby_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.groupby_apply_nb "vectorbt.generic.nb.groupby_apply_nb") and [groupby_matrix_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.groupby_matrix_apply_nb "vectorbt.generic.nb.groupby_matrix_apply_nb") for `on_matrix=True`.

For `by`, see `pd.DataFrame.groupby`.

**Usage**
    
    
    >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
    >>> df.vbt.groupby_apply([1, 1, 2, 2, 3], mean_nb)
         a    b    c
    1  1.5  4.5  1.5
    2  3.5  2.5  2.5
    3  5.0  1.0  1.0
    
    >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
    >>> df.vbt.groupby_apply([1, 1, 2, 2, 3], mean_matrix_nb, on_matrix=True)
              a         b         c
    1  2.500000  2.500000  2.500000
    2  2.833333  2.833333  2.833333
    3  2.333333  2.333333  2.333333
    

* * *

### histplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1683-L1710 "Jump to source")¶
    
    
    GenericAccessor.histplot(
        trace_names=None,
        group_by=None,
        return_fig=True,
        **kwargs
    )
    

Create [Histogram](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Histogram "vectorbt.generic.plotting.Histogram") and return the figure.

**Usage**
    
    
    >>> df.vbt.histplot()
    

* * *

### idxmax method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L894-L912 "Jump to source")¶
    
    
    GenericAccessor.idxmax(
        group_by=None,
        order='C',
        wrap_kwargs=None
    )
    

Return labeled index of max of non-NaN elements.

* * *

### idxmin method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L874-L892 "Jump to source")¶
    
    
    GenericAccessor.idxmin(
        group_by=None,
        order='C',
        wrap_kwargs=None
    )
    

Return labeled index of min of non-NaN elements.

* * *

### lineplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1630-L1640 "Jump to source")¶
    
    
    GenericAccessor.lineplot(
        **kwargs
    )
    

[GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot") with 'lines' mode.

**Usage**
    
    
    >>> df.vbt.lineplot()
    

* * *

### mapping property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L395-L398 "Jump to source")¶

Mapping.

* * *

### max method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L794-L806 "Jump to source")¶
    
    
    GenericAccessor.max(
        group_by=None,
        wrap_kwargs=None
    )
    

Return max of non-NaN elements.

* * *

### maxabs_scale method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.maxabs_scale(
        *,
        copy=True,
        clip=False,
        **kwargs
    )
    

See `sklearn.preprocessing.MaxAbsScaler`.

* * *

### mean method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L808-L821 "Jump to source")¶
    
    
    GenericAccessor.mean(
        group_by=None,
        wrap_kwargs=None
    )
    

Return mean of non-NaN elements.

* * *

### median method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L823-L835 "Jump to source")¶
    
    
    GenericAccessor.median(
        group_by=None,
        wrap_kwargs=None
    )
    

Return median of non-NaN elements.

* * *

### metrics class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py "Jump to source")¶

Metrics supported by [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").
    
    
    Config({
        "start": {
            "title": "Start",
            "calc_func": "<function GenericAccessor.<lambda> at 0x7f9582716e80>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "end": {
            "title": "End",
            "calc_func": "<function GenericAccessor.<lambda> at 0x7f9582716f20>",
            "agg_func": null,
            "tags": "wrapper"
        },
        "period": {
            "title": "Period",
            "calc_func": "<function GenericAccessor.<lambda> at 0x7f9582716fc0>",
            "apply_to_timedelta": true,
            "agg_func": null,
            "tags": "wrapper"
        },
        "count": {
            "title": "Count",
            "calc_func": "count",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "mean": {
            "title": "Mean",
            "calc_func": "mean",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "std": {
            "title": "Std",
            "calc_func": "std",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "min": {
            "title": "Min",
            "calc_func": "min",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "median": {
            "title": "Median",
            "calc_func": "median",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "max": {
            "title": "Max",
            "calc_func": "max",
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "describe"
            ]
        },
        "idx_min": {
            "title": "Min Index",
            "calc_func": "idxmin",
            "agg_func": null,
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "index"
            ]
        },
        "idx_max": {
            "title": "Max Index",
            "calc_func": "idxmax",
            "agg_func": null,
            "inv_check_has_mapping": true,
            "tags": [
                "generic",
                "index"
            ]
        },
        "value_counts": {
            "title": "Value Counts",
            "calc_func": "<function GenericAccessor.<lambda> at 0x7f9582717060>",
            "resolve_value_counts": true,
            "check_has_mapping": true,
            "tags": [
                "generic",
                "value_counts"
            ]
        }
    })
    

Returns `GenericAccessor._metrics`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change metrics, you can either change the config in-place, override this property, or overwrite the instance variable `GenericAccessor._metrics`.

* * *

### min method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L780-L792 "Jump to source")¶
    
    
    GenericAccessor.min(
        group_by=None,
        wrap_kwargs=None
    )
    

Return min of non-NaN elements.

* * *

### minmax_scale method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.minmax_scale(
        feature_range=(0, 1),
        *,
        copy=True,
        clip=False,
        **kwargs
    )
    

See `sklearn.preprocessing.MinMaxScaler`.

* * *

### normalize method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.normalize(
        norm='l2',
        *,
        copy=True,
        **kwargs
    )
    

See `sklearn.preprocessing.Normalizer`.

* * *

### pct_change method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.pct_change(
        n=1,
        *,
        wrap_kwargs=None
    )
    

See [pct_change_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.pct_change_nb "vectorbt.generic.nb.pct_change_nb").

* * *

### plot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1601-L1628 "Jump to source")¶
    
    
    GenericAccessor.plot(
        trace_names=None,
        x_labels=None,
        return_fig=True,
        **kwargs
    )
    

Create [Scatter](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Scatter "vectorbt.generic.plotting.Scatter") and return the figure.

**Usage**
    
    
    >>> df.vbt.plot()
    

* * *

### plots_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1741-L1753 "Jump to source")¶

Defaults for [PlotsBuilderMixin.plots()](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots "vectorbt.generic.accessors.GenericAccessor.plots").

Merges [PlotsBuilderMixin.plots_defaults](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults "vectorbt.generic.plots_builder.PlotsBuilderMixin.plots_defaults") and `generic.plots` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### power_transform method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.power_transform(
        method='yeo-johnson',
        *,
        standardize=True,
        copy=True,
        **kwargs
    )
    

See `sklearn.preprocessing.PowerTransformer`.

* * *

### product method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.product(
        *,
        wrap_kwargs=None
    )
    

See [nanprod_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.nanprod_nb "vectorbt.generic.nb.nanprod_nb").

* * *

### quantile_transform method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.quantile_transform(
        *,
        n_quantiles=1000,
        output_distribution='uniform',
        ignore_implicit_zeros=False,
        subsample=10000,
        random_state=None,
        copy=True,
        **kwargs
    )
    

See `sklearn.preprocessing.QuantileTransformer`.

* * *

### range_split method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1454-L1536 "Jump to source")¶
    
    
    GenericAccessor.range_split(
        **kwargs
    )
    

Split using [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.generic.accessors.GenericAccessor.split") on [RangeSplitter](https://vectorbt.dev/api/generic/splitters/#vectorbt.generic.splitters.RangeSplitter "vectorbt.generic.splitters.RangeSplitter").

**Usage**
    
    
    >>> range_df, range_indexes = sr.vbt.range_split(n=2)
    >>> range_df
    split_idx  0  1
    0          0  5
    1          1  6
    2          2  7
    3          3  8
    4          4  9
    >>> range_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-06', ..., '2020-01-10'], dtype='datetime64[ns]', name='split_1')]
    
    >>> range_df, range_indexes = sr.vbt.range_split(range_len=4)
    >>> range_df
    split_idx  0  1  2  3  4  5  6
    0          0  1  2  3  4  5  6
    1          1  2  3  4  5  6  7
    2          2  3  4  5  6  7  8
    3          3  4  5  6  7  8  9
    >>> range_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-02', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_1'),
     DatetimeIndex(['2020-01-03', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_2'),
     DatetimeIndex(['2020-01-04', ..., '2020-01-07'], dtype='datetime64[ns]', name='split_3'),
     DatetimeIndex(['2020-01-05', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_4'),
     DatetimeIndex(['2020-01-06', ..., '2020-01-09'], dtype='datetime64[ns]', name='split_5'),
     DatetimeIndex(['2020-01-07', ..., '2020-01-10'], dtype='datetime64[ns]', name='split_6')]
    
    >>> range_df, range_indexes = sr.vbt.range_split(start_idxs=[0, 2], end_idxs=[5, 7])
    >>> range_df
    split_idx  0  1
    0          0  2
    1          1  3
    2          2  4
    3          3  5
    4          4  6
    5          5  7
    >>> range_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-03', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_1')]
    
    >>> range_df, range_indexes = sr.vbt.range_split(start_idxs=[0], end_idxs=[2, 3, 4])
    >>> range_df
    split_idx    0    1  2
    0          0.0  0.0  0
    1          1.0  1.0  1
    2          2.0  2.0  2
    3          NaN  3.0  3
    4          NaN  NaN  4
    >>> range_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-03'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_1'),
     DatetimeIndex(['2020-01-01', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_2')]
    
    >>> range_df, range_indexes = sr.vbt.range_split(
    ...     start_idxs=pd.Index(['2020-01-01', '2020-01-02']),
    ...     end_idxs=pd.Index(['2020-01-04', '2020-01-05'])
    ... )
    >>> range_df
    split_idx  0  1
    0          0  1
    1          1  2
    2          2  3
    3          3  4
    >>> range_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-02', ..., '2020-01-05'], dtype='datetime64[ns]', name='split_1')]
    
     >>> sr.vbt.range_split(
     ...    start_idxs=pd.Index(['2020-01-01', '2020-01-02', '2020-01-01']),
     ...    end_idxs=pd.Index(['2020-01-08', '2020-01-04', '2020-01-07']),
     ...    plot=True
     ... )
    

* * *

### ranges property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1173-L1176 "Jump to source")¶

[GenericAccessor.get_ranges()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.get_ranges "vectorbt.generic.accessors.GenericAccessor.get_ranges") with default arguments.

* * *

### rebase method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1324-L1331 "Jump to source")¶
    
    
    GenericAccessor.rebase(
        base,
        wrap_kwargs=None
    )
    

Rebase all series to a given intial base.

This makes comparing/plotting different series together easier. Will forward and backward fill NaN values.

* * *

### reduce method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L666-L778 "Jump to source")¶
    
    
    GenericAccessor.reduce(
        reduce_func_nb,
        *args,
        returns_array=False,
        returns_idx=False,
        flatten=False,
        order='C',
        to_index=True,
        group_by=None,
        wrap_kwargs=None
    )
    

Reduce by column.

See [flat_reduce_grouped_to_array_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.flat_reduce_grouped_to_array_nb "vectorbt.generic.nb.flat_reduce_grouped_to_array_nb") if grouped, `returns_array` is True and `flatten` is True. See [flat_reduce_grouped_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.flat_reduce_grouped_nb "vectorbt.generic.nb.flat_reduce_grouped_nb") if grouped, `returns_array` is False and `flatten` is True. See [reduce_grouped_to_array_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.reduce_grouped_to_array_nb "vectorbt.generic.nb.reduce_grouped_to_array_nb") if grouped, `returns_array` is True and `flatten` is False. See [reduce_grouped_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.reduce_grouped_nb "vectorbt.generic.nb.reduce_grouped_nb") if grouped, `returns_array` is False and `flatten` is False. See [reduce_to_array_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.reduce_to_array_nb "vectorbt.generic.nb.reduce_to_array_nb") if not grouped and `returns_array` is True. See [reduce_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.reduce_nb "vectorbt.generic.nb.reduce_nb") if not grouped and `returns_array` is False.

Set `returns_idx` to True if values returned by `reduce_func_nb` are indices/positions. Set `to_index` to False to return raw positions instead of labels.

**Usage**
    
    
    >>> mean_nb = njit(lambda col, a: np.nanmean(a))
    >>> df.vbt.reduce(mean_nb)
    a    3.0
    b    3.0
    c    1.8
    dtype: float64
    
    >>> argmax_nb = njit(lambda col, a: np.argmax(a))
    >>> df.vbt.reduce(argmax_nb, returns_idx=True)
    a   2020-01-05
    b   2020-01-01
    c   2020-01-03
    dtype: datetime64[ns]
    
    >>> argmax_nb = njit(lambda col, a: np.argmax(a))
    >>> df.vbt.reduce(argmax_nb, returns_idx=True, to_index=False)
    a    4
    b    0
    c    2
    dtype: int64
    
    >>> min_max_nb = njit(lambda col, a: np.array([np.nanmin(a), np.nanmax(a)]))
    >>> df.vbt.reduce(min_max_nb, returns_array=True, wrap_kwargs=dict(name_or_index=['min', 'max']))
           a    b    c
    min  1.0  1.0  1.0
    max  5.0  5.0  3.0
    
    >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
    >>> df.vbt.reduce(mean_nb, group_by=group_by)
    group
    first     3.0
    second    1.8
    dtype: float64
    
    >>> df.vbt.reduce(min_max_nb, name_or_index=['min', 'max'],
    ...     returns_array=True, group_by=group_by)
    group  first  second
    min      1.0     1.0
    max      5.0     3.0
    

* * *

### resample_apply method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L550-L595 "Jump to source")¶
    
    
    GenericAccessor.resample_apply(
        freq,
        apply_func_nb,
        *args,
        on_matrix=False,
        wrap_kwargs=None,
        **kwargs
    )
    

See [groupby_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.groupby_apply_nb "vectorbt.generic.nb.groupby_apply_nb") and [groupby_matrix_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.groupby_matrix_apply_nb "vectorbt.generic.nb.groupby_matrix_apply_nb") for `on_matrix=True`.

For `freq`, see `pd.DataFrame.resample`.

**Usage**
    
    
    >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
    >>> df.vbt.resample_apply('2d', mean_nb)
                  a    b    c
    2020-01-01  1.5  4.5  1.5
    2020-01-03  3.5  2.5  2.5
    2020-01-05  5.0  1.0  1.0
    
    >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
    >>> df.vbt.resample_apply('2d', mean_matrix_nb, on_matrix=True)
                       a         b         c
    2020-01-01  2.500000  2.500000  2.500000
    2020-01-03  2.833333  2.833333  2.833333
    2020-01-05  2.333333  2.333333  2.333333
    

* * *

### resolve_self method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1026-L1062 "Jump to source")¶
    
    
    GenericAccessor.resolve_self(
        cond_kwargs=None,
        custom_arg_names=None,
        impacts_caching=True,
        silence_warnings=False
    )
    

Resolve self.

See [Wrapping.resolve_self()](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping.resolve_self "vectorbt.base.array_wrapper.Wrapping.resolve_self").

Creates a copy of this instance `mapping` is different in `cond_kwargs`.

* * *

### robust_scale method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.robust_scale(
        *,
        with_centering=True,
        with_scaling=True,
        quantile_range=(25.0, 75.0),
        copy=True,
        unit_variance=False,
        **kwargs
    )
    

See `sklearn.preprocessing.RobustScaler`.

* * *

### rolling_apply method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L441-L474 "Jump to source")¶
    
    
    GenericAccessor.rolling_apply(
        window,
        apply_func_nb,
        *args,
        minp=None,
        on_matrix=False,
        wrap_kwargs=None
    )
    

See [rolling_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_apply_nb "vectorbt.generic.nb.rolling_apply_nb") and [rolling_matrix_apply_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_matrix_apply_nb "vectorbt.generic.nb.rolling_matrix_apply_nb") for `on_matrix=True`.

**Usage**
    
    
    >>> mean_nb = njit(lambda i, col, a: np.nanmean(a))
    >>> df.vbt.rolling_apply(3, mean_nb)
                  a    b         c
    2020-01-01  1.0  5.0  1.000000
    2020-01-02  1.5  4.5  1.500000
    2020-01-03  2.0  4.0  2.000000
    2020-01-04  3.0  3.0  2.333333
    2020-01-05  4.0  2.0  2.000000
    
    >>> mean_matrix_nb = njit(lambda i, a: np.nanmean(a))
    >>> df.vbt.rolling_apply(3, mean_matrix_nb, on_matrix=True)
                       a         b         c
    2020-01-01  2.333333  2.333333  2.333333
    2020-01-02  2.500000  2.500000  2.500000
    2020-01-03  2.666667  2.666667  2.666667
    2020-01-04  2.777778  2.777778  2.777778
    2020-01-05  2.666667  2.666667  2.666667
    

* * *

### rolling_max method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.rolling_max(
        window,
        minp=None,
        *,
        wrap_kwargs=None
    )
    

See [rolling_max_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_max_nb "vectorbt.generic.nb.rolling_max_nb").

* * *

### rolling_mean method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.rolling_mean(
        window,
        minp=None,
        *,
        wrap_kwargs=None
    )
    

See [rolling_mean_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_mean_nb "vectorbt.generic.nb.rolling_mean_nb").

* * *

### rolling_min method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.rolling_min(
        window,
        minp=None,
        *,
        wrap_kwargs=None
    )
    

See [rolling_min_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_min_nb "vectorbt.generic.nb.rolling_min_nb").

* * *

### rolling_split method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1538-L1564 "Jump to source")¶
    
    
    GenericAccessor.rolling_split(
        **kwargs
    )
    

Split using [GenericAccessor.split()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.split "vectorbt.generic.accessors.GenericAccessor.split") on [RollingSplitter](https://vectorbt.dev/api/generic/splitters/#vectorbt.generic.splitters.RollingSplitter "vectorbt.generic.splitters.RollingSplitter").

**Usage**
    
    
    >>> train_set, valid_set, test_set = sr.vbt.rolling_split(
    ...     window_len=5, set_lens=(1, 1), left_to_right=False)
    >>> train_set[0]
    split_idx  0  1  2  3  4  5
    0          0  1  2  3  4  5
    1          1  2  3  4  5  6
    2          2  3  4  5  6  7
    >>> valid_set[0]
    split_idx  0  1  2  3  4  5
    0          3  4  5  6  7  8
    >>> test_set[0]
    split_idx  0  1  2  3  4  5
    0          4  5  6  7  8  9
    
    >>> sr.vbt.rolling_split(
    ...     window_len=5, set_lens=(1, 1), left_to_right=False,
    ...     plot=True, trace_names=['train', 'valid', 'test'])
    

* * *

### rolling_std method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L404-L408 "Jump to source")¶
    
    
    GenericAccessor.rolling_std(
        window,
        minp=None,
        ddof=1,
        wrap_kwargs=None
    )
    

See [rolling_std_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.rolling_std_nb "vectorbt.generic.nb.rolling_std_nb").

* * *

### scale method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L100-L111 "Jump to source")¶
    
    
    GenericAccessor.scale(
        *,
        copy=True,
        with_mean=True,
        with_std=True,
        **kwargs
    )
    

See `sklearn.preprocessing.StandardScaler`.

* * *

### scatterplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1642-L1652 "Jump to source")¶
    
    
    GenericAccessor.scatterplot(
        **kwargs
    )
    

[GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot") with 'markers' mode.

**Usage**
    
    
    >>> df.vbt.scatterplot()
    

* * *

### shuffle method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/decorators.py#L42-L57 "Jump to source")¶
    
    
    GenericAccessor.shuffle(
        seed=None,
        *,
        wrap_kwargs=None
    )
    

See [shuffle_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.shuffle_nb "vectorbt.generic.nb.shuffle_nb").

* * *

### split method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1335-L1452 "Jump to source")¶
    
    
    GenericAccessor.split(
        splitter,
        stack_kwargs=None,
        keys=None,
        plot=False,
        trace_names=None,
        heatmap_kwargs=None,
        **kwargs
    )
    

Split using a splitter.

Returns a tuple of tuples, each corresponding to a set and composed of a dataframe and split indexes.

A splitter can be any class instance that has `split` method, ideally subclassing `sklearn.model_selection.BaseCrossValidator` or [BaseSplitter](https://vectorbt.dev/api/generic/splitters/#vectorbt.generic.splitters.BaseSplitter "vectorbt.generic.splitters.BaseSplitter").

`heatmap_kwargs` are passed to [Heatmap](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Heatmap "vectorbt.generic.plotting.Heatmap") if `plot` is True, can be a dictionary or a list per set, for example, to set trace name for each set ('train', 'test', etc.).

`**kwargs` are passed to the `split` method.

Note

The datetime-like format of the index will be lost as result of this operation. Make sure to store the index metadata such as frequency information beforehand.

**Usage**
    
    
    >>> from sklearn.model_selection import TimeSeriesSplit
    
    >>> splitter = TimeSeriesSplit(n_splits=3)
    >>> (train_df, train_indexes), (test_df, test_indexes) = sr.vbt.split(splitter)
    
    >>> train_df
    split_idx    0    1  2
    0          0.0  0.0  0
    1          1.0  1.0  1
    2          2.0  2.0  2
    3          3.0  3.0  3
    4          NaN  4.0  4
    5          NaN  5.0  5
    6          NaN  NaN  6
    7          NaN  NaN  7
    >>> train_indexes
    [DatetimeIndex(['2020-01-01', ..., '2020-01-04'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-01', ..., '2020-01-06'], dtype='datetime64[ns]', name='split_1'),
     DatetimeIndex(['2020-01-01', ..., '2020-01-08'], dtype='datetime64[ns]', name='split_2')]
    >>> test_df
    split_idx  0  1  2
    0          4  6  8
    1          5  7  9
    >>> test_indexes
    [DatetimeIndex(['2020-01-05', '2020-01-06'], dtype='datetime64[ns]', name='split_0'),
     DatetimeIndex(['2020-01-07', '2020-01-08'], dtype='datetime64[ns]', name='split_1'),
     DatetimeIndex(['2020-01-09', '2020-01-10'], dtype='datetime64[ns]', name='split_2')]
    
    >>> sr.vbt.split(splitter, plot=True, trace_names=['train', 'test'])
    

* * *

### stats_defaults property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1066-L1078 "Jump to source")¶

Defaults for [StatsBuilderMixin.stats()](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats "vectorbt.generic.accessors.GenericAccessor.stats").

Merges [StatsBuilderMixin.stats_defaults](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults "vectorbt.generic.stats_builder.StatsBuilderMixin.stats_defaults") and `generic.stats` from [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

* * *

### std method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L837-L850 "Jump to source")¶
    
    
    GenericAccessor.std(
        ddof=1,
        group_by=None,
        wrap_kwargs=None
    )
    

Return standard deviation of non-NaN elements.

* * *

### subplots class variable[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py "Jump to source")¶

Subplots supported by [GenericAccessor](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor "vectorbt.generic.accessors.GenericAccessor").
    
    
    Config({
        "plot": {
            "check_is_not_grouped": true,
            "plot_func": "plot",
            "pass_trace_names": false,
            "tags": "generic"
        }
    })
    

Returns `GenericAccessor._subplots`, which gets (deep) copied upon creation of each instance. Thus, changing this config won't affect the class.

To change subplots, you can either change the config in-place, override this property, or overwrite the instance variable `GenericAccessor._subplots`.

* * *

### sum method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L852-L864 "Jump to source")¶
    
    
    GenericAccessor.sum(
        group_by=None,
        wrap_kwargs=None
    )
    

Return sum of non-NaN elements.

* * *

### to_mapped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1197-L1217 "Jump to source")¶
    
    
    GenericAccessor.to_mapped(
        dropna=True,
        dtype=None,
        group_by=None,
        **kwargs
    )
    

Convert this object into an instance of [MappedArray](https://vectorbt.dev/api/records/mapped_array/#vectorbt.records.mapped_array.MappedArray "vectorbt.records.mapped_array.MappedArray").

* * *

### to_returns method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1219-L1221 "Jump to source")¶
    
    
    GenericAccessor.to_returns(
        **kwargs
    )
    

Get returns of this object.

* * *

### transform method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1277-L1318 "Jump to source")¶
    
    
    GenericAccessor.transform(
        transformer,
        wrap_kwargs=None,
        **kwargs
    )
    

Transform using a transformer.

A transformer can be any class instance that has `transform` and `fit_transform` methods, ideally subclassing `sklearn.base.TransformerMixin` and `sklearn.base.BaseEstimator`.

Will fit `transformer` if not fitted.

`**kwargs` are passed to the `transform` or `fit_transform` method.

**Usage**
    
    
    >>> from sklearn.preprocessing import MinMaxScaler
    
    >>> df.vbt.transform(MinMaxScaler((-1, 1)))
                  a    b    c
    2020-01-01 -1.0  1.0 -1.0
    2020-01-02 -0.5  0.5  0.0
    2020-01-03  0.0  0.0  1.0
    2020-01-04  0.5 -0.5  0.0
    2020-01-05  1.0 -1.0 -1.0
    
    >>> fitted_scaler = MinMaxScaler((-1, 1)).fit(np.array([[2], [4]]))
    >>> df.vbt.transform(fitted_scaler)
                  a    b    c
    2020-01-01 -2.0  2.0 -2.0
    2020-01-02 -1.0  1.0 -1.0
    2020-01-03  0.0  0.0  0.0
    2020-01-04  1.0 -1.0 -1.0
    2020-01-05  2.0 -2.0 -2.0
    

* * *

### value_counts method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L954-L1022 "Jump to source")¶
    
    
    GenericAccessor.value_counts(
        normalize=False,
        sort_uniques=True,
        sort=False,
        ascending=False,
        dropna=False,
        group_by=None,
        mapping=None,
        incl_all_keys=False,
        wrap_kwargs=None,
        **kwargs
    )
    

Return a Series/DataFrame containing counts of unique values.

  * Enable `normalize` flag to return the relative frequencies of the unique values.
  * Enable `sort_uniques` flag to sort uniques.
  * Enable `sort` flag to sort by frequencies.
  * Enable `ascending` flag to sort in ascending order.
  * Enable `dropna` flag to exclude counts of NaN.
  * Enable `incl_all_keys` to include all mapping keys, no only those that are present in the array.



Mapping will be applied using [apply_mapping()](https://vectorbt.dev/api/utils/mapping/#vectorbt.utils.mapping.apply_mapping "vectorbt.utils.mapping.apply_mapping") with `**kwargs`.

* * *

### zscore method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1320-L1322 "Jump to source")¶
    
    
    GenericAccessor.zscore(
        **kwargs
    )
    

Compute z-score using `sklearn.preprocessing.StandardScaler`.

* * *

## GenericDFAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2356-L2491 "Jump to source")¶
    
    
    GenericDFAccessor(
        obj,
        mapping=None,
        **kwargs
    )
    

Accessor on top of data of any type. For DataFrames only.

Accessible through `pd.DataFrame.vbt`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [BaseDFAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseDFAccessor "vectorbt.base.accessors.BaseDFAccessor")
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
  * [GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.generic.accessors.GenericAccessor.fshift")
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
  * [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot")
  * [GenericAccessor.plots_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plots_defaults "vectorbt.generic.accessors.GenericAccessor.plots_defaults")
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
  * [GenericAccessor.stats_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.stats_defaults "vectorbt.generic.accessors.GenericAccessor.stats_defaults")
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

  * [OHLCVDFAccessor](https://vectorbt.dev/api/ohlcv_accessors/#vectorbt.ohlcv_accessors.OHLCVDFAccessor "vectorbt.ohlcv_accessors.OHLCVDFAccessor")
  * [ReturnsDFAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsDFAccessor "vectorbt.returns.accessors.ReturnsDFAccessor")
  * [SignalsDFAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsDFAccessor "vectorbt.signals.accessors.SignalsDFAccessor")
  * [Vbt_DFAccessor](https://vectorbt.dev/api/root_accessors/#vectorbt.root_accessors.Vbt_DFAccessor "vectorbt.root_accessors.Vbt_DFAccessor")



* * *

### flatten_grouped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2394-L2453 "Jump to source")¶
    
    
    GenericDFAccessor.flatten_grouped(
        group_by=None,
        order='C',
        wrap_kwargs=None
    )
    

Flatten each group of columns.

See [flatten_grouped_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.flatten_grouped_nb "vectorbt.generic.nb.flatten_grouped_nb"). If all groups have the same length, see [flatten_uniform_grouped_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.flatten_uniform_grouped_nb "vectorbt.generic.nb.flatten_uniform_grouped_nb").

Warning

Make sure that the distribution of group lengths is close to uniform, otherwise groups with less columns will be filled with NaN and needlessly occupy memory.

**Usage**
    
    
    >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
    >>> df.vbt.flatten_grouped(group_by=group_by, order='C')
    group       first  second
    2020-01-01    1.0     1.0
    2020-01-01    5.0     NaN
    2020-01-02    2.0     2.0
    2020-01-02    4.0     NaN
    2020-01-03    3.0     3.0
    2020-01-03    3.0     NaN
    2020-01-04    4.0     2.0
    2020-01-04    2.0     NaN
    2020-01-05    5.0     1.0
    2020-01-05    1.0     NaN
    
    >>> df.vbt.flatten_grouped(group_by=group_by, order='F')
    group       first  second
    2020-01-01    1.0     1.0
    2020-01-02    2.0     2.0
    2020-01-03    3.0     3.0
    2020-01-04    4.0     2.0
    2020-01-05    5.0     1.0
    2020-01-01    5.0     NaN
    2020-01-02    4.0     NaN
    2020-01-03    3.0     NaN
    2020-01-04    2.0     NaN
    2020-01-05    1.0     NaN
    

* * *

### heatmap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2455-L2486 "Jump to source")¶
    
    
    GenericDFAccessor.heatmap(
        x_labels=None,
        y_labels=None,
        return_fig=True,
        **kwargs
    )
    

Create [Heatmap](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Heatmap "vectorbt.generic.plotting.Heatmap") and return the figure.

**Usage**
    
    
    >>> df = pd.DataFrame([
    ...     [0, np.nan, np.nan],
    ...     [np.nan, 1, np.nan],
    ...     [np.nan, np.nan, 2]
    ... ])
    >>> df.vbt.heatmap()
    

* * *

### squeeze_grouped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2365-L2392 "Jump to source")¶
    
    
    GenericDFAccessor.squeeze_grouped(
        squeeze_func_nb,
        *args,
        group_by=None,
        wrap_kwargs=None
    )
    

Squeeze each group of columns into a single column.

See [squeeze_grouped_nb()](https://vectorbt.dev/api/generic/nb/#vectorbt.generic.nb.squeeze_grouped_nb "vectorbt.generic.nb.squeeze_grouped_nb").

**Usage**
    
    
    >>> group_by = pd.Series(['first', 'first', 'second'], name='group')
    >>> mean_squeeze_nb = njit(lambda i, group, a: np.nanmean(a))
    >>> df.vbt.squeeze_grouped(mean_squeeze_nb, group_by=group_by)
    group       first  second
    2020-01-01    3.0     1.0
    2020-01-02    3.0     2.0
    2020-01-03    3.0     3.0
    2020-01-04    3.0     2.0
    2020-01-05    3.0     1.0
    

* * *

### ts_heatmap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2488-L2491 "Jump to source")¶
    
    
    GenericDFAccessor.ts_heatmap(
        is_y_category=True,
        **kwargs
    )
    

Heatmap of time-series data.

* * *

## GenericSRAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1776-L2353 "Jump to source")¶
    
    
    GenericSRAccessor(
        obj,
        mapping=None,
        **kwargs
    )
    

Accessor on top of data of any type. For Series only.

Accessible through `pd.Series.vbt`.

**Superclasses**

  * [AttrResolver](https://vectorbt.dev/api/utils/attr_/#vectorbt.utils.attr_.AttrResolver "vectorbt.utils.attr_.AttrResolver")
  * [BaseAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseAccessor "vectorbt.base.accessors.BaseAccessor")
  * [BaseSRAccessor](https://vectorbt.dev/api/base/accessors/#vectorbt.base.accessors.BaseSRAccessor "vectorbt.base.accessors.BaseSRAccessor")
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
  * [GenericAccessor.fshift()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.fshift "vectorbt.generic.accessors.GenericAccessor.fshift")
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
  * [GenericAccessor.plot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plot "vectorbt.generic.accessors.GenericAccessor.plot")
  * [GenericAccessor.plots_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.plots_defaults "vectorbt.generic.accessors.GenericAccessor.plots_defaults")
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
  * [GenericAccessor.stats_defaults](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.stats_defaults "vectorbt.generic.accessors.GenericAccessor.stats_defaults")
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

  * [ReturnsSRAccessor](https://vectorbt.dev/api/returns/accessors/#vectorbt.returns.accessors.ReturnsSRAccessor "vectorbt.returns.accessors.ReturnsSRAccessor")
  * [SignalsSRAccessor](https://vectorbt.dev/api/signals/accessors/#vectorbt.signals.accessors.SignalsSRAccessor "vectorbt.signals.accessors.SignalsSRAccessor")
  * [Vbt_SRAccessor](https://vectorbt.dev/api/root_accessors/#vectorbt.root_accessors.Vbt_SRAccessor "vectorbt.root_accessors.Vbt_SRAccessor")



* * *

### flatten_grouped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1797-L1805 "Jump to source")¶
    
    
    GenericSRAccessor.flatten_grouped(
        group_by=None,
        order='C',
        wrap_kwargs=None
    )
    

Flatten each group of elements.

Based on [GenericDFAccessor.flatten_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped "vectorbt.generic.accessors.GenericDFAccessor.flatten_grouped").

* * *

### heatmap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1995-L2150 "Jump to source")¶
    
    
    GenericSRAccessor.heatmap(
        x_level=None,
        y_level=None,
        symmetric=False,
        sort=True,
        x_labels=None,
        y_labels=None,
        slider_level=None,
        active=0,
        slider_labels=None,
        return_fig=True,
        fig=None,
        **kwargs
    )
    

Create a heatmap figure based on object's multi-index and values.

If index is not a multi-index, converts Series into a DataFrame and calls [GenericDFAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.heatmap "vectorbt.generic.accessors.GenericDFAccessor.heatmap").

If multi-index contains more than two levels or you want them in specific order, pass `x_level` and `y_level`, each (`int` if index or `str` if name) corresponding to an axis of the heatmap. Optionally, pass `slider_level` to use a level as a slider.

Creates [Heatmap](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Heatmap "vectorbt.generic.plotting.Heatmap") and returns the figure.

**Usage**
    
    
    >>> multi_index = pd.MultiIndex.from_tuples([
    ...     (1, 1),
    ...     (2, 2),
    ...     (3, 3)
    ... ])
    >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
    >>> sr
    1  1    0
    2  2    1
    3  3    2
    dtype: int64
    
    >>> sr.vbt.heatmap()
    

  * Using one level as a slider:


    
    
    >>> multi_index = pd.MultiIndex.from_tuples([
    ...     (1, 1, 1),
    ...     (1, 2, 2),
    ...     (1, 3, 3),
    ...     (2, 3, 3),
    ...     (2, 2, 2),
    ...     (2, 1, 1)
    ... ])
    >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
    >>> sr
    1  1  1    0
       2  2    1
       3  3    2
    2  3  3    3
       2  2    4
       1  1    5
    dtype: int64
    
    >>> sr.vbt.heatmap(slider_level=0)
    

* * *

### overlay_with_heatmap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1945-L1993 "Jump to source")¶
    
    
    GenericSRAccessor.overlay_with_heatmap(
        other,
        trace_kwargs=None,
        heatmap_kwargs=None,
        add_trace_kwargs=None,
        fig=None,
        **layout_kwargs
    )
    

Plot Series as a line and overlays it with a heatmap.

**Args**

**`other`** : `array_like`
    Second array. Will broadcast.
**`trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter`.
**`heatmap_kwargs`** : `dict`
    Keyword arguments passed to [GenericDFAccessor.heatmap()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.heatmap "vectorbt.generic.accessors.GenericDFAccessor.heatmap").
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> df['a'].vbt.overlay_with_heatmap(df['b'])
    

* * *

### plot_against method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1807-L1943 "Jump to source")¶
    
    
    GenericSRAccessor.plot_against(
        other,
        trace_kwargs=None,
        other_trace_kwargs=None,
        pos_trace_kwargs=None,
        neg_trace_kwargs=None,
        hidden_trace_kwargs=None,
        add_trace_kwargs=None,
        fig=None,
        **layout_kwargs
    )
    

Plot Series as a line against another line.

**Args**

**`other`** : `array_like`
    Second array. Will broadcast.
**`trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter`.
**`other_trace_kwargs`** : `dict`
    

Keyword arguments passed to `plotly.graph_objects.Scatter` for `other`.

Set to 'hidden' to hide.

**`pos_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for positive line.
**`neg_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for negative line.
**`hidden_trace_kwargs`** : `dict`
    Keyword arguments passed to `plotly.graph_objects.Scatter` for hidden lines.
**`add_trace_kwargs`** : `dict`
    Keyword arguments passed to `add_trace`.
**`fig`** : `Figure` or `FigureWidget`
    Figure to add traces to.
**`**layout_kwargs`**
    Keyword arguments for layout.

**Usage**
    
    
    >>> df['a'].vbt.plot_against(df['b'])
    

* * *

### qqplot method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2312-L2353 "Jump to source")¶
    
    
    GenericSRAccessor.qqplot(
        sparams=(),
        dist='norm',
        plot_line=True,
        line_shape_kwargs=None,
        xref='x',
        yref='y',
        fig=None,
        **kwargs
    )
    

Plot probability plot using `scipy.stats.probplot`.

`**kwargs` are passed to [GenericAccessor.scatterplot()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericAccessor.scatterplot "vectorbt.generic.accessors.GenericAccessor.scatterplot").

**Usage**
    
    
    >>> pd.Series(np.random.standard_normal(100)).vbt.qqplot()
    

* * *

### squeeze_grouped method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L1785-L1795 "Jump to source")¶
    
    
    GenericSRAccessor.squeeze_grouped(
        squeeze_func_nb,
        *args,
        group_by=None,
        wrap_kwargs=None
    )
    

Squeeze each group of elements into a single element.

Based on [GenericDFAccessor.squeeze_grouped()](https://vectorbt.dev/api/generic/accessors/#vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped "vectorbt.generic.accessors.GenericDFAccessor.squeeze_grouped").

* * *

### ts_heatmap method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2152-L2154 "Jump to source")¶
    
    
    GenericSRAccessor.ts_heatmap(
        **kwargs
    )
    

Heatmap of time-series data.

* * *

### volume method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L2156-L2310 "Jump to source")¶
    
    
    GenericSRAccessor.volume(
        x_level=None,
        y_level=None,
        z_level=None,
        x_labels=None,
        y_labels=None,
        z_labels=None,
        slider_level=None,
        slider_labels=None,
        active=0,
        scene_name='scene',
        fillna=None,
        fig=None,
        return_fig=True,
        **kwargs
    )
    

Create a 3D volume figure based on object's multi-index and values.

If multi-index contains more than three levels or you want them in specific order, pass `x_level`, `y_level`, and `z_level`, each (`int` if index or `str` if name) corresponding to an axis of the volume. Optionally, pass `slider_level` to use a level as a slider.

Creates [Volume](https://vectorbt.dev/api/generic/plotting/#vectorbt.generic.plotting.Volume "vectorbt.generic.plotting.Volume") and returns the figure.

**Usage**
    
    
    >>> multi_index = pd.MultiIndex.from_tuples([
    ...     (1, 1, 1),
    ...     (2, 2, 2),
    ...     (3, 3, 3)
    ... ])
    >>> sr = pd.Series(np.arange(len(multi_index)), index=multi_index)
    >>> sr
    1  1  1    0
    2  2  2    1
    3  3  3    2
    dtype: int64
    
    >>> sr.vbt.volume().show()
    

* * *

## MetaGenericAccessor class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L265-L266 "Jump to source")¶
    
    
    MetaGenericAccessor(
        *args,
        **kwargs
    )
    

Meta class that exposes a read-only class property `StatsBuilderMixin.metrics`.

**Superclasses**

  * [MetaPlotsBuilderMixin](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.MetaPlotsBuilderMixin "vectorbt.generic.plots_builder.MetaPlotsBuilderMixin")
  * [MetaStatsBuilderMixin](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.MetaStatsBuilderMixin "vectorbt.generic.stats_builder.MetaStatsBuilderMixin")
  * `builtins.type`



**Inherited members**

  * [MetaPlotsBuilderMixin.subplots](https://vectorbt.dev/api/generic/plots_builder/#vectorbt.generic.plots_builder.MetaPlotsBuilderMixin.subplots "vectorbt.generic.plots_builder.MetaPlotsBuilderMixin.subplots")
  * [MetaStatsBuilderMixin.metrics](https://vectorbt.dev/api/generic/stats_builder/#vectorbt.generic.stats_builder.MetaStatsBuilderMixin.metrics "vectorbt.generic.stats_builder.MetaStatsBuilderMixin.metrics")



* * *

## TransformerT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L273-L281 "Jump to source")¶
    
    
    TransformerT(
        **kwargs
    )
    

Base class for protocol classes.

Protocol classes are defined as::
    
    
    class Proto(Protocol):
        def meth(self) -> int:
            ...
    

Such classes are primarily used with static type checkers that recognize structural subtyping (static duck-typing).

For example::

__ class C__
    
    
    def meth(self) -> int:
        return 0
    

def func(x: Proto) -> int: return x.meth()

func(C()) # Passes static type check

See PEP 544 for details. Protocol classes decorated with [@typing](https://github.com/typing "GitHub User: typing").runtime_checkable act as simple-minded runtime protocols that check only the presence of given attributes, ignoring their type signatures. Protocol classes can be generic, they are defined as::
    
    
    class GenProto(Protocol[T]):
        def meth(self) -> T:
            ...
    

**Superclasses**

  * `typing.Generic`
  * `typing.Protocol`



* * *

### fit_transform method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L280-L281 "Jump to source")¶
    
    
    TransformerT.fit_transform(
        *args,
        **kwargs
    )
    

* * *

### transform method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/generic/accessors.py#L277-L278 "Jump to source")¶
    
    
    TransformerT.transform(
        *args,
        **kwargs
    )
    

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
