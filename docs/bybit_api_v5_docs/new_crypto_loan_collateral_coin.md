# Get Collateral Coins

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/collateral-coin

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Get Collateral Coins



On this page

# Get Collateral Coins

info

Does not need authentication.

### HTTP Request​

GET`/v5/crypto-loan-common/collateral-data`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
collateralRatioConfigList| array| Object  
> collateralRatioList| array| Object  
>> collateralRatio| string| Collateral ratio  
>> maxValue| string| Max qty  
>> minValue| string| Min qty  
> currencies| string| Currenies with the same collateral ratio, e.g., `BTC,ETH,XRP`  
currencyLiquidationList| array| Object  
> currency| string| Coin name  
> liquidationOrder| integer| Liquidation order  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-common/collateral-data?currency=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_collateral_coins_new_crypto_loan(  
        currency="BTC",  
        amount="0.08",  
        direction="1",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "collateralRatioConfigList": [  
                {  
                    "collateralRatioList": [  
                        {  
                            "collateralRatio": "0.8",  
                            "maxValue": "10000",  
                            "minValue": "0"  
                        },  
                        {  
                            "collateralRatio": "0.7",  
                            "maxValue": "20000",  
                            "minValue": "10000"  
                        },  
                        {  
                            "collateralRatio": "0.5",  
                            "maxValue": "30000",  
                            "minValue": "20000"  
                        },  
                        {  
                            "collateralRatio": "0.4",  
                            "maxValue": "99999999999",  
                            "minValue": "30000"  
                        }  
                    ],  
                    "currencies": "ATOM,AAVE,BTC,BOB"  
                }  
            ],  
            "currencyLiquidationList": [  
                {  
                    "currency": "BTC",  
                    "liquidationOrder": 1  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1752627381571  
    }  
    

[PreviousGet Borrowable Coins](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/loan-coin)[NextGet Max. Allowed Collateral Reduction Amount](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/reduce-max-collateral-amt)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


