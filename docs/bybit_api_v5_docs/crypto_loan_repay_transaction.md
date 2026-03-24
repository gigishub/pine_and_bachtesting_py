# Get Loan Repayment History

> **Source:** https://bybit-exchange.github.io/docs/v5/crypto-loan/repay-transaction

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (legacy)
  * Get Loan Repayment History



On this page

# Get Loan Repayment History

Query for loan repayment transactions. A loan may be repaid in multiple repayments.

> Permission: "Spot trade"

info

  * Supports querying for the last 6 months worth of completed loan orders.
  * Only successful repayments can be queried for.



### HTTP Request​

GET`/v5/crypto-loan/repayment-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| false| string| Loan order ID  
repayId| false| string| Repayment tranaction ID  
loanCurrency| false| string| Loan coin name  
limit| false| string| Limit for data size per page. [`1`, `100`]. Default: `10`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> collateralCurrency| string| Collateral coin  
> collateralReturn| string| Amount of collateral returned as a result of this repayment. `"0"` if this isn't the final loan repayment  
> loanCurrency| string| Loan coin  
> loanTerm| string| Loan term, `7`, `14`, `30`, `90`, `180` days, keep `""` for flexible loan  
> orderId| string| Loan order ID  
> repayAmount| string| Repayment amount  
> repayId| string| Repayment transaction ID  
> repayStatus| integer| Repayment status, `1`: success; `2`: processing  
> repayTime| string| Repay timestamp  
> repayType| string| Repayment type, `1`: repay by user; `2`: repay by liquidation  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan/repayment-history?repayId=1794271131730737664 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728633716794  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_loan_repayment_history(  
            repayId="1794271131730737664",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getRepaymentHistory({ repayId: '1794271131730737664' })  
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
            "list": [  
                {  
                    "collateralCurrency": "BTC",  
                    "collateralReturn": "0",  
                    "loanCurrency": "USDT",  
                    "loanTerm": "",  
                    "orderId": "1794267532472646144",  
                    "repayAmount": "100",  
                    "repayId": "1794271131730737664",  
                    "repayStatus": 1,  
                    "repayTime": "1728629786875",  
                    "repayType": "1"  
                }  
            ],  
            "nextPageCursor": ""  
        },  
        "retExtInfo": {},  
        "time": 1728633717935  
    }  
    

[PreviousGet Unpaid Loans](https://bybit-exchange.github.io/docs/v5/crypto-loan/unpaid-loan-order)[NextGet Completed Loan History](https://bybit-exchange.github.io/docs/v5/crypto-loan/completed-loan-order)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


