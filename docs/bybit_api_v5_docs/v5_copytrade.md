# How To Start Copy Trading

> **Source:** https://bybit-exchange.github.io/docs/v5/copytrade

---

  * [](https://bybit-exchange.github.io/docs/)
  * How To Start Copy Trading



On this page

# How To Start Copy Trading

## Become A Master Trader​

Please go [here](https://www.bybit.com/copyTrade/) to apply to become a Master Trader

## Create The API KEY​

"Contract - Orders & Positions" are mandatory permissions for Copy Trading orders

## Understand The Scope​

From time being copy trading accounts can only trade USDT Perpetual symbols. Please check the field `copyTrading` from [Get Instruments Info](https://bybit-exchange.github.io/docs/v5/market/instrument)

## Place The Copy Trading Order​

Use V5 [Place Order](https://bybit-exchange.github.io/docs/v5/order/create-order) endpoint to place a Copy Trading order
    
    
    POST /v5/order/create HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1698376189371  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 207  
      
    {  
        "symbol": "BTCUSDT",  
        "side": "Buy",  
        "orderType": "Limit",  
        "category": "linear",  
        "qty": "0.1",  
        "price": "29000",  
        "timeInForce": "GTC",  
        "positionIdx": 1  
    }  
    

[PreviousSelf Match Prevention](https://bybit-exchange.github.io/docs/v5/smp)[NextDemo Trading Service](https://bybit-exchange.github.io/docs/v5/demo)

  * Become A Master Trader
  * Create The API KEY
  * Understand The Scope
  * Place The Copy Trading Order


