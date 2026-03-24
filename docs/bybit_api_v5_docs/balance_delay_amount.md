# Get Withdrawable Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/balance/delay-amount

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Balances
  * Get Withdrawable Amount



On this page

# Get Withdrawable Amount

info

**How can partial funds be subject to delayed withdrawal requests?**

  * **On-chain deposit** : If the number of on-chain confirmations has not reached a risk-controlled level, a portion of the funds will be frozen for a period of time until they are unfrozen.
  * **Buying crypto** : If there is a risk, the funds will be frozen for a certain period of time and cannot be withdrawn.



**During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery**

### HTTP Request​

GET`/v5/asset/withdraw/withdrawable-amount`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
limitAmountUsd| string| The frozen amount due to risk, in USD  
withdrawableAmount| Object|   
> SPOT| Object| Spot wallet, it is not returned if spot wallet is removed  
>> coin| string| Coin name  
>> withdrawableAmount| string| Amount that can be withdrawn  
>> availableBalance| string| Available balance  
> FUND| Object| Funding wallet  
>> coin| string| Coin name  
>> withdrawableAmount| string| Amount that can be withdrawn  
>> availableBalance| string| Available balance  
> UTA| Object| Unified wallet  
>> coin| string| Coin name  
>> withdrawableAmount| string| Amount that can be withdrawn  
>> availableBalance| string| Available balance  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/withdraw/withdrawable-amount?coin=USDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1677565621998  
    X-BAPI-RECV-WINDOW: 50000  
    X-BAPI-SIGN: XXXXXX  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_withdrawable_amount(  
        coin="USDT",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getWithdrawableAmount({  
        coin: 'USDT',  
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
        "retMsg": "success",  
        "result": {  
            "limitAmountUsd": "595051.7",  
            "withdrawableAmount": {  
                "FUND": {  
                    "coin": "USDT",  
                    "withdrawableAmount": "155805.847",  
                    "availableBalance": "155805.847"  
                },  
                "UTA": {  
                    "coin": "USDT",  
                    "withdrawableAmount": "498751.0882",  
                    "availableBalance": "498751.0882"  
                }  
            }  
        },  
        "retExtInfo": {},  
        "time": 1754009688289  
    }  
    

[PreviousGet All Coins Balance](https://bybit-exchange.github.io/docs/v5/asset/balance/all-balance)[NextAsset Overview](https://bybit-exchange.github.io/docs/v5/asset/balance/asset-overview)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


