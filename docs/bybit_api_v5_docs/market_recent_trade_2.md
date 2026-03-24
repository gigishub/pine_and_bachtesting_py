# Get Recent Public Trades

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/market/recent-trade

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Market
  * Get Recent Public Trades



On this page

# Get Recent Public Trades

Query recent public spread trading history in Bybit.

### HTTP Request​

GET`/v5/spread/recent-trade`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
symbol| **true**|  string| Spread combination symbol name  
limit| false| integer| Limit for data size per page [`1`,`1000`], default: `500`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array<object>| Public trade info  
> execId| string| Execution ID  
> symbol| string| Spread combination symbol name  
> price| string| Trade price  
> size| string| Trade size  
> side| string| Side of taker `Buy`, `Sell`  
> time| string| Trade time (ms)  
> seq| string| Cross sequence  
  
### Request Example​
    
    
    GET /v5/spread/recent-trade?symbol=SOLUSDT_SOL/USDT&limit=2 HTTP/1.1  
    Host: api-testnet.bybit.com  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "Success",  
        "result": {  
            "list": [  
                {  
                    "execId": "c8512970-d6fb-5039-93a5-b4196dffbe88",  
                    "symbol": "SOLUSDT_SOL/USDT",  
                    "price": "20.2805",  
                    "size": "3.3",  
                    "side": "Sell",  
                    "time": "1744078324035",  
                    "seq":"123456"  
                },  
                {  
                    "execId": "92b0002e-c49d-5618-a195-4140d7e10a2b",  
                    "symbol": "SOLUSDT_SOL/USDT",  
                    "price": "20.843",  
                    "size": "2.2",  
                    "side": "Buy",  
                    "time": "1744078322010",  
                    "seq":"123450"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1744078324682  
    }  
    

[PreviousGet Tickers](https://bybit-exchange.github.io/docs/v5/spread/market/tickers)[NextCreate Order](https://bybit-exchange.github.io/docs/v5/spread/trade/create-order)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


