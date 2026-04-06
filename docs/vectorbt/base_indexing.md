# indexing - VectorBT

> **Source:** https://vectorbt.dev/api/base/indexing/

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
      * indexing  [ indexing  ](https://vectorbt.dev/api/base/indexing/) Table of contents 
        * build_param_indexer() 
        * indexing_on_mapper() 
        * IndexingBase() 
          * indexing_func() 
        * IndexingError() 
        * Loc() 
        * LocBase() 
          * indexing_func 
          * indexing_kwargs 
        * PandasIndexer() 
          * iloc 
          * indexing_kwargs 
          * loc 
          * xs() 
        * ParamLoc() 
          * get_indices() 
          * level_name 
          * mapper 
        * iLoc() 
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

  * build_param_indexer() 
  * indexing_on_mapper() 
  * IndexingBase() 
    * indexing_func() 
  * IndexingError() 
  * Loc() 
  * LocBase() 
    * indexing_func 
    * indexing_kwargs 
  * PandasIndexer() 
    * iloc 
    * indexing_kwargs 
    * loc 
    * xs() 
  * ParamLoc() 
    * get_indices() 
    * level_name 
    * mapper 
  * iLoc() 



# indexing module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py "Jump to source")¶

Classes for indexing.

The main purpose of indexing classes is to provide pandas-like indexing to user-defined classes holding objects that have rows and/or columns. This is done by forwarding indexing commands to each structured object and constructing the new user-defined class using them. This way, one can manipulate complex classes with dozens of pandas objects using a single command.

* * *

## build_param_indexer function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L242-L323 "Jump to source")¶
    
    
    build_param_indexer(
        param_names,
        class_name='ParamIndexer',
        module_name=None
    )
    

A factory to create a class with parameter indexing.

Parameter indexer enables accessing a group of rows and columns by a parameter array (similar to `loc`). This way, one can query index/columns by another Series called a parameter mapper, which is just a `pd.Series` that maps columns (its index) to params (its values).

Parameter indexing is important, since querying by column/index labels alone is not always the best option. For example, `pandas` doesn't let you query by list at a specific index/column level.

**Args**

**`param_names`** : `list` of `str`
    Names of the parameters.
**`class_name`** : `str`
    Name of the generated class.
**`module_name`** : `str`
    Name of the module to which the class should be bound.

**Usage**
    
    
    >>> import pandas as pd
    >>> from vectorbt.base.indexing import build_param_indexer, indexing_on_mapper
    
    >>> MyParamIndexer = build_param_indexer(['my_param'])
    >>> class C(MyParamIndexer):
    ...     def __init__(self, df, param_mapper):
    ...         self.df = df
    ...         self._my_param_mapper = param_mapper
    ...         super().__init__([param_mapper])
    ...
    ...     def indexing_func(self, pd_indexing_func):
    ...         return self.__class__(
    ...             pd_indexing_func(self.df),
    ...             indexing_on_mapper(self._my_param_mapper, self.df, pd_indexing_func)
    ...         )
    
    >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    >>> param_mapper = pd.Series(['First', 'Second'], index=['a', 'b'])
    >>> c = C(df, param_mapper)
    
    >>> c.my_param_loc['First'].df
    0    1
    1    2
    Name: a, dtype: int64
    
    >>> c.my_param_loc['Second'].df
    0    3
    1    4
    Name: b, dtype: int64
    
    >>> c.my_param_loc[['First', 'First', 'Second', 'Second']].df
          a     b
    0  1  1  3  3
    1  2  2  4  4
    

* * *

## indexing_on_mapper function[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L226-L239 "Jump to source")¶
    
    
    indexing_on_mapper(
        mapper,
        ref_obj,
        pd_indexing_func
    )
    

Broadcast `mapper` Series to `ref_obj` and perform pandas indexing using `pd_indexing_func`.

* * *

## IndexingBase class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L26-L33 "Jump to source")¶
    
    
    IndexingBase()
    

Class that supports indexing through [IndexingBase.indexing_func()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase.indexing_func "vectorbt.base.indexing.IndexingBase.indexing_func").

**Subclasses**

  * [PandasIndexer](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.PandasIndexer "vectorbt.base.indexing.PandasIndexer")
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.indicators.basic.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.labels.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`
  * `vectorbt.signals.generators.ParamIndexer`



* * *

### indexing_func method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L29-L33 "Jump to source")¶
    
    
    IndexingBase.indexing_func(
        pd_indexing_func,
        **kwargs
    )
    

Apply `pd_indexing_func` on all pandas objects in question and return a new instance of the class.

Should be overridden.

* * *

## IndexingError class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L19-L20 "Jump to source")¶
    
    
    IndexingError(
        *args,
        **kwargs
    )
    

Exception raised when an indexing error has occurred.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`



* * *

## Loc class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L65-L70 "Jump to source")¶
    
    
    Loc(
        indexing_func,
        **kwargs
    )
    

Forwards `pd.Series.loc`/`pd.DataFrame.loc` operation to each Series/DataFrame and returns a new class instance.

**Superclasses**

  * [LocBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase "vectorbt.base.indexing.LocBase")



**Inherited members**

  * [LocBase.indexing_func](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_func "vectorbt.base.indexing.LocBase.indexing_func")
  * [LocBase.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_kwargs "vectorbt.base.indexing.LocBase.indexing_kwargs")



* * *

## LocBase class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L36-L54 "Jump to source")¶
    
    
    LocBase(
        indexing_func,
        **kwargs
    )
    

Class that implements location-based indexing.

**Subclasses**

  * [Loc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.Loc "vectorbt.base.indexing.Loc")
  * [ParamLoc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.ParamLoc "vectorbt.base.indexing.ParamLoc")
  * [iLoc](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.iLoc "vectorbt.base.indexing.iLoc")



* * *

### indexing_func property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L43-L46 "Jump to source")¶

Indexing function.

* * *

### indexing_kwargs property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L48-L51 "Jump to source")¶

Keyword arguments passed to [LocBase.indexing_func](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_func "vectorbt.base.indexing.LocBase.indexing_func").

* * *

## PandasIndexer class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L76-L145 "Jump to source")¶
    
    
    PandasIndexer(
        **kwargs
    )
    

Implements indexing using `iloc`, `loc`, `xs` and `__getitem__`.

**Usage**
    
    
    >>> import pandas as pd
    >>> from vectorbt.base.indexing import PandasIndexer
    
    >>> class C(PandasIndexer):
    ...     def __init__(self, df1, df2):
    ...         self.df1 = df1
    ...         self.df2 = df2
    ...         super().__init__()
    ...
    ...     def indexing_func(self, pd_indexing_func):
    ...         return self.__class__(
    ...             pd_indexing_func(self.df1),
    ...             pd_indexing_func(self.df2)
    ...         )
    
    >>> df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    >>> df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})
    >>> c = C(df1, df2)
    
    >>> c.iloc[:, 0]
    <__main__.C object at 0x1a1cacbbe0>
    
    >>> c.iloc[:, 0].df1
    0    1
    1    2
    Name: a, dtype: int64
    
    >>> c.iloc[:, 0].df2
    0    5
    1    6
    Name: a, dtype: int64
    

**Superclasses**

  * [IndexingBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase "vectorbt.base.indexing.IndexingBase")



**Inherited members**

  * [IndexingBase.indexing_func()](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.IndexingBase.indexing_func "vectorbt.base.indexing.IndexingBase.indexing_func")



**Subclasses**

  * [ArrayWrapper](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.ArrayWrapper "vectorbt.base.array_wrapper.ArrayWrapper")
  * [Wrapping](https://vectorbt.dev/api/base/array_wrapper/#vectorbt.base.array_wrapper.Wrapping "vectorbt.base.array_wrapper.Wrapping")



* * *

### iloc property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L125-L128 "Jump to source")¶

Forwards `pd.Series.iloc`/`pd.DataFrame.iloc` operation to each Series/DataFrame and returns a new class instance.

* * *

### indexing_kwargs property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L120-L123 "Jump to source")¶

Indexing keyword arguments.

* * *

### loc property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L132-L135 "Jump to source")¶

Forwards `pd.Series.loc`/`pd.DataFrame.loc` operation to each Series/DataFrame and returns a new class instance.

* * *

### xs method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L139-L142 "Jump to source")¶
    
    
    PandasIndexer.xs(
        *args,
        **kwargs
    )
    

Forwards `pd.Series.xs`/`pd.DataFrame.xs` operation to each Series/DataFrame and returns a new class instance.

* * *

## ParamLoc class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L160-L223 "Jump to source")¶
    
    
    ParamLoc(
        mapper,
        indexing_func,
        level_name=None,
        **kwargs
    )
    

Access a group of columns by parameter using `pd.Series.loc`.

Uses `mapper` to establish link between columns and parameter values.

**Superclasses**

  * [LocBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase "vectorbt.base.indexing.LocBase")



**Inherited members**

  * [LocBase.indexing_func](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_func "vectorbt.base.indexing.LocBase.indexing_func")
  * [LocBase.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_kwargs "vectorbt.base.indexing.LocBase.indexing_kwargs")



* * *

### get_indices method[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L188-L207 "Jump to source")¶
    
    
    ParamLoc.get_indices(
        key
    )
    

Get array of indices affected by this key.

* * *

### level_name property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L183-L186 "Jump to source")¶

Level name.

* * *

### mapper property[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L178-L181 "Jump to source")¶

Mapper.

* * *

## iLoc class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/base/indexing.py#L57-L62 "Jump to source")¶
    
    
    iLoc(
        indexing_func,
        **kwargs
    )
    

Forwards `pd.Series.iloc`/`pd.DataFrame.iloc` operation to each Series/DataFrame and returns a new class instance.

**Superclasses**

  * [LocBase](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase "vectorbt.base.indexing.LocBase")



**Inherited members**

  * [LocBase.indexing_func](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_func "vectorbt.base.indexing.LocBase.indexing_func")
  * [LocBase.indexing_kwargs](https://vectorbt.dev/api/base/indexing/#vectorbt.base.indexing.LocBase.indexing_kwargs "vectorbt.base.indexing.LocBase.indexing_kwargs")



* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
