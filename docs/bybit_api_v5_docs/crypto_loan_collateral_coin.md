# Get Collateral Coins

> **Source:** https://bybit-exchange.github.io/docs/v5/crypto-loan/collateral-coin

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (legacy)
  * Get Collateral Coins



On this page

# Get Collateral Coins

info

Does not need authentication.

### HTTP Request​

GET`/v5/crypto-loan/collateral-data`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
vipLevel| false| string| VIP level 

  * `VIP0`, `VIP1`, `VIP2`, `VIP3`, `VIP4`, `VIP5`, `VIP99`(supreme VIP)
  * `PRO1`, `PRO2`, `PRO3`, `PRO4`, `PRO5`, `PRO6`

  
currency| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
vipCoinList| array| Object  
> list| array| Object  
>> collateralAccuracy| integer| Valid collateral coin precision  
>> initialLTV| string| The Initial LTV ratio determines the initial amount of coins that can be borrowed. The initial LTV ratio may vary for different collateral  
>> marginCallLTV| string| If the LTV ratio (Loan Amount/Collateral Amount) reaches the threshold, you will be required to add more collateral to your loan  
>> liquidationLTV| string| If the LTV ratio (Loan Amount/Collateral Amount) reaches the threshold, Bybit will liquidate your collateral assets to repay your loan and interest in full  
>> maxLimit| string| Collateral limit  
> vipLevel| string| VIP level  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan/collateral-data?currency=ETH&vipLevel=PRO1 HTTP/1.1  
    Host: api.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_collateral_coins(  
        currency="ETH",  
        vipLevel="PRO1",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getCollateralCoins({  
        currency: 'ETH',  
        vipLevel: 'PRO1',  
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
            "vipCoinList": [  
                {  
                    "list": [  
                        {  
                            "collateralAccuracy": 8,  
                            "currency": "ETH",  
                            "initialLTV": "0.8",  
                            "liquidationLTV": "0.95",  
                            "marginCallLTV": "0.87",  
                            "maxLimit": "32000"  
                        }  
                    ],  
                    "vipLevel": "PRO1"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1728618590498  
    }  
    

[PreviousGet Repayment History](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-history)[NextGet Borrowable Coins](https://bybit-exchange.github.io/docs/v5/crypto-loan/loan-coin)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


