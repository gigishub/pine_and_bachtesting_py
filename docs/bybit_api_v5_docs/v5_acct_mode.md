# Different Account Modes

> **Source:** https://bybit-exchange.github.io/docs/v5/acct-mode

---

On this page

# Different Account Modes

There are three main account modes that have existed on the Bybit platform, namely classic account (now unavailable), unified account 1.0, and unified account 2.0.

This guide serves to assist users with old accounts into upgrading to the latest version. If you registered your account in 2025 or after then you can safely ignore this guide.

## UTA 2.0​

This account mode is the ultimate version of the unified account, integrating inverse contracts, USDT perpetual, USDT Futures, USDC perpetual, USDC Futures, spot and options into a unified trading system. In cross margin and portifolio margin modes, margin is shared among all trades.

## UTA 1.0​

Under this account mode, inverse contract transactions are in a separate trading account, and the corresponding margin currency needs to be deposited into the "inverse derivatives account" before trading, and the margins are not shared between each other. For USDT perpetual, USDT Futures, USDC perpetual, USDC Futures, spot and options are all traded within the "unified trading"

## Classic Account​

Under this account mode, contract transactions and spot transactions are separated. Inverse contracts and USDT perpetual transactions are completed in the "derivatives account", and spot transactions are completed in the "spot account"

## Determine account mode through API​

Use the key of the corresponding account to call [Get Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info), look at the field `unifiedMarginStatus`

  * `1`: classic account
  * `3`: uta1.0
  * `4`: uta1.0 (pro version)
  * `5`: uta2.0
  * `6`: uta2.0 (pro version)  
_P.S. uta or uta (pro), they are the same thing, but pro has a slight performance advantage when trading via API_



## API usage changes for UTA 2.0​

API category| API| uta2.0| uta1.0  
---|---|---|---  
category=inverse| category=inverse  
Market| [Get Instruments Info](https://bybit-exchange.github.io/docs/v5/market/instrument)| "unifiedMarginTrade" is true after UTA2.0 is implemented| "unifiedMarginTrade" is false  
Trade| [Place Order](https://bybit-exchange.github.io/docs/v5/order/create-order)| Inverse Futures no longer support hedge mode, so "positionIdx" is always `0`| Inverse Futures support hedge mode, so "positionIdx" can be `0`, `1`, `2`  
[Get Open & Closed Orders](https://bybit-exchange.github.io/docs/v5/order/open-order)| To query the final status orders, use `openOnly`=1, and only retain the latest 500 orders.| To query the final status orders, use `openOnly`=2  
[Get Order History](https://bybit-exchange.github.io/docs/v5/order/order-list)| 1\. `orderStatus` is not passed, and all final orders are queried by default  
2\. Parameters `baseCoin` and `settleCoin` are supported  
3\. Active order query is not supported, and some final orders are limited to query  
4\. Cancelled orders save up to 24 hours  
5\. Only orders generated after the upgrade can be queried| 1\. `orderStatus` is not passed, and the default query is active and final orders  
2\. The parameters `baseCoin` and `settleCoin` are not supported  
3\. Active orders and various final orders are always supported  
4\. No such restriction  
[Get Trade History](https://bybit-exchange.github.io/docs/v5/order/execution)| 1\. Supports `baseCoin` query;   
2\. The returned createType has a value  
3\. Only transactions generated after the upgrade can be queried| 1\. `baseCoin` query is not supported;  
2\. The returned createType is always empty string `""`  
[Batch Place Order](https://bybit-exchange.github.io/docs/v5/order/batch-place)| Support inverse contract| Not support inverse contract  
[Batch Amend Order](https://bybit-exchange.github.io/docs/v5/order/batch-amend)| Support inverse contract| Not support inverse contract  
[Batch Cancel Order](https://bybit-exchange.github.io/docs/v5/order/batch-cancel)| Support inverse contract| Not support inverse contract  
[Set Disconnect Cancel All](https://bybit-exchange.github.io/docs/v5/order/dcp)| Support inverse contract, inverse trading orders will be cancelled when dcp is triggered| Not support inverse contract, inverse trading orders will not be cancelled when dcp is triggered  
Pre-upgrade| [Get Pre-upgrade Order History](https://bybit-exchange.github.io/docs/v5/pre-upgrade/order-list)| Supports querying orders generated when it is a classic account or unified account 1.0| -  
[Get Pre-upgrade Trade History](https://bybit-exchange.github.io/docs/v5/pre-upgrade/execution)| Supports querying transactions generated when it is a classic account or unified account 1.0| -  
[Get Pre-upgrade Closed PnL](https://bybit-exchange.github.io/docs/v5/pre-upgrade/close-pnl)| Supports querying close pnl generated when it is a classic account or unified account 1.0| -  
Position| [Get Position Info](https://bybit-exchange.github.io/docs/v5/position)| 1\. Passing multiple symbols is not supported  
2\. In the response, there are changes in the meaning or use of "tradeMode", "liqPrice", "bustPrice" fields| 1\. Supports passing multiple symbols  
[Get Closed PnL](https://bybit-exchange.github.io/docs/v5/position/close-pnl)| Only the close pnl generated after the upgrade can be queried.|  \-   
[Set Leverage](https://bybit-exchange.github.io/docs/v5/position/leverage)| Inverse perpetual and inverse Futures only support one-way position mode, and the leverage of buy and sell must be equal| Inverse Futures support hedge-mode positions, and the leverage of buy and sell can be unequal  
[Switch Cross/Isolated Margin](https://bybit-exchange.github.io/docs/v5/abandon/cross-isolate)| The margin mode has become the account dimension, and this interface is no longer applicable| Inverse contracts support the use of this interface  
[Switch Position Mode](https://bybit-exchange.github.io/docs/v5/position/position-mode)| Inverse Futures no longer supports hedge-mode positions| Inverse Futures supports hedge-mode positions  
Account| [Get Wallet Balance](https://bybit-exchange.github.io/docs/v5/account/wallet-balance)| Not support accountType=CONTRACT| Support accountType=CONTRACT  
[Get Transaction Log (UTA)](https://bybit-exchange.github.io/docs/v5/account/transaction-log)| Transaction logs for inverse contracts will be included| The transaction log of the inverse contract needs to go through the interface below  
[Get Transaction Log(Classic)](https://bybit-exchange.github.io/docs/v5/abandon/contract-transaction-log)| After upgrading to 2.0, this interface is no longer applicable.| Data from uta 1.0 or classic account can still be obtained  
Asset| [Get Delivery Record](https://bybit-exchange.github.io/docs/v5/asset/delivery)| Support inverse futures delivery records| Not support inverse futures delivery records  
All interfaces involving accountType in this directory| CONTRACT is no longer supported because "inverse derivatives account" does not exist anymore| Support CONTRACT (inverse derivatives account)  
WebSocket Stream/Trade| [Websocket Trade Guideline](https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline)| Support inverse contract| Not support inverse contract  
  
  * UTA 2.0
  * UTA 1.0
  * Classic Account
  * Determine account mode through API
  * API usage changes for UTA 2.0


