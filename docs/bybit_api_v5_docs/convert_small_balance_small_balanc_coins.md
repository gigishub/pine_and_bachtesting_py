# Get Small Balance Coins

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/small-balanc-coins

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert Small Balances
  * Get Small Balance Coins



On this page

# Get Small Balance Coins

Query small-balance coins with a USDT equivalent of less than 10 USDT, and ensure that the total amount for each conversion transaction is between 1.0e-8 and 200 USDT.

info

  * API key permission: `Convert`
  * API rate limit: `10 req /s`



### HTTP Request​

GET`/v5/asset/covert/small-balance-list`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
accountType| **true**|  string| Wallet type `eb_convert_uta`. Only supports the Unified wallet  
fromCoin| false| string| Source currency  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
smallAssetCoins| array<object>| Small balance info  
> fromCoin| string| Source currency  
> supportConvert| integer| `1`: support, `2`: not supported  
> availableBalance| string| Available balance, the value might be bigger than the actual balance you can convert  
> baseValue| string| USDT equivalent value  
> toAmount| string| **Ignore** , reserved field  
> exchangeRate| string| **Ignore** , reserved field  
> feeInfo| null| **Ignore** , reserved field  
> taxFeeInfo| null| **Ignore** , reserved field  
supportToCoins| array| `["MNT","USDT","USDC"]`  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/covert/small-balance-list?fromCoin=XRP&accountType=eb_convert_uta HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1766125546001  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_small_balance_coins(  
        fromCoin="XRP",  
        accountType="eb_convert_uta",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "smallAssetCoins": [  
                {  
                    "fromCoin": "XRP",  
                    "supportConvert": 1,  
                    "availableBalance": "0.0002",  
                    "baseValue": "0.00036554008",  
                    "toCoin": "",  
                    "toAmount": "",  
                    "exchangeRate": "",  
                    "feeInfo": null,  
                    "taxFeeInfo": null  
                }  
            ],  
            "supportToCoins": [  
                "MNT",  
                "USDT",  
                "USDC"  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1766125546274  
    }  
    

[PreviousGet Convert History](https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-history)[NextRequest a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/request-quote)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


