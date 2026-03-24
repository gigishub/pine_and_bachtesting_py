# Get Issued Voucher

> **Source:** https://bybit-exchange.github.io/docs/v5/broker/reward/get-issue-voucher

---

  * [](https://bybit-exchange.github.io/docs/)
  * Broker
  * Exchange Broker
  * Reward
  * Get Issued Voucher



On this page

# Get Issued Voucher

### HTTP Request​

POST`/v5/broker/award/distribution-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
accountId| **true**|  string| User ID  
awardId| **true**|  string| Voucher ID  
specCode| **true**|  string| Customised unique spec code, up to 8 characters  
withUsedAmount| false| boolean| Whether or not to return the amount used by the user 

  * `true`
  * `false` (default)

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
accountId| string| User ID  
awardId| string| Voucher ID  
specCode| string| Spec code  
amount| string| Amount of voucher  
isClaimed| boolean| `true`, `false`  
startAt| string| Claim start timestamp (sec)  
endAt| string| Claim end timestamp (sec)  
effectiveAt| string| Voucher effective timestamp (sec) after claimed  
ineffectiveAt| string| Voucher inactive timestamp (sec) after claimed  
usedAmount| string| Amount used by the user  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/broker/award/distribution-record HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1726112099846  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 111  
      
    {  
        "accountId": "5714139",  
        "awardId": "189528",  
        "specCode": "demo000",  
        "withUsedAmount": false  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_issued_voucher(  
        id="80209",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getBrokerIssuedVoucher({  
        id: '80209',  
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
            "accountId": "5714139",  
            "awardId": "189528",  
            "specCode": "demo000",  
            "amount": "1",  
            "isClaimed": true,  
            "startAt": "1725926400",  
            "endAt": "1733788800",  
            "effectiveAt": "1726531200",  
            "ineffectiveAt": "1733817600",  
            "usedAmount": "",  
        }  
    }  
    

[PreviousIssue Voucher](https://bybit-exchange.github.io/docs/v5/broker/reward/issue-voucher)[NextGet Product Info](https://bybit-exchange.github.io/docs/v5/earn/product-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


