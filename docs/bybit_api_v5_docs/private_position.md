# Position

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/position

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Position



On this page

# Position

Subscribe to the position stream to see changes to your position data in **real-time**.

**All-In-One Topic:** `position`  
**Categorised Topic:** `position.linear`, `position.inverse`, `position.option`

info

  * All-In-One topic and Categorised topic **cannot** be in the same subscription request
  * All-In-One topic: Allow you to listen to all categories (linear, inverse, option) websocket updates
  * Categorised Topic: Allow you to listen only to specific category websocket updates



tip

Every time when you create/amend/cancel an order, the position topic will generate a new message (regardless if there's any actual change)

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
id| string| Message ID  
topic| string| Topic name  
creationTime| number| Data created timestamp (ms)  
data| array| Object  
> [category](https://bybit-exchange.github.io/docs/v5/enum#category)| string| Product type `linear`, `inverse`, `option`  
> symbol| string| Symbol name  
> side| string| Position side. `Buy`: long, `Sell`: short  
return an empty string `""` for an empty position  
> size| string| Position size  
> [positionIdx](https://bybit-exchange.github.io/docs/v5/enum#positionidx)| integer| Used to identify positions in different position modes  
> positionValue| string| Position value  
> riskId| integer| Risk tier ID  
 _for portfolio margin mode, this field returns 0, which means risk limit rules are invalid_  
> riskLimitValue| string| Risk limit value, become meaningless when auto risk-limit tier is applied  
 _for portfolio margin mode, this field returns 0, which means risk limit rules are invalid_  
> entryPrice| string| Average entry price 

  * For USDC Perp & Futures, it indicates average entry price, and it will not be changed with 8-hour session settlement

  
> markPrice| string| Mark price  
> leverage| string| Position leverage  
 _for portfolio margin mode, this field returns "", which means leverage rules are invalid_  
> breakEvenPrice| string| Break even price, only for `linear`,`inverse`. 

  * breakeven_price = (entry_price _qty - realized_pnl) / (qty - abs(qty)_ max(taker fee rate, 0.00055))

  
> autoAddMargin| integer| Whether to add margin automatically when using isolated margin mode 

  * `0`: false
  * `1`: true

  
> positionIM| string| Initial margin, the same value as `positionIMByMp`, please note this change [The New Margin Calculation: Adjustments and Implications](https://www.bybit.com/en/help-center/article/Understanding-the-Adjustment-and-Impact-of-the-New-Margin-Calculation)

  * Portfolio margin mode: returns ""

  
> positionMM| string| Maintenance margin, the same value as `positionMMByMp`

  * Portfolio margin mode: returns ""

  
> liqPrice| string| Position liquidation price 

  * Isolated margin:   
it is the real price for isolated and cross positions, and keeps `""` when liqPrice <= minPrice or liqPrice >= maxPrice
  * Cross margin:  
it is an **estimated** price for cross positions(because the unified mode controls the risk rate according to the account), and keeps `""` when liqPrice <= minPrice or liqPrice >= maxPrice

 _this field is empty for Portfolio Margin Mode, and no liquidation price will be provided_  
> takeProfit| string| Take profit price  
> stopLoss| string| Stop loss price  
> trailingStop| string| Trailing stop  
> unrealisedPnl| string| Unrealised profit and loss  
> curRealisedPnl| string| The realised PnL for the current holding position  
> sessionAvgPrice| string| USDC contract session avg price, it is the same figure as avg entry price shown in the web UI  
> delta| string| Delta. It is only pushed when you subscribe to the option position.  
> gamma| string| Gamma. It is only pushed when you subscribe to the option position.  
> vega| string| Vega. It is only pushed when you subscribe to the option position.  
> theta| string| Theta. It is only pushed when you subscribe to the option position.  
> cumRealisedPnl| string| Cumulative realised pnl 

  * Futures & Perp: it is the all time cumulative realised P&L
  * Option: it is the realised P&L when you hold that position

  
> [positionStatus](https://bybit-exchange.github.io/docs/v5/enum#positionstatus)| string| Position status. `Normal`, `Liq`, `Adl`  
> [adlRankIndicator](https://bybit-exchange.github.io/docs/v5/enum#adlrankindicator)| integer| Auto-deleverage rank indicator. [What is Auto-Deleveraging?](https://www.bybit.com/en-US/help-center/s/article/What-is-Auto-Deleveraging-ADL)  
> isReduceOnly| boolean| Useful when Bybit lower the risk limit 

  * `true`: Only allowed to reduce the position. You can consider a series of measures, e.g., lower the risk limit, decrease leverage or reduce the position, add margin, or cancel orders, after these operations, you can call [confirm new risk limit](https://bybit-exchange.github.io/docs/v5/position/confirm-mmr) endpoint to check if your position can be removed the reduceOnly mark
  * `false`: There is no restriction, and it means your position is under the risk when the risk limit is systematically adjusted
  * Only meaningful for isolated margin & cross margin of USDT Perp, USDC Perp, USDC Futures, Inverse Perp and Inverse Futures, meaningless for others

  
> createdTime| string| Timestamp of the first time a position was created on this symbol (ms)  
> updatedTime| string| Position data updated timestamp (ms)  
> seq| long| Cross sequence, used to associate each fill and each position update

  * Different symbols may have the same seq, please use seq + symbol to check unique
  * Returns `"-1"` if the symbol has never been traded
  * Returns the seq updated by the last transaction when there are setting like leverage, risk limit

  
> mmrSysUpdatedTime| string| Useful when Bybit lower the risk limit 

  * When isReduceOnly=`true`: the timestamp (ms) when the MMR will be forcibly adjusted by the system
When isReduceOnly=`false`: the timestamp when the MMR had been adjusted by system
    * It returns the timestamp when the system operates, and if you manually operate, there is no timestamp
    * Keeps `""` by default, if there was a lower risk limit system adjustment previously, it shows that system operation timestamp
    * Only meaningful for isolated margin & cross margin of USDT Perp, USDC Perp, USDC Futures, Inverse Perp and Inverse Futures, meaningless for others

  
> leverageSysUpdatedTime| string| Useful when Bybit lower the risk limit 

  * When isReduceOnly=`true`: the timestamp (ms) when the leverage will be forcibly adjusted by the system
When isReduceOnly=`false`: the timestamp when the leverage had been adjusted by system
    * It returns the timestamp when the system operates, and if you manually operate, there is no timestamp
    * Keeps `""` by default, if there was a lower risk limit system adjustment previously, it shows that system operation timestamp
    * Only meaningful for isolated margin & cross margin of USDT Perp, USDC Perp, USDC Futures, Inverse Perp and Inverse Futures, meaningless for others

  
> positionIMByMp| string| Initial margin calculated by mark price, the same value as `positionIM`

  * Portfolio margin mode: returns ""

  
> positionMMByMp| string| Maintenance margin calculated by mark price, the same value as `positionMM`

  * Portfolio margin mode: returns ""

  
> tpslMode| string| **Deprecated** , always "Full"  
> bustPrice| string| **Deprecated** , always `""`  
> positionBalance| string| **Deprecated** , can refer to `positionIM` or `positionIMByMp` field  
> tradeMode| integer| **Deprecated** , always `0`, check [Get Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info) to know the margin mode  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "position"  
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
    ws.position_stream(callback=handle_message)  
    while True:  
        sleep(1)  
    

### Stream Example​
    
    
    {  
        "id": "1003076014fb7eedb-c7e6-45d6-a8c1-270f0169171a",  
        "topic": "position",  
        "creationTime": 1697682317044,  
        "data": [  
            {  
                "positionIdx": 2,  
                "tradeMode": 0,  
                "riskId": 1,  
                "riskLimitValue": "2000000",  
                "symbol": "BTCUSDT",  
                "side": "",  
                "size": "0",  
                "entryPrice": "0",  
                "leverage": "10",  
                "breakEvenPrice":"93556.73034991",  
                "positionValue": "0",  
                "positionBalance": "0",  
                "markPrice": "28184.5",  
                "positionIM": "0",  
                "positionIMByMp": "0",  
                "positionMM": "0",  
                "positionMMByMp": "0",  
                "takeProfit": "0",  
                "stopLoss": "0",  
                "trailingStop": "0",  
                "unrealisedPnl": "0",  
                "curRealisedPnl": "1.26",  
                "cumRealisedPnl": "-25.06579337",  
                "sessionAvgPrice": "0",  
                "createdTime": "1694402496913",  
                "updatedTime": "1697682317038",  
                "tpslMode": "Full",  
                "liqPrice": "0",  
                "bustPrice": "",  
                "category": "linear",  
                "positionStatus": "Normal",  
                "adlRankIndicator": 0,  
                "autoAddMargin": 0,  
                "leverageSysUpdatedTime": "",  
                "mmrSysUpdatedTime": "",  
                "seq": 8327597863,  
                "isReduceOnly": false  
            }  
        ]  
    }  
    

[PreviousADL Alert](https://bybit-exchange.github.io/docs/v5/websocket/public/adl-alert)[NextExecution](https://bybit-exchange.github.io/docs/v5/websocket/private/execution)

  * Response Parameters
  * Subscribe Example
  * Stream Example


