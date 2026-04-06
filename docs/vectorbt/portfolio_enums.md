# enums - VectorBT

> **Source:** https://vectorbt.dev/api/portfolio/enums/

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
      * enums  [ enums  ](https://vectorbt.dev/api/portfolio/enums/) Table of contents 
        * AccumulationMode 
        * CallSeqType 
        * ConflictMode 
        * Direction 
        * DirectionConflictMode 
        * InitCashMode 
        * NoOrder 
        * OppositeEntryMode 
        * OrderSide 
        * OrderStatus 
        * OrderStatusInfo 
        * SizeType 
        * StopEntryPrice 
        * StopExitMode 
        * StopExitPrice 
        * StopUpdateMode 
        * TradeDirection 
        * TradeStatus 
        * TradesType 
        * log_dt 
        * order_dt 
        * status_info_desc 
        * trade_dt 
        * AccumulationModeT() 
          * AddOnly 
          * Both 
          * Disabled 
          * RemoveOnly 
        * AdjustSLContext() 
          * col 
          * curr_i 
          * curr_price 
          * curr_stop 
          * curr_trail 
          * i 
          * init_i 
          * init_price 
          * position_now 
          * val_price_now 
        * AdjustTPContext() 
          * col 
          * curr_stop 
          * i 
          * init_i 
          * init_price 
          * position_now 
          * val_price_now 
        * CallSeqTypeT() 
          * Auto 
          * Default 
          * Random 
          * Reversed 
        * ConflictModeT() 
          * Adjacent 
          * Entry 
          * Exit 
          * Ignore 
          * Opposite 
        * DirectionConflictModeT() 
          * Adjacent 
          * Ignore 
          * Long 
          * Opposite 
          * Short 
        * DirectionT() 
          * Both 
          * LongOnly 
          * ShortOnly 
        * ExecuteOrderState() 
          * cash 
          * debt 
          * free_cash 
          * position 
        * FlexOrderContext() 
          * call_idx 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * call_seq_now 
          * cash_sharing 
          * close 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * from_col 
          * group 
          * group_len 
          * group_lens 
          * i 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * to_col 
          * update_value 
        * GroupContext() 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * cash_sharing 
          * close 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * from_col 
          * group 
          * group_len 
          * group_lens 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * to_col 
          * update_value 
        * InitCashModeT() 
          * Auto 
          * AutoAlign 
        * OppositeEntryModeT() 
          * Close 
          * CloseReduce 
          * Ignore 
          * Reverse 
          * ReverseReduce 
        * Order() 
          * allow_partial 
          * direction 
          * fees 
          * fixed_fees 
          * lock_cash 
          * log 
          * max_size 
          * min_size 
          * price 
          * raise_reject 
          * reject_prob 
          * size 
          * size_granularity 
          * size_type 
          * slippage 
        * OrderContext() 
          * call_idx 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * call_seq_now 
          * cash_now 
          * cash_sharing 
          * close 
          * col 
          * debt_now 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * free_cash_now 
          * from_col 
          * group 
          * group_len 
          * group_lens 
          * i 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * pos_record_now 
          * position_now 
          * return_now 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * to_col 
          * update_value 
          * val_price_now 
          * value_now 
        * OrderResult() 
          * fees 
          * price 
          * side 
          * size 
          * status 
          * status_info 
        * OrderSideT() 
          * Buy 
          * Sell 
        * OrderStatusInfoT() 
          * CantCoverFees 
          * MaxSizeExceeded 
          * MinSizeNotReached 
          * NoCashLong 
          * NoCashShort 
          * NoOpenPosition 
          * PartialFill 
          * PriceNaN 
          * RandomEvent 
          * SizeNaN 
          * SizeZero 
          * ValPriceNaN 
          * ValueNaN 
          * ValueZeroNeg 
        * OrderStatusT() 
          * Filled 
          * Ignored 
          * Rejected 
        * PostOrderContext() 
          * call_idx 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * call_seq_now 
          * cash_before 
          * cash_now 
          * cash_sharing 
          * close 
          * col 
          * debt_before 
          * debt_now 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * free_cash_before 
          * free_cash_now 
          * from_col 
          * group 
          * group_len 
          * group_lens 
          * i 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * order_result 
          * pos_record_now 
          * position_before 
          * position_now 
          * return_now 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * to_col 
          * update_value 
          * val_price_before 
          * val_price_now 
          * value_before 
          * value_now 
        * ProcessOrderState() 
          * cash 
          * debt 
          * free_cash 
          * lidx 
          * oidx 
          * position 
          * val_price 
          * value 
        * RejectedOrderError() 
        * RowContext() 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * cash_sharing 
          * close 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * group_lens 
          * i 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * update_value 
        * SegmentContext() 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * call_seq_now 
          * cash_sharing 
          * close 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * from_col 
          * group 
          * group_len 
          * group_lens 
          * i 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * to_col 
          * update_value 
        * SignalContext() 
          * col 
          * flex_2d 
          * i 
          * position_now 
          * val_price_now 
        * SimulationContext() 
          * call_post_segment 
          * call_pre_segment 
          * call_seq 
          * cash_sharing 
          * close 
          * ffill_val_price 
          * fill_pos_record 
          * flex_2d 
          * group_lens 
          * init_cash 
          * last_cash 
          * last_debt 
          * last_free_cash 
          * last_lidx 
          * last_oidx 
          * last_pos_record 
          * last_position 
          * last_return 
          * last_val_price 
          * last_value 
          * log_records 
          * order_records 
          * second_last_value 
          * segment_mask 
          * target_shape 
          * update_value 
        * SizeTypeT() 
          * Amount 
          * Percent 
          * TargetAmount 
          * TargetPercent 
          * TargetValue 
          * Value 
        * StopEntryPriceT() 
          * Close 
          * FillPrice 
          * Price 
          * ValPrice 
        * StopExitModeT() 
          * Close 
          * CloseReduce 
          * Reverse 
          * ReverseReduce 
        * StopExitPriceT() 
          * Close 
          * Price 
          * StopLimit 
          * StopMarket 
        * StopUpdateModeT() 
          * Keep 
          * Override 
          * OverrideNaN 
        * TradeDirectionT() 
          * Long 
          * Short 
        * TradeStatusT() 
          * Closed 
          * Open 
        * TradesTypeT() 
          * EntryTrades 
          * ExitTrades 
          * Positions 
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

  * AccumulationMode 
  * CallSeqType 
  * ConflictMode 
  * Direction 
  * DirectionConflictMode 
  * InitCashMode 
  * NoOrder 
  * OppositeEntryMode 
  * OrderSide 
  * OrderStatus 
  * OrderStatusInfo 
  * SizeType 
  * StopEntryPrice 
  * StopExitMode 
  * StopExitPrice 
  * StopUpdateMode 
  * TradeDirection 
  * TradeStatus 
  * TradesType 
  * log_dt 
  * order_dt 
  * status_info_desc 
  * trade_dt 
  * AccumulationModeT() 
    * AddOnly 
    * Both 
    * Disabled 
    * RemoveOnly 
  * AdjustSLContext() 
    * col 
    * curr_i 
    * curr_price 
    * curr_stop 
    * curr_trail 
    * i 
    * init_i 
    * init_price 
    * position_now 
    * val_price_now 
  * AdjustTPContext() 
    * col 
    * curr_stop 
    * i 
    * init_i 
    * init_price 
    * position_now 
    * val_price_now 
  * CallSeqTypeT() 
    * Auto 
    * Default 
    * Random 
    * Reversed 
  * ConflictModeT() 
    * Adjacent 
    * Entry 
    * Exit 
    * Ignore 
    * Opposite 
  * DirectionConflictModeT() 
    * Adjacent 
    * Ignore 
    * Long 
    * Opposite 
    * Short 
  * DirectionT() 
    * Both 
    * LongOnly 
    * ShortOnly 
  * ExecuteOrderState() 
    * cash 
    * debt 
    * free_cash 
    * position 
  * FlexOrderContext() 
    * call_idx 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * call_seq_now 
    * cash_sharing 
    * close 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * from_col 
    * group 
    * group_len 
    * group_lens 
    * i 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * to_col 
    * update_value 
  * GroupContext() 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * cash_sharing 
    * close 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * from_col 
    * group 
    * group_len 
    * group_lens 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * to_col 
    * update_value 
  * InitCashModeT() 
    * Auto 
    * AutoAlign 
  * OppositeEntryModeT() 
    * Close 
    * CloseReduce 
    * Ignore 
    * Reverse 
    * ReverseReduce 
  * Order() 
    * allow_partial 
    * direction 
    * fees 
    * fixed_fees 
    * lock_cash 
    * log 
    * max_size 
    * min_size 
    * price 
    * raise_reject 
    * reject_prob 
    * size 
    * size_granularity 
    * size_type 
    * slippage 
  * OrderContext() 
    * call_idx 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * call_seq_now 
    * cash_now 
    * cash_sharing 
    * close 
    * col 
    * debt_now 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * free_cash_now 
    * from_col 
    * group 
    * group_len 
    * group_lens 
    * i 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * pos_record_now 
    * position_now 
    * return_now 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * to_col 
    * update_value 
    * val_price_now 
    * value_now 
  * OrderResult() 
    * fees 
    * price 
    * side 
    * size 
    * status 
    * status_info 
  * OrderSideT() 
    * Buy 
    * Sell 
  * OrderStatusInfoT() 
    * CantCoverFees 
    * MaxSizeExceeded 
    * MinSizeNotReached 
    * NoCashLong 
    * NoCashShort 
    * NoOpenPosition 
    * PartialFill 
    * PriceNaN 
    * RandomEvent 
    * SizeNaN 
    * SizeZero 
    * ValPriceNaN 
    * ValueNaN 
    * ValueZeroNeg 
  * OrderStatusT() 
    * Filled 
    * Ignored 
    * Rejected 
  * PostOrderContext() 
    * call_idx 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * call_seq_now 
    * cash_before 
    * cash_now 
    * cash_sharing 
    * close 
    * col 
    * debt_before 
    * debt_now 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * free_cash_before 
    * free_cash_now 
    * from_col 
    * group 
    * group_len 
    * group_lens 
    * i 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * order_result 
    * pos_record_now 
    * position_before 
    * position_now 
    * return_now 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * to_col 
    * update_value 
    * val_price_before 
    * val_price_now 
    * value_before 
    * value_now 
  * ProcessOrderState() 
    * cash 
    * debt 
    * free_cash 
    * lidx 
    * oidx 
    * position 
    * val_price 
    * value 
  * RejectedOrderError() 
  * RowContext() 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * cash_sharing 
    * close 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * group_lens 
    * i 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * update_value 
  * SegmentContext() 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * call_seq_now 
    * cash_sharing 
    * close 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * from_col 
    * group 
    * group_len 
    * group_lens 
    * i 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * to_col 
    * update_value 
  * SignalContext() 
    * col 
    * flex_2d 
    * i 
    * position_now 
    * val_price_now 
  * SimulationContext() 
    * call_post_segment 
    * call_pre_segment 
    * call_seq 
    * cash_sharing 
    * close 
    * ffill_val_price 
    * fill_pos_record 
    * flex_2d 
    * group_lens 
    * init_cash 
    * last_cash 
    * last_debt 
    * last_free_cash 
    * last_lidx 
    * last_oidx 
    * last_pos_record 
    * last_position 
    * last_return 
    * last_val_price 
    * last_value 
    * log_records 
    * order_records 
    * second_last_value 
    * segment_mask 
    * target_shape 
    * update_value 
  * SizeTypeT() 
    * Amount 
    * Percent 
    * TargetAmount 
    * TargetPercent 
    * TargetValue 
    * Value 
  * StopEntryPriceT() 
    * Close 
    * FillPrice 
    * Price 
    * ValPrice 
  * StopExitModeT() 
    * Close 
    * CloseReduce 
    * Reverse 
    * ReverseReduce 
  * StopExitPriceT() 
    * Close 
    * Price 
    * StopLimit 
    * StopMarket 
  * StopUpdateModeT() 
    * Keep 
    * Override 
    * OverrideNaN 
  * TradeDirectionT() 
    * Long 
    * Short 
  * TradeStatusT() 
    * Closed 
    * Open 
  * TradesTypeT() 
    * EntryTrades 
    * ExitTrades 
    * Positions 



# enums module[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Named tuples and enumerated types.

Defines enums and other schemas for [vectorbt.portfolio](https://vectorbt.dev/api/portfolio/ "vectorbt.portfolio").

* * *

## AccumulationMode AccumulationModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Accumulation mode.
    
    
    {
        "Disabled": 0,
        "Both": 1,
        "AddOnly": 2,
        "RemoveOnly": 3
    }
    

Accumulation allows gradually increasing and decreasing positions by a size.

**Attributes**

**`Disabled`**
    Disable accumulation.
**`Both`**
    Allow both adding to and removing from the position.
**`AddOnly`**
    Allow accumulation to only add to the position.
**`RemoveOnly`**
    Allow accumulation to only remove from the position.

Note

Accumulation acts differently for exits and opposite entries: exits reduce the current position but won't enter the opposite one, while opposite entries reduce the position by the same amount, but as soon as this position is closed, they begin to increase the opposite position.

The behavior for opposite entries can be changed by [OppositeEntryMode](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OppositeEntryMode "vectorbt.portfolio.enums.OppositeEntryMode") and for stop orders by [StopExitMode](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.StopExitMode "vectorbt.portfolio.enums.StopExitMode").

* * *

## CallSeqType CallSeqTypeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Call sequence type.
    
    
    {
        "Default": 0,
        "Reversed": 1,
        "Random": 2,
        "Auto": 3
    }
    

**Attributes**

**`Default`**
    Place calls from left to right.
**`Reversed`**
    Place calls from right to left.
**`Random`**
    Place calls randomly.
**`Auto`**
    Place calls dynamically based on order value.

* * *

## ConflictMode ConflictModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Conflict mode.
    
    
    {
        "Ignore": 0,
        "Entry": 1,
        "Exit": 2,
        "Adjacent": 3,
        "Opposite": 4
    }
    

What should happen if both entry and exit signals occur simultaneously?

**Attributes**

**`Ignore`**
    Ignore both signals.
**`Entry`**
    Execute the entry signal.
**`Exit`**
    Execute the exit signal.
**`Adjacent`**
    

Execute the adjacent signal.

Takes effect only when in position, otherwise ignores.

**`Opposite`**
    

Execute the opposite signal.

Takes effect only when in position, otherwise ignores.

* * *

## Direction DirectionT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Position direction.
    
    
    {
        "LongOnly": 0,
        "ShortOnly": 1,
        "Both": 2
    }
    

**Attributes**

**`LongOnly`**
    Only long positions.
**`ShortOnly`**
    Only short positions.
**`Both`**
    Both long and short positions.

* * *

## DirectionConflictMode DirectionConflictModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Direction conflict mode.
    
    
    {
        "Ignore": 0,
        "Long": 1,
        "Short": 2,
        "Adjacent": 3,
        "Opposite": 4
    }
    

What should happen if both long and short entry signals occur simultaneously?

**Attributes**

**`Ignore`**
    Ignore both entry signals.
**`Long`**
    Execute the long entry signal.
**`Short`**
    Execute the short entry signal.
**`Adjacent`**
    

Execute the adjacent entry signal. 

Takes effect only when in position, otherwise ignores.

**`Opposite`**
    

Execute the opposite entry signal. 

Takes effect only when in position, otherwise ignores.

* * *

## InitCashMode InitCashModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Initial cash mode.
    
    
    {
        "Auto": 0,
        "AutoAlign": 1
    }
    

**Attributes**

**`Auto`**
    Initial cash is infinite within simulation, and then set to the total cash spent.
**`AutoAlign`**
    Initial cash is set to the total cash spent across all columns.

* * *

## NoOrder Order[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order that should not be processed.

* * *

## OppositeEntryMode OppositeEntryModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Opposite entry mode.
    
    
    {
        "Ignore": 0,
        "Close": 1,
        "CloseReduce": 2,
        "Reverse": 3,
        "ReverseReduce": 4
    }
    

What should happen if an entry signal of opposite direction occurs before an exit signal?

**Attributes**

**`Ignore`**
    Ignore the opposite entry signal.
**`Close`**
    Close the current position.
**`CloseReduce`**
    Close the current position or reduce it if accumulation is enabled.
**`Reverse`**
    Reverse the current position.
**`ReverseReduce`**
    Reverse the current position or reduce it if accumulation is enabled.

* * *

## OrderSide OrderSideT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order side.
    
    
    {
        "Buy": 0,
        "Sell": 1
    }
    

* * *

## OrderStatus OrderStatusT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order status.
    
    
    {
        "Filled": 0,
        "Ignored": 1,
        "Rejected": 2
    }
    

**Attributes**

**`Filled`**
    Order has been filled.
**`Ignored`**
    Order has been ignored.
**`Rejected`**
    Order has been rejected.

* * *

## OrderStatusInfo OrderStatusInfoT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order status information.
    
    
    {
        "SizeNaN": 0,
        "PriceNaN": 1,
        "ValPriceNaN": 2,
        "ValueNaN": 3,
        "ValueZeroNeg": 4,
        "SizeZero": 5,
        "NoCashShort": 6,
        "NoCashLong": 7,
        "NoOpenPosition": 8,
        "MaxSizeExceeded": 9,
        "RandomEvent": 10,
        "CantCoverFees": 11,
        "MinSizeNotReached": 12,
        "PartialFill": 13
    }
    

* * *

## SizeType SizeTypeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Size type.
    
    
    {
        "Amount": 0,
        "Value": 1,
        "Percent": 2,
        "TargetAmount": 3,
        "TargetValue": 4,
        "TargetPercent": 5
    }
    

**Attributes**

**`Amount`**
    Amount of assets to trade.
**`Value`**
    

Asset value to trade.

Gets converted into `SizeType.Amount` using [OrderContext.val_price_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.val_price_now "vectorbt.portfolio.enums.OrderContext.val_price_now").

**`Percent`**
    

Percentage of available resources to use in either direction (not to be confused with the percentage of position value!)

  * When buying, it's the percentage of [OrderContext.cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.cash_now "vectorbt.portfolio.enums.OrderContext.cash_now"). 
  * When selling, it's the percentage of [OrderContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.position_now "vectorbt.portfolio.enums.OrderContext.position_now").
  * When short selling, it's the percentage of [OrderContext.free_cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.free_cash_now "vectorbt.portfolio.enums.OrderContext.free_cash_now").
  * When selling and short selling (i.e. reversing position), it's the percentage of [OrderContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.position_now "vectorbt.portfolio.enums.OrderContext.position_now") and [OrderContext.free_cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.free_cash_now "vectorbt.portfolio.enums.OrderContext.free_cash_now").



Note

Takes into account fees and slippage to find the limit. In reality, slippage and fees are not known beforehand.

**`TargetAmount`**
    

Target amount of assets to hold (= target position).

Uses [OrderContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.position_now "vectorbt.portfolio.enums.OrderContext.position_now") to get the current position. Gets converted into `SizeType.Amount`.

**`TargetValue`**
    

Target asset value. 

Uses [OrderContext.val_price_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.val_price_now "vectorbt.portfolio.enums.OrderContext.val_price_now") to get the current asset value. Gets converted into `SizeType.TargetAmount`.

**`TargetPercent`**
    

Target percentage of total value. 

Uses [OrderContext.value_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.value_now "vectorbt.portfolio.enums.OrderContext.value_now") to get the current total value. Gets converted into `SizeType.TargetValue`.

* * *

## StopEntryPrice StopEntryPriceT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Stop entry price.
    
    
    {
        "ValPrice": 0,
        "Price": 1,
        "FillPrice": 2,
        "Close": 3
    }
    

Which price to use as an initial stop price?

**Attributes**

**`ValPrice`**
    Asset valuation price.
**`Price`**
    Default price.
**`FillPrice`**
    Fill price (that is, slippage is already applied).
**`Close`**
    Closing price.

* * *

## StopExitMode StopExitModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Stop exit mode.
    
    
    {
        "Close": 0,
        "CloseReduce": 1,
        "Reverse": 2,
        "ReverseReduce": 3
    }
    

How to exit the current position upon a stop signal?

**Attributes**

**`Close`**
    Close the current position.
**`CloseReduce`**
    Close the current position or reduce it if accumulation is enabled.
**`Reverse`**
    Reverse the current position.
**`ReverseReduce`**
    Reverse the current position or reduce it if accumulation is enabled.

* * *

## StopExitPrice StopExitPriceT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Stop exit price.
    
    
    {
        "StopLimit": 0,
        "StopMarket": 1,
        "Price": 2,
        "Close": 3
    }
    

Which price to use when exiting a position upon a stop signal?

**Attributes**

**`StopLimit`**
    

Stop price as from a limit order.

If the stop was hit before, the opening price at the next bar is used. User-defined slippage is not applied.

**`StopMarket`**
    

Stop price as from a market order.

If the stop was hit before, the opening price at the next bar is used. User-defined slippage is applied.

**`Price`**
    

Default price.

User-defined slippage is applied.

Note

Make sure to use `StopExitPrice.Price` only together with `StopEntryPrice.Close`. Otherwise, there is no proof that the price comes after the stop price.

**`Close`**
    

Closing price.

User-defined slippage is applied.

Note

We can execute only one signal per asset and bar. This means the following:

1) Stop signal cannot be processed at the same bar as the entry signal.

2) When dealing with stop orders, we have another signal - stop signal - that may be in a conflict with the signals placed by the user. To choose between both, we assume that any stop signal comes before any other signal in time. Thus, make sure to always execute ordinary signals using the closing price when using stop orders. Otherwise, you're looking into the future.

* * *

## StopUpdateMode StopUpdateModeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Stop update mode.
    
    
    {
        "Keep": 0,
        "Override": 1,
        "OverrideNaN": 2
    }
    

What to do with the old stop upon new acquisition? 

**Attributes**

**`Keep`**
    Keep the old stop.
**`Override`**
    Override the old stop, but only if the new stop is not NaN.
**`OverrideNaN`**
    Override the old stop, even if the new stop is NaN.

* * *

## TradeDirection TradeDirectionT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Event direction.
    
    
    {
        "Long": 0,
        "Short": 1
    }
    

* * *

## TradeStatus TradeStatusT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Event status.
    
    
    {
        "Open": 0,
        "Closed": 1
    }
    

* * *

## TradesType TradesTypeT[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Trades type.
    
    
    {
        "EntryTrades": 0,
        "ExitTrades": 1,
        "Positions": 2
    }
    

* * *

## log_dt VoidDType[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

`np.dtype` of log records.
    
    
    {
        "id": "int64",
        "group": "int64",
        "col": "int64",
        "idx": "int64",
        "cash": "float64",
        "position": "float64",
        "debt": "float64",
        "free_cash": "float64",
        "val_price": "float64",
        "value": "float64",
        "req_size": "float64",
        "req_price": "float64",
        "req_size_type": "int64",
        "req_direction": "int64",
        "req_fees": "float64",
        "req_fixed_fees": "float64",
        "req_slippage": "float64",
        "req_min_size": "float64",
        "req_max_size": "float64",
        "req_size_granularity": "float64",
        "req_reject_prob": "float64",
        "req_lock_cash": "bool",
        "req_allow_partial": "bool",
        "req_raise_reject": "bool",
        "req_log": "bool",
        "new_cash": "float64",
        "new_position": "float64",
        "new_debt": "float64",
        "new_free_cash": "float64",
        "new_val_price": "float64",
        "new_value": "float64",
        "res_size": "float64",
        "res_price": "float64",
        "res_fees": "float64",
        "res_side": "int64",
        "res_status": "int64",
        "res_status_info": "int64",
        "order_id": "int64"
    }
    

* * *

## order_dt VoidDType[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

`np.dtype` of order records.
    
    
    {
        "id": "int64",
        "col": "int64",
        "idx": "int64",
        "size": "float64",
        "price": "float64",
        "fees": "float64",
        "side": "int64"
    }
    

* * *

## status_info_desc list[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order status description.
    
    
    [
        "Size is NaN",
        "Price is NaN",
        "Asset valuation price is NaN",
        "Asset/group value is NaN",
        "Asset/group value is zero or negative",
        "Size is zero",
        "Not enough cash to short",
        "Not enough cash to long",
        "No open position to reduce/close",
        "Size is greater than maximum allowed",
        "Random event happened",
        "Not enough cash to cover fees",
        "Final size is less than minimum allowed",
        "Final size is less than requested"
    ]
    

* * *

## trade_dt VoidDType[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

`np.dtype` of trade records.
    
    
    {
        "id": "int64",
        "col": "int64",
        "size": "float64",
        "entry_idx": "int64",
        "entry_price": "float64",
        "entry_fees": "float64",
        "exit_idx": "int64",
        "exit_price": "float64",
        "exit_fees": "float64",
        "pnl": "float64",
        "return": "float64",
        "direction": "int64",
        "status": "int64",
        "parent_id": "int64"
    }
    

* * *

## AccumulationModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L111-L115 "Jump to source")¶
    
    
    AccumulationModeT(
        Disabled=0,
        Both=1,
        AddOnly=2,
        RemoveOnly=3
    )
    

AccumulationModeT(Disabled, Both, AddOnly, RemoveOnly)

**Superclasses**

  * `builtins.tuple`



* * *

### AddOnly method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### Both method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Disabled method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### RemoveOnly method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

## AdjustSLContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1517-L1527 "Jump to source")¶
    
    
    AdjustSLContext(
        i,
        col,
        position_now,
        val_price_now,
        init_i,
        init_price,
        curr_i,
        curr_price,
        curr_stop,
        curr_trail
    )
    

A named tuple representing the context for generation of signals.

**Superclasses**

  * `builtins.tuple`



* * *

### col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Current column.

Has range `[0, target_shape[1])` and is always within `[from_col, to_col)`.

* * *

### curr_i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the row of the updated stop.

Gets updated once the price is updated.

* * *

### curr_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Current stop price.

Gets updated in trailing SL once a higher price is discovered.

* * *

### curr_stop method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Current stop value.

Can be updated by adjustment function.

* * *

### curr_trail method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Current trailing flag.

Can be updated by adjustment function.

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the current row.

Has range `[0, target_shape[0])`.

* * *

### init_i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the row of the initial stop.

Doesn't change.

* * *

### init_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Price of the initial stop.

Doesn't change.

* * *

### position_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest position.

* * *

### val_price_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest valuation price.

* * *

## AdjustTPContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1559-L1566 "Jump to source")¶
    
    
    AdjustTPContext(
        i,
        col,
        position_now,
        val_price_now,
        init_i,
        init_price,
        curr_stop
    )
    

A named tuple representing the context for adjusting take profit.

**Superclasses**

  * `builtins.tuple`



* * *

### col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.col "vectorbt.portfolio.enums.AdjustSLContext.col").

* * *

### curr_stop method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.curr_stop](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.curr_stop "vectorbt.portfolio.enums.AdjustSLContext.curr_stop").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.i "vectorbt.portfolio.enums.AdjustSLContext.i").

* * *

### init_i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.init_i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.init_i "vectorbt.portfolio.enums.AdjustSLContext.init_i").

* * *

### init_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.curr_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.curr_price "vectorbt.portfolio.enums.AdjustSLContext.curr_price").

* * *

### position_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.position_now "vectorbt.portfolio.enums.AdjustSLContext.position_now").

* * *

### val_price_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [AdjustSLContext.val_price_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.AdjustSLContext.val_price_now "vectorbt.portfolio.enums.AdjustSLContext.val_price_now").

* * *

## CallSeqTypeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L87-L91 "Jump to source")¶
    
    
    CallSeqTypeT(
        Default=0,
        Reversed=1,
        Random=2,
        Auto=3
    )
    

CallSeqTypeT(Default, Reversed, Random, Auto)

**Superclasses**

  * `builtins.tuple`



* * *

### Auto method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### Default method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Random method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### Reversed method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## ConflictModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L144-L149 "Jump to source")¶
    
    
    ConflictModeT(
        Ignore=0,
        Entry=1,
        Exit=2,
        Adjacent=3,
        Opposite=4
    )
    

ConflictModeT(Ignore, Entry, Exit, Adjacent, Opposite)

**Superclasses**

  * `builtins.tuple`



* * *

### Adjacent method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### Entry method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Exit method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### Ignore method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Opposite method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

## DirectionConflictModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L176-L181 "Jump to source")¶
    
    
    DirectionConflictModeT(
        Ignore=0,
        Long=1,
        Short=2,
        Adjacent=3,
        Opposite=4
    )
    

DirectionConflictModeT(Ignore, Long, Short, Adjacent, Opposite)

**Superclasses**

  * `builtins.tuple`



* * *

### Adjacent method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### Ignore method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Long method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Opposite method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

### Short method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

## DirectionT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L413-L416 "Jump to source")¶
    
    
    DirectionT(
        LongOnly=0,
        ShortOnly=1,
        Both=2
    )
    

DirectionT(LongOnly, ShortOnly, Both)

**Superclasses**

  * `builtins.tuple`



* * *

### Both method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### LongOnly method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### ShortOnly method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## ExecuteOrderState class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L600-L604 "Jump to source")¶
    
    
    ExecuteOrderState(
        cash,
        position,
        debt,
        free_cash
    )
    

State after order execution.

**Superclasses**

  * `builtins.tuple`



* * *

### cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [ProcessOrderState.cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.ProcessOrderState.cash "vectorbt.portfolio.enums.ProcessOrderState.cash").

* * *

### debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [ProcessOrderState.debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.ProcessOrderState.debt "vectorbt.portfolio.enums.ProcessOrderState.debt").

* * *

### free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [ProcessOrderState.free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.ProcessOrderState.free_cash "vectorbt.portfolio.enums.ProcessOrderState.free_cash").

* * *

### position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [ProcessOrderState.position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.ProcessOrderState.position "vectorbt.portfolio.enums.ProcessOrderState.position").

* * *

## FlexOrderContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1323-L1356 "Jump to source")¶
    
    
    FlexOrderContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        group,
        group_len,
        from_col,
        to_col,
        i,
        call_seq_now,
        call_idx
    )
    

A named tuple representing the context of a flexible order.

Contains all fields from [SegmentContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext "vectorbt.portfolio.enums.SegmentContext") plus the current call index.

Passed to `flex_order_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_idx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the current call.

* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### call_seq_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SegmentContext.call_seq_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext.call_seq_now "vectorbt.portfolio.enums.SegmentContext.call_seq_now").

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### from_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.from_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.from_col "vectorbt.portfolio.enums.GroupContext.from_col").

* * *

### group method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group "vectorbt.portfolio.enums.GroupContext.group").

* * *

### group_len method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group_len](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group_len "vectorbt.portfolio.enums.GroupContext.group_len").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [RowContext.i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.RowContext.i "vectorbt.portfolio.enums.RowContext.i").

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### to_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.to_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.to_col "vectorbt.portfolio.enums.GroupContext.to_col").

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

## GroupContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L959-L989 "Jump to source")¶
    
    
    GroupContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        group,
        group_len,
        from_col,
        to_col
    )
    

A named tuple representing the context of a group.

A group is a set of nearby columns that are somehow related (for example, by sharing the same capital). In each row, the columns under the same group are bound to the same segment.

Contains all fields from [SimulationContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext "vectorbt.portfolio.enums.SimulationContext") plus fields describing the current group.

Passed to `pre_group_func_nb` and `post_group_func_nb`.

**Example**

Consider a group of three columns, a group of two columns, and one more column:

group | group_len | from_col | to_col  
---|---|---|---  
0 | 3 | 0 | 3  
1 | 2 | 3 | 5  
2 | 1 | 5 | 6  
  
**Superclasses**

  * `builtins.tuple`



* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### from_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the first column in the current group.

Has range `[0, target_shape[1])`.

* * *

### group method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the current group.

Has range `[0, group_lens.shape[0])`.

* * *

### group_len method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Number of columns in the current group.

Scalar value. Same as `group_lens[group]`.

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### to_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the last column in the current group plus one.

Has range `[1, target_shape[1] + 1)`. 

If columns are not grouped, equals to `from_col + 1`.

Warning

In the last group, `to_col` points at a column that doesn't exist.

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

## InitCashModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L67-L69 "Jump to source")¶
    
    
    InitCashModeT(
        Auto=0,
        AutoAlign=1
    )
    

InitCashModeT(Auto, AutoAlign)

**Superclasses**

  * `builtins.tuple`



* * *

### Auto method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### AutoAlign method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## OppositeEntryModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L208-L213 "Jump to source")¶
    
    
    OppositeEntryModeT(
        Ignore=0,
        Close=1,
        CloseReduce=2,
        Reverse=3,
        ReverseReduce=4
    )
    

OppositeEntryModeT(Ignore, Close, CloseReduce, Reverse, ReverseReduce)

**Superclasses**

  * `builtins.tuple`



* * *

### Close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### CloseReduce method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### Ignore method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Reverse method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### ReverseReduce method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

## Order class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1377-L1392 "Jump to source")¶
    
    
    Order(
        size=inf,
        price=inf,
        size_type=0,
        direction=2,
        fees=0.0,
        fixed_fees=0.0,
        slippage=0.0,
        min_size=0.0,
        max_size=inf,
        size_granularity=nan,
        reject_prob=0.0,
        lock_cash=False,
        allow_partial=True,
        raise_reject=False,
        log=False
    )
    

A named tuple representing an order.

Note

Currently, Numba has issues with using defaults when filling named tuples. Use [order_nb()](https://vectorbt.dev/api/portfolio/nb/#vectorbt.portfolio.nb.order_nb "vectorbt.portfolio.nb.order_nb") to create an order.

**Superclasses**

  * `builtins.tuple`



* * *

### allow_partial method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to allow partial fill.

Otherwise, the order gets rejected.

Does not apply when [Order.size](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.size "vectorbt.portfolio.enums.Order.size") is `np.inf`.

* * *

### direction method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [Direction](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Direction "vectorbt.portfolio.enums.Direction").

* * *

### fees method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Fees in percentage of the order value.

Negative trading fees like -0.05 means earning 0.05% per trade instead of paying a fee.

Note

0.01 = 1%.

* * *

### fixed_fees method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Fixed amount of fees to pay for this order.

* * *

### lock_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to lock cash when shorting. 

If enabled, prevents `free_cash` from turning negative when buying or short selling. A negative `free_cash` means one column used collateral of another column, which is generally undesired.

* * *

### log method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to log this order by filling a log record. 

Remember to increase `max_logs`.

* * *

### max_size method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Maximum size in both directions. 

Higher than that will be partly filled.

* * *

### min_size method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Minimum size in both directions. 

Lower than that will be rejected.

* * *

### price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Price per unit. 

Final price will depend upon slippage.

  * If `-np.inf`, replaced by the current open (if available) or the previous close (≈ the current open in crypto).
  * If `np.inf`, replaced by the current close.



Note

Make sure to use timestamps that come between (and ideally not including) the current open and close.

* * *

### raise_reject method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to raise exception if order has been rejected.

Terminates the simulation.

* * *

### reject_prob method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Probability of rejecting this order to simulate a random rejection event.

Not everything goes smoothly in real life. Use random rejections to test your order management for robustness.

* * *

### size method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Size in units.

Behavior depends upon [Order.size_type](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.size_type "vectorbt.portfolio.enums.Order.size_type") and [Order.direction](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.direction "vectorbt.portfolio.enums.Order.direction").

For any fixed size:

  * Set to any number to buy/sell some fixed amount or value. Longs are limited by the current cash balance, while shorts are only limited if [Order.lock_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.lock_cash "vectorbt.portfolio.enums.Order.lock_cash").
  * Set to `np.inf` to buy for all cash, or `-np.inf` to sell for all free cash. If [Order.direction](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.direction "vectorbt.portfolio.enums.Order.direction") is not `Direction.Both`, `-np.inf` will close the position.
  * Set to `np.nan` or 0 to skip.



For any target size:

  * Set to any number to buy/sell an amount relative to the current position or value.
  * Set to 0 to close the current position.
  * Set to `np.nan` to skip.



* * *

### size_granularity method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Granularity of the size.

For example, granularity of 1.0 makes the quantity to behave like an integer. Placing an order of 12.5 shares (in any direction) will order exactly 12.0 shares.

Note

The filled size remains a floating number.

* * *

### size_type method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SizeType](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SizeType "vectorbt.portfolio.enums.SizeType").

* * *

### slippage method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Slippage in percentage of [Order.price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.Order.price "vectorbt.portfolio.enums.Order.price"). 

Slippage is a penalty applied on the price.

Note

0.01 = 1%.

* * *

## OrderContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1149-L1191 "Jump to source")¶
    
    
    OrderContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        group,
        group_len,
        from_col,
        to_col,
        i,
        call_seq_now,
        col,
        call_idx,
        cash_now,
        position_now,
        debt_now,
        free_cash_now,
        val_price_now,
        value_now,
        return_now,
        pos_record_now
    )
    

A named tuple representing the context of an order.

Contains all fields from [SegmentContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext "vectorbt.portfolio.enums.SegmentContext") plus fields describing the current state.

Passed to `order_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_idx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the current call in [SegmentContext.call_seq_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext.call_seq_now "vectorbt.portfolio.enums.SegmentContext.call_seq_now").

Has range `[0, group_len)`.

* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### call_seq_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SegmentContext.call_seq_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext.call_seq_now "vectorbt.portfolio.enums.SegmentContext.call_seq_now").

* * *

### cash_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash") for the current column/group.

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Current column.

Has range `[0, target_shape[1])` and is always within `[from_col, to_col)`.

* * *

### debt_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt") for the current column.

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### free_cash_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash") for the current column/group.

* * *

### from_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.from_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.from_col "vectorbt.portfolio.enums.GroupContext.from_col").

* * *

### group method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group "vectorbt.portfolio.enums.GroupContext.group").

* * *

### group_len method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group_len](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group_len "vectorbt.portfolio.enums.GroupContext.group_len").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [RowContext.i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.RowContext.i "vectorbt.portfolio.enums.RowContext.i").

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### pos_record_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record") for the current column.

* * *

### position_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position") for the current column.

* * *

### return_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return") for the current column/group.

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### to_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.to_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.to_col "vectorbt.portfolio.enums.GroupContext.to_col").

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

### val_price_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price") for the current column.

* * *

### value_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value") for the current column/group.

* * *

## OrderResult class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1499-L1505 "Jump to source")¶
    
    
    OrderResult(
        size,
        price,
        fees,
        side,
        status,
        status_info
    )
    

A named tuple representing an order result.

**Superclasses**

  * `builtins.tuple`



* * *

### fees method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Total fees paid for this order.

* * *

### price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Filled price per unit, adjusted with slippage.

* * *

### side method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [OrderSide](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderSide "vectorbt.portfolio.enums.OrderSide").

* * *

### size method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Filled size.

* * *

### status method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [OrderStatus](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderStatus "vectorbt.portfolio.enums.OrderStatus").

* * *

### status_info method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [OrderStatusInfo](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderStatusInfo "vectorbt.portfolio.enums.OrderStatusInfo").

* * *

## OrderSideT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L457-L459 "Jump to source")¶
    
    
    OrderSideT(
        Buy=0,
        Sell=1
    )
    

OrderSideT(Buy, Sell)

**Superclasses**

  * `builtins.tuple`



* * *

### Buy method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Sell method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## OrderStatusInfoT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L473-L487 "Jump to source")¶
    
    
    OrderStatusInfoT(
        SizeNaN=0,
        PriceNaN=1,
        ValPriceNaN=2,
        ValueNaN=3,
        ValueZeroNeg=4,
        SizeZero=5,
        NoCashShort=6,
        NoCashLong=7,
        NoOpenPosition=8,
        MaxSizeExceeded=9,
        RandomEvent=10,
        CantCoverFees=11,
        MinSizeNotReached=12,
        PartialFill=13
    )
    

OrderStatusInfoT(SizeNaN, PriceNaN, ValPriceNaN, ValueNaN, ValueZeroNeg, SizeZero, NoCashShort, NoCashLong, NoOpenPosition, MaxSizeExceeded, RandomEvent, CantCoverFees, MinSizeNotReached, PartialFill)

**Superclasses**

  * `builtins.tuple`



* * *

### CantCoverFees method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 11

* * *

### MaxSizeExceeded method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 9

* * *

### MinSizeNotReached method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 12

* * *

### NoCashLong method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 7

* * *

### NoCashShort method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 6

* * *

### NoOpenPosition method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 8

* * *

### PartialFill method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 13

* * *

### PriceNaN method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### RandomEvent method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 10

* * *

### SizeNaN method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### SizeZero method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 5

* * *

### ValPriceNaN method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### ValueNaN method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### ValueZeroNeg method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

## OrderStatusT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L435-L438 "Jump to source")¶
    
    
    OrderStatusT(
        Filled=0,
        Ignored=1,
        Rejected=2
    )
    

OrderStatusT(Filled, Ignored, Rejected)

**Superclasses**

  * `builtins.tuple`



* * *

### Filled method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Ignored method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Rejected method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

## PostOrderContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1227-L1276 "Jump to source")¶
    
    
    PostOrderContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        group,
        group_len,
        from_col,
        to_col,
        i,
        call_seq_now,
        col,
        call_idx,
        cash_before,
        position_before,
        debt_before,
        free_cash_before,
        val_price_before,
        value_before,
        order_result,
        cash_now,
        position_now,
        debt_now,
        free_cash_now,
        val_price_now,
        value_now,
        return_now,
        pos_record_now
    )
    

A named tuple representing the context after an order has been processed.

Contains all fields from [OrderContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext "vectorbt.portfolio.enums.OrderContext") plus fields describing the order result and the previous state.

Passed to `post_order_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_idx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [OrderContext.call_idx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.call_idx "vectorbt.portfolio.enums.OrderContext.call_idx").

* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### call_seq_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SegmentContext.call_seq_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext.call_seq_now "vectorbt.portfolio.enums.SegmentContext.call_seq_now").

* * *

### cash_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.cash_now "vectorbt.portfolio.enums.OrderContext.cash_now") before execution.

* * *

### cash_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.cash_now "vectorbt.portfolio.enums.OrderContext.cash_now") after execution.

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [OrderContext.col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.col "vectorbt.portfolio.enums.OrderContext.col").

* * *

### debt_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.debt_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.debt_now "vectorbt.portfolio.enums.OrderContext.debt_now") before execution.

* * *

### debt_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.debt_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.debt_now "vectorbt.portfolio.enums.OrderContext.debt_now") after execution.

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### free_cash_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.free_cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.free_cash_now "vectorbt.portfolio.enums.OrderContext.free_cash_now") before execution.

* * *

### free_cash_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.free_cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.free_cash_now "vectorbt.portfolio.enums.OrderContext.free_cash_now") after execution.

* * *

### from_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.from_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.from_col "vectorbt.portfolio.enums.GroupContext.from_col").

* * *

### group method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group "vectorbt.portfolio.enums.GroupContext.group").

* * *

### group_len method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group_len](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group_len "vectorbt.portfolio.enums.GroupContext.group_len").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [RowContext.i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.RowContext.i "vectorbt.portfolio.enums.RowContext.i").

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### order_result method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order result of type [OrderResult](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderResult "vectorbt.portfolio.enums.OrderResult").

Can be used to check whether the order has been filled, ignored, or rejected.

* * *

### pos_record_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.pos_record_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.pos_record_now "vectorbt.portfolio.enums.OrderContext.pos_record_now") after execution.

* * *

### position_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.position_now "vectorbt.portfolio.enums.OrderContext.position_now") before execution.

* * *

### position_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.position_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.position_now "vectorbt.portfolio.enums.OrderContext.position_now") after execution.

* * *

### return_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.return_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.return_now "vectorbt.portfolio.enums.OrderContext.return_now") after execution.

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### to_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.to_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.to_col "vectorbt.portfolio.enums.GroupContext.to_col").

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

### val_price_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.val_price_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.val_price_now "vectorbt.portfolio.enums.OrderContext.val_price_now") before execution.

* * *

### val_price_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.val_price_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.val_price_now "vectorbt.portfolio.enums.OrderContext.val_price_now") after execution.

If [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value"), gets replaced with the fill price, as it becomes the most recently known price. Otherwise, stays the same.

* * *

### value_before method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.value_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.value_now "vectorbt.portfolio.enums.OrderContext.value_now") before execution.

* * *

### value_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

[OrderContext.value_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.value_now "vectorbt.portfolio.enums.OrderContext.value_now") after execution.

If [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value"), gets updated with the new cash and value of the column. Otherwise, stays the same.

* * *

## ProcessOrderState class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L578-L586 "Jump to source")¶
    
    
    ProcessOrderState(
        cash,
        position,
        debt,
        free_cash,
        val_price,
        value,
        oidx,
        lidx
    )
    

State before or after order processing.

**Superclasses**

  * `builtins.tuple`



* * *

### cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Cash in the current column or group with cash sharing.

* * *

### debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Debt from shorting in the current column.

* * *

### free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Free cash in the current column or group with cash sharing.

* * *

### lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of log record.

* * *

### oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of order record.

* * *

### position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Position in the current column.

* * *

### val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Valuation price in the current column.

* * *

### value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Value in the current column or group with cash sharing.

* * *

## RejectedOrderError class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L59-L61 "Jump to source")¶
    
    
    RejectedOrderError(
        *args,
        **kwargs
    )
    

Rejected order error.

**Superclasses**

  * `builtins.BaseException`
  * `builtins.Exception`



* * *

## RowContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1036-L1063 "Jump to source")¶
    
    
    RowContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        i
    )
    

A named tuple representing the context of a row.

A row is a time step in which segments are executed.

Contains all fields from [SimulationContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext "vectorbt.portfolio.enums.SimulationContext") plus fields describing the current row.

Passed to `pre_row_func_nb` and `post_row_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the current row.

Has range `[0, target_shape[0])`.

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

## SegmentContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1083-L1115 "Jump to source")¶
    
    
    SegmentContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record,
        group,
        group_len,
        from_col,
        to_col,
        i,
        call_seq_now
    )
    

A named tuple representing the context of a segment.

A segment is an intersection between groups and rows. It's an entity that defines how and in which order elements within the same group and row are processed.

Contains all fields from [SimulationContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext "vectorbt.portfolio.enums.SimulationContext"), [GroupContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext "vectorbt.portfolio.enums.GroupContext"), and [RowContext](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.RowContext "vectorbt.portfolio.enums.RowContext"), plus fields describing the current segment.

Passed to `pre_segment_func_nb` and `post_segment_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment").

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.call_seq](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_seq "vectorbt.portfolio.enums.SimulationContext.call_seq").

* * *

### call_seq_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Sequence of calls within the current segment.

Has shape `(group_len,)`. 

Each value in this sequence should indicate the position of column in the group to call next. Processing goes always from left to right.

You can use `pre_segment_func_nb` to override `call_seq_now`.

**Example**

`[2, 0, 1]` would first call column 2, then 0, and finally 1.

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing").

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close").

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price").

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.fill_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.fill_pos_record "vectorbt.portfolio.enums.SimulationContext.fill_pos_record").

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.flex_2d](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.flex_2d "vectorbt.portfolio.enums.SimulationContext.flex_2d").

* * *

### from_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.from_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.from_col "vectorbt.portfolio.enums.GroupContext.from_col").

* * *

### group method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group "vectorbt.portfolio.enums.GroupContext.group").

* * *

### group_len method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.group_len](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.group_len "vectorbt.portfolio.enums.GroupContext.group_len").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.group_lens](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.group_lens "vectorbt.portfolio.enums.SimulationContext.group_lens").

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [RowContext.i](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.RowContext.i "vectorbt.portfolio.enums.RowContext.i").

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_cash "vectorbt.portfolio.enums.SimulationContext.last_cash").

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_debt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_debt "vectorbt.portfolio.enums.SimulationContext.last_debt").

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_free_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_free_cash "vectorbt.portfolio.enums.SimulationContext.last_free_cash").

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx").

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_pos_record](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_pos_record "vectorbt.portfolio.enums.SimulationContext.last_pos_record").

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_position](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_position "vectorbt.portfolio.enums.SimulationContext.last_position").

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_return](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_return "vectorbt.portfolio.enums.SimulationContext.last_return").

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.log_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.log_records "vectorbt.portfolio.enums.SimulationContext.log_records").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records").

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

* * *

### to_col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [GroupContext.to_col](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.GroupContext.to_col "vectorbt.portfolio.enums.GroupContext.to_col").

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

See [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value").

* * *

## SignalContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L1579-L1584 "Jump to source")¶
    
    
    SignalContext(
        i,
        col,
        position_now,
        val_price_now,
        flex_2d
    )
    

SignalContext(i, col, position_now, val_price_now, flex_2d)

**Superclasses**

  * `builtins.tuple`



* * *

### col method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

### i method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### position_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### val_price_now method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

## SimulationContext class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L614-L640 "Jump to source")¶
    
    
    SimulationContext(
        target_shape,
        group_lens,
        init_cash,
        cash_sharing,
        call_seq,
        segment_mask,
        call_pre_segment,
        call_post_segment,
        close,
        ffill_val_price,
        update_value,
        fill_pos_record,
        flex_2d,
        order_records,
        log_records,
        last_cash,
        last_position,
        last_debt,
        last_free_cash,
        last_val_price,
        last_value,
        second_last_value,
        last_return,
        last_oidx,
        last_lidx,
        last_pos_record
    )
    

A named tuple representing the context of a simulation.

Contains general information available to all other contexts.

Passed to `pre_sim_func_nb` and `post_sim_func_nb`.

**Superclasses**

  * `builtins.tuple`



* * *

### call_post_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to call `post_segment_func_nb` regardless of [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

Allows, for example, to write user-defined arrays such as returns at the end of each segment.

* * *

### call_pre_segment method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to call `pre_segment_func_nb` regardless of [SimulationContext.segment_mask](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.segment_mask "vectorbt.portfolio.enums.SimulationContext.segment_mask").

* * *

### call_seq method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Default sequence of calls per segment.

Controls the sequence in which `order_func_nb` is executed within each segment.

Has shape [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape") and each value must exist in the range `[0, group_len)`.

Note

To use `sort_call_seq_nb`, should be generated using `CallSeqType.Default`.

To change the call sequence dynamically, better change [SegmentContext.call_seq_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SegmentContext.call_seq_now "vectorbt.portfolio.enums.SegmentContext.call_seq_now") in-place.

**Example**

The default call sequence for three data points and two groups with three columns each:
    
    
    np.array([
        [0, 1, 2, 0, 1, 2],
        [0, 1, 2, 0, 1, 2],
        [0, 1, 2, 0, 1, 2]
    ])
    

* * *

### cash_sharing method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether cash sharing is enabled.

* * *

### close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest asset price at each time step.

Utilizes flexible indexing using [flex_select_auto_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_select_auto_nb "vectorbt.base.reshape_fns.flex_select_auto_nb") and `flex_2d`, so it can be passed as 

  * 2-dim array, 
  * 1-dim array per column (requires `flex_2d=True`), 
  * 1-dim array per row (requires `flex_2d=False`), and
  * a scalar. 



Broadcasts to the shape [SimulationContext.target_shape](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.target_shape "vectorbt.portfolio.enums.SimulationContext.target_shape").

Note

To modify the array in place, make sure to build an array of the full shape.

* * *

### ffill_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to track valuation price only if it's known.

Otherwise, unknown [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close") will lead to NaN in valuation price at the next timestamp.

* * *

### fill_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to fill position record.

Disable this to make simulation a bit faster for simple use cases.

* * *

### flex_2d method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether the elements in a 1-dim array should be treated per column rather than per row.

This flag is set automatically when using [Portfolio.from_order_func()](https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.from_order_func "vectorbt.portfolio.base.Portfolio.from_order_func") depending upon whether there is any argument that has been broadcast to 2 dimensions.

Has only effect when using flexible indexing, for example, with [flex_select_auto_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_select_auto_nb "vectorbt.base.reshape_fns.flex_select_auto_nb").

* * *

### group_lens method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Number of columns in each group.

Even if columns are not grouped, `group_lens` contains ones - one column per group.

**Example**

In pairs trading, `group_lens` would be `np.array([2])`, while three independent columns would be represented by `group_lens` of `np.array([1, 1, 1])`.

* * *

### init_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Initial capital per column or group with cash sharing.

If [SimulationContext.cash_sharing](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.cash_sharing "vectorbt.portfolio.enums.SimulationContext.cash_sharing"), has shape `(group_lens.shape[0],)`, otherwise has shape `(target_shape[1],)`.

**Example**

Consider three columns, each having $100 of starting capital. If we built one group of two columns with cash sharing and one (imaginary) group with the last column, the `init_cash` would be `np.array([200, 100])`. Without cash sharing, the `init_cash` would be `np.array([100, 100, 100])`.

* * *

### last_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest cash per column or group with cash sharing.

Has the same shape as [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

Gets updated right after `order_func_nb`.

* * *

### last_debt method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest debt from shorting per column.

Debt is the total value from shorting that hasn't been covered yet. Used to update [OrderContext.free_cash_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.free_cash_now "vectorbt.portfolio.enums.OrderContext.free_cash_now").

Has shape `(target_shape[1],)`. 

Gets updated right after `order_func_nb`.

* * *

### last_free_cash method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest free cash per column or group with cash sharing.

Free cash never goes above the initial level, because an operation always costs money.

Has shape `(target_shape[1],)`. 

Gets updated right after `order_func_nb`.

* * *

### last_lidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the latest log record of each column.

Similar to [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx") but for log records.

* * *

### last_oidx method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Index of the latest order record of each column.

Points to [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records") and has shape `(target_shape[1],)`.

**Example**

`last_oidx` of `np.array([1, 100, -1])` means the latest filled order is `order_records[1]` for the first column, `order_records[100]` for the second column, and no orders have been filled yet for the third column.

* * *

### last_pos_record method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest position record of each column.

It's a 1-dimensional array with records of type [trade_dt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.trade_dt "vectorbt.portfolio.enums.trade_dt").

Has shape `(target_shape[1],)`.

The array is initialized with empty records first (they contain random data) and the field `id` is set to -1. Once the first position is entered in a column, the `id` becomes 0 and the record materializes. Once the position is closed, the record fixes its identifier and other data until the next position is entered. 

The fields `entry_price` and `exit_price` are average entry and exit price respectively. The fields `pnl` and `return` contain statistics as if the position has been closed and are re-calculated using [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price") after `pre_segment_func_nb` (in case [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price") has been overridden) and before `post_segment_func_nb`.

Note

In an open position record, the field `exit_price` doesn't reflect the latest valuation price, but keeps the average price at which the position has been reduced.

The position record is updated after successfully filling an order (after `order_func_nb` and before `post_order_func_nb`).

**Example**

Consider a simulation that orders `order_size` for `order_price` and $1 fixed fees. Here's order info from `order_func_nb` and the updated position info from `post_order_func_nb`:
    
    
        order_size  order_price  id  col  size  entry_idx  entry_price  \
    0          NaN            1  -1    0   1.0         13    14.000000   
    1          0.5            2   0    0   0.5          1     2.000000   
    2          1.0            3   0    0   1.5          1     2.666667   
    3          NaN            4   0    0   1.5          1     2.666667   
    4         -1.0            5   0    0   1.5          1     2.666667   
    5         -0.5            6   0    0   1.5          1     2.666667   
    6          NaN            7   0    0   1.5          1     2.666667   
    7         -0.5            8   1    0   0.5          7     8.000000   
    8         -1.0            9   1    0   1.5          7     8.666667   
    9          1.0           10   1    0   1.5          7     8.666667   
    10         0.5           11   1    0   1.5          7     8.666667   
    11         1.0           12   2    0   1.0         11    12.000000   
    12        -2.0           13   3    0   1.0         12    13.000000   
    13         2.0           14   4    0   1.0         13    14.000000   
    
        entry_fees  exit_idx  exit_price  exit_fees   pnl    return  direction  status
    0          0.5        -1         NaN        0.0 -0.50 -0.035714          0       0
    1          1.0        -1         NaN        0.0 -1.00 -1.000000          0       0
    2          2.0        -1         NaN        0.0 -1.50 -0.375000          0       0
    3          2.0        -1         NaN        0.0 -0.75 -0.187500          0       0
    4          2.0        -1    5.000000        1.0  0.50  0.125000          0       0
    5          2.0         5    5.333333        2.0  0.00  0.000000          0       1
    6          2.0         5    5.333333        2.0  0.00  0.000000          0       1
    7          1.0        -1         NaN        0.0 -1.00 -0.250000          1       0
    8          2.0        -1         NaN        0.0 -2.50 -0.192308          1       0
    9          2.0        -1   10.000000        1.0 -5.00 -0.384615          1       0
    10         2.0        10   10.333333        2.0 -6.50 -0.500000          1       1
    11         1.0        -1         NaN        0.0 -1.00 -0.083333          0       0
    12         0.5        -1         NaN        0.0 -0.50 -0.038462          1       0
    13         0.5        -1         NaN        0.0 -0.50 -0.035714          0       0
    

* * *

### last_position method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest position per column.

Has shape `(target_shape[1],)`.

Gets updated right after `order_func_nb`.

* * *

### last_return method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest return per column or group with cash sharing.

Has the same shape as [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

Calculated by comparing [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value") to [SimulationContext.second_last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.second_last_value "vectorbt.portfolio.enums.SimulationContext.second_last_value").

Gets updated each time [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value") is updated.

* * *

### last_val_price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest valuation price per column.

Has shape `(target_shape[1],)`.

Enables `SizeType.Value`, `SizeType.TargetValue`, and `SizeType.TargetPercent`.

Gets multiplied by the current position to get the value of the column (see [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value")).

Defaults to the [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close") before `post_segment_func_nb`. If [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price"), gets updated only if [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close") is not NaN. For example, close of `[1, 2, np.nan, np.nan, 5]` yields valuation price of `[1, 2, 2, 2, 5]`.

Also gets updated right after `pre_segment_func_nb` \- you can use `pre_segment_func_nb` to override `last_val_price` in-place, such that `order_func_nb` can use the new group value. You are not allowed to use `-np.inf` or `np.inf` \- only finite values. If [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value"), gets also updated right after `order_func_nb` using filled order price as the latest known price.

Note

Since the previous [SimulationContext.close](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.close "vectorbt.portfolio.enums.SimulationContext.close") is NaN in the first row, the first `last_val_price` is also NaN.

Overriding `last_val_price` with NaN won't apply [SimulationContext.ffill_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.ffill_val_price "vectorbt.portfolio.enums.SimulationContext.ffill_val_price"), so your entire group will become NaN.

**Example**

Consider 10 units in column 1 and 20 units in column 2. The previous close of them is $40 and $50 respectively, which is also the default valuation price in the current row, available as `last_val_price` in `pre_segment_func_nb`. If both columns are in the same group with cash sharing, the group is valued at $1400 before any `order_func_nb` is called, and can be later accessed via [OrderContext.value_now](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.OrderContext.value_now "vectorbt.portfolio.enums.OrderContext.value_now").

* * *

### last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Latest value per column or group with cash sharing.

Has the same shape as [SimulationContext.init_cash](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.init_cash "vectorbt.portfolio.enums.SimulationContext.init_cash").

Calculated by multiplying valuation price by the current position. The value of each column in a group with cash sharing is summed to get the value of the entire group.

Gets updated using [SimulationContext.last_val_price](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_val_price "vectorbt.portfolio.enums.SimulationContext.last_val_price") after `pre_segment_func_nb` and before `post_segment_func_nb`. If [SimulationContext.update_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.update_value "vectorbt.portfolio.enums.SimulationContext.update_value"), gets also updated right after `order_func_nb` using filled order price as the latest known price (the difference will be minimal, only affected by costs).

* * *

### log_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Log records.

Similar to [SimulationContext.order_records](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.order_records "vectorbt.portfolio.enums.SimulationContext.order_records") but of type [log_dt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.log_dt "vectorbt.portfolio.enums.log_dt") and index [SimulationContext.last_lidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_lidx "vectorbt.portfolio.enums.SimulationContext.last_lidx").

* * *

### order_records method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Order records.

It's a 1-dimensional array with records of type [order_dt](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.order_dt "vectorbt.portfolio.enums.order_dt").

The array is initialized with empty records first (they contain random data), and then gradually filled with order data. The number of initialized records depends upon `max_orders`, but usually it's `target_shape[0] * target_shape[1]`, meaning there is maximal one order record per element. `max_orders` can be chosen lower if not every `order_func_nb` leads to a filled order, to save memory.

You can use [SimulationContext.last_oidx](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_oidx "vectorbt.portfolio.enums.SimulationContext.last_oidx") to get the index of the latest filled order of each column.

**Example**

Before filling, each order record looks like this:
    
    
    np.array([(-8070450532247928832, -8070450532247928832, 4, 0., 0., 0., 5764616306889786413)]
    

After filling, it becomes like this:
    
    
    np.array([(0, 0, 1, 50., 1., 0., 1)]
    

* * *

### second_last_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Second-latest value per column or group with cash sharing.

Has the same shape as [SimulationContext.last_value](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.last_value "vectorbt.portfolio.enums.SimulationContext.last_value").

Contains the latest known value two rows before (`i - 2`) to be compared either with the latest known value one row before (`i - 1`) or now (`i`).

Gets updated at the end of each segment/row. 

* * *

### segment_mask method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Mask of whether a particular segment should be executed.

A segment is simply a sequence of `order_func_nb` calls under the same group and row.

If a segment is inactive, any callback function inside of it will not be executed. You can still execute the segment's pre- and postprocessing function by enabling [SimulationContext.call_pre_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_pre_segment "vectorbt.portfolio.enums.SimulationContext.call_pre_segment") and [SimulationContext.call_post_segment](https://vectorbt.dev/api/portfolio/enums/#vectorbt.portfolio.enums.SimulationContext.call_post_segment "vectorbt.portfolio.enums.SimulationContext.call_post_segment") respectively.

Utilizes flexible indexing using [flex_select_auto_nb()](https://vectorbt.dev/api/base/reshape_fns/#vectorbt.base.reshape_fns.flex_select_auto_nb "vectorbt.base.reshape_fns.flex_select_auto_nb") and `flex_2d`, so it can be passed as 

  * 2-dim array, 
  * 1-dim array per column (requires `flex_2d=True`), 
  * 1-dim array per row (requires `flex_2d=False`), and
  * a scalar. 



Broadcasts to the shape `(target_shape[0], group_lens.shape[0])`.

Note

To modify the array in place, make sure to build an array of the full shape.

**Example**

Consider two groups with two columns each and the following activity mask:
    
    
    np.array([[ True, False], 
              [False,  True]])
    

The first group is only executed in the first row and the second group is only executed in the second row.

* * *

### target_shape method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Target shape of the simulation.

A tuple with exactly two elements: the number of rows and columns.

**Example**

One day of minute data for three assets would yield a `target_shape` of `(1440, 3)`, where the first axis are rows (minutes) and the second axis are columns (assets).

* * *

### update_value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Whether to update group value after each filled order.

Otherwise, stays the same for all columns in the group (the value is calculated only once, before executing any order).

The change is marginal and mostly driven by transaction costs and slippage.

* * *

## SizeTypeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L363-L369 "Jump to source")¶
    
    
    SizeTypeT(
        Amount=0,
        Value=1,
        Percent=2,
        TargetAmount=3,
        TargetValue=4,
        TargetPercent=5
    )
    

SizeTypeT(Amount, Value, Percent, TargetAmount, TargetValue, TargetPercent)

**Superclasses**

  * `builtins.tuple`



* * *

### Amount method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Percent method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### TargetAmount method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### TargetPercent method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 5

* * *

### TargetValue method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 4

* * *

### Value method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## StopEntryPriceT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L236-L240 "Jump to source")¶
    
    
    StopEntryPriceT(
        ValPrice=0,
        Price=1,
        FillPrice=2,
        Close=3
    )
    

StopEntryPriceT(ValPrice, Price, FillPrice, Close)

**Superclasses**

  * `builtins.tuple`



* * *

### Close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### FillPrice method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### Price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### ValPrice method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

## StopExitModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L312-L316 "Jump to source")¶
    
    
    StopExitModeT(
        Close=0,
        CloseReduce=1,
        Reverse=2,
        ReverseReduce=3
    )
    

StopExitModeT(Close, CloseReduce, Reverse, ReverseReduce)

**Superclasses**

  * `builtins.tuple`



* * *

### Close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### CloseReduce method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Reverse method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### ReverseReduce method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

## StopExitPriceT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L262-L266 "Jump to source")¶
    
    
    StopExitPriceT(
        StopLimit=0,
        StopMarket=1,
        Price=2,
        Close=3
    )
    

StopExitPriceT(StopLimit, StopMarket, Price, Close)

**Superclasses**

  * `builtins.tuple`



* * *

### Close method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 3

* * *

### Price method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

### StopLimit method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### StopMarket method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## StopUpdateModeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L339-L342 "Jump to source")¶
    
    
    StopUpdateModeT(
        Keep=0,
        Override=1,
        OverrideNaN=2
    )
    

StopUpdateModeT(Keep, Override, OverrideNaN)

**Superclasses**

  * `builtins.tuple`



* * *

### Keep method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Override method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### OverrideNaN method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

## TradeDirectionT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L526-L528 "Jump to source")¶
    
    
    TradeDirectionT(
        Long=0,
        Short=1
    )
    

TradeDirectionT(Long, Short)

**Superclasses**

  * `builtins.tuple`



* * *

### Long method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### Short method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

## TradeStatusT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L542-L544 "Jump to source")¶
    
    
    TradeStatusT(
        Open=0,
        Closed=1
    )
    

TradeStatusT(Open, Closed)

**Superclasses**

  * `builtins.tuple`



* * *

### Closed method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Open method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

## TradesTypeT class[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py#L558-L561 "Jump to source")¶
    
    
    TradesTypeT(
        EntryTrades=0,
        ExitTrades=1,
        Positions=2
    )
    

TradesTypeT(EntryTrades, ExitTrades, Positions)

**Superclasses**

  * `builtins.tuple`



* * *

### EntryTrades method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 0

* * *

### ExitTrades method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 1

* * *

### Positions method-wrapper[](https://github.com/polakowo/vectorbt/blob/993ceca7116fc8e55f4cd3a36fe43d83dab62b27/vectorbt/portfolio/enums.py "Jump to source")¶

Alias for field number 2

* * *

[ ](https://github.com/sponsors/polakowo "Become a sponsor")

* * *
