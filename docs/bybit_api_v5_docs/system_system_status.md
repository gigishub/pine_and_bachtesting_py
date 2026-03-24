# System Status

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/system/system-status

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * System
  * System Status



On this page

# System Status

Listen to the system status when there is a platform maintenance or service incident.

info

Please note currently system maintenance that may result in short interruption (lasting less than 10 seconds) or websocket disconnection (users can immediately reconnect) will not be announced.

## URL​

  * **Mainnet:**  
`wss://stream.bybit.com/v5/public/misc/status`



info

  * EU users registered from "[www.bybit.eu"](http://www.bybit.eu%22), please use `wss://stream.bybit.eu/v5/public/misc/status`



**Topic:**  
`system.status`

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object  
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
  
### Subscribe Example​

  * JSON
  * Python


    
    
    {  
        "op": "subscribe",  
        "args": [  
            "system.status"  
        ]  
    }  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="misc/status",  
    )  
    def handle_message(message):  
        print(message)  
    ws.system_status_stream(  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​
    
    
    {  
        "topic": "system.status",  
        "ts": 1751858399649,  
        "data": [  
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
            }  
        ]  
    }  
    

[PreviousWebsocket Trade Guideline](https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline)[NextRate Limit Rules](https://bybit-exchange.github.io/docs/v5/rate-limit)

  * URL
    * Response Parameters
    * Subscribe Example
    * Response Example


