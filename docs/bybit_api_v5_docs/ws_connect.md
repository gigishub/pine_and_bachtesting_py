# Connect

> **Source:** https://bybit-exchange.github.io/docs/v5/ws/connect

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Websocket Stream
  * Connect



On this page

# Connect

**[WebSocket public stream](https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook):**

  * **Mainnet:**  
Spot: `wss://stream.bybit.com/v5/public/spot`  
USDT, USDC perpetual & USDT Futures: `wss://stream.bybit.com/v5/public/linear`  
Inverse contract: `wss://stream.bybit.com/v5/public/inverse`  
Spread trading: `wss://stream.bybit.com/v5/public/spread`  
RFQ: `wss://stream-testnet.bybit.com/v5/public/rfq`  
USDT/USDC Options: `wss://stream.bybit.com/v5/public/option`

  * **Testnet:**  
Spot: `wss://stream-testnet.bybit.com/v5/public/spot`  
USDT,USDC perpetual & USDT Futures: `wss://stream-testnet.bybit.com/v5/public/linear`  
Inverse contract: `wss://stream-testnet.bybit.com/v5/public/inverse`  
Spread trading: `wss://stream-testnet.bybit.com/v5/public/spread`  
RFQ: `wss://stream-testnet.bybit.com/v5/public/rfq`  
USDT/USDC Options: `wss://stream-testnet.bybit.com/v5/public/option`




**[WebSocket private stream](https://bybit-exchange.github.io/docs/v5/websocket/private/order):**

  * **Mainnet:**  
`wss://stream.bybit.com/v5/private`

  * **Testnet:**  
`wss://stream-testnet.bybit.com/v5/private`




**[WebSocket Order Entry](https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline):**

  * **Mainnet:**  
`wss://stream.bybit.com/v5/trade` (Spread trading is not supported)

  * **Testnet:**  
`wss://stream-testnet.bybit.com/v5/trade` (Spread trading is not supported)




**[WebSocket GET System Status](https://bybit-exchange.github.io/docs/v5/websocket/system/system-status):**

  * **Mainnet:**  
`wss://stream.bybit.com/v5/public/misc/status`

  * **Testnet:**  
`wss://stream-testnet.bybit.com/v5/public/misc/status`




info

  * If your account is registered from [www.bybit-tr.com](http://www.bybit-tr.com), please use `stream.bybit-tr.com` for mainnet access
  * If your account is registered from [www.bybit.kz](http://www.bybit.kz), please use `stream.bybit.kz` for mainnet access
  * If your account is registered from [www.bybitgeorgia.ge](http://www.bybitgeorgia.ge), please use `stream.bybitgeorgia.ge` for mainnet access



Customise Private Connection Alive Time

For private stream and order entry, you can customise alive duration by adding a param `max_active_time`, the lowest value is `30s` (30 seconds), the highest value is `600s` (10 minutes). You can also pass `1m`, `2m` etc when you try to configure by minute level. e.g., _wss://stream-testnet.bybit.com/v5/private?max_active_time=1m_.

In general, if there is no "ping-pong" and no stream data sent from server end, the connection will be cut off after 10 minutes. When you have a particular need, you can configure connection alive time by `max_active_time`.

Since ticker scans every 30s, so it is not fully exact, i.e., if you configure 45s, and your last update or ping-pong is occurred on `2023-08-15 17:27:23`, your disconnection time maybe happened on `2023-08-15 17:28:15`

## Authentication​

info

**Public** topics do not require authentication. The following section applies to **private** topics only.

Apply for authentication when establishing a connection.

Note: if you're using [pybit](https://github.com/bybit-exchange/pybit), [bybit-api](https://www.npmjs.com/package/bybit-api), or another high-level library, you can ignore this code - as authentication is handled for you.
    
    
    {  
        "req_id": "10001", // optional  
        "op": "auth",  
        "args": [  
            "api_key",  
            1662350400000, // expires; is greater than your current timestamp  
            "signature"  
        ]  
    }  
    
    
    
    # based on: https://github.com/bybit-exchange/pybit/blob/master/pybit/_http_manager.py  
      
    import hmac  
    import json  
    import time  
    import websocket  
      
    api_key = ""  
    api_secret = ""  
      
    # Generate expires.  
    expires = int((time.time() + 1) * 1000)  
      
    # Generate signature.  
    signature = str(hmac.new(  
        bytes(api_secret, "utf-8"),  
        bytes(f"GET/realtime{expires}", "utf-8"), digestmod="sha256"  
    ).hexdigest())  
      
    ws = websocket.WebSocketApp(  
        url=url,  
        ...  
    )  
      
    # Authenticate with API.  
    ws.send(  
        json.dumps({  
            "op": "auth",  
            "args": [api_key, expires, signature]  
        })  
    )  
    

> Successful authentication sample response
    
    
    {  
        "success": true,  
        "ret_msg": "",  
        "op": "auth",  
        "conn_id": "cejreaspqfh3sjdnldmg-p"  
    }  
    

note

Example signature algorithms can be found [here](https://github.com/bybit-exchange/api-usage-examples).

caution

Due to network complexity, your may get disconnected at any time. Please follow the instructions below to ensure that you receive WebSocket messages on time:

  1. Keep connection alive by [sending the heartbeat packet](https://bybit-exchange.github.io/docs/v5/ws/connect#how-to-send-the-heartbeat-packet)
  2. Reconnect as soon as possible if disconnected



## IP Limits​

  * Do not frequently connect and disconnect the connection.
  * Do not build over 500 connections in 5 minutes. This is counted per WebSocket domain.



## Public channel - Args limits​

Regardless of Perpetual, Futures, Options or Spot, for one public connection, you cannot have length of "args" array over 21,000 characters.

  * Spot can input up to 10 args for each subscription request sent to one connection
  * Options can input up to 2000 args for a single connection
  * No args limit for Futures and Spread for now



## How to Send the Heartbeat Packet​

> How to Send
    
    
    // req_id is a customised ID, which is optional  
    ws.send(JSON.stringify({"req_id": "100001", "op": "ping"}));  
    

> Pong message example of public channels

  * Spot
  * Linear/Inverse
  * Option/Spread


    
    
    {  
        "success": true,  
        "ret_msg": "pong",  
        "conn_id": "0970e817-426e-429a-a679-ff7f55e0b16a",  
        "op": "ping"  
    }  
    
    
    
    {  
        "success": true,  
        "ret_msg": "pong",  
        "conn_id": "465772b1-7630-4fdc-a492-e003e6f0f260",  
        "req_id": "",  
        "op": "ping"  
    }  
    
    
    
    {  
        "args": [  
            "1672916271846"  
        ],  
        "op": "pong"  
    }  
    

> Pong message example of private channels
    
    
    {  
        "req_id": "test",  
        "op": "pong",  
        "args": [  
            "1675418560633"  
        ],  
        "conn_id": "cfcb4ocsvfriu23r3er0-1b"  
    }  
    

caution

To avoid network or program issues, we recommend that you send the `ping` heartbeat packet every **20** seconds to maintain the WebSocket connection.

## How to Subscribe to Topics​

### Understanding WebSocket Filters​

How to subscribe with a filter
    
    
    // Subscribing level 1 orderbook  
    {  
        "req_id": "test", // optional  
        "op": "subscribe",  
        "args": [  
            "orderbook.1.BTCUSDT"  
        ]  
    }  
    

Subscribing with multiple symbols and topics is supported.
    
    
    {  
        "req_id": "test", // optional  
        "op": "subscribe",  
        "args": [  
            "orderbook.1.BTCUSDT",  
            "publicTrade.BTCUSDT",  
            "orderbook.1.ETHUSDT"  
        ]  
    }  
    

### Understanding WebSocket Filters: Unsubscription​

You can dynamically subscribe and unsubscribe from topics without unsubscribing from the WebSocket like so:
    
    
    {  
        "op": "unsubscribe",  
        "args": [  
            "publicTrade.ETHUSD"  
        ],  
        "req_id": "customised_id"  
    }  
    

## Understanding the Subscription Response​

> Topic subscription response message example

  * Private
  * Public Spot
  * Linear/Inverse
  * Option/Spread


    
    
    {  
        "success": true,  
        "ret_msg": "",  
        "op": "subscribe",  
        "conn_id": "cejreassvfrsfvb9v1a0-2m"  
    }  
    
    
    
    {  
        "success": true,  
        "ret_msg": "subscribe",  
        "conn_id": "2324d924-aa4d-45b0-a858-7b8be29ab52b",  
        "req_id": "10001",  
        "op": "subscribe"  
    }  
    
    
    
    {  
        "success": true,  
        "ret_msg": "",  
        "conn_id": "3cd84cb1-4d06-4a05-930a-2efe5fc70f0f",  
        "req_id": "",  
        "op": "subscribe"  
    }  
    
    
    
    {  
        "success": true,  
        "conn_id": "aa01fbfffe80af37-00000001-000b37b9-7147f432704fd28c-00e1c172",  
        "data": {  
        "failTopics": [],  
        "successTopics": [  
            "orderbook.100.BTC-6JAN23-18000-C"  
        ]  
    },  
        "type": "COMMAND_RESP"  
    }  
    

[PreviousGet Trade History](https://bybit-exchange.github.io/docs/v5/spread/trade/trade-history)[NextOrderbook](https://bybit-exchange.github.io/docs/v5/spread/websocket/public/orderbook)

  * Authentication
  * IP Limits
  * Public channel - Args limits
  * How to Send the Heartbeat Packet
  * How to Subscribe to Topics
    * Understanding WebSocket Filters
    * Understanding WebSocket Filters: Unsubscription
  * Understanding the Subscription Response


