# Get Account Instruments Info

> **Source:** https://bybit-exchange.github.io/docs/v5/account/instrument

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Account Instruments Info



On this page

# Get Account Instruments Info

Query for the instrument specification of online trading pairs that available to users.

> **Covers: Spot / USDT contract / USDC contract / Inverse contract**

caution

  * Spot does not support pagination, so `limit`, `cursor` are invalid.
  * This endpoint returns 200 entries by default. There are now more than 200 `linear` symbols on the platform. As a result, you will need to use `cursor` for pagination or `limit` to get all entries.
  * Custodial sub-accounts do not support queries.
  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery
  * The fields `maxLimitOrderQty`, `maxMarketOrderQty`, and `postOnlyMaxLimitOrderSize` are adjusted bi-monthly (3rd and 17th, 08:00 UTC+8). Developers should not assume these values remain constant.



### HTTP Request​

GET`/v5/account/instruments-info`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type. `spot`,`linear`,`inverse`  
[symbol](https://bybit-exchange.github.io/docs/v5/enum#symbol)| false| string| Symbol name, like `BTCUSDT`, uppercase only  
limit| false| integer| Limit for data size per page. [`1`, `200`]. Default: `200`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

  * Linear/Inverse
  * Spot



Parameter| Type| Comments  
---|---|---  
category| string| Product type  
nextPageCursor| string| Cursor. Used to pagination  
list| array| Object  
> symbol| string| Symbol name   
> [contractType](https://bybit-exchange.github.io/docs/v5/enum#contracttype)| string| Contract type  
> [status](https://bybit-exchange.github.io/docs/v5/enum#status)| string| Instrument status   
> baseCoin| string| Base coin   
> quoteCoin| string| Quote coin   
> [symbolType](https://bybit-exchange.github.io/docs/v5/enum#symboltype)| string| the region to which the trading pair belongs  
> launchTime| string| Launch timestamp (ms)   
> deliveryTime| string| Delivery timestamp (ms) 

  * Expired futures delivery time
  * Perpetual delisting time

  
> deliveryFeeRate| string| Delivery fee rate  
> priceScale| string| Price scale   
> leverageFilter| Object| Leverage attributes   
>> minLeverage| string| Minimum leverage   
>> maxLeverage| string| Maximum leverage   
>> leverageStep| string| The step to increase/reduce leverage   
> priceFilter| Object| Price attributes   
>> minPrice| string| Minimum order price   
>> maxPrice| string| Maximum order price   
>> tickSize| string| The step to increase/reduce order price   
> lotSizeFilter| Object| Size attributes   
>> minNotionalValue| string| Minimum notional value  
>> maxOrderQty| string| Maximum quantity for Limit and PostOnly order   
>> maxMktOrderQty| string| Maximum quantity for Market order   
>> minOrderQty| string| Minimum order quantity   
>> qtyStep| string| The step to increase/reduce order quantity   
>> postOnlyMaxOrderQty| string| deprecated, please use `maxOrderQty`  
> unifiedMarginTrade| boolean| Whether to support unified margin trade   
> fundingInterval| integer| Funding interval (minute)   
> settleCoin| string| Settle coin   
> [copyTrading](https://bybit-exchange.github.io/docs/v5/enum#copytrading)| string| Copy trade symbol or not   
> upperFundingRate| string| Upper limit of funding date  
> lowerFundingRate| string| Lower limit of funding date  
> displayName| string| The USDC futures & perpetual name displayed in the Web or App  
> riskParameters| object| Risk parameters for limit order price. Note that the [formula changed](https://announcements.bybit.com/en/article/adjustments-to-bybit-s-derivative-trading-limit-order-mechanism-blt469228de1902fff6/) in Jan 2025  
>> priceLimitRatioX| string| Ratio X  
>> priceLimitRatioY| string| Ratio Y  
> isPreListing| boolean| 

  * Whether the contract is a pre-market contract
  * When the pre-market contract is converted to official contract, it will be false

  
> preListingInfo| object| 

  * If isPreListing=false, preListingInfo=null
  * If isPreListing=true, preListingInfo is an object

  
>> [curAuctionPhase](https://bybit-exchange.github.io/docs/v5/enum#curauctionphase)| string| The current auction phase  
>> phases| array<object>| Each phase time info  
>>> [phase](https://bybit-exchange.github.io/docs/v5/enum#curauctionphase)| string| pre-market trading phase  
>>> startTime| string| The start time of the phase, timestamp(ms)  
>>> endTime| string| The end time of the phase, timestamp(ms)  
>> auctionFeeInfo| object| Action fee info  
>>> auctionFeeRate| string| The trading fee rate during auction phase 

  * There is no trading fee until entering continues trading phase

  
>>> takerFeeRate| string| The taker fee rate during continues trading phase   
>>> makerFeeRate| string| The maker fee rate during continues trading phase  
>> skipCallAuction| boolean| `false`, `true` Whether the pre-market contract skips the call auction phase  
> isPublicRpi | boolean| Whether RPI Is Openly Provided to Market Makers or not.

  * true: RPI Is Openly Provided to Market Makers
  * false: RPI Is Not Openly Provided to Market Makers

  
> myRpiPermission | boolean| Whether the Current User Has RPI Permissions or not

  * true: Has RPI Permissions
  * false: Does Not Have RPI Permissions

  
  
Parameter| Type| Comments  
---|---|---  
category| string| Product type  
list| array| Object  
> symbol| string| Symbol name   
> baseCoin| string| Base coin   
> quoteCoin| string| Quote coin   
> innovation| string| deprecated, please use `symbolType`  
> [symbolType](https://bybit-exchange.github.io/docs/v5/enum#symboltype)| string| the region to which the trading pair belongs  
> [status](https://bybit-exchange.github.io/docs/v5/enum#status)| string| Instrument status   
> [marginTrading](https://bybit-exchange.github.io/docs/v5/enum#margintrading)| string| Margin trade symbol or not 

  * This is to identify if the symbol support margin trading under different account modes
  * You may find some symbols not supporting margin buy or margin sell, so you need to go to [Collateral Info (UTA)](https://bybit-exchange.github.io/docs/v5/account/collateral-info) to check if that coin is borrowable

  
> stTag| string| Whether or not it has an [special treatment label](https://www.bybit.com/en/help-center/article/Bybit-Special-Treatment-ST-Label-Management-Rules). `0`: false, `1`: true   
> lotSizeFilter| Object| Size attributes   
>> basePrecision| string| The precision of base coin   
>> quotePrecision| string| The precision of quote coin   
>> minOrderQty| string| Minimum order quantity, deprecated, no longer check `minOrderQty`, check `minOrderAmt` instead  
>> maxOrderQty| string| Maximum order quantity, deprecated, please refer to `maxLimitOrderQty`, `maxMarketOrderQty` based on order type   
>> minOrderAmt| string| Minimum order amount   
>> maxOrderAmt| string| Maximum order amount, deprecated, no longer check `maxOrderAmt`, check `maxLimitOrderQty` and `maxMarketOrderQty` instead  
>> maxLimitOrderQty| string| Maximum Limit order quantity   
>> maxMarketOrderQty| string| Maximum Market order quantity   
>> postOnlyMaxLimitOrderSize | string| Maximum limit order size for Post-only and RPI orders   
> priceFilter| Object| Price attributes   
>> tickSize| string| The step to increase/reduce order price   
> riskParameters| Object| Risk parameters for limit order price, refer to [announcement](https://announcements.bybit.com/en/article/title-adjustments-to-bybit-s-spot-trading-limit-order-mechanism-blt786c0c5abf865983/)  
>> priceLimitRatioX| string| Ratio X  
>> priceLimitRatioY| string| Ratio Y  
> isPublicRpi | boolean| Whether RPI Is Openly Provided to Market Makers or not.

  * true: RPI Is Openly Provided to Market Makers
  * false: RPI Is Not Openly Provided to Market Makers

  
> myRpiPermission | boolean| Whether the Current User Has RPI Permissions or not

  * true: Has RPI Permissions
  * false: Does Not Have RPI Permissions

  
  
* * *

### Request Example​

  * Linear
  * Spot



  * HTTP


    
    
    GET /v5/account/instruments-info?category=linear&symbol=1000000BABYDOGEUSDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    

  * HTTP


    
    
    GET /v5/account/instruments-info?category=spot&symbol=BTCUSDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    

### Response Example​

  * Linear
  * Spot


    
    
    // official USDT Perpetual instrument structure  
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "category": "linear",  
            "list": [  
                {  
                    "symbol": "1000000BABYDOGEUSDT",  
                    "contractType": "LinearPerpetual",  
                    "status": "Trading",  
                    "baseCoin": "1000000BABYDOGE",  
                    "quoteCoin": "USDT",  
                    "launchTime": "1718098044000",  
                    "deliveryTime": "0",  
                    "deliveryFeeRate": "",  
                    "priceScale": "7",  
                    "leverageFilter": {  
                        "minLeverage": "1",  
                        "maxLeverage": "25.00",  
                        "leverageStep": "0.01"  
                    },  
                    "priceFilter": {  
                        "minPrice": "0.0000001",  
                        "maxPrice": "1.9999998",  
                        "tickSize": "0.0000001"  
                    },  
                    "lotSizeFilter": {  
                        "maxOrderQty": "60000000",  
                        "minOrderQty": "100",  
                        "qtyStep": "100",  
                        "postOnlyMaxOrderQty": "60000000",  
                        "maxMktOrderQty": "12000000",  
                        "minNotionalValue": "5"  
                    },  
                    "unifiedMarginTrade": true,  
                    "fundingInterval": 240,  
                    "settleCoin": "USDT",  
                    "copyTrading": "none",  
                    "upperFundingRate": "0.02",  
                    "lowerFundingRate": "-0.02",  
                    "isPreListing": false,  
                    "preListingInfo": null,  
                    "riskParameters": {  
                        "priceLimitRatioX": "0.15",  
                        "priceLimitRatioY": "0.3"  
                    },  
                    "displayName": "",  
                    "symbolType": "innovation",  
                    "myRpiPermission": true,  
                    "isPublicRpi": true  
                }  
            ],  
            "nextPageCursor": ""  
        },  
        "retExtInfo": {},  
        "time": 1760510800094  
    }  
      
    
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "category": "spot",  
            "list": [  
                {  
                    "symbol": "BTCUSDT",  
                    "baseCoin": "BTC",  
                    "quoteCoin": "USDT",  
                    "innovation": "0",  
                    "status": "Trading",  
                    "marginTrading": "utaOnly",  
                    "stTag": "0",  
                    "lotSizeFilter": {  
                        "basePrecision": "0.000001",  
                        "quotePrecision": "0.00000001",  
                        "minOrderQty": "0.000001",  
                        "maxOrderQty": "17000",  
                        "minOrderAmt": "5",  
                        "maxOrderAmt": "1999999999",  
                        "maxLimitOrderQty": "17000",  
                        "maxMarketOrderQty": "8500",  
                        "postOnlyMaxLimitOrderSize":"60000"  
                    },  
                    "priceFilter": {  
                        "tickSize": "0.01"  
                    },  
                    "riskParameters": {  
                        "priceLimitRatioX": "0.05",  
                        "priceLimitRatioY": "0.05"  
                    },  
                    "symbolType": "",  
                    "isPublicRpi": true,  
                    "myRpiPermission": true  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1760682563907  
    }  
    

[PreviousGet Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info)[NextManual Borrow](https://bybit-exchange.github.io/docs/v5/account/borrow)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


