# Get Sub Account All API Keys

> **Source:** https://bybit-exchange.github.io/docs/v5/user/list-sub-apikeys

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Get Sub Account All API Keys



On this page

# Get Sub Account All API Keys

Query all api keys information of a sub UID.

tip

  * Any permission can access this endpoint
  * Only master account can call this endpoint



### HTTP Request​

GET`/v5/user/sub-apikeys`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
subMemberId| **true**|  string| Sub UID  
limit| false| integer| Limit for data size per page. [`1`, `20`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Object  
> id| string| Unique ID. Internal use  
> ips| array<string>| IP bound  
> apiKey| string| Api key  
> note| string| The remark  
> status| integer| `1`: permanent, `2`: expired, `3`: within the validity period, `4`: expires soon (less than 7 days)  
> expiredAt| datetime| The expiry day of the api key. Only for those api key with no IP bound or the password has been changed  
> createdAt| datetime| The create day of the api key  
> type| integer| The type of api key. `1`: personal, `2`: connected to the third-party app  
> permissions| Object| The types of permission  
>> ContractTrade| array| Permission of contract trade `Order`, `Position`  
>> Spot| array| Permission of spot `SpotTrade`  
>> Wallet| array| Permission of wallet `AccountTransfer`, `SubMemberTransferList`  
>> Options| array| Permission of USDC Contract. It supports trade option and USDC perpetual. `OptionsTrade`  
>> Derivatives| array| `DerivativesTrade`  
>> Exchange| array| Permission of convert `ExchangeHistory`  
>> Earn| array| Permission of earn product `Earn`  
>> Affiliate| array| Not applicable to sub account, always `[]`  
>> BlockTrade| array| Not applicable to subaccount, always `[]`  
>> NFT| array| **Deprecated** , always `[]`  
>> CopyTrading| array| **Deprecated** , always `[]`  
> secret| string| Always `"******"`  
> readOnly| boolean| `true`, `false`  
> deadlineDay| integer| The remaining valid days of api key. Only for those api key with no IP bound or the password has been changed  
> flag| string| Api key type  
nextPageCursor| string| Refer to the `cursor` request parameter  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/user/list-sub-apikeys)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/user/sub-apikeys?subMemberId=100400345 HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1699515251088  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    Content-Type: application/json  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSubAccountAllApiKeys({  
        subMemberId: 'subUID',  
        limit: 20,  
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
        "retMsg": "",  
        "result": {  
            "result": [  
                {  
                    "id": "24828209",  
                    "ips": [  
                        "*"  
                    ],  
                    "apiKey": "XXXXXX",  
                    "note": "UTA",  
                    "status": 3,  
                    "expiredAt": "2023-12-01T02:36:06Z",  
                    "createdAt": "2023-08-25T06:42:39Z",  
                    "type": 1,  
                    "permissions": {  
                        "ContractTrade": [  
                            "Order",  
                            "Position"  
                        ],  
                        "Spot": [  
                            "SpotTrade"  
                        ],  
                        "Wallet": [  
                            "AccountTransfer",  
                            "SubMemberTransferList"  
                        ],  
                        "Options": [  
                            "OptionsTrade"  
                        ],  
                        "Derivatives": [  
                            "DerivativesTrade"  
                        ],  
                        "CopyTrading": [],  
                        "BlockTrade": [],  
                        "Exchange": [  
                            "ExchangeHistory"  
                        ],  
                        "NFT": [],  
                        "Affiliate": [],  
                        "Earn": []  
                    },  
                    "secret": "******",  
                    "readOnly": false,  
                    "deadlineDay": 21,  
                    "flag": "hmac"  
                }  
            ],  
            "nextPageCursor": ""  
        },  
        "retExtInfo": {},  
        "time": 1699515251698  
    }  
    

[PreviousGet API Key Information](https://bybit-exchange.github.io/docs/v5/user/apikey-info)[NextGet UID Wallet Type](https://bybit-exchange.github.io/docs/v5/user/wallet-type)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


