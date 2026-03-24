# Repay Liability

> **Source:** https://bybit-exchange.github.io/docs/v5/account/repay-liability

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Repay Liability



On this page

# Repay Liability

You can manually repay the liabilities of Unified account

> **Permission** : USDC Contracts  
> 

info

  1. Starting Mar 17, 2026 (gradual rollout, fully released on Mar 24, 2026), BYUSDT can be used for repayment.
  2. MNT will temporarily not be used for repayment, and repaying MNT liabilities through convert-repay is not supported. However, you may still use [Manual Repay Without Asset Conversion](https://bybit-exchange.github.io/docs/v5/account/no-convert-repay) to repay MNT using your existing balance.
  3. Starting Feb 10, 2026 at 08:00 UTC, UTA Loan manual repayments will be updated to calculate coin-conversion repayment fees using the higher of the collateral or debt asset fee rate and introduce a per-transaction coin-conversion limit of USD 300,000 (Total coin-conversion amount must less than 300,000 USD equivalent) to strengthen stability and risk controls. Please refer to [UTA Loan manual repayment update](https://announcements.bybit.com/article/uta-loan-manual-repayment-update-bltbef3f1ad72a8295d/)



### HTTP Request​

POST`/v5/account/quick-repayment`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| false| string| The coin with liability, uppercase only 

  * Input the specific coin: repay the liability of this coin in particular
  * No coin specified: repay the liability of all coins

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> coin| string| Coin used for repayment 

  * The order of currencies used to repay liability is based on `liquidationOrder` from [this endpoint](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin)

  
> repaymentQty| string| Repayment qty  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/quick-repayment HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1701848610019  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 22  
      
    {  
        "coin": "USDT"  
    }  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .repayLiability({  
        coin: 'USDT',  
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
                    "coin": "BTC",  
                    "repaymentQty": "0.10549670"  
                },  
                {  
                    "coin": "ETH",  
                    "repaymentQty": "2.27768114"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1701848610941  
    }  
    

[PreviousSet Price Limit Behaviour](https://bybit-exchange.github.io/docs/v5/account/set-price-limit)[NextUpgrade to Unified Account Pro](https://bybit-exchange.github.io/docs/v5/account/upgrade-unified-account)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


