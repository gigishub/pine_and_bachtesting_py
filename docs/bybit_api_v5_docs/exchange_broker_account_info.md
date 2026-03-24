# Get Account Info

> **Source:** https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/account-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Broker
  * Exchange Broker
  * Get Account Info



On this page

# Get Account Info

info

  * Use exchange broker master account to query



> API rate limit: 10 req / sec

### HTTP Request​

GET`/v5/broker/account-info`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subAcctQty| string| The qty of sub account has been created  
maxSubAcctQty| string| The max limit of sub account can be created  
baseFeeRebateRate| Object| Rebate percentage of the base fee  
> spot| string| Rebate percentage of the base fee for spot, e.g., 10.00%  
> derivatives| string| Rebate percentage of the base fee for derivatives, e.g., 10.00%  
markupFeeRebateRate| Object| Rebate percentage of the mark up fee  
> spot| string| Rebate percentage of the mark up fee for spot, e.g., 10.00%  
> derivatives| string| Rebate percentage of the mark up fee for derivatives, e.g., 10.00%  
> convert| string| Rebate percentage of the mark up fee for convert, e.g., 10.00%  
ts| string| System timestamp (ms)  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/broker/account-info HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1701399431920  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_exchange_broker_account_info())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getExchangeBrokerAccountInfo()  
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
            "subAcctQty": "2",  
            "maxSubAcctQty": "20",  
            "baseFeeRebateRate": {  
                "spot": "10.0%",  
                "derivatives": "10.0%"  
            },  
            "markupFeeRebateRate": {  
                "spot": "6.00%",  
                "derivatives": "9.00%",  
                "convert": "3.00%",  
            },  
            "ts": "1701395633402"  
        },  
        "retExtInfo": {},  
        "time": 1701395633403  
    }  
    

[PreviousGet Earning](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/exchange-earning)[NextGet Sub Account Deposit Records](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/sub-deposit-record)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


