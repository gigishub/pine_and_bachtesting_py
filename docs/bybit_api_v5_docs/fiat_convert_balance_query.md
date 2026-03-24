# Get Balance

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/balance-query

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Get Balance



On this page

# Get Balance

### HTTP Request​

GET`/v5/fiat/balance-query`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| `Fiat`: fiat currency code (ISO 4217) etc: KZT. not set will query all fiat balance list  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object| object  
> totalBalance| string| Total balance  
> balance| string| Available balance  
> frozenBalance| string| Frozen balance  
> currency| string| Currency  
  
### Request Example​

  * HTTP


    
    
    GET /v5/fiat/balance-query HTTP/1.1    
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720074159814  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": [  
            {  
                "currency": "GEL",  
                "totalBalance": "100000",  
                "balance": "100000",  
                "frozenBalance": "0"  
            }  
        ]  
    }  
    

[PreviousGet Convert History](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-trade-history)[NextTrade Notify](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/trade-notify)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


