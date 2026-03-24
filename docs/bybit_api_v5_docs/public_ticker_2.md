# Ticker

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/ticker

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * Ticker



On this page

# Ticker

Subscribe to the ticker stream.

note

  * This topic utilises the snapshot field and delta field. If a response param is not found in the message, then its value has not changed.
  * Spot & Option tickers message are `snapshot` **only**



Push frequency: Derivatives & Options - **100ms** , Spot - **50ms**

**Topic:**  
`tickers.{symbol}`

### Response Parameters​

  * Linear/Inverse
  * Option
  * Spot



Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`,`delta`  
cs| integer| Cross sequence  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object  
> symbol| string| Symbol name   
> [tickDirection](https://bybit-exchange.github.io/docs/v5/enum#tickdirection)| string| Tick direction   
> price24hPcnt| string| Percentage change of market price in the last 24 hours   
> lastPrice| string| Last price   
> prevPrice24h| string| Market price 24 hours ago   
> highPrice24h| string| The highest price in the last 24 hours   
> lowPrice24h| string| The lowest price in the last 24 hours   
> prevPrice1h| string| Market price an hour ago   
> markPrice| string| Mark price   
> indexPrice| string| Index price   
> openInterest| string| Open interest size   
> openInterestValue| string| Open interest value   
> turnover24h| string| Turnover for 24h   
> volume24h| string| Volume for 24h   
> nextFundingTime| string| Next funding timestamp (ms)   
> fundingRate| string| Funding rate   
> bid1Price| string| Best bid price   
> bid1Size| string| Best bid size   
> ask1Price| string| Best ask price   
> ask1Size| string| Best ask size   
> deliveryTime| datetime| Delivery date time (UTC+0), applicable to expired futures only  
> basisRate| string| Basis rate. _Unique field for inverse futures & USDT/USDC futures_  
> deliveryFeeRate| string| Delivery fee rate. _Unique field for inverse futures & USDT/USDC futures_  
> predictedDeliveryPrice| string| Predicated delivery price. _Unique field for inverse futures & USDT/USDC futures_  
> preOpenPrice| string| Estimated pre-market contract open price 

  * The value is meaningless when entering continuous trading phase
  * USDC Futures and Inverse Futures do not have this field

  
> preQty| string| Estimated pre-market contract open qty 

  * The value is meaningless when entering continuous trading phase
  * USDC Futures and Inverse Futures do not have this field

  
> [curPreListingPhase](https://bybit-exchange.github.io/docs/v5/enum#curauctionphase)| string| The current pre-market contract phase 

  * USDC Futures and Inverse Futures do not have this field

  
> fundingIntervalHour| string| Funding interval hour

  * This value currently only supports whole hours
  * Only for Perpetual,For Futures,this field will not return

  
> fundingCap| string| Funding rate upper and lower limits

  * Only for Perpetual,For Futures,this field will not return

  
> basisRateYear| string| Annual basis rate

  * Only for Futures,For Perpetual,this field will not return

  
  
Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`  
id| string| message ID  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object  
> symbol| string| Symbol name   
> bidPrice| string| Best bid price   
> bidSize| string| Best bid size   
> bidIv| string| Best bid iv   
> askPrice| string| Best ask price   
> askSize| string| Best ask size   
> askIv| string| Best ask iv   
> lastPrice| string| Last price   
> highPrice24h| string| The highest price in the last 24 hours   
> lowPrice24h| string| The lowest price in the last 24 hours   
> markPrice| string| Mark price   
> indexPrice| string| Index price   
> markPriceIv| string| Mark price iv   
> underlyingPrice| string| Underlying price   
> openInterest| string| Open interest size   
> turnover24h| string| Turnover for 24h   
> volume24h| string| Volume for 24h   
> totalVolume| string| Total volume   
> totalTurnover| string| Total turnover   
> delta| string| Delta   
> gamma| string| Gamma   
> vega| string| Vega   
> theta| string| Theta   
> predictedDeliveryPrice| string| Predicated delivery price. It has value when 30 min before delivery   
> change24h| string| The change in the last 24 hous   
  
Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
ts| number| The timestamp (ms) that the system generates the data  
type| string| Data type. `snapshot`  
cs| integer| Cross sequence  
data| array| Object  
> symbol| string| Symbol name   
> lastPrice| string| Last price   
> highPrice24h| string| The highest price in the last 24 hours   
> lowPrice24h| string| The lowest price in the last 24 hours   
> prevPrice24h| string| Percentage change of market price relative to 24h   
> volume24h| string| Volume for 24h   
> turnover24h| string| Turnover for 24h   
> price24hPcnt| string| Percentage change of market price relative to 24h   
> usdIndexPrice| string| USD index price 

  * used to calculate USD value of the assets in Unified account
  * non-collateral margin coin returns ""

  
  
### Subscribe Example​

  * Linear
  * Option
  * Spot


    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="linear",  
    )  
    def handle_message(message):  
        print(message)  
    ws.ticker_stream(  
        symbol="BTCUSDT",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="option",  
    )  
    def handle_message(message):  
        print(message)  
    ws.ticker_stream(  
        symbol="tickers.BTC-22JAN23-17500-C",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="spot",  
    )  
    def handle_message(message):  
        print(message)  
    ws.ticker_stream(  
        symbol="BTCUSDT",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​

  * Linear
  * Option
  * Spot


    
    
    LinearPerpetual  
    {  
      "topic": "tickers.BTCUSDT",  
      "type": "snapshot",  
      "data": {  
        "symbol": "BTCUSDT",  
        "tickDirection": "MinusTick",  
        "price24hPcnt": "-0.158315",  
        "lastPrice": "66666.60",  
        "prevPrice24h": "79206.20",  
        "highPrice24h": "79266.30",  
        "lowPrice24h": "65076.90",  
        "prevPrice1h": "66666.60",  
        "markPrice": "66666.60",  
        "indexPrice": "115418.19",  
        "openInterest": "492373.72",  
        "openInterestValue": "32824881841.75",  
        "turnover24h": "4936790807.6521",  
        "volume24h": "73191.3870",  
        "fundingIntervalHour": "8",  
        "fundingCap": "0.005",  
        "nextFundingTime": "1760342400000",  
        "fundingRate": "-0.005",  
        "bid1Price": "66666.60",  
        "bid1Size": "23789.165",  
        "ask1Price": "66666.70",  
        "ask1Size": "23775.469",  
        "preOpenPrice": "",  
        "preQty": "",  
        "curPreListingPhase": ""  
      },  
      "cs": 9532239429,  
      "ts": 1760325052630  
    }  
    LinearFutures  
    {  
      "topic": "tickers.BTC-26DEC25",  
      "type": "snapshot",  
      "data": {  
        "symbol": "BTC-26DEC25",  
        "tickDirection": "ZeroMinusTick",  
        "price24hPcnt": "0",  
        "lastPrice": "109401.50",  
        "prevPrice24h": "109401.50",  
        "highPrice24h": "109401.50",  
        "lowPrice24h": "109401.50",  
        "prevPrice1h": "109401.50",  
        "markPrice": "121144.63",  
        "indexPrice": "114132.51",  
        "openInterest": "6.622",  
        "openInterestValue": "802219.74",  
        "turnover24h": "0.0000",  
        "volume24h": "0.0000",  
        "deliveryTime": "2025-12-26T08:00:00Z",  
        "basisRate": "0.06129209",  
        "deliveryFeeRate": "0",  
        "predictedDeliveryPrice": "0.00",  
        "basis": "-4730.84",  
        "basisRateYear": "0.30655351",  
        "nextFundingTime": "",  
        "fundingRate": "",  
        "bid1Price": "111254.50",  
        "bid1Size": "0.176",  
        "ask1Price": "131001.00",  
        "ask1Size": "0.580"  
      },  
      "cs": 31337927919,  
      "ts": 1760409119857  
    }  
    
    
    
    {  
        "id": "tickers.BTC-6JAN23-17500-C-2480334983-1672917511074",  
        "topic": "tickers.BTC-6JAN23-17500-C",  
        "ts": 1672917511074,  
        "data": {  
            "symbol": "BTC-6JAN23-17500-C",  
            "bidPrice": "0",  
            "bidSize": "0",  
            "bidIv": "0",  
            "askPrice": "10",  
            "askSize": "5.1",  
            "askIv": "0.514",  
            "lastPrice": "10",  
            "highPrice24h": "25",  
            "lowPrice24h": "5",  
            "markPrice": "7.86976724",  
            "indexPrice": "16823.73",  
            "markPriceIv": "0.4896",  
            "underlyingPrice": "16815.1",  
            "openInterest": "49.85",  
            "turnover24h": "446802.8473",  
            "volume24h": "26.55",  
            "totalVolume": "86",  
            "totalTurnover": "1437431",  
            "delta": "0.047831",  
            "gamma": "0.00021453",  
            "vega": "0.81351067",  
            "theta": "-19.9115368",  
            "predictedDeliveryPrice": "0",  
            "change24h": "-0.33333334"  
        },  
        "type": "snapshot"  
    }  
    
    
    
    {  
        "topic": "tickers.BTCUSDT",  
        "ts": 1673853746003,  
        "type": "snapshot",  
        "cs": 2588407389,  
        "data": {  
            "symbol": "BTCUSDT",  
            "lastPrice": "21109.77",  
            "highPrice24h": "21426.99",  
            "lowPrice24h": "20575",  
            "prevPrice24h": "20704.93",  
            "volume24h": "6780.866843",  
            "turnover24h": "141946527.22907118",  
            "price24hPcnt": "0.0196",  
            "usdIndexPrice": "21120.2400136"  
        }  
    }  
    

[PreviousTrade](https://bybit-exchange.github.io/docs/v5/websocket/public/trade)[NextKline](https://bybit-exchange.github.io/docs/v5/websocket/public/kline)

  * Response Parameters
  * Subscribe Example
  * Response Example


