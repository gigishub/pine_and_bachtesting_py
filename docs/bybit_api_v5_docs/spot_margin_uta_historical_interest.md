# Get Historical Interest Rate

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/historical-interest

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Historical Interest Rate



On this page

# Get Historical Interest Rate

You can query up to six months borrowing interest rate of Margin trading.

info

  * Need authentication, the api key needs "Spot" permission
  * Only supports Unified account 
  * It is public data, i.e., different users get the same historical interest rate for the same VIP/Pro



### HTTP Request​

GET`/v5/spot-margin-trade/interest-rate-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Coin name, uppercase only  
[vipLevel](https://bybit-exchange.github.io/docs/v5/enum#viplevel)| false| string| VIP level 

  * Please note that "No VIP" should be passed like "No%20VIP" in the query string
  * If not passed, it returns your account's VIP level data

  
startTime| false| integer| The start timestamp (ms) 

  * Either both time parameters are passed or neither is passed.
  * Returns 7 days data when both are not passed
  * Supports up to 30 days interval when both are passed

  
endTime| false| integer| The end timestamp (ms)  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array<object>|   
> timestamp| long| timestamp  
> currency| string| coin name  
> hourlyBorrowRate| string| Hourly borrowing rate  
> vipLevel| string| VIP/Pro level  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/spot-margin-trade/interest-rate-history?currency=USDC&vipLevel=No%20VIP&startTime=1721458800000&endTime=1721469600000 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1721891663064  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.spot_margin_trade_get_historical_interest_rate(  
        currency="BTC"  
    ))  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "timestamp": 1721469600000,  
                    "currency": "USDC",  
                    "hourlyBorrowRate": "0.000014621596",  
                    "vipLevel": "No VIP"  
                },  
                {  
                    "timestamp": 1721466000000,  
                    "currency": "USDC",  
                    "hourlyBorrowRate": "0.000014621596",  
                    "vipLevel": "No VIP"  
                },  
                {  
                    "timestamp": 1721462400000,  
                    "currency": "USDC",  
                    "hourlyBorrowRate": "0.000014621596",  
                    "vipLevel": "No VIP"  
                },  
                {  
                    "timestamp": 1721458800000,  
                    "currency": "USDC",  
                    "hourlyBorrowRate": "0.000014621596",  
                    "vipLevel": "No VIP"  
                }  
            ]  
        },  
        "retExtInfo": "{}",  
        "time": 1721899048991  
    }  
    

[PreviousGet Currency Data](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/currency-data)[NextToggle Margin Trade](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


