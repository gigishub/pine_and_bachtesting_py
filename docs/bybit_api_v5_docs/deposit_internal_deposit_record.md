# Get Internal Deposit Records (off-chain)

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/deposit/internal-deposit-record

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Deposit
  * Get Internal Deposit Records (off-chain)



On this page

# Get Internal Deposit Records (off-chain)

Query deposit records within the Bybit platform. These transactions are not on the blockchain.

Rules

  * The maximum difference between the start time and the end time is 30 days
  * Support to get deposit records by Master or Sub Member Api Key



### HTTP Request​

GET`/v5/asset/deposit/query-internal-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
txID| false| string| Internal transfer transaction ID  
startTime| false| integer| Start time (ms). Default value: 30 days before the current time  
endTime| false| integer| End time (ms). Default value: current time  
coin| false| string| Coin name: for example, BTC. Default value: all  
cursor| false| string| Cursor, used for pagination  
limit| false| integer| Number of items per page, [`1`, `50`]. Default value: 50  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
rows| array| Object  
> id| string| ID  
> type| integer| `1`: Internal deposit  
> coin| string| Deposit coin  
> amount| string| Deposit amount  
> status| integer| 

  * 1=Processing
  * 2=Success
  * 3=deposit failed

  
> address| string| Email address or phone number  
> createdTime| string| Deposit created timestamp  
> fromMemberId| string| Sender UID  
> txID| string| Internal transfer transaction ID  
> taxDepositRecordsId| string| This field is used for tax purposes by Bybit EU (Austria) users, declare tax id  
> taxStatus| integer| This field is used for tax purposes by Bybit EU (Austria) users 

  * 0: No reporting required
  * 1: Reporting pending
  * 2: Reporting completed

  
nextPageCursor| string| cursor information: used for pagination. Default value: `""`  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/internal-deposit-record)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/deposit/query-internal-record HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1682099024473  
    X-BAPI-RECV-WINDOW: 50000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_internal_deposit_records(  
        startTime=1667260800000,  
        endTime=1667347200000,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getInternalDepositRecords({  
        startTime: 1667260800000,  
        endTime: 1667347200000,  
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
            "rows": [  
                {  
                    "id": "1103",  
                    "amount": "0.1",  
                    "type": 1,  
                    "coin": "ETH",  
                    "address": "xxxx***@gmail.com",  
                    "status": 2,  
                    "createdTime": "1705393280",  
                    "fromMemberId": "118027304",  
                    "txID": "77c37e5c-d9fa-41e5-bd13-c9b59d95"，  
                    "taxDepositRecordsId": "0",  
                    "taxStatus": 0,  
                }  
            ],  
            "nextPageCursor": "eyJtaW5JRCI6MTEwMywibWF4SUQiOjExMDN9"  
        },  
        "retExtInfo": {},  
        "time": 1705395632689  
    }  
    

[PreviousGet Sub Deposit Records (on-chain)](https://bybit-exchange.github.io/docs/v5/asset/deposit/sub-deposit-record)[NextGet Master Deposit Address](https://bybit-exchange.github.io/docs/v5/asset/deposit/master-deposit-addr)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


