# Get VIP Margin Data

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get VIP Margin Data



On this page

# Get VIP Margin Data

This margin data is for **Unified account** in particular.

info

Does not need authentication.

### HTTP Request​

GET`/v5/spot-margin-trade/data`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[vipLevel](https://bybit-exchange.github.io/docs/v5/enum#viplevel)| false| string| VIP level  
currency| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
vipCoinList| array| Object  
> list| array| Object  
>> borrowable| boolean| Whether it is allowed to be borrowed  
>> collateralRatio| string| Due to the new Tiered Collateral value logic, this field will no longer be accurate starting on February 19, 2025. Please refer to [Get Tiered Collateral Ratio](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/tier-collateral-ratio)  
>> currency| string| Coin name  
>> hourlyBorrowRate| string| Borrow interest rate per hour  
>> liquidationOrder| string| Liquidation order  
>> marginCollateral| boolean| Whether it can be used as a margin collateral currency  
>> maxBorrowingAmount| string| Max borrow amount  
> vipLevel| string| VIP level  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/spot-margin-uta/vip-margin)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/data?vipLevel=No VIP&currency=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.spot_margin_trade_get_vip_margin_data())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getVIPMarginData({  
        vipLevel: 'No VIP',  
        currency: 'BTC',  
      })  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "vipCoinList": [  
                {  
                    "list": [  
                        {  
                            "borrowable": true,  
                            "collateralRatio": "0.95",  
                            "currency": "BTC",  
                            "hourlyBorrowRate": "0.0000015021220000",  
                            "liquidationOrder": "11",  
                            "marginCollateral": true,  
                            "maxBorrowingAmount": "3"  
                        }  
                    ],  
                    "vipLevel": "No VIP"  
                }  
            ]  
        }  
    }  
    

[PreviousGet Affiliate User Info](https://bybit-exchange.github.io/docs/v5/affiliate/affiliate-info)[NextGet Tiered Collateral Ratio](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/tier-collateral-ratio)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


