# Adjust Collateral Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/crypto-loan/adjust-collateral

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (legacy)
  * Adjust Collateral Amount



On this page

# Adjust Collateral Amount

You can increase or reduce your collateral amount. When you reduce, please obey the [max. allowed reduction amount](https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt).

> Permission: "Spot trade"

info

  * The adjusted collateral amount will be returned to or deducted from the Funding wallet.



### HTTP Request​

POST`/v5/crypto-loan/adjust-ltv`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| **true**|  string| Loan order ID  
amount| **true**|  string| Adjustment amount  
direction| **true**|  string| `0`: add collateral; `1`: reduce collateral  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
adjustId| string| Collateral adjustment transaction ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan/adjust-ltv HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728635421137  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 85  
      
    {  
        "orderId": "1794267532472646144",  
        "amount": "0.001",  
        "direction": "1"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.adjust_collateral_amount(  
        orderId="1794267532472646144",  
        amount="0.001",  
        direction="1",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .adjustCollateralAmount({  
        orderId: '1794267532472646144',  
        amount: '0.001',  
        direction: '1',  
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
        "retMsg": "request.success",  
        "result": {  
            "adjustId": "1794318409405331968"  
        },  
        "retExtInfo": {},  
        "time": 1728635422833  
    }  
    

[PreviousGet Max. Allowed Collateral Reduction Amount](https://bybit-exchange.github.io/docs/v5/crypto-loan/reduce-max-collateral-amt)[NextGet Loan LTV Adjustment History](https://bybit-exchange.github.io/docs/v5/crypto-loan/ltv-adjust-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


