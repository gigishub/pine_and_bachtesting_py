# Repay

> **Source:** https://bybit-exchange.github.io/docs/v5/crypto-loan/repay

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (legacy)
  * Repay



On this page

# Repay

Fully or partially repay a loan. If interest is due, that is paid off first, with the loaned amount being paid off only after due interest.

> Permission: "Spot trade"

info

  * The repaid amount will be deducted from the Funding wallet.
  * The collateral amount will not be auto returned when you don't fully repay the debt, but you can also adjust collateral amount



### HTTP Request​

POST`/v5/crypto-loan/repay`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| **true**|  string| Loan order ID  
amount| **true**|  string| Repay amount  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
repayId| string| Repayment transaction ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan/repay HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728629785224  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 61  
      
    {  
        "orderId": "1794267532472646144",  
        "amount": "100"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.repay_crypto_loan(  
            orderId="1794267532472646144",  
            amount="100",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .repayCryptoLoan({  
        orderId: '1794267532472646144',  
        amount: '100',  
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
            "repayId": "1794271131730737664"  
        },  
        "retExtInfo": {},  
        "time": 1728629786884  
    }  
    

[PreviousGet Account Borrowable/Collateralizable Limit](https://bybit-exchange.github.io/docs/v5/crypto-loan/acct-borrow-collateral)[NextGet Unpaid Loans](https://bybit-exchange.github.io/docs/v5/crypto-loan/unpaid-loan-order)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


