# Upgrade to Unified Account Pro

> **Source:** https://bybit-exchange.github.io/docs/v5/account/upgrade-unified-account

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Upgrade to Unified Account Pro



On this page

# Upgrade to Unified Account Pro

Upgrade Guidance

Check your current account status by calling this [Get Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info)

  * if unifiedMarginStatus=5, then it is [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20), you can call below upgrade endpoint to [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20) Pro. Check [Get Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info) after a while and if unifiedMarginStatus=6, then the account has successfully upgraded to [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20) Pro.
  * When the user is a master account, the current user is allowed to upgrade to UTA PRO if they are a VIP or PRO level user.
  * When the user is a sub-account, only parent accounts with VIP or PRO level are allowed to upgrade to UTA PRO.



info

please note belows:

  1. Please avoid upgrading during these period:

|   
---|---  
every hour| 50th minute to 5th minute of next hour  
  
  2. Please ensure: there is no open orders when upgrade from [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20) to [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20) Pro  
  

  3. During the account upgrade process, the data of **Rest API/Websocket stream** may be inaccurate due to the fact that the account-related asset data is in the processing state. It is recommended to query and use it after the upgrade is completed.



### HTTP Request​

POST`/v5/account/upgrade-to-uta`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
unifiedUpdateStatus| string| Upgrade status. `FAIL`,`PROCESS`,`SUCCESS`  
unifiedUpdateMsg| Object| If `PROCESS`,`SUCCESS`, it returns `null`  
> msg| array| Error message array. Only `FAIL` will have this field  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/upgrade-unified-account)

* * *

### Request Example​

  * HTTP
  * Python
  * GO
  * Java
  * .Net
  * Node.js


    
    
    POST /v5/account/upgrade-to-uta HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672125123533  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {}  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.upgrade_to_unified_trading_account())  
    
    
    
    import (  
        "context"  
        "fmt"  
        bybit "github.com/bybit-exchange/bybit.go.api"  
    )  
    client := bybit.NewBybitHttpClient("YOUR_API_KEY", "YOUR_API_SECRET")  
    client.NewUtaBybitServiceNoParams().UpgradeToUTA(context.Background())  
    
    
    
    import com.bybit.api.client.config.BybitApiConfig;  
    import com.bybit.api.client.domain.account.request.AccountDataRequest;  
    import com.bybit.api.client.domain.account.AccountType;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance("YOUR_API_KEY", "YOUR_API_SECRET", BybitApiConfig.TESTNET_DOMAIN).newAccountRestClient();  
    System.out.println(client.upgradeAccountToUTA());  
    
    
    
    using bybit.net.api;  
    using bybit.net.api.ApiServiceImp;  
    using bybit.net.api.Models;  
    BybitAccountService accountService = new(apiKey: "xxxxxx", apiSecret: "xxxxx");  
    Console.WriteLine(await accountService.UpgradeAccount());  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .upgradeToUnifiedAccount()  
        .then((response) => {  
            console.log(response);  
        })  
        .catch((error) => {  
            console.error(error);  
        });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "unifiedUpdateStatus": "FAIL",  
            "unifiedUpdateMsg": {  
                "msg": [  
                    "Update account failed. You have outstanding liabilities in your Spot account.",  
                    "Update account failed. Please close the usdc perpetual positions in USDC Account.",  
                    "unable to upgrade, please cancel the usdt perpetual open orders in USDT account.",  
                    "unable to upgrade, please close the usdt perpetual positions in USDT account."  
                ]  
        }  
    },  
        "retExtInfo": {},  
        "time": 1672125124195  
    }  
    

[PreviousRepay Liability](https://bybit-exchange.github.io/docs/v5/account/repay-liability)[NextFunding Account Transaction History](https://bybit-exchange.github.io/docs/v5/asset/fund-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


