# Get Auto Repay Mode

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/get-auto-repay-mode

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Auto Repay Mode



On this page

# Get Auto Repay Mode

Get spot automatic repayment mode

### HTTP Request​

GET`/v5/spot-margin-trade/get-auto-repay-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| Coin name, uppercase only. If `currency` is not passed, automatic repay mode for all currencies will be returned.  
  
* * *

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
data| array| Object  
> currency| string| Coin name, uppercase only.  
> autoRepayMode| string| 

  * `1`: On
  * `0`: Off

  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/get-auto-repay-mode?currency=ETH HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672299806626  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "Success",  
        "result": {  
            "data": [  
                {  
                    "autoRepayMode": "1",  
                    "currency": "ETH"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1766977353904  
    }  
    

[PreviousSet Auto Repay Mode](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-auto-repay-mode)[NextGet Borrowable Coins](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/loan-coin)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


