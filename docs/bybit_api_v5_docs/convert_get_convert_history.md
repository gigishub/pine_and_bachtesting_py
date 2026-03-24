# Get Convert History

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-history

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert
  * Get Convert History



On this page

# Get Convert History

Returns all confirmed quotes.

info

Starting from September 10, 2025, converts executed on the webpage can also be queried via this API.

### HTTP Request​

GET`/v5/asset/exchange/query-convert-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#convertaccounttype)| false| string| Wallet type   
`eb_convert_funding`: funding wallet convert records via API  
`eb_convert_uta`: uta wallet convert records via API  
`funding`: normal crypto convert via web/app  
`funding_fiat`: fiat crypto convert via web/app  
`funding_fbtc_convert`: FBTC to BTC convert via web/app  
`funding_block_trade`: block trade convert via web/app 

  * Supports passing multiple types, separated by comma e.g., `eb_convert_funding,eb_convert_uta`
  * Return all wallet types data if not passed

  
index| false| integer| Page number 
* started from 1
* 1st page by default  
limit| false| integer| Page size 
* 20 records by default
* up to 100 records, return 100 when exceeds 100  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array<object>| Array of quotes  
> [accountType](https://bybit-exchange.github.io/docs/v5/enum#convertaccounttype)| string| Wallet type  
`eb_convert_funding`: funding wallet convert records via API  
`eb_convert_uta`: uta wallet convert records via API  
`funding`: normal crypto convert via web/app  
`funding_fiat`: fiat crypto convert via web/app  
`funding_fbtc_convert`: FBTC to BTC convert via web/app  
`funding_block_trade`: block trade convert via web/app  
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

  
> extInfo| object|   
>> paramType| string| This field is published when you send it in the [Request a Quote ](https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote)  
>> paramValue| string| This field is published when you send it in the [Request a Quote ](https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote)  
> convertRate| string| Exchange rate  
> createdAt| string| Quote created time  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/exchange/query-convert-history?accountType=eb_convert_uta,eb_convert_funding HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720074159814  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_convert_history(  
        accountType="eb_convert_uta,eb_convert_funding",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getConvertHistory()  
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
            "list": [  
                {  
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
                    "extInfo": {  
                        "paramType": "opFrom",  
                        "paramValue": "broker-id-001"  
                    },  
                    "convertRate": "0.0534882723991",  
                    "createdAt": "1720071899995"  
                },  
                {  
                    "accountType": "eb_convert_uta",  
                    "exchangeTxId": "23070eb_convert_uta408933875189391360",  
                    "userId": "XXXXX",  
                    "fromCoin": "BTC",  
                    "fromCoinType": "crypto",  
                    "fromAmount": "0.1",  
                    "toCoin": "ETH",  
                    "toCoinType": "crypto",  
                    "toAmount": "1.773938248611074",  
                    "exchangeStatus": "success",  
                    "extInfo": {},  
                    "convertRate": "17.73938248611074",  
                    "createdAt": "1719974243256"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1720074457715  
    }  
    

[PreviousGet Convert Status](https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result)[NextGet Small Balance Coins](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/small-balanc-coins)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


