# Get Coin Exchange Records

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/exchange

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Get Coin Exchange Records



On this page

# Get Coin Exchange Records

Query the coin exchange records.

info

It sometimes has 5 secs delay

### HTTP Request​

GET`/v5/asset/exchange/order-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
fromCoin| false| string| The currency to convert from, uppercase only. e.g,`BTC`  
toCoin| false| string| The currency to convert to, uppercase only. e.g,`USDT`  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `10`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
nextPageCursor| string| Refer to the `cursor` request parameter  
orderBody| array| Object  
> fromCoin| string| The currency to convert from  
> fromAmount| string| The amount to convert from  
> toCoin| string| The currency to convert to  
> toAmount| string| The amount to convert to  
> exchangeRate| string| Exchange rate  
> createdTime| string| Exchange created timestamp (sec)  
> exchangeTxId| string| Exchange transaction ID  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/exchange)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/exchange/order-record?limit=10 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672990462492  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_coin_exchange_records(  
        limit=10,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getCoinExchangeRecords({ limit: 10 })  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "orderBody": [  
                {  
                    "fromCoin": "BTC",  
                    "fromAmount": "0.100000000000000000",  
                    "toCoin": "ETH",  
                    "toAmount": "1.385866230000000000",  
                    "exchangeRate": "13.858662380000000000",  
                    "createdTime": "1672197760",  
                    "exchangeTxId": "145102533285208544812654440448"  
                }  
            ],  
            "nextPageCursor": "173341:1672197760"  
        },  
        "retExtInfo": {},  
        "time": 1672990464021  
    }  
    

[PreviousGet USDC Session Settlement (2 years)](https://bybit-exchange.github.io/docs/v5/asset/settlement)[NextGet Coin Info](https://bybit-exchange.github.io/docs/v5/asset/coin-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


