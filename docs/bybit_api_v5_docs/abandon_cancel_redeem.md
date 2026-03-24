# Cancel Redeem

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/cancel-redeem

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Cancel Redeem



On this page

# Cancel Redeem

Cancel the withdrawal operation.

### HTTP Request​

POST`/v5/lending/redeem-cancel`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| false| string| Coin name  
orderId| false| string| The order ID of redemption  
serialNo| false| string| Serial no. The customised ID of redemption  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
orderId| string| Order ID  
serialNo| string| Serial No  
updatedTime| string| Updated timestamp (ms)  
  
### Request Example​
    
    
    POST /v5/lending/redeem-cancel HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682048277724  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "coin": "BTC",  
        "orderId": "1403517113428086272",  
        "serialNo": null  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "orderId": "1403517113428086272",  
            "serialNo": "linear004",  
            "updatedTime": "1682048277963"  
        },  
        "retExtInfo": {},  
        "time": 1682048278001  
    }  
    

[PreviousRedeem Funds](https://bybit-exchange.github.io/docs/v5/abandon/redeem)[NextBorrow](https://bybit-exchange.github.io/docs/v5/abandon/borrow)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


