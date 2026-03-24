# Get System Status

> **Source:** https://bybit-exchange.github.io/docs/v5/system-status

---

  * [](https://bybit-exchange.github.io/docs/)
  * Get System Status



On this page

# Get System Status

Get the system status when there is a platform maintenance or service incident.

info

Please note currently system maintenance that may result in short interruption (lasting less than 10 seconds) or websocket disconnection (users can immediately reconnect) will not be announced.

### HTTP Request​

GET`/v5/system/status`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
id| false| string| id. Unique identifier  
[state](https://bybit-exchange.github.io/docs/v5/enum#state)| false| string| system state  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> id| string| Id. Unique identifier  
> title| string| Title of system maintenance  
> [state](https://bybit-exchange.github.io/docs/v5/enum#state)| string| System state  
> begin| string| Start time of system maintenance, timestamp in milliseconds  
> end| string| End time of system maintenance, timestamp in milliseconds. Before maintenance is completed, it is the expected end time; After maintenance is completed, it will be changed to the actual end time.  
> href| string| Hyperlink to system maintenance details. Default value is empty string  
> [serviceTypes](https://bybit-exchange.github.io/docs/v5/enum#servicetypes)| array<int>| Service Type  
> [product](https://bybit-exchange.github.io/docs/v5/enum#product)| array<int>| Product  
> uidSuffix| array<int>| Affected UID tail number  
> [maintainType](https://bybit-exchange.github.io/docs/v5/enum#maintaintype)| string| Maintenance type  
> [env](https://bybit-exchange.github.io/docs/v5/enum#env)| string| Environment  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/system/status HTTP/1.1  
    Host: api.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_price_limit(  
        category="linear",  
        symbol="BTCUSDT",  
    ))  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "list": [  
                {  
                    "id": "4d95b2a0-587f-11f0-bcc9-56f28c94d6ea",  
                    "title": "t06",  
                    "state": "completed",  
                    "begin": "1751596902000",  
                    "end": "1751597011000",  
                    "href": "",  
                    "serviceTypes": [  
                        2,  
                        3,  
                        4,  
                        5  
                    ],  
                    "product": [  
                        1,  
                        2  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 1,  
                    "env": 1  
                },  
                {  
                    "id": "19bb6f82-587f-11f0-bcc9-56f28c94d6ea",  
                    "title": "t05",  
                    "state": "completed",  
                    "begin": "1751254200000",  
                    "end": "1751254500000",  
                    "href": "",  
                    "serviceTypes": [  
                        1,  
                        4  
                    ],  
                    "product": [  
                        1  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 3,  
                    "env": 1  
                },  
                {  
                    "id": "25f4bc8c-533c-11f0-bcc9-56f28c94d6ea",  
                    "title": "t04",  
                    "state": "completed",  
                    "begin": "1751017967000",  
                    "end": "1751018096000",  
                    "href": "",  
                    "serviceTypes": [  
                        2  
                    ],  
                    "product": [  
                        2  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 1,  
                    "env": 1  
                },  
                {  
                    "id": "679a9c5f-533b-11f0-bcc9-56f28c94d6ea",  
                    "title": "t03",  
                    "state": "completed",  
                    "begin": "1751017532000",  
                    "end": "1751017658000",  
                    "href": "",  
                    "serviceTypes": [  
                        5,  
                        4  
                    ],  
                    "product": [  
                        1,  
                        2  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 2,  
                    "env": 1  
                },  
                {  
                    "id": "c8990f96-5332-11f0-8fd3-c241b123dd9e",  
                    "title": "t02",  
                    "state": "completed",  
                    "begin": "1751013817000",  
                    "end": "1751013890000",  
                    "href": "",  
                    "serviceTypes": [  
                        5,  
                        4,  
                        3,  
                        2,  
                        1  
                    ],  
                    "product": [  
                        4,  
                        3,  
                        2,  
                        1  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 2,  
                    "env": 1  
                },  
                {  
                    "id": "f9d6842d-5331-11f0-8fd3-c241b123dd9e",  
                    "title": "t01",  
                    "state": "completed",  
                    "begin": "1751012688000",  
                    "end": "1751012760000",  
                    "href": "",  
                    "serviceTypes": [  
                        1,  
                        2,  
                        3,  
                        4,  
                        5  
                    ],  
                    "product": [  
                        1,  
                        2,  
                        3,  
                        4  
                    ],  
                    "uidSuffix": [],  
                    "maintainType": 3,  
                    "env": 2  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1751858399649  
    }  
    

[PreviousDemo Trading Service](https://bybit-exchange.github.io/docs/v5/demo)[NextGet Bybit Server Time](https://bybit-exchange.github.io/docs/v5/market/time)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


