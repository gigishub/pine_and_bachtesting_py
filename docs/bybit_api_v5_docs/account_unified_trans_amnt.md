# Get Transferable Amount (Unified)

> **Source:** https://bybit-exchange.github.io/docs/v5/account/unified-trans-amnt

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Transferable Amount (Unified)



On this page

# Get Transferable Amount (Unified)

Query the available amount to transfer of a specific coin in the Unified wallet.

info

Formula of Asset Available Balance for withdraw: 

  1. Reverse calculate Asset Available Amount = X, using `totalAvailableBalance` in [Get Wallet Balance](https://bybit-exchange.github.io/docs/v5/account/wallet-balance) and the asset's tiered collateral ratio   

  2. Asset Available Balance for withdraw = min(X, asset withdraw Available balance)


  * under Cross marin mode: asset withdraw Available balance = asset wallet balance + min(unrealised pnl,0) + asset reservation - frozen + negative option value - bonus - Positive Option OrderIM + orderloss   

  * under Portfolio margin mode: asset withdraw Available balance = asset wallet balance + min(unrealised pnl,0) + asset reservation - frozen - max(bonus, Pm spot Hedged Balance) + orderloss + min(optionValue,0)   



  3. During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/account/withdrawal`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coinName| **true**|  string| Coin name, uppercase only. Supports up to 20 coins per request, use comma to separate. `BTC,USDC,USDT,SOL`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
availableWithdrawal| string| Transferable amount for the 1st coin in the request  
availableWithdrawalMap| Object| Transferable amount map for each requested coin. In the map, key is the requested coin, and value is the accordingly amount(string)  
e.g., "availableWithdrawalMap":{"BTC":"4.54549050","SOL":"33.16713007","XRP":"10805.54548970","ETH":"17.76451865"}  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/withdrawal?coinName=BTC,SOL,ETH,XRP HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1739861239242  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "availableWithdrawal": "4.54549050",  
            "availableWithdrawalMap": {  
                "BTC": "4.54549050",  
                "SOL": "33.16713007",  
                "XRP": "10805.54548970",  
                "ETH": "17.76451865"  
            }  
        },  
        "retExtInfo": {},  
        "time": 1739858984601  
    }  
    

[PreviousGet Wallet Balance](https://bybit-exchange.github.io/docs/v5/account/wallet-balance)[NextGet Transaction Log (UTA)](https://bybit-exchange.github.io/docs/v5/account/transaction-log)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


