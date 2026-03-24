# Get Sub Deposit Address

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/deposit/sub-deposit-addr

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Deposit
  * Get Sub Deposit Address



On this page

# Get Sub Deposit Address

Query the deposit address information of SUB account.

info

  * Use master UID's api key **only**
  * Custodial sub account deposit address cannot be obtained



### HTTP Request​

GET`/v5/asset/deposit/query-sub-member-address`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin, uppercase only  
chainType| **true**|  string| Please use the value of `chain` from [coin-info](https://bybit-exchange.github.io/docs/v5/asset/coin-info) endpoint  
subMemberId| **true**|  string| Sub user ID  
  
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
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/sub-deposit-addr)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/deposit/query-sub-member-address?coin=USDT&chainType=TRX&subMemberId=592334 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672194349421  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_sub_deposit_address(  
        coin="USDT",  
        chainType="TRX",  
        subMemberId=592334,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSubDepositAddress('USDT', 'TRX', '592334')  
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
            "chains": {  
                "chainType": "TRC20",  
                "addressDeposit": "XXXXXX",  
                "tagDeposit": "",  
                "chain": "TRX",  
                "batchReleaseLimit": "-1",  
                "contractAddress": "gjLj6t"  
            }  
        },  
        "retExtInfo": {},  
        "time": 1736394845821  
    }  
    

[PreviousGet Master Deposit Address](https://bybit-exchange.github.io/docs/v5/asset/deposit/master-deposit-addr)[NextGet Withdrawal Address List](https://bybit-exchange.github.io/docs/v5/asset/withdraw/withdraw-address)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


