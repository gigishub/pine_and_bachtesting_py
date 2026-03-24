# Get Purchase/Redemption Records

> **Source:** https://bybit-exchange.github.io/docs/v5/lt/order-record

---

On this page

# Get Purchase/Redemption Records

Get purchase or redeem history

### HTTP Request​

GET`/v5/spot-lever-token/order-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
ltCoin| false| string| Abbreviation of the LT, such as BTC3L  
orderId| false| string| Order ID  
startTime| false| integer| The start timestamp (ms)  
endTime| false| integer| The end timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `500`]. Default: `100`  
ltOrderType| false| integer| LT order type. `1`: purchase, `2`: redemption  
serialNo| false| string| Serial number  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> ltCoin| string| Abbreviation of the LT, such as BTC3L  
> orderId| string| Order ID  
> ltOrderType| integer| LT order type. `1`: purchase, `2`: redeem  
> orderTime| number| Order time  
> updateTime| number| Last update time of the order status  
> ltOrderStatus| string| Order status. `1`: completed, `2`: in progress, `3`: failed  
> fee| string| Trading fees  
> amount| string| Order quantity of the LT  
> value| string| Filled value  
> valueCoin| string| Quote coin  
> serialNo| string| Serial number  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/spot-lever-token/order-record?orderId=2611 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672294422027  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_purchase_redemption_records(  
        orderId=2611  
    ))  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "list": [  
                {  
                    "amount": "222.90757477",  
                    "fee": "0",  
                    "ltCoin": "EOS3L",  
                    "ltOrderStatus": "1",  
                    "ltOrderType": "1",  
                    "orderId": "2611",  
                    "orderTime": "1672737465000",  
                    "serialNo": "pruchase-002",  
                    "updateTime": "1672737478000",  
                    "value": "95.13860435",  
                    "valueCoin": "USDT"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672294446137  
    }  
    

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


