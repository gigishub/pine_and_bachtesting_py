# Get Lending Coin Info

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/coin-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Lending Coin Info



On this page

# Get Lending Coin Info

Get the basic information of lending coins

info

All `v5/lending` APIs need **SPOT** permission.

### HTTP Request​

GET`/v5/lending/info`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| false| string| Coin name. Return all currencies by default  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> coin| string| Coin name  
> maxRedeemQty| string| The maximum redeemable qty per day (measured from 0 - 24 UTC)  
> minPurchaseQty| string| The minimum qty that can be deposited per request  
> precision| string| Deposit quantity accuracy  
> rate| string| Annualized interest rate. e.g. 0.0002 means 0.02%  
> loanToPoolRatio| string| Capital utilization rate. e.g. 0.0004 means 0.04%  
> actualApy| string| The actual annualized interest rate  
  
### Request Example​
    
    
    GET /v5/lending/info?coin=ETH HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682045949295  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "actualApy": "0.003688421873941958",  
                    "coin": "ETH",  
                    "loanToPoolRatio": "0.16855491872747133044",  
                    "maxRedeemQty": "161",  
                    "minPurchaseQty": "0.03",  
                    "precision": "8",  
                    "rate": "0.003411300771389848"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1682045942972  
    }  
    

[PreviousGet Asset Info (Spot)](https://bybit-exchange.github.io/docs/v5/abandon/asset-info)[NextGet LTV](https://bybit-exchange.github.io/docs/v5/abandon/ltv)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


