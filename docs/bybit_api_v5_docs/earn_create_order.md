# Stake / Redeem

> **Source:** https://bybit-exchange.github.io/docs/v5/earn/create-order

---

  * [](https://bybit-exchange.github.io/docs/)
  * Earn
  * Stake / Redeem



On this page

# Stake / Redeem

info

API key needs "Earn" permission, custody accounts are not supported for now

note

In times of high demand for loans in the market for a specific cryptocurrency, the redemption of the principal may encounter delays and is expected to be processed within 48 hours. The redemption of on-chain products may take up to a few days to complete. Once the redemption request is initiated, it cannot be cancelled.

### HTTP Request​

POST`/v5/earn/place-order`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| `FlexibleSaving`,`OnChain`   
**Remarks** : currently, only flexible savings and on chain is supported  
orderType| **true**|  string| `Stake`, `Redeem`  
accountType| **true**|  string| `FUND`, `UNIFIED`. Onchain only supports FUND  
amount| **true**|  string| 

  * Stake amount needs to satisfy minStake and maxStake
  * Both stake and redeem amount need to satify precision requirement

  
coin| **true**|  string| Coin name  
productId| **true**|  string| Product ID  
orderLinkId| **true**|  string| Customised order ID, used to prevent from replay

  * support up to 36 characters
  * The same orderLinkId can't be used in 30 mins

  
redeemPositionId| false| string| The position ID that the user needs to redeem. Only is required in Onchain non-LST mode  
toAccountType| false| string| `FUND`, `UNIFIED`. Onchain LST mode supports `FUND` and `UNIFIED`(Private wealth management custodial subaccount only supports `UNIFIED`). Onchain non-LST mode only supports `FUND`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
orderId| string| Order ID  
orderLinkId| string| Order link ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/earn/place-order HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1739936605822  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 190  
      
    {  
        "category": "FlexibleSaving",  
        "orderType": "Redeem",  
        "accountType": "FUND",  
        "amount": "0.35",  
        "coin": "BTC",  
        "productId": "430",  
        "orderLinkId": "btc-earn-001"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.stake_or_redeem(  
        category="FlexibleSaving",  
        orderType="Redeem",  
        accountType="FUND",  
        amount="0.35",  
        coin="BTC",  
        productId="430",  
        orderLinkId="btc-earn-001"  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "orderId": "0572b030-6a0b-423f-88c4-b6ce31c0c82d",  
            "orderLinkId": "btc-earn-001"  
        },  
        "retExtInfo": {},  
        "time": 1739936607117  
    }  
    

[PreviousGet Product Info](https://bybit-exchange.github.io/docs/v5/earn/product-info)[NextGet Stake/Redeem Order History](https://bybit-exchange.github.io/docs/v5/earn/order-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


