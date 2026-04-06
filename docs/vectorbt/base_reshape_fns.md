# reshape_fns - VectorBT

> **Source:** https://vectorbt.dev/api/base/reshape_fns/

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
      * reshape_fns  [ reshape_fns  ](https://vectorbt.dev/api/base/reshape_fns/) Table of contents 
        * IndexFromLike 
        * broadcast() 
        * broadcast_index() 
        * broadcast_to() 
        * broadcast_to_array_of() 
        * broadcast_to_axis_of() 
        * flex_choose_i_and_col_nb() 
        * flex_select_auto_nb() 
        * flex_select_nb() 
        * get_multiindex_series() 
        * make_symmetric() 
        * repeat() 
        * soft_to_ndim() 
        * tile() 
        * to_1d() 
        * to_2d() 
        * to_any_array() 
        * to_dict() 
        * to_pd_array() 
        * unstack_to_array() 
        * unstack_to_df() 
        * wrap_broadcasted() 
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

  * IndexFromLike 
  * broadcast() 
  * broadcast_index() 
  * broadcast_to() 
  * broadcast_to_array_of() 
  * broadcast_to_axis_of() 
  * flex_choose_i_and_col_nb() 
  * flex_select_auto_nb() 
  * flex_select_nb() 
  * get_multiindex_series() 
  * make_symmetric() 
  * repeat() 
  * soft_to_ndim() 
  * tile() 
  * to_1d() 
  * to_2d() 
  * to_any_array() 
  * to_dict() 
  * to_pd_array() 
  * unstack_to_array() 
  * unstack_to_df() 
  * wrap_broadcasted() 



# reshape_fns module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py "Jump to source")¶

Functions for reshaping arrays.

Reshape functions transform a pandas object/NumPy array in some way, such as tiling, broadcasting, and unstacking.

* * *

## IndexFromLike _UnionGenericAlias[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py "Jump to source")¶

Any object that can be coerced into a `index_from` argument.

* * *

## broadcast function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L332-L631 "Jump to source")¶
    
    
    broadcast(
        *args,
        to_shape=None,
        to_pd=None,
        to_frame=None,
        align_index=None,
        align_columns=None,
        index_from=None,
        columns_from=None,
        require_kwargs=None,
        keep_raw=False,
        return_meta=False,
        **kwargs
    )
    

Bring any array-like object in `args` to the same shape by using NumPy broadcasting.

See [Broadcasting](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).

Can broadcast pandas objects by broadcasting their index/columns with [broadcast_index()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast_index "vectorbt.base.reshape_fns.broadcast_index").

**Args**

**`*args`** : `array_like`
    Array-like objects.
**`to_shape`** : `tuple` of `int`
    Target shape. If set, will broadcast every element in `args` to `to_shape`.
**`to_pd`** : `bool` or `list` of `bool`
    

Whether to convert all output arrays to pandas, otherwise returns raw NumPy arrays. If None, converts only if there is at least one pandas object among them.

If sequence, applies to each argument.

**`to_frame`** : `bool`
    Whether to convert all Series to DataFrames.
**`align_index`** : `bool`
    

Whether to align index of pandas objects using multi-index.

Pass None to use the default.

**`align_columns`** : `bool`
    

Whether to align columns of pandas objects using multi-index.

Pass None to use the default.

**`index_from`** : `any`
    

Broadcasting rule for index.

Pass None to use the default.

**`columns_from`** : `any`
    

Broadcasting rule for columns.

Pass None to use the default.

**`require_kwargs`** : `dict` or `list` of `dict`
    

Keyword arguments passed to `np.require`.

If sequence, applies to each argument.

**`keep_raw`** : `bool` or `list` of `bool`
    

Whether to keep the unbroadcasted version of the array.

Only makes sure that the array can be broadcast to the target shape.

If sequence, applies to each argument.

**`return_meta`** : `bool`
    Whether to also return new shape, index and columns.
**`**kwargs`**
    Keyword arguments passed to [broadcast_index()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast_index "vectorbt.base.reshape_fns.broadcast_index").

For defaults, see `broadcasting` in [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

**Usage**

  * Without broadcasting index and columns:


    
    
    >>> import numpy as np
    >>> import pandas as pd
    >>> from vectorbt.base.reshape_fns import broadcast
    
    >>> v = 0
    >>> a = np.array([1, 2, 3])
    >>> sr = pd.Series([1, 2, 3], index=pd.Index(['x', 'y', 'z']), name='a')
    >>> df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    ...     index=pd.Index(['x2', 'y2', 'z2']),
    ...     columns=pd.Index(['a2', 'b2', 'c2']))
    
    >>> for i in broadcast(
    ...     v, a, sr, df,
    ...     index_from='keep',
    ...     columns_from='keep',
    ... ): print(i)
       0  1  2
    0  0  0  0
    1  0  0  0
    2  0  0  0
       0  1  2
    0  1  2  3
    1  1  2  3
    2  1  2  3
       a  a  a
    x  1  1  1
    y  2  2  2
    z  3  3  3
        a2  b2  c2
    x2   1   2   3
    y2   4   5   6
    z2   7   8   9
    

  * Taking new index and columns from position:


    
    
    >>> for i in broadcast(
    ...     v, a, sr, df,
    ...     index_from=2,
    ...     columns_from=3
    ... ): print(i)
       a2  b2  c2
    x   0   0   0
    y   0   0   0
    z   0   0   0
       a2  b2  c2
    x   1   2   3
    y   1   2   3
    z   1   2   3
       a2  b2  c2
    x   1   1   1
    y   2   2   2
    z   3   3   3
       a2  b2  c2
    x   1   2   3
    y   4   5   6
    z   7   8   9
    

  * Broadcasting index and columns through stacking:


    
    
    >>> for i in broadcast(
    ...     v, a, sr, df,
    ...     index_from='stack',
    ...     columns_from='stack'
    ... ): print(i)
          a2  b2  c2
    x x2   0   0   0
    y y2   0   0   0
    z z2   0   0   0
          a2  b2  c2
    x x2   1   2   3
    y y2   1   2   3
    z z2   1   2   3
          a2  b2  c2
    x x2   1   1   1
    y y2   2   2   2
    z z2   3   3   3
          a2  b2  c2
    x x2   1   2   3
    y y2   4   5   6
    z z2   7   8   9
    

  * Setting index and columns manually:


    
    
    >>> for i in broadcast(
    ...     v, a, sr, df,
    ...     index_from=['a', 'b', 'c'],
    ...     columns_from=['d', 'e', 'f']
    ... ): print(i)
       d  e  f
    a  0  0  0
    b  0  0  0
    c  0  0  0
       d  e  f
    a  1  2  3
    b  1  2  3
    c  1  2  3
       d  e  f
    a  1  1  1
    b  2  2  2
    c  3  3  3
       d  e  f
    a  1  2  3
    b  4  5  6
    c  7  8  9
    

* * *

## broadcast_index function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L165-L287 "Jump to source")¶
    
    
    broadcast_index(
        args,
        to_shape,
        index_from=None,
        axis=0,
        ignore_sr_names=None,
        **kwargs
    )
    

Produce a broadcast index/columns.

**Args**

**`args`** : `list` of `array_like`
    Array-like objects.
**`to_shape`** : `tuple` of `int`
    Target shape.
**`index_from`** : `any`
    

Broadcasting rule for this index/these columns.

Accepts the following values:

  * 'keep' or None - keep the original index/columns of the objects in `args`
  * 'stack' - stack different indexes/columns using [stack_indexes()](https://vectorbt.dev/api/base/index_fns/#vectorbt.base.index_fns.stack_indexes "vectorbt.base.index_fns.stack_indexes")
  * 'strict' - ensure that all pandas objects have the same index/columns
  * 'reset' - reset any index/columns (they become a simple range)
  * integer - use the index/columns of the i-th object in `args`
  * everything else will be converted to `pd.Index`


**`axis`** : `int`
    Set to 0 for index and 1 for columns.
**`ignore_sr_names`** : `bool`
    

Whether to ignore Series names if they are in conflict.

Conflicting Series names are those that are different but not None.

**`**kwargs`**
    Keyword arguments passed to [stack_indexes()](https://vectorbt.dev/api/base/index_fns/#vectorbt.base.index_fns.stack_indexes "vectorbt.base.index_fns.stack_indexes").

For defaults, see `broadcasting` in [settings](https://vectorbt.dev/api/_settings/#vectorbt._settings.settings "vectorbt._settings.settings").

Note

Series names are treated as columns with a single element but without a name. If a column level without a name loses its meaning, better to convert Series to DataFrames with one column prior to broadcasting. If the name of a Series is not that important, better to drop it altogether by setting it to None.

* * *

## broadcast_to function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L634-L675 "Jump to source")¶
    
    
    broadcast_to(
        arg1,
        arg2,
        to_pd=None,
        index_from=None,
        columns_from=None,
        **kwargs
    )
    

Broadcast `arg1` to `arg2`.

Pass None to `index_from`/`columns_from` to use index/columns of the second argument.

Keyword arguments `**kwargs` are passed to [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast").

**Usage**
    
    
    >>> import numpy as np
    >>> import pandas as pd
    >>> from vectorbt.base.reshape_fns import broadcast_to
    
    >>> a = np.array([1, 2, 3])
    >>> sr = pd.Series([4, 5, 6], index=pd.Index(['x', 'y', 'z']), name='a')
    
    >>> broadcast_to(a, sr)
    x    1
    y    2
    z    3
    Name: a, dtype: int64
    
    >>> broadcast_to(sr, a)
    array([4, 5, 6])
    

* * *

## broadcast_to_array_of function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L678-L710 "Jump to source")¶
    
    
    broadcast_to_array_of(
        arg1,
        arg2
    )
    

Broadcast `arg1` to the shape `(1, *arg2.shape)`.

`arg1` must be either a scalar, a 1-dim array, or have 1 dimension more than `arg2`.

**Usage**
    
    
    >>> import numpy as np
    >>> from vectorbt.base.reshape_fns import broadcast_to_array_of
    
    >>> broadcast_to_array_of([0.1, 0.2], np.empty((2, 2)))
    [[[0.1 0.1]
      [0.1 0.1]]
    
     [[0.2 0.2]
      [0.2 0.2]]]
    

* * *

## broadcast_to_axis_of function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L713-L727 "Jump to source")¶
    
    
    broadcast_to_axis_of(
        arg1,
        arg2,
        axis,
        require_kwargs=None
    )
    

Broadcast `arg1` to an axis of `arg2`.

If `arg2` has less dimensions than requested, will broadcast `arg1` to a single number.

For other keyword arguments, see [broadcast()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.broadcast "vectorbt.base.reshape_fns.broadcast").

* * *

## flex_choose_i_and_col_nb function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L922-L952 "Jump to source")¶
    
    
    flex_choose_i_and_col_nb(
        a,
        flex_2d=True
    )
    

Choose selection index and column based on the array's shape.

Instead of expensive broadcasting, keep the original shape and do indexing in a smart way. A nice feature of this is that it has almost no memory footprint and can broadcast in any direction infinitely.

Call it once before using [flex_select_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_select_nb "vectorbt.base.reshape_fns.flex_select_nb").

if `flex_2d` is True, 1-dim array will correspond to columns, otherwise to rows.

* * *

## flex_select_auto_nb function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L971-L975 "Jump to source")¶
    
    
    flex_select_auto_nb(
        a,
        i,
        col,
        flex_2d=True
    )
    

Combines [flex_choose_i_and_col_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_choose_i_and_col_nb "vectorbt.base.reshape_fns.flex_choose_i_and_col_nb") and [flex_select_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_select_nb "vectorbt.base.reshape_fns.flex_select_nb").

* * *

## flex_select_nb function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L955-L968 "Jump to source")¶
    
    
    flex_select_nb(
        a,
        i,
        col,
        flex_i,
        flex_col,
        flex_2d=True
    )
    

Select element of `a` as if it has been broadcast.

* * *

## get_multiindex_series function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L730-L743 "Jump to source")¶
    
    
    get_multiindex_series(
        arg
    )
    

Get Series with a multi-index.

If DataFrame has been passed, should at maximum have one row or column.

* * *

## make_symmetric function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L801-L864 "Jump to source")¶
    
    
    make_symmetric(
        arg,
        sort=True
    )
    

Make `arg` symmetric.

The index and columns of the resulting DataFrame will be identical.

Requires the index and columns to have the same number of levels.

Pass `sort=False` if index and columns should not be sorted, but concatenated and get duplicates removed.

**Usage**
    
    
    >>> import pandas as pd
    >>> from vectorbt.base.reshape_fns import make_symmetric
    
    >>> df = pd.DataFrame([[1, 2], [3, 4]], index=['a', 'b'], columns=['c', 'd'])
    
    >>> make_symmetric(df)
         a    b    c    d
    a  NaN  NaN  1.0  2.0
    b  NaN  NaN  3.0  4.0
    c  1.0  3.0  NaN  NaN
    d  2.0  4.0  NaN  NaN
    

* * *

## repeat function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L120-L135 "Jump to source")¶
    
    
    repeat(
        arg,
        n,
        axis=1,
        raw=False
    )
    

Repeat each element in `arg` `n` times along the specified axis.

* * *

## soft_to_ndim function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L51-L65 "Jump to source")¶
    
    
    soft_to_ndim(
        arg,
        ndim,
        raw=False
    )
    

Try to softly bring `arg` to the specified number of dimensions `ndim` (max 2).

* * *

## tile function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L138-L158 "Jump to source")¶
    
    
    tile(
        arg,
        n,
        axis=1,
        raw=False
    )
    

Repeat the whole `arg` `n` times along the specified axis.

* * *

## to_1d function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L68-L83 "Jump to source")¶
    
    
    to_1d(
        arg,
        raw=False
    )
    

Reshape argument to one dimension. 

If `raw` is True, returns NumPy array. If 2-dim, will collapse along axis 1 (i.e., DataFrame with one column to Series).

* * *

## to_2d function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L89-L106 "Jump to source")¶
    
    
    to_2d(
        arg,
        raw=False,
        expand_axis=1
    )
    

Reshape argument to two dimensions. 

If `raw` is True, returns NumPy array. If 1-dim, will expand along axis 1 (i.e., Series to DataFrame with one column).

* * *

## to_any_array function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L30-L36 "Jump to source")¶
    
    
    to_any_array(
        arg,
        raw=False
    )
    

Convert any array-like object to an array.

Pandas objects are kept as-is.

* * *

## to_dict function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L112-L117 "Jump to source")¶
    
    
    to_dict(
        arg,
        orient='dict'
    )
    

Convert object to dict.

* * *

## to_pd_array function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L39-L48 "Jump to source")¶
    
    
    to_pd_array(
        arg
    )
    

Convert any array-like object to a pandas object.

* * *

## unstack_to_array function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L746-L798 "Jump to source")¶
    
    
    unstack_to_array(
        arg,
        levels=None
    )
    

Reshape `arg` based on its multi-index into a multi-dimensional array.

Use `levels` to specify what index levels to unstack and in which order.

**Usage**
    
    
    >>> import pandas as pd
    >>> from vectorbt.base.reshape_fns import unstack_to_array
    
    >>> index = pd.MultiIndex.from_arrays(
    ...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']])
    >>> sr = pd.Series([1, 2, 3, 4], index=index)
    
    >>> unstack_to_array(sr).shape
    (2, 2, 4)
    
    >>> unstack_to_array(sr)
    [[[ 1. nan nan nan]
     [nan  2. nan nan]]
    
     [[nan nan  3. nan]
    [nan nan nan  4.]]]
    
    >>> unstack_to_array(sr, levels=(2, 0))
    [[ 1. nan]
     [ 2. nan]
     [nan  3.]
     [nan  4.]]
    

* * *

## unstack_to_df function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L867-L919 "Jump to source")¶
    
    
    unstack_to_df(
        arg,
        index_levels=None,
        column_levels=None,
        symmetric=False,
        sort=True
    )
    

Reshape `arg` based on its multi-index into a DataFrame.

Use `index_levels` to specify what index levels will form new index, and `column_levels` for new columns. Set `symmetric` to True to make DataFrame symmetric.

**Usage**
    
    
    >>> import pandas as pd
    >>> from vectorbt.base.reshape_fns import unstack_to_df
    
    >>> index = pd.MultiIndex.from_arrays(
    ...     [[1, 1, 2, 2], [3, 4, 3, 4], ['a', 'b', 'c', 'd']],
    ...     names=['x', 'y', 'z'])
    >>> sr = pd.Series([1, 2, 3, 4], index=index)
    
    >>> unstack_to_df(sr, index_levels=(0, 1), column_levels=2)
    z      a    b    c    d
    x y
    1 3  1.0  NaN  NaN  NaN
    1 4  NaN  2.0  NaN  NaN
    2 3  NaN  NaN  3.0  NaN
    2 4  NaN  NaN  NaN  4.0
    

* * *

## wrap_broadcasted function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/reshape_fns.py#L290-L323 "Jump to source")¶
    
    
    wrap_broadcasted(
        old_arg,
        new_arg,
        is_pd=False,
        new_index=None,
        new_columns=None
    )
    

If the newly brodcasted array was originally a pandas object, make it pandas object again and assign it the newly broadcast index/columns.

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
