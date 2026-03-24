# Sign Agreement

> **Source:** https://bybit-exchange.github.io/docs/v5/user/sign-agreement

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Sign Agreement



On this page

# Sign Agreement

To trade commodity contracts, please complete the agreement signing first. Once completed, you will be able to trade all metals commodity contracts.

info

  * Only the master account can sign the agreement via this endpoint. Subaccounts are not supported for this action.
  * Once the master account has signed, all subaccounts will be eligible to trade.
  * The API key must have at least one of the following permissions to call this endpoint: Account Transfer, Subaccount Transfer, or Withdrawal.



### HTTP Request​

POST`/v5/user/agreement`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  integer| `2`: Metals commodity contracts (XAU & XAG)  
`3`: Crude oil commodity contract  
agree| **true**|  boolean| `true`  
  
### Response Parameters​

None

### Request Example​
    
    
    POST /v5/user/agreement HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1772695036541  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 40  
      
    {  
        "agree": true,  
        "category": 2  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1772695037330  
    }  
    

[PreviousTrade Notify](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/trade-notify)[NextCreate Sub UID](https://bybit-exchange.github.io/docs/v5/user/create-subuid)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


