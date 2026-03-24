# Get Master Deposit Address

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/deposit/master-deposit-addr

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Deposit
  * Get Master Deposit Address



On this page

# Get Master Deposit Address

Query the deposit address information of MASTER account.

### HTTP Request​

GET`/v5/asset/deposit/query-address`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin, uppercase only  
chainType| false| string| Please use the value of `>> chain` from [coin-info](https://bybit-exchange.github.io/docs/v5/asset/coin-info) endpoint  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
coin| string| Coin  
chains| array| Object  
> chainType| string| Chain type  
> addressDeposit| string| The address for deposit  
> tagDeposit| string| Tag of deposit  
> chain| string| Chain  
> batchReleaseLimit| string| The deposit limit for this coin in this chain. `"-1"` means no limit  
> contractAddress| string| The contract address of the coin. Only display last 6 characters, if there is no contract address, it shows `""`  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/master-deposit-addr)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/deposit/query-address?coin=USDT&chainType=ETH HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672192792371  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_master_deposit_address(  
        coin="USDT",  
        chainType="ETH",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getMasterDepositAddress('USDT', 'ETH')  
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
            "coin": "USDT",  
            "chains": [  
                {  
                    "chainType": "Ethereum (ERC20)",  
                    "addressDeposit": "XXXXXX",  
                    "tagDeposit": "",  
                    "chain": "ETH",  
                    "batchReleaseLimit": "-1",  
                    "contractAddress": "831ec7"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1736394811459  
    }  
    

[PreviousGet Internal Deposit Records (off-chain)](https://bybit-exchange.github.io/docs/v5/asset/deposit/internal-deposit-record)[NextGet Sub Deposit Address](https://bybit-exchange.github.io/docs/v5/asset/deposit/sub-deposit-addr)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


