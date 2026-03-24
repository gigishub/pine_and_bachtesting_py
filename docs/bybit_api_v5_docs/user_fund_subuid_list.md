# Get Fund Custodial Sub Acct

> **Source:** https://bybit-exchange.github.io/docs/v5/user/fund-subuid-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Get Fund Custodial Sub Acct



On this page

# Get Fund Custodial Sub Acct

The institutional client can query the fund custodial sub accounts.

tip

The API key must have one of the below permissions in order to call this endpoint..

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



### HTTP Request​

GET`/v5/user/escrow_sub_members`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
pageSize| false| string| Data size per page. Return up to 100 records per request  
nextCursor| false| string| Cursor. Use the `nextCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subMembers| array| Object  
> uid| string| Sub userId  
> username| string| User name  
> memberType| integer| `12`: Fund custodial account  
> status| integer| Account state.

  * `1`: normal
  * `2`: forbidden login
  * `4`: frozen 

  
> accountMode| integer| Account mode.

  * `1`: classic account
  * `3`: UTA account 

  
> remark| string| Remark  
nextCursor| string| The next page cursor value. "0" means no more pages  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/user/escrow_sub_members?pageSize=2 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1739763787703  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "subMembers": [  
                {  
                    "uid": "104274894",  
                    "username": "Private_Wealth_Management",  
                    "memberType": 12,  
                    "status": 1,  
                    "remark": "earn fund",  
                    "accountMode": 3  
                },  
                {  
                    "uid": "104274884",  
                    "username": "Private_Wealth_Management",  
                    "memberType": 12,  
                    "status": 1,  
                    "remark": "earn fund",  
                    "accountMode": 3  
                }  
            ],  
            "nextCursor": "344"  
        },  
        "retExtInfo": {},  
        "time": 1739763788699  
    }  
    

[PreviousGet Sub UID List (Unlimited)](https://bybit-exchange.github.io/docs/v5/user/page-subuid)[NextFreeze Sub UID](https://bybit-exchange.github.io/docs/v5/user/froze-subuid)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


