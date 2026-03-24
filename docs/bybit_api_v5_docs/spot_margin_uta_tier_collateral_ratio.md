# Get Tiered Collateral Ratio

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/tier-collateral-ratio

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Tiered Collateral Ratio



On this page

# Get Tiered Collateral Ratio

UTA loan tiered collateral ratio

info

Does not need authentication.

### HTTP Request​

GET`/v5/spot-margin-trade/collateral`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> currency| string| Coin name  
> collateralRatioList| array| Object  
>> maxQty| string| Upper limit(in coin) of the tiered range, `""` means positive infinity  
>> minQty| string| lower limit(in coin) of the tiered range  
>> collateralRatio| string| Collateral ratio  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/collateral?currency=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_tiered_collateral_ratio(  
        currency="BTC",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "currency": "BTC",  
                    "collateralRatioList": [  
                        {  
                            "minQty": "0",  
                            "maxQty": "1000000",  
                            "collateralRatio": "0.85"  
                        },  
                        {  
                            "minQty": "1000000",  
                            "maxQty": "",  
                            "collateralRatio": "0"  
                        }  
                    ]  
                }  
            ]  
        },  
        "retExtInfo": "{}",  
        "time": 1739848984945  
    }  
    

[PreviousGet VIP Margin Data](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin)[NextGet Currency Data](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/currency-data)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


