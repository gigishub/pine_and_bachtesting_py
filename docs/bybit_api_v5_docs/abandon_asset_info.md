# Get Asset Info

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/asset-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Asset Info (Spot)



On this page

# Get Asset Info

Query Spot asset information

> Apply to: classic account

### HTTP Request​

GET`/v5/asset/transfer/query-asset-info`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| Account type. `SPOT`  
coin| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
spot| Object|   
> status| string| account status. `ACCOUNT_STATUS_NORMAL`: normal, `ACCOUNT_STATUS_UNSPECIFIED`: banned  
> assets| array| Object  
>> coin| string| Coin  
>> frozen| string| Freeze amount  
>> free| string| Free balance  
>> withdraw| string| Amount in withdrawing  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/asset-info)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/query-asset-info?accountType=SPOT&coin=ETH HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672136538042  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_spot_asset_info(  
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
      .getAssetInfo({ accountType: 'FUND', coin: 'USDC' })  
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
            "spot": {  
                "status": "ACCOUNT_STATUS_NORMAL",  
                "assets": [  
                    {  
                        "coin": "ETH",  
                        "frozen": "0",  
                        "free": "11.53485",  
                        "withdraw": ""  
                    }  
                ]  
            }  
        },  
        "retExtInfo": {},  
        "time": 1672136539127  
    }  
    

[PreviousError Codes](https://bybit-exchange.github.io/docs/v5/error)[NextGet Lending Coin Info](https://bybit-exchange.github.io/docs/v5/abandon/coin-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


