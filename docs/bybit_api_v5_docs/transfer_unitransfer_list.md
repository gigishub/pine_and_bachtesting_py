# Get Universal Transfer Records

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Transfer
  * Get Universal Transfer Records



On this page

# Get Universal Transfer Records

Query universal transfer records

tip

  * Main acct api key or Sub acct api key are both supported
  * Main acct api key needs "SubMemberTransfer" permission
  * Sub acct api key needs "SubMemberTransferList" permission



info

  * If startTime and endTime are not provided, the API returns data from the past 7 days by default.
  * If only startTime is provided, the API returns records from startTime to startTime + 7 days.
  * If only endTime is provided, the API returns records from endTime - 7 days to endTime.
  * If both are provided, the maximum allowed range is 7 days (endTime - startTime ≤ 7 days).



### HTTP Request​

GET`/v5/asset/transfer/query-universal-transfer-list`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
transferId| false| string| UUID. Use the one you generated in [createTransfer](https://bybit-exchange.github.io/docs/v5/asset/transfer/create-inter-transfer#response-parameters)  
coin| false| string| Coin, uppercase only  
[status](https://bybit-exchange.github.io/docs/v5/enum#transferstatus)| false| string| Transfer status. `SUCCESS`,`FAILED`,`PENDING`  
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
> fromMemberId| string| From UID  
> toMemberId| string| TO UID  
> fromAccountType| string| From account type  
> toAccountType| string| To account type  
> timestamp| string| Transfer created timestamp (ms)  
> [status](https://bybit-exchange.github.io/docs/v5/enum#transferstatus)| string| Transfer status  
nextPageCursor| string| Refer to the `cursor` request parameter  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/unitransfer-list)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/query-universal-transfer-list?limit=1&cursor=eyJtaW5JRCI6MTc5NjU3OCwibWF4SUQiOjE3OTY1Nzh9 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN-TYPE: 2  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672190762800  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_universal_transfer_records(  
        limit=1,  
        cursor="eyJtaW5JRCI6MTc5NjU3OCwibWF4SUQiOjE3OTY1Nzh9",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getUniversalTransferRecords({  
        limit: 1,  
        cursor: 'eyJtaW5JRCI6MTc5NjU3OCwibWF4SUQiOjE3OTY1Nzh9',  
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
                    "transferId": "universalTransfer_4c3cfe2f-85cb-11ed-ac09-9e37823c81cd_533285",  
                    "coin": "USDC",  
                    "amount": "1000",  
                    "timestamp": "1672134373000",  
                    "status": "SUCCESS",  
                    "fromAccountType": "UNIFIED",  
                    "toAccountType": "UNIFIED",  
                    "fromMemberId": "533285",  
                    "toMemberId": "592324"  
                }  
            ],  
            "nextPageCursor": "eyJtaW5JRCI6MTc4OTYwNSwibWF4SUQiOjE3ODk2MDV9"  
        },  
        "retExtInfo": {},  
        "time": 1672190763079  
    }  
    

[PreviousCreate Universal Transfer](https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer)[NextGet Transferable Coin](https://bybit-exchange.github.io/docs/v5/asset/transfer/transferable-coin)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


