# Get available VASPs

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/withdraw/vasp-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Withdraw
  * Get available VASPs



On this page

# Get available VASPs

This endpoint is used for query the available VASPs. This API distinguishes which compliance zone the user belongs to and the corresponding list of exchanges based on the user's UID.

### HTTP Request​

GET`/v5/asset/withdraw/vasp/list`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
vasp| array| Exchange entity info  
> vaspEntityId| string| Receiver platform id. When transfer to the exchanges that are not in the list, please use vaspEntityId='others'  
> vaspName| string| Receiver platform name  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/withdraw/vasp/list HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1715067106163  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getExchangeEntities()  
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
            "vasp": [  
                {  
                    "vaspEntityId": "basic-finance",  
                    "vaspName": "Basic-finance"  
                },  
                {  
                    "vaspEntityId": "beeblock",  
                    "vaspName": "Beeblock"  
                },  
                {  
                    "vaspEntityId": "bithumb",  
                    "vaspName": "bithumb"  
                },  
                {  
                    "vaspEntityId": "cardo",  
                    "vaspName": "cardo"  
                },  
                {  
                    "vaspEntityId": "codevasp",  
                    "vaspName": "codevasp"  
                },  
                {  
                    "vaspEntityId": "codexchange-kor",  
                    "vaspName": "CODExchange-kor"  
                },  
                {  
                    "vaspEntityId": "coinone",  
                    "vaspName": "coinone"  
                },  
                {  
                    "vaspEntityId": "dummy",  
                    "vaspName": "Dummy"  
                },  
                {  
                    "vaspEntityId": "flata-exchange",  
                    "vaspName": "flataexchange"  
                },  
                {  
                    "vaspEntityId": "fobl",  
                    "vaspName": "Foblgate"  
                },  
                {  
                    "vaspEntityId": "hanbitco",  
                    "vaspName": "hanbitco"  
                },  
                {  
                    "vaspEntityId": "hexlant",  
                    "vaspName": "hexlant"  
                },  
                {  
                    "vaspEntityId": "inex",  
                    "vaspName": "INEX"  
                },  
                {  
                    "vaspEntityId": "infiniteblock-corp",  
                    "vaspName": "InfiniteBlock Corp"  
                },  
                {  
                    "vaspEntityId": "kdac",  
                    "vaspName": "kdac"  
                },  
                {  
                    "vaspEntityId": "korbit",  
                    "vaspName": "korbit"  
                },  
                {  
                    "vaspEntityId": "paycoin",  
                    "vaspName": "Paycoin"  
                },  
                {  
                    "vaspEntityId": "qbit",  
                    "vaspName": "Qbit"  
                },  
                {  
                    "vaspEntityId": "tennten",  
                    "vaspName": "TENNTEN"  
                },  
                {  
                    "vaspEntityId": "others",  
                    "vaspName": "Others (including Upbit)"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1715067106537  
    }  
    

[PreviousGet Withdrawal Records](https://bybit-exchange.github.io/docs/v5/asset/withdraw/withdraw-record)[NextWithdraw](https://bybit-exchange.github.io/docs/v5/asset/withdraw)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


