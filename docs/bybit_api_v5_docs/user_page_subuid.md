# Get Sub UID List (Unlimited)

> **Source:** https://bybit-exchange.github.io/docs/v5/user/page-subuid

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Get Sub UID List (Unlimited)



On this page

# Get Sub UID List (Unlimited)

This API is applicable to the client who has over 10k sub accounts. Use **master user's api key** **only**.

tip

The API key must have one of the below permissions in order to call this endpoint..

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



### HTTP Request​

GET`/v5/user/submembers`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
pageSize| false| string| Data size per page. Return up to 100 records per request  
nextCursor| false| string| Cursor. Use the `nextCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subMembers| array| Object  
> uid| string| Sub user Id  
> username| string| Username  
> memberType| integer| `1`: standard subaccount, `6`: [custodial subaccount](https://www.bybit.com/en/help-center/article?id=000001683)  
> status| integer| The status of the user account

  * `1`: normal
  * `2`: login banned
  * `4`: frozen 

  
> accountMode| integer| The account mode of the user account

  * `1`: Classic Account
  * `3`: UTA1.0
  * `4`: UTA1.0 Pro
  * `5`: UTA2.0
  * `6`: UTA2.0 Pro

  
> remark| string| The remark  
nextCursor| string| The next page cursor value. "0" means no more pages  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/user/submembers?pageSize=1 HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676430318405  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_sub_uid_list_unlimited(  
        pageSize="1",  
    ))  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "subMembers": [  
                {  
                    "uid": "106314365",  
                    "username": "xxxx02",  
                    "memberType": 1,  
                    "status": 1,  
                    "remark": "",  
                    "accountMode": 5  
                },  
                {  
                    "uid": "106279879",  
                    "username": "xxxx01",  
                    "memberType": 1,  
                    "status": 1,  
                    "remark": "",  
                    "accountMode": 6  
                }  
            ],  
            "nextCursor": "0"  
        },  
        "retExtInfo": {},  
        "time": 1760388041006  
    }  
    

[PreviousGet Sub UID List (Limited)](https://bybit-exchange.github.io/docs/v5/user/subuid-list)[NextGet Fund Custodial Sub Acct](https://bybit-exchange.github.io/docs/v5/user/fund-subuid-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


