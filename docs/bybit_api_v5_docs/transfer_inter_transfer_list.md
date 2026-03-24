# Get Internal Transfer Records

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/transfer/inter-transfer-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Transfer
  * Get Internal Transfer Records



On this page

# Get Internal Transfer Records

Query the internal transfer records between different [account types](https://bybit-exchange.github.io/docs/v5/enum#accounttype) under the same UID.

info

  * If startTime and endTime are not provided, the API returns data from the past 7 days by default.
  * If only startTime is provided, the API returns records from startTime to startTime + 7 days.
  * If only endTime is provided, the API returns records from endTime - 7 days to endTime.
  * If both are provided, the maximum allowed range is 7 days (endTime - startTime ≤ 7 days).



### HTTP Request​

GET`/v5/asset/transfer/query-inter-transfer-list`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
transferId| false| string| UUID. Use the one you generated in [createTransfer](https://bybit-exchange.github.io/docs/v5/asset/transfer/create-inter-transfer#response-parameters)  
coin| false| string| Coin, uppercase only  
[status](https://bybit-exchange.github.io/docs/v5/enum#transferstatus)| false| string| Transfer status  
startTime| false| integer| The start timestamp (ms) _Note: the query logic is actually effective based on**second** level_  
endTime| false| integer| The end timestamp (ms) _Note: the query logic is actually effective based on**second** level_  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> transferId| string| Transfer ID  
> coin| string| Transferred coin  
> amount| string| Transferred amount  
> [fromAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| string| From account type  
> [toAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| string| To account type  
> timestamp| string| Transfer created timestamp (ms)  
> [status](https://bybit-exchange.github.io/docs/v5/enum#transferstatus)| string| Transfer status  
nextPageCursor| string| Refer to the `cursor` request parameter  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/inter-transfer-list)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/inter-transfer-list-query?coin=USDT&limit=1 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1670988271299  
    X-BAPI-RECV-WINDOW: 50000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_internal_transfer_records(  
        coin="USDT",  
        limit=1,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getInternalTransferRecords({  
        coin: 'USDT',  
        limit: 1,  
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
        "retMsg": "success",  
        "result": {  
        "list": [  
            {  
                "transferId": "selfTransfer_a1091cc7-9364-4b74-8de1-18f02c6f2d5c",  
                "coin": "USDT",  
                "amount": "5000",  
                "fromAccountType": "SPOT",  
                "toAccountType": "UNIFIED",  
                "timestamp": "1667283263000",  
                "status": "SUCCESS"  
            }  
        ],  
        "nextPageCursor": "eyJtaW5JRCI6MTM1ODQ2OCwibWF4SUQiOjEzNTg0Njh9"  
    },  
        "retExtInfo": {},  
        "time": 1670988271677  
    }  
    

[PreviousCreate Internal Transfer](https://bybit-exchange.github.io/docs/v5/asset/transfer/create-inter-transfer)[NextCreate Universal Transfer](https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


