# Request a Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/quote-apply

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Request a Quote



On this page

# Request a Quote

info

Request by the master UID's api key only

### HTTP Request​

POST`/v5/fiat/quote-apply`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
fromCoin| **true**|  string| Convert from coin (coin to sell)  
fromCoinType| **true**|  string| `fiat` or `crypto`  
toCoin| **true**|  string| Convert to coin (coin to buy)  
toCoinType| **true**|  string| `fiat` or `crypto`  
requestAmount| **true**|  string| request coin amount (the amount you want to sell)  
requestCoinType| false| string| coinType you want to sell, `fiat` or `crypto`, default to `fiat`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
quoteTxId| string| Quote transaction ID. It is system generated, and it is used to confirm quote  
exchangeRate| string| Exchange rate  
fromCoin| string| Convert from coin (coin to sell)  
fromCoinType| string| From coin type. `fiat` or `crypto`  
toCoin| string| Convert to coin (coin to buy)  
toCoinType| string| To coin type. `fiat` or `crypto`  
fromAmount| string| From coin amount (amount to sell)  
toAmount| string| To coin amount (amount to buy according to exchange rate)  
expiredTime| string| The expiry time for this quote (milliseconds)  
  
### Request Example​

  * HTTP


    
    
    POST /v5/fiat/quote-apply HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720071077014  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    Content-Type: application/json  
    Content-Length: 172  
      
    {  
        "fromCoin": "ETH",  
        "fromCoinType": "fiat",  
        "toCoin": "BTC",  
        "toCoinType": "crypto",  
        "requestAmount": "0.1",  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "quoteTaxId": "QuoteTaxId123456",  
            "exchangeRate": "1.0",  
            "fromCoin": "ETH",  
            "fromCoinType": "fiat",  
            "toCoin": "BTC",  
            "toCoinType": "crypto",  
            "fromAmount": "0.1",  
            "toAmount": "0.1",  
            "expireTime": "1764561045346"  
        }  
    }  
    

[PreviousGet Reference Price](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/reference-price)[NextConfirm a Quote](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/confirm-quote)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


