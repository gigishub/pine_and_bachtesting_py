# Borrow

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/borrow

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Borrow



On this page

# Borrow

> Permission: "Spot trade"

info

  * The loan funds are released to the Funding wallet.
  * The collateral funds are deducted from the Funding wallet, so make sure you have enough collateral amount in the Funding wallet.



### HTTP Request​

POST`/v5/crypto-loan/borrow`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
loanCurrency| **true**|  string| Loan coin name  
loanAmount| false| string| Amount to borrow

  * **Required** when collateral amount is not filled

  
loanTerm| false| string| Loan term 

  * flexible term: `null` or not passed
  * fixed term: `7`, `14`, `30`, `90`, `180` days

  
collateralCurrency| **true**|  string| Currency used to mortgage  
collateralAmount| false| string| Amount to mortgage

  * **Required** when loan amount is not filled

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
orderId| string| Loan order ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan/borrow HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728629356551  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 140  
      
    {  
        "loanCurrency": "USDT",  
        "loanAmount": "550",  
        "collateralCurrency": "BTC",  
        "loanTerm": null,  
        "collateralAmount": null  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.borrow_crypto_loan(  
            loanCurrency="USDT",  
            loanAmount="550",  
            collateralCurrency="BTC",  
            loanTerm=None,  
            collateralAmount=None,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .borrowCryptoLoan({  
        loanCurrency: 'USDT',  
        loanAmount: '550',  
        collateralCurrency: 'BTC',  
        loanTerm: null,  
        collateralAmount: null,  
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
            "orderId": "1794267532472646144"  
        },  
        "retExtInfo": {},  
        "time": 1728629357820  
    }  
    

[PreviousCancel Redeem](https://bybit-exchange.github.io/docs/v5/abandon/cancel-redeem)[NextGet Broker Earning](https://bybit-exchange.github.io/docs/v5/abandon/earning)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


