# Enums Definitions

> **Source:** https://bybit-exchange.github.io/docs/v5/enum

---

  * [](https://bybit-exchange.github.io/docs/)
  * Enums Definitions



On this page

# Enums Definitions

### locale​

  * `de-DE`
  * `en-US`
  * `es-AR`
  * `es-ES`
  * `es-MX`
  * `fr-FR`
  * `kk-KZ`
  * `id-ID`
  * `uk-UA`
  * `ja-JP`
  * `ru-RU`
  * `th-TH`
  * `pt-BR`
  * `tr-TR`
  * `vi-VN`
  * `zh-TW`
  * `ar-SA`
  * `hi-IN`
  * `fil-PH`



### announcementType​

  * `new_crypto`
  * `latest_bybit_news`
  * `delistings`
  * `latest_activities`
  * `product_updates`
  * `maintenance_updates`
  * `new_fiat_listings`
  * `other`



### announcementTag​

  * `Spot`
  * `Derivatives`
  * `Spot Listings`
  * `BTC`
  * `ETH`
  * `Trading Bots`
  * `USDC`
  * `Leveraged Tokens`
  * `USDT`
  * `Margin Trading`
  * `Partnerships`
  * `Launchpad`
  * `Upgrades`
  * `ByVotes`
  * `Delistings`
  * `VIP`
  * `Futures`
  * `Institutions`
  * `Options`
  * `WEB3`
  * `Copy Trading`
  * `Earn`
  * `Bybit Savings`
  * `Dual Asset`
  * `Liquidity Mining`
  * `Shark Fin`
  * `Launchpool`
  * `NFT GrabPic`
  * `Buy Crypto`
  * `P2P Trading`
  * `Fiat Deposit`
  * `Crypto Deposit`
  * `Спот`
  * `Спот лістинги`
  * `Торгові боти`
  * `Токени з кредитним плечем`
  * `Маржинальна торгівля`
  * `Партнерство`
  * `Оновлення`
  * `Делістинги`
  * `Ф'ючерси`
  * `Опціони`
  * `Копітрейдинг`
  * `Bybit Накопичення`
  * `Бівалютні інвестиції`
  * `Майнінг ліквідності`
  * `Купівля криптовалюти`
  * `P2P торгівля`
  * `Фіатні депозити`
  * `Криптодепозити`
  * `Копитрейдинг`
  * `Торговые боты`
  * `Деривативы`
  * `P2P`
  * `Спот листинги`
  * `Деривативи`
  * `MT4`
  * `Lucky Draw`
  * `Unified Trading Account`
  * `Єдиний торговий акаунт`
  * `Единый торговый аккаунт`
  * `Институциональный трейдинг`
  * `Інституціональний трейдинг`
  * `Делистинг`



### category​

  * `spot`
  * `linear` USDT perpetual, USDT Futures and USDC contract, including USDC perp, USDC futures
  * `inverse` Inverse contract, including Inverse perp, Inverse futures
  * `option`



### orderStatus​

 _open status_

  * `New` order has been placed successfully
  * `PartiallyFilled`
  * `Untriggered` Conditional orders are created



 _closed status_

  * `Rejected`
  * `PartiallyFilledCanceled` Only spot has this order status
  * `Filled`
  * `Cancelled` In derivatives, orders with this status may have an executed qty
  * `Triggered` instantaneous state for conditional orders from Untriggered to New
  * `Deactivated` UTA: Spot tp/sl order, conditional order, OCO order are cancelled before they are triggered



### timeInForce​

  * `GTC` GoodTillCancel
  * `IOC` ImmediateOrCancel
  * `FOK` FillOrKill
  * [PostOnly](https://www.bybit.com/en/help-center/article/Post-Only-Order)
  * [RPI](https://www.bybit.com/en/help-center/article/Retail-Price-Improvement-RPI-Order) features:
    * **Exclusive Matching** : Only match non-algorithmic users; no execution against orders from Open API.
    * **Post-Only Mechanism** : Act as maker orders, adding liquidity
    * **Lower Priority** : Execute after non-RPI orders at the same price level.
    * **Limited Access** : Initially for select market makers across multiple pairs.
    * **Order Book Updates** : Excluded from API but displayed on the GUI.



### createType​

  * `CreateByUser`
  * `CreateByFutureSpread` Spread order
  * `CreateByAdminClosing`
  * `CreateBySettle` USDC Futures delivery; position closed as a result of the delisting of a contract. This is recorded as a [trade](https://bybit-exchange.github.io/docs/v5/order/execution) but not an [order](https://bybit-exchange.github.io/docs/v5/order/order-list).
  * `CreateByStopOrder` Futures conditional order
  * `CreateByTakeProfit` Futures take profit order
  * `CreateByPartialTakeProfit` Futures partial take profit order
  * `CreateByStopLoss` Futures stop loss order
  * `CreateByPartialStopLoss` Futures partial stop loss order
  * `CreateByTrailingStop` Futures trailing stop order
  * `CreateByTrailingProfit` Futures trailing take profit order
  * `CreateByLiq` Laddered liquidation to reduce the required maintenance margin
  * `CreateByTakeOver_PassThrough`If the position is still subject to liquidation (i.e., does not meet the required maintenance margin level), the position shall be taken over by the liquidation engine and closed at the bankruptcy price.
  * `CreateByAdl_PassThrough` [Auto-Deleveraging(ADL)](https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL)
  * `CreateByBlock_PassThrough` Order placed via Paradigm
  * `CreateByBlockTradeMovePosition_PassThrough` Order created by move position
  * `CreateByClosing` The close order placed via web or app position area - web/app
  * `CreateByFGridBot` Order created via grid bot - web/app
  * `CloseByFGridBot` Order closed via grid bot - web/app
  * `CreateByTWAP` Order created by TWAP - web/app
  * `CreateByTVSignal` Order created by TV webhook - web/app
  * `CreateByMmRateClose` Order created by Mm rate close function - web/app
  * `CreateByMartingaleBot` Order created by Martingale bot - web/app
  * `CloseByMartingaleBot` Order closed by Martingale bot - web/app
  * `CreateByIceBerg` Order created by Ice berg strategy - web/app
  * `CreateByArbitrage` Order created by arbitrage - web/app
  * `CreateByDdh` Option dynamic delta hedge order - web/app
  * `CreateByBboOrder` BBO order



### execType​

  * `Trade`
  * `AdlTrade` [Auto-Deleveraging](https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL)
  * `Funding` [Funding fee](https://www.bybit.com/en/help-center/article/Introduction-to-Funding-Rate)
  * `BustTrade` Takeover liquidation
  * `Delivery` USDC futures delivery; Position closed by contract delisted
  * `Settle` Inverse futures settlement; Position closed due to delisting
  * `BlockTrade`
  * `MovePosition`
  * `FutureSpread` Spread leg execution
  * `UNKNOWN` May be returned by a classic account. Cannot query by this type



### orderType​

  * `Market`
  * `Limit`
  * `UNKNOWN` is not a valid request parameter value. Is only used in some responses. Mainly, it is used when `execType` is `Funding`.



### stopOrderType​

  * `TakeProfit`
  * `StopLoss`
  * `TrailingStop`
  * `Stop`
  * `PartialTakeProfit`
  * `PartialStopLoss`
  * `tpslOrder` spot TP/SL order
  * `OcoOrder` spot Oco order
  * `MmRateClose` On web or app can set MMR to close position
  * `BidirectionalTpslOrder` Spot bidirectional tpsl order



### tickDirection​

  * `PlusTick` price rise
  * `ZeroPlusTick` trade occurs at the same price as the previous trade, which occurred at a price higher than that for the trade preceding it
  * `MinusTick` price drop
  * `ZeroMinusTick` trade occurs at the same price as the previous trade, which occurred at a price lower than that for the trade preceding it



### interval​

  * `1` `3` `5` `15` `30` `60` `120` `240` `360` `720` minute
  * `D` day
  * `W` week
  * `M` month



### intervalTime​

  * `5min` `15min` `30min` minute
  * `1h` `4h` hour
  * `1d` day



### positionIdx​

  * `0` one-way mode position
  * `1` Buy side of hedge-mode position
  * `2` Sell side of hedge-mode position



### positionStatus​

  * `Normal`
  * `Liq` in the liquidation progress
  * `Adl` in the auto-deleverage progress



### rejectReason​

  * `EC_NoError`
  * `EC_Others`
  * `EC_UnknownMessageType`
  * `EC_MissingClOrdID`
  * `EC_MissingOrigClOrdID`
  * `EC_ClOrdIDOrigClOrdIDAreTheSame`
  * `EC_DuplicatedClOrdID`
  * `EC_OrigClOrdIDDoesNotExist`
  * `EC_TooLateToCancel`
  * `EC_UnknownOrderType`
  * `EC_UnknownSide`
  * `EC_UnknownTimeInForce`
  * `EC_WronglyRouted`
  * `EC_MarketOrderPriceIsNotZero`
  * `EC_LimitOrderInvalidPrice`
  * `EC_NoEnoughQtyToFill`
  * `EC_NoImmediateQtyToFill` a maker could not be found to fill your order
  * `EC_PerCancelRequest`
  * `EC_MarketOrderCannotBePostOnly`
  * `EC_PostOnlyWillTakeLiquidity` your post only order would have executed as a taker, and so was rejected
  * `EC_CancelReplaceOrder`
  * `EC_InvalidSymbolStatus`
  * `EC_CancelForNoFullFill`
  * `EC_BySelfMatch`
  * `EC_InCallAuctionStatus` used for pre-market order operation, e.g., during 2nd phase of call auction, cancel order is not allowed, when the cancel request is failed to be rejected by trading server, the request will be rejected by matching box finally
  * `EC_QtyCannotBeZero`
  * `EC_MarketOrderNoSupportTIF`
  * `EC_ReachMaxTradeNum`
  * `EC_InvalidPriceScale`
  * `EC_BitIndexInvalid`
  * `EC_StopBySelfMatch`
  * `EC_InvalidSmpType`
  * `EC_CancelByMMP`
  * `EC_InvalidUserType`
  * `EC_InvalidMirrorOid`
  * `EC_InvalidMirrorUid`
  * `EC_EcInvalidQty`
  * `EC_InvalidAmount`
  * `EC_LoadOrderCancel`
  * `EC_MarketQuoteNoSuppSell`
  * `EC_DisorderOrderID`
  * `EC_InvalidBaseValue`
  * `EC_LoadOrderCanMatch`
  * `EC_SecurityStatusFail`
  * `EC_ReachRiskPriceLimit`
  * `EC_OrderNotExist`
  * `EC_CancelByOrderValueZero` order cancelled as its remaining value is zero
  * `EC_CancelByMatchValueZero` order cancelled as the order it matched with has a remaining value of zero
  * `EC_ReachMarketPriceLimit`



### accountType​

  * `UNIFIED` Unified Trading Account
  * `FUND` Funding Account



### assetCategory​

  * `Easy Earn` Earn account sub-category
  * `Futures Grid Bot` Trading Bot account sub-category
  * `Futures Combo Bot` Trading Bot account sub-category
  * `Futures Martingale Bot` Trading Bot account sub-category
  * `Copy Trading Classic` Copy Trading account sub-category
  * `Copy Trading TradFi` Copy Trading account sub-category
  * `Copy Trading Pro` Copy Trading account sub-category



### assetAccountType​

  * `FundingAccount` Funding Account
  * `UnifiedTradingAccount` Unified Trading Account
  * `Earn` Earn Account
  * `TradingBot` Trading Bot Account
  * `CopyTrading` Copy Trading Account
  * `CryptoLoans` Crypto Loans Account
  * `CryptoLoans_legacy` Crypto Loans Account (Legacy)
  * `BybitPayLater` Bybit Pay Later Account
  * `Launchpool` Launchpool Account
  * `TradFi` TradFi Account
  * `MarginStakedSOL` Margin Staked SOL Account
  * `Alpha` Alpha Account



### transferStatus​

  * `SUCCESS`
  * `PENDING`
  * `FAILED`



### depositStatus​

  * `0` unknown
  * `1` toBeConfirmed
  * `2` processing
  * `3` success (finalised status of a success deposit)
  * `4` deposit failed
  * `10011` pending to be credited to funding pool
  * `10012` Credited to funding pool successfully



### withdrawStatus​

  * `SecurityCheck`
  * `Pending`
  * `success`
  * `CancelByUser`
  * `Reject`
  * `Fail`
  * `BlockchainConfirmed`
  * `MoreInformationRequired`
  * `Unknown` a rare status



### triggerBy​

  * `LastPrice`
  * `IndexPrice`
  * `MarkPrice`



### cancelType​

  * `CancelByUser`
  * `CancelByReduceOnly` cancelled by [reduceOnly](https://bybit-exchange.github.io/docs/v5/order/create-order)
  * `CancelByPrepareLiq` `CancelAllBeforeLiq` cancelled in order to attempt [liquidation prevention](https://www.bybit.com/en/help-center/article/Liquidation-Process-Derivatives-Standard-Account) by freeing up margin
  * `CancelByPrepareAdl` `CancelAllBeforeAdl` cancelled due to [ADL](https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL)
  * `CancelByAdmin`
  * `CancelBySettle` cancelled due to delisting contract
  * `CancelByTpSlTsClear` TP/SL order cancelled when the position is cleared
  * `CancelBySmp` cancelled by [SMP](https://bybit-exchange.github.io/docs/v5/smp)
  * `CancelByDCP` cancelled by DCP triggering
  * `CancelByRebalance` Spread trading: the order price of a single leg order is outside the limit price range.
  * `CancelByOCOTpCanceledBySlTriggered` The take profit order was canceled due to the triggering of the stop loss
  * `CancelByOCOSlCanceledByTpTriggered` The stop loss order was canceled due to the triggering of the take profit



 _Options:_

  * `CancelByUser`
  * `CancelByReduceOnly`
  * `CancelAllBeforeLiq` cancelled due to liquidation
  * `CancelAllBeforeAdl` cancelled due to ADL
  * `CancelBySettle`
  * `CancelByCannotAffordOrderCost`
  * `CancelByPmTrialMmOverEquity`
  * `CancelByAccountBlocking`
  * `CancelByDelivery`
  * `CancelByMmpTriggered`
  * `CancelByCrossSelfMuch`
  * `CancelByCrossReachMaxTradeNum`
  * `CancelByDCP`
  * `CancelBySmp`



### optionPeriod​

  * BTC: `7`,`14`,`21`,`30`,`60`,`90`,`180`,`270`days
  * ETH: `7`,`14`,`21`,`30`,`60`,`90`,`180`,`270`days
  * SOL: `7`,`14`,`21`,`30`,`60`,`90`days



### dataRecordingPeriod​

  * `5min` `15min` `30min` minute
  * `1h` `4h` hour
  * `4d` day



### contractType​

  * `InversePerpetual`
  * `LinearPerpetual`
  * `LinearFutures` USDT/USDC Futures
  * `InverseFutures`



### status​

  * `PreLaunch`
  * `Trading`
  * `Delivering`
  * `Closed`



### symbolType​

  * `innovation` linear
  * `adventure` spot
  * `xstocks` spot
  * `commodity` linear



### curAuctionPhase​

  * `NotStarted` Pre-market trading is not started
  * `Finished` Pre-market trading is finished
    * After the auction, if the pre-market contract fails to enter continues trading phase, it will be delisted and phase="Finished"
    * After the continuous trading, if the pre-market contract fails to be converted to official contract, it will be delisted and phase="Finished"
  * `CallAuction` Auction phase of pre-market trading
    * only timeInForce=GTC, orderType=Limit order is allowed to submit
    * TP/SL are not supported; Conditional orders are not supported
    * cannot **modify** the order at this stage
    * order price range: [[preOpenPrice](https://bybit-exchange.github.io/docs/v5/market/tickers) x 0.5, [maxPrice](https://bybit-exchange.github.io/docs/v5/market/instrument)]
  * `CallAuctionNoCancel` Auction no cancel phase of pre-market trading
    * only timeInForce=GTC, orderType=Limit order is allowed to submit
    * TP/SL are not supported; Conditional orders are not supported
    * cannot **modify and cancel** the order at this stage
    * order price range: Buy [[lastPrice](https://bybit-exchange.github.io/docs/v5/market/tickers) x 0.5, [markPrice](https://bybit-exchange.github.io/docs/v5/market/tickers) x 1.1], Sell [[markPrice](https://bybit-exchange.github.io/docs/v5/market/tickers) x 0.9, [maxPrice](https://bybit-exchange.github.io/docs/v5/market/instrument)]
  * `CrossMatching` cross matching phase
    * cannot **create, modify and cancel** the order at this stage
    * Candle data is released from this stage
  * `ContinuousTrading` Continuous trading phase
    * There is no restriction to create, amend, cancel orders
    * orderbook, public trade data is released from this stage



### marginTrading​

  * `none` Regardless of normal account or UTA account, this trading pair does not support margin trading
  * `both` For both normal account and UTA account, this trading pair supports margin trading
  * `utaOnly` Only for UTA account,this trading pair supports margin trading
  * `normalSpotOnly` Only for normal account, this trading pair supports margin trading



### copyTrading​

  * `none` Regardless of normal account or UTA account, this trading pair does not support copy trading
  * `both` For both normal account and UTA account, this trading pair supports copy trading
  * `utaOnly` Only for UTA account,this trading pair supports copy trading
  * `normalOnly` Only for normal account, this trading pair supports copy trading



### type(uta-translog)​

  * `TRANSFER_IN` Assets that transferred into Unified wallet
  * `TRANSFER_OUT` Assets that transferred out from Unified wallet
  * `TRADE`
  * `SETTLEMENT` USDT Perp funding settlement, and USDC Perp funding settlement + USDC 8-hour session settlement
  * `DELIVERY` USDC Futures, Option delivery
  * `LIQUIDATION`
  * `ADL` Auto-Deleveraging
  * `AIRDROP`
  * `BONUS` Bonus claimed
  * `BONUS_RECOLLECT` Bonus expired
  * `FEE_REFUND` Trading fee refunded
  * `INTEREST` Interest occurred due to borrowing
  * `CURRENCY_BUY` Currency convert, and the liquidation for borrowing asset(UTA loan)
  * `CURRENCY_SELL` Currency convert, and the liquidation for borrowing asset(UTA loan)
  * `BORROWED_AMOUNT_INS_LOAN`
  * `PRINCIPLE_REPAYMENT_INS_LOAN`
  * `INTEREST_REPAYMENT_INS_LOAN`
  * `AUTO_SOLD_COLLATERAL_INS_LOAN` the liquidation for borrowing asset(INS loan)
  * `AUTO_BUY_LIABILITY_INS_LOAN` the liquidation for borrowing asset(INS loan)
  * `AUTO_PRINCIPLE_REPAYMENT_INS_LOAN`
  * `AUTO_INTEREST_REPAYMENT_INS_LOAN`
  * `TRANSFER_IN_INS_LOAN` Transfer In when in the liquidation of OTC loan
  * `TRANSFER_OUT_INS_LOAN` Transfer Out when in the liquidation of OTC loan
  * `SPOT_REPAYMENT_SELL` One-click repayment currency sell
  * `SPOT_REPAYMENT_BUY` One-click repayment currency buy
  * `TOKENS_SUBSCRIPTION` Spot leverage token subscription
  * `TOKENS_REDEMPTION` Spot leverage token redemption
  * `AUTO_DEDUCTION` Asset auto deducted by system (roll back)
  * `FLEXIBLE_STAKING_SUBSCRIPTION` Byfi flexible stake subscription
  * `FLEXIBLE_STAKING_REDEMPTION` Byfi flexible stake redemption
  * `FIXED_STAKING_SUBSCRIPTION` Byfi fixed stake subscription
  * `FLEXIBLE_STAKING_REFUND` Byfi flexiable stake refund
  * `FIXED_STAKING_REFUND` Byfi fixed stake refund
  * `PREMARKET_TRANSFER_OUT`
  * `PREMARKET_DELIVERY_SELL_NEW_COIN`
  * `PREMARKET_DELIVERY_BUY_NEW_COIN`
  * `PREMARKET_DELIVERY_PLEDGE_PAY_SELLER`
  * `PREMARKET_DELIVERY_PLEDGE_BACK`
  * `PREMARKET_ROLLBACK_PLEDGE_BACK`
  * `PREMARKET_ROLLBACK_PLEDGE_PENALTY_TO_BUYER`
  * `CUSTODY_NETWORK_FEE` fireblocks business
  * `CUSTODY_SETTLE_FEE` fireblocks business
  * `CUSTODY_LOCK` fireblocks / copper business
  * `CUSTODY_UNLOCK` fireblocks business
  * `CUSTODY_UNLOCK_REFUND` fireblocks business
  * `LOANS_BORROW_FUNDS` crypto loan
  * `LOANS_PLEDGE_ASSET` crypto loan repayment
  * `BONUS_TRANSFER_IN`
  * `BONUS_TRANSFER_OUT`
  * `PEF_TRANSFER_IN`
  * `PEF_TRANSFER_OUT`
  * `PEF_PROFIT_SHARE`
  * `ONCHAINEARN_SUBSCRIPTION` tranfer out for on chain earn
  * `ONCHAINEARN_REDEMPTION` tranfer in for on chain earn
  * `ONCHAINEARN_REFUND` tranfer in for on chain earn failed
  * `STRUCTURE_PRODUCT_SUBSCRIPTION` tranfer out for structure product
  * `STRUCTURE_PRODUCT_REFUND` tranfer in for structure product
  * `CLASSIC_WEALTH_MANAGEMENT_SUBSCRIPTION` tranfer out for classic wealth management
  * `PREMIMUM_WEALTH_MANAGEMENT_SUBSCRIPTION` tranfer in for classic wealth management
  * `PREMIMUM_WEALTH_MANAGEMENT_REFUND` tranfer in for classic wealth management refund
  * `LIQUIDITY_MINING_SUBSCRIPTION` tranfer out for liquidity mining
  * `LIQUIDITY_MINING_REFUND` tranfer in for liquidity mining
  * `PWM_SUBSCRIPTION` tranfer out for PWM
  * `PWM_REFUND` tranfer in for PWM
  * `DEFI_INVESTMENT_SUBSCRIPTION` tranfer out for DEFI subscription
  * `DEFI_INVESTMENT_REFUND` transfer in for DEFI refund
  * `DEFI_INVESTMENT_REDEMPTION` tranfer in for DEFI redemption
  * `INSTITUTION_LOAN_IN` Borrowed Amount (INS Loan)
  * `INSTITUTION_PAYBACK_PRINCIPAL_OUT` Principal repayment (INS Loan)
  * `INSTITUTION_PAYBACK_INTEREST_OUT` Interest repayment (INS Loan) 
  * `INSTITUTION_EXCHANGE_SELL` Auto sold collateral (INS Loan)
  * `INSTITUTION_EXCHANGE_BUY` Auto buy liability (INS Loan)
  * `INSTITUTION_LIQ_PRINCIPAL_OUT` Forced principal repayment, i.e. liquidation (INS Loan)
  * `INSTITUTION_LIQ_INTEREST_OUT` Forced interest repayment, i.e. liquidation (INS Loan)
  * `INSTITUTION_LOAN_TRANSFER_IN` Transfer in (INS Loan)
  * `INSTITUTION_LOAN_TRANSFER_OUT` Transfer out (INS Loan)
  * `INSTITUTION_LOAN_WITHOUT_WITHDRAW` Transfer out (INS Loan)
  * `INSTITUTION_LOAN_RESERVE_IN` Reserve fund in (INS Loan)
  * `INSTITUTION_LOAN_RESERVE_OUT` Reserve fund out (INS Loan)
  * `SPREAD_FEE_OUT` Spread fee for EU Broker
  * `PLATFORM_TOKEN_MNT_LIQRECALLEDMMNT` Recall MNT
  * `PLATFORM_TOKEN_MNT_LIQRETURNEDMNT` Return MNT
  * `BORROW` Manual loan borrow and auto loan borrow
  * `REPAY` Manual loan repay and auto loan repay
  * `CONVERT` Currency convert repayment
  * `BROKER_ABACCOUNT_FEE` Borker AB fee deduction
  * `EARNING_REDEMPTION_SELL`
  * `EARNING_REDEMPTION_BUY`
  * `DBS_CASH_OUT`
  * `DBS_CASH_IN`
  * `DBS_CASH_OUT_TR`
  * `DBS_CASH_IN_TR`
  * `CUSTODY_CASH_RECOVER_TR`
  * `ALPHA_SMALL_TOKEN_REFUND`
  * `TWAP_BUDGET_AIRDROP`
  * `TWAP_BUDGET_RECALL`
  * `FLOATING_TO_FIXED_BORROW`
  * `FLOATING_TO_FIXED_REPAY`
  * `IDN_CONVERT_IN`
  * `IDN_CONVERT_OUT`



### type(contract-translog)​

  * `TRANSFER_IN` Assets that transferred into (inverse) derivatives wallet
  * `TRANSFER_OUT` Assets that transferred out from (inverse) derivatives wallet
  * `TRADE`
  * `SETTLEMENT` USDT / Inverse Perp funding settlement
  * `DELIVERY` Inverse Futures delivery
  * `LIQUIDATION`
  * `ADL` Auto-Deleveraging
  * `AIRDROP`
  * `BONUS` Bonus claimed
  * `BONUS_RECOLLECT` Bonus expired
  * `FEE_REFUND` Trading fee refunded
  * `CURRENCY_BUY` Currency convert
  * `CURRENCY_SELL` Currency convert
  * `AUTO_DEDUCTION` Asset auto deducted by system (roll back)
  * `Others`



### unifiedMarginStatus​

  * `1` Classic account
  * `3` Unified trading account 1.0
  * `4` Unified trading account 1.0 (pro version)
  * `5` Unified trading account 2.0
  * `6` Unified trading account 2.0 (pro version)



### convertAccountType​

  * `eb_convert_uta` Unified Trading Account
  * `eb_convert_funding` Funding Account



### symbol​

 _USDT Perpetual_ :

  * `BTCUSDT`
  * `ETHUSDT`



 _USDT Futures_ :

  * `BTCUSDT-21FEB25`
  * `ETHUSDT-14FEB25`  
The types of USDT Futures contracts offered by Bybit include: Weekly, Bi-Weekly, Tri-Weekly, Monthly, Bi-Monthly, Quarterly, Bi-Quarterly, Tri-Quarterly



 _USDC Perpetual_ :

  * `BTCPERP`
  * `ETHPERP`



 _USDC Futures_ :

  * `BTC-24MAR23`



 _Inverse Perpetual_ :

  * `BTCUSD`
  * `ETHUSD`



 _Inverse Futures_ :

  * `BTCUSDH23` H: First quarter; 23: 2023
  * `BTCUSDM23` M: Second quarter; 23: 2023
  * `BTCUSDU23` U: Third quarter; 23: 2023
  * `BTCUSDZ23` Z: Fourth quarter; 23: 2023



 _Spot_ :

  * `BTCUSDT`
  * `ETHUSDC`



 _Option_ :

  * `BTC-13FEB25-89000-P-USDT` USDT Option
  * `ETH-28FEB25-2800-C` USDC Option



### vipLevel​

  * No VIP
  * VIP-1
  * VIP-2
  * VIP-3
  * VIP-4
  * VIP-5
  * VIP-Supreme
  * PRO-1
  * PRO-2
  * PRO-3
  * PRO-4
  * PRO-5
  * PRO-6



### adlRankIndicator​

  * `0` default value of empty position
  * `1`
  * `2`
  * `3`
  * `4`
  * `5`



### smpType​

  * default: `None`
  * `CancelMaker`
  * `CancelTaker`
  * `CancelBoth`



### extraFees.feeType​

  * `UNKNOWN`
  * `TAX` Government tax. Only for Indonesian site
  * `CFX` Indonesian foreign exchange tax. Only for Indonesian site
  * `WHT` EU withholding tax. Only for EU site
  * `GST` Indian GST tax. Only for kyc=Indian users
  * `VAT` ARE VAT tax. Only for kyc=ARE users



### extraFees.subFeeType​

  * `UNKNOWN`
  * `TAX_PNN` Tax fee, fiat currency to digital currency. Only for Indonesian site
  * `TAX_PPH` Tax fee, digital currency to fiat currency. Only for Indonesian site
  * `CFX_FIEE` CFX fee, fiat currency to digital currency. Only for Indonesian site
  * `AUT_WITHHOLDING_TAX` EU site withholding tax. Only for EU site
  * `IND_GST` Indian GST tax. Only for kyc=Indian users
  * `ARE_VAT` ARE VAT tax. Only for kyc=ARE users



### state​

  * `scheduled`
  * `ongoing`
  * `completed`
  * `canceled`



### serviceTypes​

  * `1` Trading service
  * `2` Trading service via http request
  * `3` Trading service via websocket
  * `4` Private websocket stream
  * `5` Market data service



### product​

  * `1` Futures
  * `2` Spot
  * `3` Option
  * `4` Spread



### maintainType​

  * `1` Planned maintenance
  * `2` Temporary maintenance
  * `3` Incident



### env​

  * `1` Production
  * `2` Production Demo service



### bizType​

  * `SPOT`
  * `DERIVATIVES`
  * `OPTIONS`



### msg​

  * `API limit updated successfully`
  * `Requested limit exceeds maximum allowed per user`
  * `No permission to operate these UIDs`
  * `API cap configuration not found`
  * `API cap configuration not found for bizType`
  * `Requested limit would exceed institutional quota`



### groupId​

  * `1` Major Coins
  * `2` High Growth
  * `3` Mid-Tier Liquidity
  * `4` Mid-Tier Activation
  * `5` Long Tail
  * `6` Innovation Zone
  * `7` Pre-Listing
  * `8` USDC contracts



### groupName​

  * `G1(Major Coins)` Major Coins
  * `G2(High Growth)` High Growth
  * `G3(Mid-Tier Liquidity)` Mid-Tier Liquidity
  * `G4(Mid-Tier Activation)` Mid-Tier Activation
  * `G5(Long Tail)` Long Tail
  * `Innovation-Zone` Innovation Zone
  * `Pre-listing` Pre-listing
  * `USDC` USDC group



### Spot Fee Currency Instruction​

with the example of BTCUSDT:

  * Is makerFeeRate positive?
    * TRUE
      * Side = Buy -> base currency (BTC)
      * Side = Sell -> quote currency (USDT)
    * FALSE
      * IsMakerOrder = TRUE
        * Side = Buy -> quote currency (USDT)
        * Side = Sell -> base currency (BTC)
      * IsMakerOrder = FALSE
        * Side = Buy -> base currency (BTC)
        * Side = Sell -> quote currency (USDT)



### sbe-orderStatus​

  * `5` Rejected
  * `6` New
  * `7` Cancelled
  * `8` PartiallyFilled
  * `9` Filled
  * `0` Others



### sbe-rejectReason​

  * `0` EC_NoError 
  * `1` EC_Others 
  * `2` EC_UnknownMessageType 
  * `3` EC_MissingClOrdID 
  * `4` EC_OrderNotExist 
  * `5` EC_MissingOrigClOrdID 
  * `6` EC_ClOrdIDOrigClOrdIDAreTheSame 
  * `7` EC_OrigClOrdIDDoesNotExist 
  * `8` EC_TooLateToCancel 
  * `9` EC_UnknownOrderType 
  * `10` EC_UnknownSide 
  * `11` EC_UnknownTimeInForce 
  * `12` EC_WronglyRouted 
  * `13` EC_MarketOrderPriceIsNotZero 
  * `14` EC_LimitOrderInvalidPrice 
  * `15` EC_NoEnoughQtyToFill 
  * `16` EC_NoImmediateQtyToFill 
  * `17` EC_QtyCannotBeZero 
  * `18` EC_PerCancelRequest 
  * `19` EC_MarketOrderCannotBePostOnly 
  * `20` EC_PostOnlyWillTakeLiquidity 
  * `21` EC_CancelReplaceOrder 
  * `22` EC_InvalidSymbolStatus 
  * `23` EC_MarketOrderNoSupportTIF 
  * `24` EC_ReachMaxTradeNum 
  * `25` EC_InvalidPriceScale 
  * `28` EC_BySelfMatch 
  * `29` EC_InvalidSmpType 
  * `30` EC_CancelByMMP 
  * `31` EC_InCallAuctionStatus 
  * `34` EC_InvalidUserType 
  * `35` EC_InvalidMirrorOid 
  * `36` EC_InvalidMirrorUid 
  * `100` EC_EcInvalidQty 
  * `101` EC_InvalidAmount 
  * `102` EC_LoadOrderCancel 
  * `103` EC_CancelForNoFullFill 
  * `104` EC_MarketQuoteNoSuppSell 
  * `105` EC_DisorderOrderID 
  * `106` EC_InvalidBaseValue 
  * `107` EC_LoadOrderCanMatch 
  * `108` EC_SecurityStatusFail 
  * `110` EC_ReachRiskPriceLimit 
  * `111` EC_CancelByOrderValueZero 
  * `112` EC_CancelByMatchValueZero 
  * `113` EC_CancelByMatchValueZero 
  * `200` EC_ReachMarketPriceLimit



[PreviousGet All Rate Limits](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query-all)[NextError Codes](https://bybit-exchange.github.io/docs/v5/error)

  * locale
  * announcementType
  * announcementTag
  * category
  * orderStatus
  * timeInForce
  * createType
  * execType
  * orderType
  * stopOrderType
  * tickDirection
  * interval
  * intervalTime
  * positionIdx
  * positionStatus
  * rejectReason
  * accountType
  * assetCategory
  * assetAccountType
  * transferStatus
  * depositStatus
  * withdrawStatus
  * triggerBy
  * cancelType
  * optionPeriod
  * dataRecordingPeriod
  * contractType
  * status
  * symbolType
  * curAuctionPhase
  * marginTrading
  * copyTrading
  * type(uta-translog)
  * type(contract-translog)
  * unifiedMarginStatus
  * convertAccountType
  * symbol
  * vipLevel
  * adlRankIndicator
  * smpType
  * extraFees.feeType
  * extraFees.subFeeType
  * state
  * serviceTypes
  * product
  * maintainType
  * env
  * bizType
  * msg
  * groupId
  * groupName
  * Spot Fee Currency Instruction
  * sbe-orderStatus
  * sbe-rejectReason


