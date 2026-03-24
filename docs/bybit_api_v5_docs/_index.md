# introduction — Documentation Index
Crawled from: https://bybit-exchange.github.io/docs/v5/intro
Pages saved : 315
Generated   : 2026-03-23 16:19

---
| File | Title | Description |
|------|-------|-------------|
| [v5_intro.md](v5_intro.md) | Introduction | Overview |
| [abandon_account_info.md](abandon_account_info.md) | Get Lending Account Info | HTTP Request |
| [abandon_asset_info.md](abandon_asset_info.md) | Get Asset Info | Query Spot asset information |
| [abandon_borrow.md](abandon_borrow.md) | Borrow | Permission: "Spot trade" |
| [abandon_cancel_redeem.md](abandon_cancel_redeem.md) | Cancel Redeem | Cancel the withdrawal operation. |
| [abandon_coin_info.md](abandon_coin_info.md) | Get Lending Coin Info | Get the basic information of lending coins |
| [abandon_contract_transaction_log.md](abandon_contract_transaction_log.md) | Get Transaction Log | Query transaction logs in the derivatives wallet (classic account), and inverse derivatives account (upgraded to UTA) |
| [abandon_cross_isolate.md](abandon_cross_isolate.md) | Switch Cross/Isolated Margin | Select cross margin mode or isolated margin mode per symbol level |
| [abandon_deposit.md](abandon_deposit.md) | Deposit Funds | Lending funds to Bybit asset pool |
| [abandon_earning.md](abandon_earning.md) | Get Broker Earning | This endpoint has been deprecated, please move to new Get Exchange Broker Earning |
| [abandon_enable_unitransfer_subuid.md](abandon_enable_unitransfer_subuid.md) | Enable Universal Transfer for Sub UID | You no longer need to configure transferable sub UIDs. Now, all sub UIDs are automatically enabled for universal transfe |
| [abandon_ltv.md](abandon_ltv.md) | Get LTV | HTTP Request |
| [abandon_margin_coin_info.md](abandon_margin_coin_info.md) | Get Margin Coin Info | HTTP Request |
| [abandon_order_record.md](abandon_order_record.md) | Get Order Records | Get lending or redeem history |
| [abandon_redeem.md](abandon_redeem.md) | Redeem Funds | Withdraw funds from the Bybit asset pool. |
| [abandon_set_risk_limit.md](abandon_set_risk_limit.md) | Set Risk Limit | Since bybit has launched auto risk limit on 12 March 2024, please click here to learn more, so it will not take effect e |
| [abandon_tpsl_mode.md](abandon_tpsl_mode.md) | Set TP/SL Mode | _To some extent, this endpoint is deprecated because now tpsl is based on order level. This API was used for position le |
| [account_account_info.md](account_account_info.md) | Get Account Info | Query the account information, like margin mode, account mode, etc. |
| [account_batch_set_collateral.md](account_batch_set_collateral.md) | Batch Set Collateral Coin | HTTP Request |
| [account_borrow.md](account_borrow.md) | Manual Borrow | Borrowing via OpenAPI endpoint supports variable rate borrowing only. |
| [account_borrow_history.md](account_borrow_history.md) | Get Borrow History | Get interest records, sorted in reverse order of creation time. |
| [account_coin_greeks.md](account_coin_greeks.md) | Get Coin Greeks | Get current account Greeks information |
| [account_collateral_info.md](account_collateral_info.md) | Get Collateral Info | Get the collateral information of the current unified margin account, including loan interest rate, loanable amount, |
| [account_dcp_info.md](account_dcp_info.md) | Get DCP Info | Query the DCP configuration of the account. Before calling the interface, please make sure you have applied for the UTA  |
| [account_fee_rate.md](account_fee_rate.md) | Get Fee Rate | Get the trading fee rate. |
| [account_get_mmp_state.md](account_get_mmp_state.md) | Get MMP State | HTTP Request |
| [account_get_user_setting_config.md](account_get_user_setting_config.md) | Get Trade Behaviour Config | You can get configuration how the system behaves when your limit order price exceeds the highest bid or lowest ask price |
| [account_instrument.md](account_instrument.md) | Get Account Instruments Info | Query for the instrument specification of online trading pairs that available to users. |
| [account_no_convert_repay.md](account_no_convert_repay.md) | Manual Repay Without Asset Conversion | * If coin is passed in input parameter and amount is not, the repayment amount will be the available spot balance of tha |
| [account_repay.md](account_repay.md) | Manual Repay | * If neither coin nor amount is passed in input parameter, then repay all the liabilities. |
| [account_repay_liability.md](account_repay_liability.md) | Repay Liability | You can manually repay the liabilities of Unified account |
| [account_reset_mmp.md](account_reset_mmp.md) | Reset MMP | * Once the mmp triggered, you can unfreeze the account by this endpoint, then qtyLimit and deltaLimit will be reset to 0 |
| [account_set_collateral.md](account_set_collateral.md) | Set Collateral Coin | You can decide whether the assets in the Unified account needs to be collateral coins. |
| [account_set_delta_mode.md](account_set_delta_mode.md) | Set Delta Neutral Mode | Delta Neutral Mode is designed to enhance the trading experience for users running delta-neutral strategies. When enable |
| [account_set_margin_mode.md](account_set_margin_mode.md) | Set Margin Mode | Default is regular margin mode |
| [account_set_mmp.md](account_set_mmp.md) | Set MMP | What is MMP? |
| [account_set_price_limit.md](account_set_price_limit.md) | Set Price Limit Behaviour | You can configure how the system behaves when your limit order price exceeds the highest bid or lowest ask price. |
| [account_set_spot_hedge.md](account_set_spot_hedge.md) | Set Spot Hedging | You can turn on/off Spot hedging feature in Portfolio margin |
| [account_smp_group.md](account_smp_group.md) | Get SMP Group ID | Query the SMP group ID of self match prevention |
| [account_transaction_log.md](account_transaction_log.md) | Get Transaction Log | Query for transaction logs in your Unified account. It supports up to 2 years worth of data. |
| [account_unified_trans_amnt.md](account_unified_trans_amnt.md) | Get Transferable Amount (Unified) | Query the available amount to transfer of a specific coin in the Unified wallet. |
| [account_upgrade_unified_account.md](account_upgrade_unified_account.md) | Upgrade to Unified Account Pro | Check your current account status by calling this Get Account Info |
| [account_wallet_balance.md](account_wallet_balance.md) | Get Wallet Balance | Obtain wallet balance, query asset information of each currency. By default, currency |
| [v5_acct_mode.md](v5_acct_mode.md) | Different Account Modes | There are three main account modes that have existed on the Bybit platform, namely classic account (now unavailable), un |
| [affiliate_affiliate_info.md](affiliate_affiliate_info.md) | Get Affiliate User Info | To use this endpoint, you should have an affiliate account and only tick "affiliate" permission while creating the API k |
| [affiliate_affiliate_user_list.md](affiliate_affiliate_user_list.md) | Get Affiliate User List | To use this endpoint, you should have an affiliate account and only tick "affiliate" permission while creating the API k |
| [v5_announcement.md](v5_announcement.md) | Get Announcement | HTTP Request |
| [balance_account_coin_balance.md](balance_account_coin_balance.md) | Get Single Coin Balance | Query the balance of a specific coin in a specific account type. Supports querying sub UID's balance. |
| [balance_all_balance.md](balance_all_balance.md) | Get All Coins Balance | You could get all coin balance of all account types under the master account, and sub account. |
| [balance_asset_overview.md](balance_asset_overview.md) | Asset Overview | Query master account or one subaccounts' total assets and detailed asset holdings across different accounts and product  |
| [balance_delay_amount.md](balance_delay_amount.md) | Get Withdrawable Amount | How can partial funds be subject to delayed withdrawal requests? |
| [asset_coin_info.md](asset_coin_info.md) | Get Coin Info | Query coin information, including chain information, withdraw and deposit status. |
| [convert_small_balance_confirm_quote.md](convert_small_balance_confirm_quote.md) | Confirm a Quote | * API key permission: Convert |
| [convert_small_balance_exchange_history.md](convert_small_balance_exchange_history.md) | Get Exchange History | * API key permission: Convert |
| [convert_small_balance_request_quote.md](convert_small_balance_request_quote.md) | Request a Quote | Custody accounts, like copper, fireblock, etc are not supported to make a convertion |
| [convert_small_balance_small_balanc_coins.md](convert_small_balance_small_balanc_coins.md) | Get Small Balance Coins | Query small-balance coins with a USDT equivalent of less than 10 USDT, and ensure that the total amount for each convers |
| [convert_apply_quote.md](convert_apply_quote.md) | Request a Quote | HTTP Request |
| [convert_confirm_quote.md](convert_confirm_quote.md) | Confirm a Quote | 1. The exchange is async; please check the final status by calling the query result API. |
| [convert_convert_coin_list.md](convert_convert_coin_list.md) | Get Convert Coin List | Query for the list of coins you can convert to/from. |
| [convert_get_convert_history.md](convert_get_convert_history.md) | Get Convert History | Returns all confirmed quotes. |
| [convert_get_convert_result.md](convert_get_convert_result.md) | Get Convert Status | You can query the exchange result by sending quoteTxId. |
| [convert_guideline.md](convert_guideline.md) | Convert Guideline | * All convert API endpoints need authentication |
| [asset_delivery.md](asset_delivery.md) | Get Delivery Record | Query delivery records of Invese Futures, USDC Futures, USDT Futures and Options, sorted by deliveryTime in descending o |
| [deposit_deposit_record.md](deposit_deposit_record.md) | Get Deposit Records (on-chain) | Query deposit records |
| [deposit_internal_deposit_record.md](deposit_internal_deposit_record.md) | Get Internal Deposit Records (off-chain) | Query deposit records within the Bybit platform. These transactions are not on the blockchain. |
| [deposit_master_deposit_addr.md](deposit_master_deposit_addr.md) | Get Master Deposit Address | Query the deposit address information of MASTER account. |
| [deposit_set_deposit_acct.md](deposit_set_deposit_acct.md) | Set Deposit Account | Set auto transfer account after deposit. The same function as the setting for Deposit on web GUI |
| [deposit_sub_deposit_addr.md](deposit_sub_deposit_addr.md) | Get Sub Deposit Address | Query the deposit address information of SUB account. |
| [deposit_sub_deposit_record.md](deposit_sub_deposit_record.md) | Get Sub Deposit Records (on-chain) | Query subaccount's deposit records by main UID's API key. |
| [asset_exchange.md](asset_exchange.md) | Get Coin Exchange Records | Query the coin exchange records. |
| [fiat_convert_balance_query.md](fiat_convert_balance_query.md) | Get Balance | HTTP Request |
| [fiat_convert_confirm_quote.md](fiat_convert_confirm_quote.md) | Confirm a Quote | 1. The exchange is async; please check the final status by calling the convert history API. |
| [fiat_convert_query_coin_list.md](fiat_convert_query_coin_list.md) | Get Trading Pair List | Query for the list of coins you can convert to/from. |
| [fiat_convert_query_trade.md](fiat_convert_query_trade.md) | Get Convert Status | Returns the details of this convert. |
| [fiat_convert_query_trade_history.md](fiat_convert_query_trade_history.md) | Get Convert History | Returns all the convert history |
| [fiat_convert_quote_apply.md](fiat_convert_quote_apply.md) | Request a Quote | Request by the master UID's api key only |
| [fiat_convert_reference_price.md](fiat_convert_reference_price.md) | Get Reference Price | HTTP Request |
| [fiat_convert_trade_notify.md](fiat_convert_trade_notify.md) | Trade Notify | Trade Notify |
| [asset_fund_history.md](asset_fund_history.md) | Funding Account Transaction History | Return transaction log in Funding Account. This endpoint supports filtering by transaction type and time range. |
| [asset_settlement.md](asset_settlement.md) | Get USDC Session Settlement | Query session settlement records of USDC perpetual and futures |
| [asset_sub_uid_list.md](asset_sub_uid_list.md) | Get Sub UID | Query the sub UIDs under a main UID. It returns up to 2000 sub accounts, if you need more, please call this endpoint. |
| [transfer_create_inter_transfer.md](transfer_create_inter_transfer.md) | Create Internal Transfer | Create the internal transfer between different account types under the same UID. |
| [transfer_inter_transfer_list.md](transfer_inter_transfer_list.md) | Get Internal Transfer Records | Query the internal transfer records between different account types under the same UID. |
| [transfer_transferable_coin.md](transfer_transferable_coin.md) | Get Transferable Coin | Query the transferable coin list between each account type |
| [transfer_unitransfer.md](transfer_unitransfer.md) | Create Universal Transfer | Transfer between sub-sub or main-sub. |
| [transfer_unitransfer_list.md](transfer_unitransfer_list.md) | Get Universal Transfer Records | Query universal transfer records |
| [asset_withdraw.md](asset_withdraw.md) | Withdraw | Withdraw assets from your Bybit account. You can make an off-chain transfer if the target wallet address is from Bybit.  |
| [withdraw_cancel_withdraw.md](withdraw_cancel_withdraw.md) | Cancel Withdrawal | Cancel the withdrawal |
| [withdraw_vasp_list.md](withdraw_vasp_list.md) | Get available VASPs | This endpoint is used for query the available VASPs. This API distinguishes which compliance zone the user belongs to an |
| [withdraw_withdraw_address.md](withdraw_withdraw_address.md) | Get Withdrawal Address List | Query the withdrawal addresses in the address book. |
| [withdraw_withdraw_record.md](withdraw_withdraw_record.md) | Get Withdrawal Records | Query withdrawal records. |
| [api_broker_guidance.md](api_broker_guidance.md) | OAuth Integration Guidance | 1. Information Submission |
| [exchange_broker_account_info.md](exchange_broker_account_info.md) | Get Account Info | * Use exchange broker master account to query |
| [exchange_broker_exchange_earning.md](exchange_broker_exchange_earning.md) | Get Earning | * Use exchange broker master account to query |
| [rate_limit_introduction.md](rate_limit_introduction.md) | Introduction | API Rate Limit For Exchange Broker Client |
| [rate_limit_query_all.md](rate_limit_query_all.md) | Get All Rate Limits | API rate limit: 1 req per second |
| [rate_limit_query_cap.md](rate_limit_query_cap.md) | Get Rate Limit Cap | API rate limit: 5 req per second |
| [rate_limit_set.md](rate_limit_set.md) | Set Rate Limit | API rate limit: 1 req per second |
| [exchange_broker_sub_deposit_record.md](exchange_broker_sub_deposit_record.md) | Get Sub Account Deposit Records | Exchange broker can query subaccount's deposit records by main UID's API key without specifying uid. |
| [reward_get_issue_voucher.md](reward_get_issue_voucher.md) | Get Issued Voucher | HTTP Request |
| [reward_issue_voucher.md](reward_issue_voucher.md) | Issue Voucher | HTTP Request |
| [reward_voucher.md](reward_voucher.md) | Get Voucher Spec | HTTP Request |
| [v5_copytrade.md](v5_copytrade.md) | How To Start Copy Trading | Become A Master Trader |
| [crypto_loan_acct_borrow_collateral.md](crypto_loan_acct_borrow_collateral.md) | Get Account Borrowable/Collateralizable Limit | Query for the minimum and maximum amounts your account can borrow and how much collateral you can put up. |
| [crypto_loan_adjust_collateral.md](crypto_loan_adjust_collateral.md) | Adjust Collateral Amount | You can increase or reduce your collateral amount. When you reduce, please obey the max. allowed reduction amount. |
| [crypto_loan_collateral_coin.md](crypto_loan_collateral_coin.md) | Get Collateral Coins | Does not need authentication. |
| [crypto_loan_completed_loan_order.md](crypto_loan_completed_loan_order.md) | Get Completed Loan History | Query for the last 6 months worth of your completed (fully paid off) loans. |
| [crypto_loan_loan_coin.md](crypto_loan_loan_coin.md) | Get Borrowable Coins | Does not need authentication. |
| [crypto_loan_ltv_adjust_history.md](crypto_loan_ltv_adjust_history.md) | Get Loan LTV Adjustment History | Query for your LTV adjustment history. |
| [crypto_loan_reduce_max_collateral_amt.md](crypto_loan_reduce_max_collateral_amt.md) | Get Max. Allowed Collateral Reduction Amount | Query for the maximum amount by which collateral may be reduced by. |
| [crypto_loan_repay.md](crypto_loan_repay.md) | Repay | Fully or partially repay a loan. If interest is due, that is paid off first, with the loaned amount being paid off only  |
| [crypto_loan_repay_transaction.md](crypto_loan_repay_transaction.md) | Get Loan Repayment History | Query for loan repayment transactions. A loan may be repaid in multiple repayments. |
| [crypto_loan_unpaid_loan_order.md](crypto_loan_unpaid_loan_order.md) | Get Unpaid Loans | Query for your ongoing loans. |
| [v5_demo.md](v5_demo.md) | Demo Trading Service | Introduction |
| [dmm_listing_dmm_listing_spot.md](dmm_listing_dmm_listing_spot.md) | dmm-listing-spot | const Home = () => { |
| [earn_apr_history.md](earn_apr_history.md) | Get APR History | Does not need authentication. |
| [earn_create_order.md](earn_create_order.md) | Stake / Redeem | API key needs "Earn" permission, custody accounts are not supported for now |
| [earn_hourly_yield.md](earn_hourly_yield.md) | Get Hourly Yield History | API key needs "Earn" permission |
| [earn_modify_position.md](earn_modify_position.md) | Modify Position | API key needs "Earn" permission |
| [earn_order_history.md](earn_order_history.md) | Get Stake/Redeem Order History | API key needs "Earn" permission |
| [earn_position.md](earn_position.md) | Get Staked Position | API key needs "Earn" permission |
| [earn_product_info.md](earn_product_info.md) | Get Product Info | Does not need authentication. |
| [earn_yield_history.md](earn_yield_history.md) | Get Yield History | You can get the past 3 months data |
| [v5_enum.md](v5_enum.md) | Enums Definitions | locale |
| [v5_error.md](v5_error.md) | Error Codes | HTTP Code |
| [v5.md](v5.md) | Integration Guidance | To learn more about the V5 API, please read the Introduction. |
| [lt_leverage_token_info.md](lt_leverage_token_info.md) | Get Leverage Token Info | Query leverage token information |
| [lt_leverage_token_reference.md](lt_leverage_token_reference.md) | Get Leveraged Token Market | Get leverage token market information |
| [lt_order_record.md](lt_order_record.md) | Get Purchase/Redemption Records | Get purchase or redeem history |
| [lt_purchase.md](lt_purchase.md) | Purchase | Purchase levearge token |
| [lt_redeem.md](lt_redeem.md) | Redeem | Redeem leverage token |
| [market_adl_alert.md](market_adl_alert.md) | Get ADL Alert | Query for ADL (auto-deleveraging mechanism) alerts and insurance pool information. |
| [market_delivery_price.md](market_delivery_price.md) | Get Delivery Price | Get the delivery price. |
| [market_fee_group_info.md](market_fee_group_info.md) | Get Fee Group Structure | Query for the group fee structure and fee rates. |
| [market_history_fund_rate.md](market_history_fund_rate.md) | Get Funding Rate History | Query for historical funding rates. Each symbol has a different funding interval. For example, if the interval is 8 hour |
| [market_index_components.md](market_index_components.md) | Get Index Price Components | HTTP Request |
| [market_index_kline.md](market_index_kline.md) | Get Index Price Kline | Query for historical index price klines. Charts are returned in groups based on the requested interval. |
| [market_instrument.md](market_instrument.md) | Get Instruments Info | Query for the instrument specification of online trading pairs. |
| [market_insurance.md](market_insurance.md) | Get Insurance Pool | Query for Bybit insurance pool data (BTC/USDT/USDC etc) |
| [market_iv.md](market_iv.md) | Get Historical Volatility | Query option historical volatility |
| [market_kline.md](market_kline.md) | Get Kline | Query for historical klines (also known as candles/candlesticks). Charts are returned in groups based on the requested i |
| [market_long_short_ratio.md](market_long_short_ratio.md) | Get Long Short Ratio | This refers to the net long and short positions as percentages of all position holders during the selected time. |
| [market_mark_kline.md](market_mark_kline.md) | Get Mark Price Kline | Query for historical mark price klines. Charts are returned in groups based on the requested interval. |
| [market_new_delivery_price.md](market_new_delivery_price.md) | Get New Delivery Price | Get historical option delivery prices. |
| [market_open_interest.md](market_open_interest.md) | Get Open Interest | Get the open interest of each symbol. |
| [market_order_price_limit.md](market_order_price_limit.md) | Get Order Price Limit | For derivative trading order price limit, refer to announcement |
| [market_orderbook.md](market_orderbook.md) | Get Orderbook | Query for orderbook depth data. |
| [market_premium_index_kline.md](market_premium_index_kline.md) | Get Premium Index Price Kline | Query for historical premium index klines. Charts are returned in groups based on the requested interval. |
| [market_recent_trade.md](market_recent_trade.md) | Get Recent Public Trades | Query recent public trading history in Bybit. |
| [market_risk_limit.md](market_risk_limit.md) | Get Risk Limit | Query for the risk limit margin parameters. This information is also displayed on the website here. |
| [market_rpi_orderbook.md](market_rpi_orderbook.md) | Get RPI Orderbook | Query for orderbook depth data. |
| [market_tickers.md](market_tickers.md) | Get Tickers | Query for the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours. |
| [market_time.md](market_time.md) | Get Bybit Server Time | * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in da |
| [new_crypto_loan_adjust_collateral.md](new_crypto_loan_adjust_collateral.md) | Adjust Collateral Amount | You can increase or reduce your collateral amount. When you reduce, please obey the Get Max. Allowed Collateral Reductio |
| [new_crypto_loan_collateral_coin.md](new_crypto_loan_collateral_coin.md) | Get Collateral Coins | Does not need authentication. |
| [new_crypto_loan_crypto_loan_position.md](new_crypto_loan_crypto_loan_position.md) | Get Crypto Loan Position | Permission: "Spot trade" |
| [fixed_borrow.md](fixed_borrow.md) | Create Borrow Order | Permission: "Spot trade" |
| [fixed_borrow_contract.md](fixed_borrow_contract.md) | Get Borrow Contract Info | Permission: "Spot trade" |
| [fixed_borrow_market.md](fixed_borrow_market.md) | Get Borrowing Market | Does not need authentication. |
| [fixed_borrow_order.md](fixed_borrow_order.md) | Get Borrow Order Info | Permission: "Spot trade" |
| [fixed_cancel_borrow.md](fixed_cancel_borrow.md) | Cancel Borrow Order | Permission: "Spot trade" |
| [fixed_cancel_supply.md](fixed_cancel_supply.md) | Cancel Supply Order | Permission: "Spot trade" |
| [fixed_renew.md](fixed_renew.md) | Renew Borrow Order | Permission: "Spot trade" |
| [fixed_renew_order.md](fixed_renew_order.md) | Get Renew Order Info | Permission: "Spot trade" |
| [fixed_repay.md](fixed_repay.md) | Repay | Permission: "Spot trade" |
| [fixed_repay_collateral.md](fixed_repay_collateral.md) | Collateral Repayment | Permission: "Spot trade" |
| [fixed_repay_history.md](fixed_repay_history.md) | Get Repayment History | Permission: "Spot trade" |
| [fixed_supply.md](fixed_supply.md) | Create Supply Order | Permission: "Spot trade" |
| [fixed_supply_contract20copy.md](fixed_supply_contract20copy.md) | Get Supply Contract Info | Permission: "Spot trade" |
| [fixed_supply_market.md](fixed_supply_market.md) | Get Lending Market | Does not need authentication. |
| [fixed_supply_order.md](fixed_supply_order.md) | Get Supply Order Info | Permission: "Spot trade" |
| [flexible_borrow.md](flexible_borrow.md) | Borrow | Permission: "Spot trade" |
| [flexible_loan_orders.md](flexible_loan_orders.md) | Get Borrowing History | Permission: "Spot trade" |
| [flexible_repay.md](flexible_repay.md) | Repay | Fully or partially repay a loan. If interest is due, that is paid off first, with the loaned amount being paid off only  |
| [flexible_repay_collateral.md](flexible_repay_collateral.md) | Collateral Repayment | Permission: "Spot trade" |
| [flexible_repay_orders.md](flexible_repay_orders.md) | Get Repayment History | Permission: "Spot trade" |
| [flexible_unpaid_loan_order.md](flexible_unpaid_loan_order.md) | Get Flexible Loans | Query for your ongoing loans |
| [new_crypto_loan_loan_coin.md](new_crypto_loan_loan_coin.md) | Get Borrowable Coins | Does not need authentication. |
| [new_crypto_loan_ltv_adjust_history.md](new_crypto_loan_ltv_adjust_history.md) | Get Collateral Adjustment History | Query for your LTV adjustment history. |
| [new_crypto_loan_max_loan_amt.md](new_crypto_loan_max_loan_amt.md) | Obtain Max Loan Amount | Permission: "Spot trade" |
| [new_crypto_loan_reduce_max_collateral_amt.md](new_crypto_loan_reduce_max_collateral_amt.md) | Get Max. Allowed Collateral Reduction Amount | Retrieve the maximum redeemable amount of your collateral asset based on LTV. |
| [order_amend_order.md](order_amend_order.md) | Amend Order | You can only modify unfilled or partially filled orders. |
| [order_batch_amend.md](order_batch_amend.md) | Batch Amend Order | This endpoint allows you to amend more than one open order in a single request. |
| [order_batch_cancel.md](order_batch_cancel.md) | Batch Cancel Order | This endpoint allows you to cancel more than one open order in a single request. |
| [order_batch_place.md](order_batch_place.md) | Batch Place Order | This endpoint allows you to place more than one order in a single request. |
| [order_cancel_all.md](order_cancel_all.md) | Cancel All Orders | Cancel all open orders |
| [order_cancel_order.md](order_cancel_order.md) | Cancel Order | - You must specify orderId or orderLinkId to cancel the order. |
| [order_create_order.md](order_create_order.md) | Place Order | This endpoint supports to create the order for Spot, Margin trading, USDT perpetual, USDT futures, USDC perpetual, USDC  |
| [order_dcp.md](order_dcp.md) | Set Disconnect Cancel All | What is Disconnection Protect (DCP)? |
| [order_execution.md](order_execution.md) | Get Trade History | Query users' execution records, sorted by execTime in descending order. |
| [order_open_order.md](order_open_order.md) | Get Open & Closed Orders | Primarily query unfilled or partially filled orders in real-time, but also supports querying recent 500 closed status (C |
| [order_order_list.md](order_order_list.md) | Get Order History | Query order history. As order creation/cancellation is asynchronous, the data returned from this endpoint may delay. If  |
| [order_pre_check_order.md](order_pre_check_order.md) | Pre Check Order | This endpoint is used to calculate the changes in IMR and MMR of UTA account before and after placing an order. |
| [order_spot_borrow_quota.md](order_spot_borrow_quota.md) | Get Borrow Quota (Spot) | Query the available balance for Spot trading and Margin trading |
| [otc_bind_uid.md](otc_bind_uid.md) | Bind Or Unbind UID | For the institutional loan product, you can bind new UIDs to the risk unit or unbind UID from the risk unit. |
| [otc_loan_info.md](otc_loan_info.md) | Get Loan Orders | Get up to 2 years worth of historical loan orders. |
| [otc_ltv_convert.md](otc_ltv_convert.md) | Get LTV | Get your loan-to-value (LTV) ratio. |
| [otc_margin_coin_convert_info.md](otc_margin_coin_convert_info.md) | Get Margin Coin Info | * When queried without an API key, this endpoint returns public margin data |
| [otc_margin_product_info.md](otc_margin_product_info.md) | Get Product Info | * When queried without an API key, this endpoint returns public product data |
| [otc_repay.md](otc_repay.md) | Repay | You can repay the INS loan by calling this API. |
| [otc_repay_info.md](otc_repay_info.md) | Get Repayment Orders | Get a list of your loan repayment orders (orders which repaid the loan). |
| [v5_position.md](v5_position.md) | Get Position Info | Query real-time position data, such as position size, cumulative realized PNL, etc. |
| [position_auto_add_margin.md](position_auto_add_margin.md) | Set Auto Add Margin | Turn on/off auto-add-margin for isolated margin position |
| [position_close_pnl.md](position_close_pnl.md) | Get Closed PnL | Query user's closed profit and loss records |
| [position_close_position.md](position_close_position.md) | Get Closed Options Positions | Query user's closed options positions, sorted by closeTime in descending order. |
| [position_confirm_mmr.md](position_confirm_mmr.md) | Confirm New Risk Limit | It is only applicable when the user is marked as only reducing positions (please see the isReduceOnly field in |
| [position_leverage.md](position_leverage.md) | Set Leverage | According to the risk limit, leverage affects the maximum position value that can be opened, |
| [position_manual_add_margin.md](position_manual_add_margin.md) | Add Or Reduce Margin | Manually add or reduce margin for isolated margin position |
| [position_move_position.md](position_move_position.md) | Move Position | You can move positions between sub-master, master-sub, or sub-sub UIDs when necessary |
| [position_move_position_history.md](position_move_position_history.md) | Get Move Position History | You can query moved position data by master UID api key |
| [position_position_mode.md](position_position_mode.md) | Switch Position Mode | It supports to switch the position mode for USDT perpetual and Inverse futures. If you are in one-way Mode, you can only |
| [position_trading_stop.md](position_trading_stop.md) | Set Trading Stop | Set the take profit, stop loss or trailing stop for the position. |
| [pre_upgrade_close_pnl.md](pre_upgrade_close_pnl.md) | Get Pre-upgrade Closed PnL | Query user's closed profit and loss records from before you upgraded the account to a Unified account. The results are s |
| [pre_upgrade_delivery.md](pre_upgrade_delivery.md) | Get Pre-upgrade Delivery Record | Query delivery records of Options before you upgraded the account to a Unified account, sorted by deliveryTime in descen |
| [pre_upgrade_execution.md](pre_upgrade_execution.md) | Get Pre-upgrade Trade History | Get users' execution records which occurred before you upgraded the account to a Unified account, sorted by execTime in  |
| [pre_upgrade_order_list.md](pre_upgrade_order_list.md) | Get Pre-upgrade Order History | After the account is upgraded to a Unified account, you can get the orders which occurred before the upgrade. |
| [pre_upgrade_settlement.md](pre_upgrade_settlement.md) | Get Pre-upgrade USDC Session Settlement | Query session settlement records of USDC perpetual before you upgrade the account to Unified account. |
| [pre_upgrade_transaction_log.md](pre_upgrade_transaction_log.md) | Get Pre-upgrade Transaction Log | Query transaction logs which occurred in the USDC Derivatives wallet before the account was upgraded to a Unified accoun |
| [v5_rate_limit.md](v5_rate_limit.md) | Rate Limit Rules | IP Limit |
| [rules_for_pros_apilimit_query.md](rules_for_pros_apilimit_query.md) | Get Rate Limit | API rate limit: 50 req per second |
| [rules_for_pros_apilimit_query_all.md](rules_for_pros_apilimit_query_all.md) | Get All Rate Limits | API rate limit: 50 req per second |
| [rules_for_pros_apilimit_query_cap.md](rules_for_pros_apilimit_query_cap.md) | Get Rate Limit Cap | API rate limit: 50 req per second |
| [rules_for_pros_apilimit_set.md](rules_for_pros_apilimit_set.md) | Set Rate Limit | API rate limit: 50 req per second |
| [rules_for_pros_introduction.md](rules_for_pros_introduction.md) | Introduction | API Rate Limit Rules for PROs |
| [rate_limit_rules_for_vips.md](rate_limit_rules_for_vips.md) | API Rate Limit Rules for VIPs | API Rate Limit Rules for VIPs |
| [rfq_basic_workflow.md](rfq_basic_workflow.md) | Basic Workflow | Basic concepts |
| [trade_accept_other_quote.md](trade_accept_other_quote.md) | Accept non-LP Quote | Accept non-LP Quote. Up to 50 requests per second. |
| [trade_cancel_all_quotes.md](trade_cancel_all_quotes.md) | Cancel All Quotes | Cancel all active quotes. Up to 50 requests per second |
| [trade_cancel_all_rfq.md](trade_cancel_all_rfq.md) | Cancel All RFQs | Cancel all active RFQs. Up to 50 requests per second |
| [trade_cancel_quote.md](trade_cancel_quote.md) | Cancel Quote | Cancel a quote. Up to 50 requests per second |
| [trade_cancel_rfq.md](trade_cancel_rfq.md) | Cancel RFQ | Cancel RFQ. Up to 50 requests per second |
| [trade_create_quote.md](trade_create_quote.md) | Create Quote | Create a quote. Up to 50 requests per second. The quoting party sends a quote in response to the inquirier. |
| [trade_create_rfq.md](trade_create_rfq.md) | Create RFQ | Create RFQ. Up to 50 requests per second. |
| [trade_execute_quote.md](trade_execute_quote.md) | Execute Quote | Execute quote – only for the creator of the RFQ. Up to 50 requests per second. |
| [trade_public_trades.md](trade_public_trades.md) | Get Public Trades | Get the recently executed rfq successfully. Up to 50 requests per second |
| [trade_quote_list.md](trade_quote_list.md) | Get Quotes | Obtain historical quote information. Up to 50 requests per second |
| [trade_quote_realtime.md](trade_quote_realtime.md) | Get Quotes (real-time) | Get real-time quote information. Up to 50 requests per second |
| [trade_rfq_config.md](trade_rfq_config.md) | Get RFQ Configuration | RFQ Config. Up to 50 requests per second. |
| [trade_rfq_list.md](trade_rfq_list.md) | Get RFQs | Obtain historical inquiry information. Up to 50 requests per second |
| [trade_rfq_realtime.md](trade_rfq_realtime.md) | Get RFQs (real-time) | Obtain real-time inquiry information. Up to 50 requests per second |
| [trade_trade_list.md](trade_trade_list.md) | Get Trade History | Obtain transaction information. Up to 50 requests per second |
| [private_inquiry.md](private_inquiry.md) | RFQ | Obtain the inquiries (requests for quotes) information sent or received by the user themselves. Whenever the user sends  |
| [private_quote.md](private_quote.md) | Quote | Obtain the quote information sent or received by the user themselves. Whenever the user sends or receives a quote themse |
| [private_transaction.md](private_transaction.md) | Execution | Obtain the user's own block trade information. All legs in the same block trade are included in the same update. As long |
| [public_public_transaction.md](public_public_transaction.md) | Trade | Latest block trade information. All legs in the same block trade are included in the same update. Data will be pushed wh |
| [bbo_sbe_bbo.md](bbo_sbe_bbo.md) | SBE BBO Integration | Overview |
| [level_50_sbe_level_50.md](level_50_sbe_level_50.md) | SBE Level 50 Integration | Overview |
| [sbe_sbe_basic_info.md](sbe_sbe_basic_info.md) | SBE Basic Information | All SBE-based feeds are described in this section are available only via the Market Maker WebSocket (MMWS) / Market Make |
| [sbe_sbe_public_trade.md](sbe_sbe_public_trade.md) | SBE Public Trade Integration | Overview |
| [v5_smp.md](v5_smp.md) | Self Match Prevention | What is SMP? |
| [spot_margin_uta_coinstate.md](spot_margin_uta_coinstate.md) | Get Coin State | HTTP Request |
| [spot_margin_uta_currency_data.md](spot_margin_uta_currency_data.md) | Get Currency Data | If the borrowable switch is disabled (false), the related configuration fields will return "". |
| [spot_margin_uta_get_auto_repay_mode.md](spot_margin_uta_get_auto_repay_mode.md) | Get Auto Repay Mode | Get spot automatic repayment mode |
| [spot_margin_uta_historical_interest.md](spot_margin_uta_historical_interest.md) | Get Historical Interest Rate | You can query up to six months borrowing interest rate of Margin trading. |
| [spot_margin_uta_max_borrowable.md](spot_margin_uta_max_borrowable.md) | Get Max Borrowable Amount | HTTP Request |
| [spot_margin_uta_position_tiers.md](spot_margin_uta_position_tiers.md) | Get Position Tiers | * If currency is passed in the input parameter, query by currency; if currency is not passed in the input parameter, que |
| [spot_margin_uta_repayment_available_amount.md](spot_margin_uta_repayment_available_amount.md) | Get Available Amount to Repay | HTTP Request |
| [spot_margin_uta_set_auto_repay_mode.md](spot_margin_uta_set_auto_repay_mode.md) | Set Auto Repay Mode | Set spot automatic repayment mode |
| [spot_margin_uta_set_leverage.md](spot_margin_uta_set_leverage.md) | Set Leverage | Set the user's maximum leverage in spot cross margin |
| [spot_margin_uta_status.md](spot_margin_uta_status.md) | Get Status And Leverage | Query the Spot margin status and leverage |
| [spot_margin_uta_switch_mode.md](spot_margin_uta_switch_mode.md) | Toggle Margin Trade | Turn on / off spot margin trade |
| [spot_margin_uta_tier_collateral_ratio.md](spot_margin_uta_tier_collateral_ratio.md) | Get Tiered Collateral Ratio | UTA loan tiered collateral ratio |
| [spot_margin_uta_vip_margin.md](spot_margin_uta_vip_margin.md) | Get VIP Margin Data | This margin data is for Unified account in particular. |
| [market_instrument_2.md](market_instrument_2.md) | Get Instruments Info | Query for the instrument specification of spread combinations. |
| [market_orderbook_2.md](market_orderbook_2.md) | Get Orderbook | Query spread orderbook depth data. |
| [market_recent_trade_2.md](market_recent_trade_2.md) | Get Recent Public Trades | Query recent public spread trading history in Bybit. |
| [market_tickers_2.md](market_tickers_2.md) | Get Tickers | Query for the latest price snapshot, best bid/ask price, and trading volume of different spread combinations in the last |
| [trade_amend_order.md](trade_amend_order.md) | Amend Order | You can only modify unfilled or partially filled orders. |
| [trade_cancel_all.md](trade_cancel_all.md) | Cancel All Orders | Cancel all open orders |
| [trade_cancel_order.md](trade_cancel_order.md) | Cancel Order | HTTP Request |
| [trade_create_order.md](trade_create_order.md) | Create Order | Place a spread combination order. Up to 50 open orders per account. |
| [trade_open_order.md](trade_open_order.md) | Get Open Orders | * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in da |
| [trade_order_history.md](trade_order_history.md) | Get Order History | * orderId & orderLinkId has a higher priority than startTime & endTime |
| [trade_trade_history.md](trade_trade_history.md) | Get Trade History | * In self-trade cases, both the maker and taker single-leg trades will be returned in the same request. |
| [private_execution.md](private_execution.md) | Execution | Topic: spread.execution |
| [private_order.md](private_order.md) | Order | Subscribe to the order stream to see changes to your orders in real-time. |
| [public_orderbook.md](public_orderbook.md) | Orderbook | Subscribe to the spread orderbook stream. |
| [public_ticker.md](public_ticker.md) | Ticker | Subscribe to the ticker stream. |
| [public_trade.md](public_trade.md) | Trade | Subscribe to the public trades stream. |
| [v5_system_status.md](v5_system_status.md) | Get System Status | Get the system status when there is a platform maintenance or service incident. |
| [user_apikey_info.md](user_apikey_info.md) | Get API Key Information | Get the information of the api key. Use the api key pending to be checked to call the endpoint. Both master and sub user |
| [user_create_subuid.md](user_create_subuid.md) | Create Sub UID | Create a new sub user id. Use master account's api key. |
| [user_create_subuid_apikey.md](user_create_subuid_apikey.md) | Create Sub UID API Key | To create new API key for those newly created sub UID. Use master user's api key only. |
| [user_friend_referral.md](user_friend_referral.md) | Get Friend Referrals | Any permission can access this endpoint. |
| [user_froze_subuid.md](user_froze_subuid.md) | Freeze Sub UID | Freeze Sub UID. Use master user's api key only. |
| [user_fund_subuid_list.md](user_fund_subuid_list.md) | Get Fund Custodial Sub Acct | The institutional client can query the fund custodial sub accounts. |
| [user_list_sub_apikeys.md](user_list_sub_apikeys.md) | Get Sub Account All API Keys | Query all api keys information of a sub UID. |
| [user_modify_master_apikey.md](user_modify_master_apikey.md) | Modify Master API Key | Modify the settings of master api key. Use the api key pending to be modified to call the endpoint. Use master user's ap |
| [user_modify_sub_apikey.md](user_modify_sub_apikey.md) | Modify Sub API Key | Modify the settings of sub api key. Use the sub account api key pending to be modified to call the endpoint or use maste |
| [user_page_subuid.md](user_page_subuid.md) | Get Sub UID List (Unlimited) | This API is applicable to the client who has over 10k sub accounts. Use master user's api key only. |
| [user_rm_master_apikey.md](user_rm_master_apikey.md) | Delete Master API Key | Delete the api key of master account. Use the api key pending to be delete to call the endpoint. Use master user's api k |
| [user_rm_sub_apikey.md](user_rm_sub_apikey.md) | Delete Sub API Key | Delete the api key of sub account. Use the sub api key pending to be delete to call the endpoint or use the master api k |
| [user_rm_subuid.md](user_rm_subuid.md) | Delete Sub UID | Delete a sub UID. If a sub-account’s asset balance is greater than 0.001 USDT, it cannot be deleted. |
| [user_sign_agreement.md](user_sign_agreement.md) | Sign Agreement | To trade commodity contracts, please complete the agreement signing first. Once completed, you will be able to trade all |
| [user_subuid_list.md](user_subuid_list.md) | Get Sub UID List (Limited) | Get at most 10k sub UID of master account. Use master user's api key only. |
| [user_wallet_type.md](user_wallet_type.md) | Get UID Wallet Type | Get available wallet types for the master account or sub account |
| [private_dcp.md](private_dcp.md) | Dcp | Subscribe to the dcp stream to trigger DCP function. |
| [private_execution_2.md](private_execution_2.md) | Execution | Subscribe to the execution stream to see your executions in real-time. |
| [private_fast_execution.md](private_fast_execution.md) | Fast Execution | Fast execution stream significantly reduces data latency compared original "execution" stream. However, it pushes limite |
| [private_greek.md](private_greek.md) | Greek | Subscribe to the greeks stream to see changes to your greeks data in real-time. option only. |
| [private_order_2.md](private_order_2.md) | Order | Subscribe to the order stream to see changes to your orders in real-time. |
| [private_position.md](private_position.md) | Position | Subscribe to the position stream to see changes to your position data in real-time. |
| [private_wallet.md](private_wallet.md) | Wallet | Subscribe to the wallet stream to see changes to your wallet in real-time. |
| [public_adl_alert.md](public_adl_alert.md) | ADL Alert | Subscribe to ADL alerts and insurance pool information. |
| [public_all_liquidation.md](public_all_liquidation.md) | All Liquidation | Subscribe to the liquidation stream, push all liquidations that occur on Bybit. |
| [public_insurance_pool.md](public_insurance_pool.md) | Insurance Pool | Subscribe to get the update of insurance pool balance |
| [public_kline.md](public_kline.md) | Kline | Subscribe to the klines stream. |
| [public_order_price_limit.md](public_order_price_limit.md) | Order Price Limit | Subscribe to Get Order Price Limit. |
| [public_orderbook_2.md](public_orderbook_2.md) | Orderbook | Subscribe to the orderbook stream. Supports different depths. |
| [public_orderbook_rpi.md](public_orderbook_rpi.md) | RPI Orderbook | Subscribe to the orderbook stream including RPI quote |
| [public_ticker_2.md](public_ticker_2.md) | Ticker | Subscribe to the ticker stream. |
| [public_trade_2.md](public_trade_2.md) | Trade | Subscribe to the recent trades stream. |
| [system_system_status.md](system_system_status.md) | System Status | Listen to the system status when there is a platform maintenance or service incident. |
| [trade_guideline.md](trade_guideline.md) | Websocket Trade Guideline | URL |
| [ws_connect.md](ws_connect.md) | Connect | WebSocket public stream: |
