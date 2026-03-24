# Get Margin Coin Info

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/margin-coin-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Margin Coin Info



On this page

# Get Margin Coin Info

### HTTP Request​

GET`/v5/ins-loan/ensure-tokens`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
productId| false| string| ProductId. If not passed, then return all product margin coin. For spot, it returns coin that convertRation greater than 0.  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
marginToken| array| Object  
> productId| string| Product Id  
> spotToken| array| Spot margin coin  
>> token| string| Margin coin  
>> convertRatio| string| Margin coin convert ratio  
> contractToken| array| Contract margin coin  
>> token| string| Margin coin  
>> convertRatio| string| Margin coin convert ratio  
  
### Request Example​
    
    
    GET /v5/ins-loan/ensure-tokens?productId=70 HTTP/1.1  
    Host: api-testnet.bybit.com  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "marginToken": [  
                {  
                    "productId": "70",  
                    "spotToken": [  
                        {  
                            "token": "BTC",  
                            "convertRatio": "1.00000000"  
                        },  
                        {  
                            "token": "ETH",  
                            "convertRatio": "1.00000000"  
                        },  
                        {  
                            "token": "USDT",  
                            "convertRatio": "1"  
                        }  
                    ],  
                    "contractToken": [  
                        {  
                            "token": "USDT",  
                            "convertRatio": "1"  
                        }  
                    ]  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1669363954802  
    }  
    

[PreviousDeposit Funds](https://bybit-exchange.github.io/docs/v5/abandon/deposit)[NextEnable Universal Transfer for Sub UID](https://bybit-exchange.github.io/docs/v5/abandon/enable-unitransfer-subuid)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


