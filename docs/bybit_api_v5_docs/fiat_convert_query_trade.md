# Get Convert Status

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-trade

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Get Convert Status



On this page

# Get Convert Status

Returns the details of this convert.

### HTTP Request​

GET`/v5/fiat/trade-query`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
tradeNo| false| string| Trade order No,tradeNo or merchantRequestId must be provided  
merchantRequestId| false| string| Customised request ID,tradeNo or merchantRequestId must be provided  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object| object  
> tradeNo| string| Trade order No  
> status| string| Trade status:

  * processing
  * success
  * failed

  
> quoteTxId| string| Quote transaction ID. It is system generated, and it is used to confirm quote  
> exchangeRate| string| Exchange rate  
> fromCoin| string| Convert from coin (coin to sell)  
> fromCoinType| string| From coin type. `fiat` or `crypto`  
> toCoin| string| Convert to coin (coin to buy)  
> toCoinType| string| To coin type. `fiat` or `crypto`  
> fromAmount| string| From coin amount (amount to sell)  
> toAmount| string| To coin amount (amount to buy according to exchange rate)  
> createdAt| string| Trade created time  
> subUserId| string| The user's sub userId in bybit  
  
### Request Example​

  * HTTP


    
    
    GET /v5/fiat/trade-query?tradeNo=TradeNo123456 HTTP/1.1    
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720074159814  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "tradeNo": "TradeNo123456",  
            "status": "success",  
            "quoteTaxId": "QuoteTaxId123456",  
            "exchangeRate": "1.0",  
            "fromCoin": "GEL",  
            "fromCoinType": "fiat",  
            "toCoin": "USDT",  
            "toCoinType": "crypto",  
            "fromAmount": "100",  
            "toAmount": "100",  
            "createdAt": "1764558832014",  
            "subUserId": "123456"  
        }  
    }  
    

[PreviousConfirm a Quote](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/confirm-quote)[NextGet Convert History](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-trade-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


