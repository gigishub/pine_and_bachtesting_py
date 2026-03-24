# Get Position Tiers

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/position-tiers

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Position Tiers



On this page

# Get Position Tiers

info

  * If `currency` is passed in the input parameter, query by currency; if `currency` is not passed in the input parameter, query all configured currencies



### HTTP Request​

GET`/v5/spot-margin-trade/position-tiers`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> currency| string| Coin name, uppercase only  
> positionTiersRatioList| string| Object  
>> tier| string| Tiers. Display from small to large  
>> borrowLimit| string| Tiers Accumulation Borrow limit  
>> positionMMR| string| Loan Maintenance Margin Rate. Precision 8 decimal places  
>> positionIMR| string| Loan Initial Margin Rate. Precision 8 decimal places  
>> maxLeverage| string| Max Loan Leverage  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/position-tiers?currency=BTC HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1692696840996  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "currency": "BTC",  
                    "positionTiersRatioList": [  
                        {  
                            "tier": "1",  
                            "borrowLimit": "390",  
                            "positionMMR": "0.04",  
                            "positionIMR": "0.2",  
                            "maxLeverage": "5"  
                        },  
                        {  
                            "tier": "2",  
                            "borrowLimit": "391",  
                            "positionMMR": "0.04",  
                            "positionIMR": "0.25",  
                            "maxLeverage": "4"  
                        },  
                        {  
                            "tier": "3",  
                            "borrowLimit": "392",  
                            "positionMMR": "0.04",  
                            "positionIMR": "0.33333333",  
                            "maxLeverage": "3"  
                        },  
                        {  
                            "tier": "4",  
                            "borrowLimit": "393",  
                            "positionMMR": "0.04",  
                            "positionIMR": "0.5",  
                            "maxLeverage": "2"  
                        }  
                    ]  
                }  
            ]  
        },  
        "retExtInfo": "{}",  
        "time": 1756272543440  
    }  
    

[PreviousGet Max Borrowable Amount](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/max-borrowable)[NextGet Coin State](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/coinstate)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


