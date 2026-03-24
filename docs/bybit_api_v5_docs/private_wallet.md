# Wallet

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/wallet

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Wallet



On this page

# Wallet

Subscribe to the wallet stream to see changes to your wallet in **real-time**.

info

  * There is no snapshot event given at the time when the subscription is successful
  * The unrealised PnL change does not trigger an event
  * Under the new logic of UTA manual borrow, `spotBorrow` field corresponding to spot liabilities is detailed in the [ announcement](https://announcements.bybit.com/en/article/bybit-uta-function-optimization-manual-coin-borrowing-will-be-launched-soon-blt5d858199bd12e849/).  
Old `walletBalance` = New `walletBalance` \- `spotBorrow`



**Topic:** `wallet`

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
id| string| Message ID  
topic| string| Topic name  
creationTime| number| Data created timestamp (ms)  
data| array| Object  
> accountType| string| Account type `UNIFIED`  
> accountIMRate| string| Account IM rate 

  * You can refer to this [Glossary](https://www.bybit.com/en/help-center/article/Glossary-Unified-Trading-Account) to understand the below fields calculation and mearning
  * All account wide fields are **not** applicable to isolated margin

  
> accountMMRate| string| Account MM rate  
> totalEquity| string| Account total equity (USD): ∑Asset Equity By USD value of each asset  
> totalWalletBalance| string| Account wallet balance (USD): ∑Asset Wallet Balance By USD value of each asset  
> totalMarginBalance| string| Account margin balance (USD): totalWalletBalance + totalPerpUPL  
> totalAvailableBalance| string| Account available balance (USD), 

  * Cross Margin: totalMarginBalance - Haircut - totalInitialMargin.
  * Porfolio Margin: total Equity - Haircut - totalInitialMargin 

  
> totalPerpUPL| string| Account Perps and Futures unrealised p&l (USD): ∑Each Perp and USDC Futures upl by base coin  
> totalInitialMargin| string| Account initial margin (USD): ∑Asset Total Initial Margin Base Coin  
> totalMaintenanceMargin| string| Account maintenance margin (USD): ∑ Asset Total Maintenance Margin Base Coin  
> accountIMRateByMp| string| You can **ignore** this field, and refer to `accountIMRate`, which has the same calculation  
> accountMMRateByMp| string| You can **ignore** this field, and refer to `accountMMRate`, which has the same calculation  
> totalInitialMarginByMp| string| You can **ignore** this field, and refer to `totalInitialMargin`, which has the same calculation  
> totalMaintenanceMarginByMp| string| You can **ignore** this field, and refer to `totalMaintenanceMargin`, which has the same calculation  
> accountLTV| string| **Deprecated** field  
> coin| array| Object  
>> coin| string| Coin name, such as BTC, ETH, USDT, USDC  
>> equity| string| Equity of coin. Asset Equity = Asset Wallet Balance + Asset Perp UPL + Asset Future UPL + Asset Option Value = `walletBalance` \- `spotBorrow` \+ `unrealisedPnl` \+ Asset Option Value  
>> usdValue| string| USD value of coin. If this coin cannot be collateral, then it is 0  
>> walletBalance| string| Wallet balance of coin  
>> locked| string| Locked balance due to the Spot open order  
>> spotHedgingQty| string| The spot asset qty that is used to hedge in the portfolio margin, truncate to 8 decimals and "0" by default  
>> borrowAmount| string| Borrow amount of coin = spot liabilities + derivatives liabilities  
>> accruedInterest| string| Accrued interest  
>> totalOrderIM| string| Pre-occupied margin for order. For portfolio margin mode, it returns ""  
>> totalPositionIM| string| Sum of initial margin of all positions + Pre-occupied liquidation fee. For portfolio margin mode, it returns ""  
>> totalPositionMM| string| Sum of maintenance margin for all positions. For portfolio margin mode, it returns ""  
>> unrealisedPnl| string| Unrealised P&L  
>> cumRealisedPnl| string| Cumulative Realised P&L  
>> bonus| string| Bonus  
>> collateralSwitch| boolean| Whether it can be used as a margin collateral currency (platform) 

  * When marginCollateral=false, then collateralSwitch is meaningless

  
>> marginCollateral| boolean| Whether the collateral is turned on by user (user) 

  * When marginCollateral=true, then collateralSwitch is meaningful

  
>> spotBorrow| string| Borrow amount by spot margin trade and manual borrow amount(does not include borrow amount by spot margin active order). `spotBorrow` field corresponding to spot liabilities is detailed in the [ announcement](https://announcements.bybit.com/en/article/bybit-uta-function-optimization-manual-coin-borrowing-will-be-launched-soon-blt5d858199bd12e849/).  
>> free| string| **Deprecated** since there is no Spot wallet any more  
>> availableToBorrow| string| **Deprecated** field, always return `""`. Please refer to `availableToBorrow` in the [Get Collateral Info](https://bybit-exchange.github.io/docs/v5/account/collateral-info)  
>> availableToWithdraw| string| **Deprecated** for `accountType=UNIFIED` from 9 Jan, 2025 

  * Transferable balance: you can use [Get Transferable Amount (Unified)](https://bybit-exchange.github.io/docs/v5/account/unified-trans-amnt) or [Get All Coins Balance](https://bybit-exchange.github.io/docs/v5/asset/balance/all-balance) instead
  * Derivatives available balance:   
**isolated margin** : walletBalance - totalPositionIM - totalOrderIM - locked - bonus  
**cross & portfolio margin**: look at field `totalAvailableBalance`(USD), which needs to be converted into the available balance of accordingly coin through index price
  * Spot (margin) available balance: refer to [Get Borrow Quota (Spot)](https://bybit-exchange.github.io/docs/v5/order/spot-borrow-quota)

  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "wallet"  
        ]  
    }  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="private",  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    def handle_message(message):  
        print(message)  
    ws.wallet_stream(callback=handle_message)  
    while True:  
        sleep(1)  
    

### Stream Example​
    
    
    {  
        "id": "592324d2bce751-ad38-48eb-8f42-4671d1fb4d4e",  
        "topic": "wallet",  
        "creationTime": 1700034722104,  
        "data": [  
            {  
                "accountIMRate": "0",  
                "accountIMRateByMp": "0",  
                "accountMMRate": "0",  
                "accountMMRateByMp": "0",  
                "totalEquity": "10262.91335023",  
                "totalWalletBalance": "9684.46297164",  
                "totalMarginBalance": "9684.46297164",  
                "totalAvailableBalance": "9556.6056555",  
                "totalPerpUPL": "0",  
                "totalInitialMargin": "0",  
                "totalInitialMarginByMp": "0",  
                "totalMaintenanceMargin": "0",  
                "totalMaintenanceMarginByMp": "0",  
                "coin": [  
                    {  
                        "coin": "BTC",  
                        "equity": "0.00102964",  
                        "usdValue": "36.70759517",  
                        "walletBalance": "0.00102964",  
                        "availableToWithdraw": "0.00102964",  
                        "availableToBorrow": "",  
                        "borrowAmount": "0",  
                        "accruedInterest": "0",  
                        "totalOrderIM": "",  
                        "totalPositionIM": "",  
                        "totalPositionMM": "",  
                        "unrealisedPnl": "0",  
                        "cumRealisedPnl": "-0.00000973",  
                        "bonus": "0",  
                        "collateralSwitch": true,  
                        "marginCollateral": true,  
                        "locked": "0",  
                        "spotHedgingQty": "0.01592413",  
                        "spotBorrow": "0"  
                    }  
                ],  
                "accountLTV": "0",  
                "accountType": "UNIFIED"  
            }  
        ]  
    }  
    

[PreviousOrder](https://bybit-exchange.github.io/docs/v5/websocket/private/order)[NextGreek](https://bybit-exchange.github.io/docs/v5/websocket/private/greek)

  * Response Parameters
  * Subscribe Example
  * Stream Example


