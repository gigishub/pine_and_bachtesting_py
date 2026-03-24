# Get Quotes

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/quote-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Get Quotes



On this page

# Get Quotes

Obtain historical quote information. **Up to 50 requests per second**

info

  * Obtain historical quotes. This data is not real-time. Please see Get RFQs (real-time).
  * If both quoteId and quoteLinkId are passed, only both is considered.
  * If both rfqId and rfqLinkId are passed, only rfqId is considered.
  * Sorted in descending order by createdAt.



### HTTP Request​

GET`/v5/rfq/quote-list`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
rfqId|  _false_|  string| Inquiry ID  
quoteId|  _false_|  string| Quote ID  
quoteLinkId|  _false_|  string| Custom quote ID. If traderType is `request` this field is invalid  
traderType| false| string| Trader type, `quote` , `request`. Default: `quote`  
status| false| string| Status of the RFQ: `Active` `Canceled` `PendingFill` `Filled` `Expired` `Failed`  
limit| false| integer| Return the number of items. [`1`, `100`]. Default: `50`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| Object|   
> cursor| string| Refer to the `cursor` request parameter  
> list| array| An array of quotes  
>> rfqId| string| Inquiry ID  
>> rfqLinkId| string| Custom RFQ ID. Not publicly disclosed.  
>> quoteId| string| Quote ID  
>> quoteLinkId| string| Custom quote ID. Not publicly disclosed.  
>> expiresAt| string| The quote's expiration time (ms)  
>> deskCode| string| The unique identification code of the inquiring party, which is not visible when anonymous was set to `true` when the quote was created  
>> status| string| Status of the RFQ: `Active` `PendingFill` `Canceled` `Filled` `Expired` `Failed`  
>> execQuoteSide| string| Execute the quote direction, `Buy` or `Sell` . When the quote direction is `Buy` , for maker, the execution direction is the same as the direction in legs, and opposite for taker. Conversely, the same applies  
>> createdAt| string| Time (ms) when the trade is created in epoch, such as 1650380963  
>> updatedAt| string| Time (ms) when the trade is updated in epoch, such as 1650380964  
>> quoteBuyList| array of objects| Quote `Buy` Direction  
>>> category| string| Product type: `spot`,`linear`,`option`  
>>> symbol| string| The unique instrument ID  
>>> price| string| Order price in the quote currency of the instrument.  
>>> qty| string| Order quantity of the instrument.  
>> quoteSellList| array of objects| Quote `Sell` Direction  
>>> category| string| Product type: `spot`,`linear`,`option`  
>>> symbol| string| The unique instrument ID  
>>> price| string| Order price in the quote currency of the instrument.  
>>> qty| string| Order quantity of the instrument.  
  
### Request Example​
    
    
    GET /v5/rfq/quote-list HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676430842094  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "cursor": "",  
            "list": [  
                {  
                    "rfqLinkId": "",  
                    "rfqId": "175740578143743543930777169307022",  
                    "quoteId": "1757405933130044334361923221559805",  
                    "quoteLinkId": "",  
                    "expiresAt": "1757405993126",  
                    "status": "Expired",  
                    "deskCode": "test0904",  
                    "execQuoteSide": "",  
                    "quoteBuyList": [  
                        {  
                            "category": "linear",  
                            "symbol": "BTCUSDT",  
                            "price": "113790",  
                            "qty": "0.5"  
                        }  
                    ],  
                    "quoteSellList": [  
                        {  
                            "category": "linear",  
                            "symbol": "BTCUSDT",  
                            "price": "110500",  
                            "qty": "0.5"  
                        }  
                    ],  
                    "createdAt": "1757405933126",  
                    "updatedAt": "1757405999156"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1757406548275  
    }  
    

[PreviousGet Quotes (real-time)](https://bybit-exchange.github.io/docs/v5/rfq/trade/quote-realtime)[NextGet Trade History](https://bybit-exchange.github.io/docs/v5/rfq/trade/trade-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


