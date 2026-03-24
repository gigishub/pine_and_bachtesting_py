# Redeem Funds

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/redeem

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Redeem Funds



On this page

# Redeem Funds

Withdraw funds from the Bybit asset pool.

tip

There will be two redemption records: one for the redeemed quantity, and the other one is for the total interest occurred.

### HTTP Request​

POST`/v5/lending/redeem`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin name  
quantity| **ture**|  string| Redemption quantity  
serialNo| false| string| Serial no. A customised ID, and it will automatically generated if not passed  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
coin| string| Coin name  
createdTime| string| Created timestamp (ms)  
orderId| string| Order ID  
principalQty| string| Redemption quantity  
serialNo| string| Serial No  
status| string| Order status. `0`: Initial, `1`: Processing, `2`: Success, `10`: Failed  
updatedTime| string| Updated timestamp (ms)  
  
### Request Example​
    
    
    POST /v5/lending/redeem HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682048277724  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "coin": "BTC",  
        "quantity": "0.1",  
        "serialNo": null  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "coin": "BTC",  
            "createdTime": "1682048277963",  
            "orderId": "1403517113428086272",  
            "principalQty": "0.1",  
            "serialNo": "14035171132183710722373",  
            "status": "0",  
            "updatedTime": "1682048277963"  
        },  
        "retExtInfo": {},  
        "time": 1682048278001  
    }  
    

[PreviousEnable Universal Transfer for Sub UID](https://bybit-exchange.github.io/docs/v5/abandon/enable-unitransfer-subuid)[NextCancel Redeem](https://bybit-exchange.github.io/docs/v5/abandon/cancel-redeem)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


