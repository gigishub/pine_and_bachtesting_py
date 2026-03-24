# Get Max. Allowed Collateral Reduction Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (legacy)
  * Get Max. Allowed Collateral Reduction Amount



On this page

# Get Max. Allowed Collateral Reduction Amount

Query for the maximum amount by which collateral may be reduced by.

> Permission: "Spot trade"

### HTTP Request​

GET`/v5/crypto-loan/max-collateral-amount`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| **true**|  string| Loan coin ID  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
maxCollateralAmount| string| Max. reduction collateral amount  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan/max-collateral-amount?orderId=1794267532472646144 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728634289933  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_max_allowed_collateral_reduction_amount(  
            orderId="1794267532472646144",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getMaxAllowedReductionCollateralAmount({ orderId: '1794267532472646144' })  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "request.success",  
        "result": {  
            "maxCollateralAmount": "0.00210611"  
        },  
        "retExtInfo": {},  
        "time": 1728634291554  
    }  
    

[PreviousGet Completed Loan History](https://bybit-exchange.github.io/docs/v5/crypto-loan/completed-loan-order)[NextAdjust Collateral Amount](https://bybit-exchange.github.io/docs/v5/crypto-loan/adjust-collateral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


