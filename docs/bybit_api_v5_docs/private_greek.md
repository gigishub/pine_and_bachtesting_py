# Greek

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/greek

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Greek



On this page

# Greek

Subscribe to the greeks stream to see changes to your greeks data in **real-time**. `option` only.

**Topic:** `greeks`

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
id| string| Message ID  
topic| string| Topic name  
creationTime| number| Data created timestamp (ms)  
data| array| Object  
> baseCoin| string| Base coin  
> totalDelta| string| Delta value  
> totalGamma| string| Gamma value  
> totalVega| string| Vega value  
> totalTheta| string| Theta value  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "greeks"  
        ]  
    }  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="private",  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    def handle_message(message):  
        print(message)  
    ws.greek_stream(callback=handle_message)  
    while True:  
        sleep(1)  
    

### Stream Example​
    
    
    {  
        "id": "592324fa945a30-2603-49a5-b865-21668c29f2a6",  
        "topic": "greeks",  
        "creationTime": 1672364262482,  
        "data": [  
            {  
                "baseCoin": "ETH",  
                "totalDelta": "0.06999986",  
                "totalGamma": "-0.00000001",  
                "totalVega": "-0.00000024",  
                "totalTheta": "0.00001314"  
            }  
        ]  
    }  
    

[PreviousWallet](https://bybit-exchange.github.io/docs/v5/websocket/private/wallet)[NextDcp](https://bybit-exchange.github.io/docs/v5/websocket/private/dcp)

  * Response Parameters
  * Subscribe Example
  * Stream Example


