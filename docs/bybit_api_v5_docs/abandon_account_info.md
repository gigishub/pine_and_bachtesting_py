# Get Lending Account Info

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/account-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Lending Account Info



On this page

# Get Lending Account Info

### HTTP Request​

GET`/v5/lending/account`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin name  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
coin| string| Coin name  
principalInterest| string| User Redeemable interest  
principalQty| string| Leftover quantity you can redeem for today (measured from 0 - 24 UTC), formula: min(the rest amount of principle, the amount that the user can redeem on the day)  
principalTotal| string| Total amount redeemable by user  
quantity| string| Current deposit quantity  
  
### Request Example​
    
    
    GET /v5/lending/account?coin=ETH HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682049556563  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "coin": "BTC",  
            "principalInterest": "0",  
            "principalQty": "1",  
            "principalTotal": "1",  
            "quantity": "1"  
        },  
        "retExtInfo": {},  
        "time": 1682049706988  
    }  
    

[PreviousGet Order Records](https://bybit-exchange.github.io/docs/v5/abandon/order-record)[NextSwitch Cross/Isolated Margin](https://bybit-exchange.github.io/docs/v5/abandon/cross-isolate)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


