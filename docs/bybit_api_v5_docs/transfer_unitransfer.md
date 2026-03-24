# Create Universal Transfer

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Transfer
  * Create Universal Transfer



On this page

# Create Universal Transfer

Transfer between sub-sub or main-sub.

tip

  * Use master or sub acct api key to request 
    * To use sub acct api key, it must have "SubMemberTransferList" permission
    * When use sub acct api key, it can only transfer to main account
  * If you encounter errorCode: `131228` and msg: `your balance is not enough`, please go to [Get Single Coin Balance](https://bybit-exchange.github.io/docs/v5/asset/balance/account-coin-balance) to check transfer safe amount.
  * You can not transfer between the same UID.



### HTTP Request​

POST`/v5/asset/transfer/universal-transfer`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
transferId| **true**|  string| [UUID](https://www.uuidgenerator.net/dev-corner). Please manually generate a UUID  
coin| **true**|  string| Coin, uppercase only  
amount| **true**|  string| Amount  
fromMemberId| **true**|  integer| From UID  
toMemberId| **true**|  integer| To UID  
[fromAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| From account type  
[toAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| To account type  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
transferId| string| UUID  
status| string| Transfer status 

  * `STATUS_UNKNOWN`
  * `SUCCESS`
  * `PENDING`
  * `FAILED`

  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/unitransfer)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/asset/transfer/universal-transfer HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672189449697  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXX  
    Content-Type: application/json  
      
    {  
        "transferId": "be7a2462-1138-4e27-80b1-62653f24925e",  
        "coin": "ETH",  
        "amount": "0.5",  
        "fromMemberId": 592334,  
        "toMemberId": 691355,  
        "fromAccountType": "CONTRACT",  
        "toAccountType": "UNIFIED"  
      
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.create_universal_transfer(  
        transferId="be7a2462-1138-4e27-80b1-62653f24925e",  
        coin="ETH",  
        amount="0.5",  
        fromMemberId=592334,  
        toMemberId=691355,  
        fromAccountType="CONTRACT",  
        toAccountType="UNIFIED",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .createUniversalTransfer({  
        transferId: 'be7a2462-1138-4e27-80b1-62653f24925e',  
        coin: 'ETH',  
        amount: '0.5',  
        fromMemberId: 592334,  
        toMemberId: 691355,  
        fromAccountType: 'CONTRACT',  
        toAccountType: 'UNIFIED',  
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
            "transferId": "be7a2462-1138-4e27-80b1-62653f24925e",  
            "status": "SUCCESS"  
        },  
        "retExtInfo": {},  
        "time": 1672189450195  
    }  
    

[PreviousGet Internal Transfer Records](https://bybit-exchange.github.io/docs/v5/asset/transfer/inter-transfer-list)[NextGet Universal Transfer Records](https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


