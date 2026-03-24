# Cancel Order

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/trade/cancel-order

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Trade
  * Cancel Order



On this page

# Cancel Order

### HTTP Request​

POST`/v5/spread/order/cancel`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| false| string| Spread combination order ID. Either `orderId` or `orderLinkId` is **required**  
orderLinkId| false| string| User customised order ID. Either `orderId` or `orderLinkId` is **required**  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
orderId| string| Order ID  
orderLinkId| string| User customised order ID  
  
info

The acknowledgement of an cancel order request indicates that the request was sucessfully accepted. This request is asynchronous so please use the websocket to confirm the order status.

### Request Example​
    
    
    POST /v5/spread/order/cancel HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: XXXXXXX  
    X-BAPI-TIMESTAMP: 1744090699418  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 48  
      
    {  
        "orderLinkId": "1744072052193428476"  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "orderId": "4496253b-b55b-4407-8c5c-29629d169caf",  
            "orderLinkId": "1744072052193428476"  
        },  
        "retExtInfo": {},  
        "time": 1744090702715  
    }  
    

[PreviousAmend Order](https://bybit-exchange.github.io/docs/v5/spread/trade/amend-order)[NextCancel All Orders](https://bybit-exchange.github.io/docs/v5/spread/trade/cancel-all)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


