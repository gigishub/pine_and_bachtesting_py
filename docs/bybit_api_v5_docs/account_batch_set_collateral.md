# Batch Set Collateral Coin

> **Source:** https://bybit-exchange.github.io/docs/v5/account/batch-set-collateral

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Batch Set Collateral Coin



On this page

# Batch Set Collateral Coin

### HTTP Request​

POST`/v5/account/set-collateral-switch-batch`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
request| **true**|  array| Object  
> coin| **true**|  string| Coin name, uppercase only 

  * You can get collateral coin from [here](https://bybit-exchange.github.io/docs/v5/account/collateral-info)
  * USDT, USDC cannot be set

  
> collateralSwitch| **true**|  string| `ON`: switch on collateral, `OFF`: switch off collateral  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| Object|   
> list| array| Object  
>> coin| string| Coin name  
>> collateralSwitch| string| `ON`: switch on collateral, `OFF`: switch off collateral  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-collateral-switch-batch HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1704782042755  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 371  
      
    {  
        "request": [  
            {  
                "coin": "MATIC",  
                "collateralSwitch": "OFF"  
            },  
            {  
                "coin": "BTC",  
                "collateralSwitch": "OFF"  
            },  
            {  
                "coin": "ETH",  
                "collateralSwitch": "OFF"  
            },  
            {  
                "coin": "SOL",  
                "collateralSwitch": "OFF"  
            }  
        ]  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.batch_set_collateral_coin(  
      request=[  
        {  
          "coin": "BTC",  
          "collateralSwitch": "ON",  
        },  
        {  
          "coin": "ETH",  
          "collateralSwitch": "ON",  
        }  
      ]  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .batchSetCollateralCoin({  
        request: [  
          {  
            coin: 'BTC',  
            collateralSwitch: 'ON',  
          },  
          {  
            coin: 'ETH',  
            collateralSwitch: 'OFF',  
          },  
        ],  
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
        "retMsg": "SUCCESS",  
        "result": {  
            "list": [  
                {  
                    "coin": "MATIC",  
                    "collateralSwitch": "OFF"  
                },  
                {  
                    "coin": "BTC",  
                    "collateralSwitch": "OFF"  
                },  
                {  
                    "coin": "ETH",  
                    "collateralSwitch": "OFF"  
                },  
                {  
                    "coin": "SOL",  
                    "collateralSwitch": "OFF"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1704782042913  
    }  
    

[PreviousGet Borrow History (2 years)](https://bybit-exchange.github.io/docs/v5/account/borrow-history)[NextGet Coin Greeks](https://bybit-exchange.github.io/docs/v5/account/coin-greeks)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


