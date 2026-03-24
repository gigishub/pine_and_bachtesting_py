# Get Convert Status

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert
  * Get Convert Status



On this page

# Get Convert Status

You can query the exchange result by sending quoteTxId.

### HTTP Request​

GET`/v5/asset/exchange/convert-result-query`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
quoteTxId| **true**|  string| Quote tx ID  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#convertaccounttype)| **true**|  string| Wallet type  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object|   
> [accountType](https://bybit-exchange.github.io/docs/v5/enum#convertaccounttype)| string| Wallet type  
> exchangeTxId| string| Exchange tx ID, same as quote tx ID  
> userId| string| User ID  
> fromCoin| string| From coin  
> fromCoinType| string| From coin type. `crypto`  
> toCoin| string| To coin  
> toCoinType| string| To coin type. `crypto`  
> fromAmount| string| From coin amount (amount to sell)  
> toAmount| string| To coin amount (amount to buy according to exchange rate)  
> exchangeStatus| string| Exchange status 

  * init
  * processing
  * success
  * failure

  
> extInfo| object| Reserved field, ignored for now  
> convertRate| string| Exchange rate  
> createdAt| string| Quote created time  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/exchange/convert-result-query?quoteTxId=10100108106409343501030232064&accountType=eb_convert_funding HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720073659847  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_convert_status(  
        accountType="eb_convert_funding",  
        quoteTxId="10100108106409343501030232064",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getConvertStatus({  
        quoteTxId: 'quoteTransactionId',  
        accountType: 'eb_convert_funding',  
      })  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "result": {  
                "accountType": "eb_convert_funding",  
                "exchangeTxId": "10100108106409343501030232064",  
                "userId": "XXXXX",  
                "fromCoin": "ETH",  
                "fromCoinType": "crypto",  
                "fromAmount": "0.1",  
                "toCoin": "BTC",  
                "toCoinType": "crypto",  
                "toAmount": "0.00534882723991",  
                "exchangeStatus": "success",  
                "extInfo": {},  
                "convertRate": "0.0534882723991",  
                "createdAt": "1720071899995"  
            }  
        },  
        "retExtInfo": {},  
        "time": 1720073660696  
    }  
    

[PreviousConfirm a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert/confirm-quote)[NextGet Convert History](https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


