# Get DCP Info

> **Source:** https://bybit-exchange.github.io/docs/v5/account/dcp-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get DCP Info



On this page

# Get DCP Info

Query the DCP configuration of the account. Before calling the interface, please make sure you have applied for the UTA account DCP configuration with your account manager

  * Only the configured main / sub account can query information from this API. Calling this API by an account always returns empty.

  * If you only request to activate Spot trading for DCP, the contract and options data will not be returned.




info

  * Support USDT Perpetuals, USDT Futures, USDC Perpetuals, USDC Futures, Inverse Perpetuals, Inverse Futures [DERIVATIVES]  
Spot [SPOT]  
Options [OPTIONS]



### HTTP Request​

GET`/v5/account/query-dcp-info`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
dcpInfos| array<object>| DCP config for each product  
> product| string| `SPOT`, `DERIVATIVES`, `OPTIONS`  
> dcpStatus| string| [Disconnected-CancelAll-Prevention](https://bybit-exchange.github.io/docs/v5/order/dcp) status: `ON`  
> timeWindow| string| DCP trigger time window which user pre-set. Between [3, 300] seconds, default: 10 sec  
  
### Request Example​

  * HTTP
  * Node.js


    
    
    GET /v5/account/query-dcp-info HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1717065530867  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getDCPInfo()  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    // it means my account enables Spot and Deriviatvies on the backend  
    // Options is not enabled with DCP  
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "dcpInfos": [  
                {  
                    "product": "SPOT",  
                    "dcpStatus": "ON",  
                    "timeWindow": "10"  
                },  
                {  
                    "product": "DERIVATIVES",  
                    "dcpStatus": "ON",  
                    "timeWindow": "10"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1717065531697  
    }  
    

[PreviousGet Collateral Info](https://bybit-exchange.github.io/docs/v5/account/collateral-info)[NextSet Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/set-collateral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


