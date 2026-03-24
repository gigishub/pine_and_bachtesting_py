# Get Instruments Info

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/market/instrument

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Market
  * Get Instruments Info



On this page

# Get Instruments Info

Query for the instrument specification of spread combinations.

info

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/spread/instrument`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
symbol| false| string| Spread combination symbol name  
baseCoin| false| string| Base coin, uppercase only  
limit| false| integer| Limit for data size per page. [`1`, `500`]. Default: `200`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array<object>| instrument info  
> symbol| string| Spread combination symbol name  
> contractType| string| Product type 

  * `FundingRateArb`: perpetual & spot combination
  * `CarryTrade`: futures & spot combination
  * `FutureSpread`: different expiry futures combination
  * `PerpBasis`: futures & perpetual

  
> status| string| Spread status. `Trading`, `Settling`  
> baseCoin| string| Base coin  
> quoteCoin| string| Quote coin  
> settleCoin| string| Settle coin  
> tickSize| string| The step to increase/reduce order price  
> minPrice| string| Min. order price  
> maxPrice| string| Max. order price  
> lotSize| string| Order qty precision  
> minSize| string| Min. order qty  
> maxSize| string| Max. order qty  
> launchTime| string| Launch timestamp (ms)  
> deliveryTime| string| Delivery timestamp (ms)  
> legs| array<object>| Legs information  
>> symbol| string| Legs symbol name  
>> contractType| string| Legs contract type. `LinearPerpetual`, `LinearFutures`, `Spot`  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​
    
    
    GET /v5/spread/instrument?limit=1 HTTP/1.1  
    Host: api-testnet.bybit.com  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "symbol": "SOLUSDT_SOL/USDT",  
                    "contractType": "FundingRateArb",  
                    "status": "Trading",  
                    "baseCoin": "SOL",  
                    "quoteCoin": "USDT",  
                    "settleCoin": "USDT",  
                    "tickSize": "0.0001",  
                    "minPrice": "-1999.9998",  
                    "maxPrice": "1999.9998",  
                    "lotSize": "0.1",  
                    "minSize": "0.1",  
                    "maxSize": "50000",  
                    "launchTime": "1743675300000",  
                    "deliveryTime": "0",  
                    "legs": [  
                        {  
                            "symbol": "SOLUSDT",  
                            "contractType": "LinearPerpetual"  
                        },  
                        {  
                            "symbol": "SOLUSDT",  
                            "contractType": "Spot"  
                        }  
                    ]  
                }  
            ],  
            "nextPageCursor": "first%3D100008%26last%3D100008"  
        },  
        "retExtInfo": {},  
        "time": 1744076802479  
    }  
    

[PreviousGet Friend Referrals](https://bybit-exchange.github.io/docs/v5/user/friend-referral)[NextGet Orderbook](https://bybit-exchange.github.io/docs/v5/spread/market/orderbook)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


