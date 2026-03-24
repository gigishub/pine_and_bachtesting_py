# Issue Voucher

> **Source:** https://bybit-exchange.github.io/docs/v5/broker/reward/issue-voucher

---

  * [](https://bybit-exchange.github.io/docs/)
  * Broker
  * Exchange Broker
  * Reward
  * Issue Voucher



On this page

# Issue Voucher

### HTTP Request​

POST`/v5/broker/award/distribute-award`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
accountId| **true**|  string| User ID  
awardId| **true**|  string| Voucher ID  
specCode| **true**|  string| Customised unique spec code, up to 8 characters  
amount| **true**|  string| Issue amount 

  * Spot airdrop supports up to 16 decimals
  * Other types supports up to 4 decimals

  
brokerId| **true**|  string| Broker ID  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/broker/award/distribute-award HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1726110531734  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 128  
      
    {  
        "accountId": "2846381",  
        "awardId": "123456",  
        "specCode": "award-001",  
        "amount": "100",  
        "brokerId": "v-28478"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.issue_voucher(  
        accountId="2846381",  
        awardId="123456",  
        specCode="award-001",  
        amount="100",  
        brokerId="v-28478",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .issueBrokerVoucher({  
        accountId: '2846381',  
        awardId: '123456',  
        specCode: 'award-001',  
        amount: '100',  
        brokerId: 'v-28478',  
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
        "retMsg": ""  
    }  
    

[PreviousGet Voucher Spec](https://bybit-exchange.github.io/docs/v5/broker/reward/voucher)[NextGet Issued Voucher](https://bybit-exchange.github.io/docs/v5/broker/reward/get-issue-voucher)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


