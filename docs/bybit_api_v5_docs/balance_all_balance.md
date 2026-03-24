# Get All Coins Balance

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/balance/all-balance

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Balances
  * Get All Coins Balance



On this page

# Get All Coins Balance

You could get all coin balance of all account types under the master account, and sub account.

important

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/asset/transfer/query-account-coins-balance`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
memberId| false| string| User Id. It is **required** when you use master api key to check sub account coin balance  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| Account type  
coin| false| string| Coin name, uppercase only 

  * Query all coins if not passed
  * Can query multiple coins, separated by comma. `USDT,USDC,ETH`

**Note:** this field is **mandatory** for accountType=`UNIFIED`, and supports up to 10 coins each request  
withBonus| false| integer| `0`(default): not query bonus. `1`: query bonus  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| string| Account type  
memberId| string| UserID  
balance| array| Object  
> coin| string| Currency  
> walletBalance| string| Wallet balance  
> transferBalance| string| Transferable balance  
> bonus| string| Bonus  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/all-balance)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/query-account-coins-balance?accountType=FUND&coin=USDC HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675866354698  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_coins_balance(  
        accountType="FUND",  
        coin="USDC",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getAllCoinsBalance({ accountType: 'FUND', coin: 'USDC' })  
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
            "memberId": "XXXX",  
            "accountType": "FUND",  
            "balance": [  
                {  
                    "coin": "USDC",  
                    "transferBalance": "0",  
                    "walletBalance": "0",  
                    "bonus": ""  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1675866354913  
    }  
    

[PreviousGet Single Coin Balance](https://bybit-exchange.github.io/docs/v5/asset/balance/account-coin-balance)[NextGet Withdrawable Amount](https://bybit-exchange.github.io/docs/v5/asset/balance/delay-amount)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


