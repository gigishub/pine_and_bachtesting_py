# Get Index Price Components

> **Source:** https://bybit-exchange.github.io/docs/v5/market/index-components

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Index Price Components



On this page

# Get Index Price Components

### HTTP Request​

GET`/v5/market/index-price-components`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
indexName| **true**|  string| Index name, like `BTCUSDT`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
indexName| string| Name of the index (e.g., BTCUSDT)  
lastPrice| string| Last price of the index  
updateTime| string| Timestamp of the last update in milliseconds  
components| array| List of components contributing to the index price  
> exchange| string| Name of the exchange  
> spotPair| string| Spot trading pair on the exchange (e.g., BTCUSDT)  
> equivalentPrice| string| Equivalent price  
> multiplier| string| Multiplier used for the component price  
> price| string| Actual price  
> weight| string| Weight in the index calculation  
  
### Request Example​

  * HTTP
  * Python
  * Go
  * Java
  * Node.js


    
    
    GET /v5/market/index-price-components?indexName=1000BTTUSDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
      
    
    
    
      
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
      "retCode": 0,  
      "retMsg": "",  
      "result": {  
        "indexName": "1000BTTUSDT",  
        "lastPrice": "0.0006496",  
        "updateTime": "1758182745072",  
        "components": [  
          {  
            "exchange": "GateIO",  
            "spotPair": "BTT_USDT",  
            "equivalentPrice": "0.0006485",  
            "multiplier": "1000",  
            "price": "0.0006485",  
            "weight": "0.1383220862762299"  
          },  
          {  
            "exchange": "Bybit",  
            "spotPair": "BTTUSDT",  
            "equivalentPrice": "0.0006502",  
            "multiplier": "1000",  
            "price": "0.0006502",  
            "weight": "0.0407528429737999"  
          },  
          {  
            "exchange": "Bitget",  
            "spotPair": "BTTUSDT",  
            "equivalentPrice": "0.000648",  
            "multiplier": "1000",  
            "price": "0.000648",  
            "weight": "0.1629044859431618"  
          },  
          {  
            "exchange": "BitMart",  
            "spotPair": "BTT_USDT",  
            "equivalentPrice": "0.000649",  
            "multiplier": "1000",  
            "price": "0.000649",  
            "weight": "0.0432327388538453"  
          },  
          {  
            "exchange": "Binance",  
            "spotPair": "BTTCUSDT",  
            "equivalentPrice": "0.00065",  
            "multiplier": "1000",  
            "price": "0.00065",  
            "weight": "0.5322401401714303"  
          },  
          {  
            "exchange": "Mexc",  
            "spotPair": "BTTUSDT",  
            "equivalentPrice": "0.0006517",  
            "multiplier": "1000",  
            "price": "0.0006517",  
            "weight": "0.0825477057815328"  
          }  
        ]  
      },  
      "retExtInfo": {},  
      "time": 1758182745621  
    }  
      
    

[PreviousGet Long Short Ratio](https://bybit-exchange.github.io/docs/v5/market/long-short-ratio)[NextGet Order Price Limit](https://bybit-exchange.github.io/docs/v5/market/order-price-limit)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


