# Get Order Records

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/order-record

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Order Records



On this page

# Get Order Records

Get lending or redeem history

### HTTP Request​

GET`/v5/lending/history-order`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| false| string| Coin name  
orderId| false| string| Order ID  
startTime| false| long| The start timestamp (ms)  
endTime| false| long| The end timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `500`]. Default: `50`  
orderType| false| string| Order type. `1`: deposit, `2`: redemption, `3`: Payment of proceeds  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> coin| string| Coin name  
> createdTime| string| Created timestamp (ms)  
> orderId| string| Order ID  
> quantity| string| quantity  
> serialNo| string| Serial No  
> status| string| Order status. `0`: Initial, `1`: Processing, `2`: Success, `10`: Failed, `11`: Cancelled  
> updatedTime| string| Updated timestamp (ms)  
  
### Request Example​
    
    
    GET /v5/lending/history-order?orderNo=1403517113428086272 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682049395799  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "coin": "BTC",  
                    "createdTime": "1682048277963",  
                    "orderId": "1403517113428086272",  
                    "orderType": "2",  
                    "quantity": "0.1",  
                    "serialNo": "14035171132183710722373",  
                    "status": "2",  
                    "updatedTime": "1682048278245"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1682049395967  
    }  
    

[PreviousGet Broker Earning](https://bybit-exchange.github.io/docs/v5/abandon/earning)[NextGet Lending Account Info](https://bybit-exchange.github.io/docs/v5/abandon/account-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


