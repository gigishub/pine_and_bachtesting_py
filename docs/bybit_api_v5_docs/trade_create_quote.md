# Create Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/create-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Create Quote



On this page

# Create Quote

Create a quote. **Up to 50 requests** per second. The quoting party sends a quote in response to the inquirier.

info

  * Only support UTA2.0 accounts
  * Cannot quote for your own inquiry
  * One request reports in two directions
  * You must pass at least one quoteBuyList and quoteSellList
  * If you would like to quote a spot quote, please ensure the corresponding collateral asset is enabled using [Set Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/set-collateral) or [Batch Set Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/batch-set-collateral)



### HTTP Request​

POST`/v5/rfq/create-quote`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
rfqId| **true**|  string| Inquiry ID  
quoteLinkId| false| string| Custom quote ID: 

  * The length should be between 1-32 bits 
  * Combination of letters (case sensitive) and numbers
  * An rfqLinkId expires after three months – after which it can be reused
  * Open orders must have a unique ID whereas orders that have reached a final/terminated status do not have to be unique. 

  
anonymous| false| boolean| Whether or not it is anonymous quote. The default value is `false`. When it is `true` the identity of the quoting party will not be revealed even after the transaction is concluded.  
expireIn| false| integer| Duration of the quote (in secs). [`10`, `120`]. Default: `60`  
quoteBuyList| false| array of objects| Quote direction 

  * In the `Buy` direction, for the maker (the quoting party), the execution direction is the same as the direction of the legs
  * For the taker (the inquiring party) it is opposite direction

  
> category| **true**|  string| Product type: Unified account: `spot`, `linear`,`option`  
> symbol| **true**|  string| Name of the trading contract  
> price| **true**|  string| Quote price  
quoteSellList| false| array of objects| Ask direction 

  * In the `Sell` direction, for the maker (the quoting party), the execution direction is opposite to the direction of the legs
  * For the taker (the inquiring party) it is the same direction

  
> category| **true**|  string| Product type: Unified account: `spot`, `linear`,`option`  
> symbol| **true**|  string| Name of the trading contract  
> price| **true**|  string| Quote price  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object|   
> rfqId| string| Inquiry ID  
> quoteId| string| Quote ID  
> quoteLinkId| string| Custom quote ID  
> expiresAt| string| The quote's expiration time (ms)  
> deskCode| string| Quoter's unique identification code  
> status| string| Status of quotation: `Active` `Canceled` `Filled` `Expired` `Failed`  
  
### Request Example​
    
    
    POST /v5/rfq/create-quote HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
      
    {  
      "rfqId":"1754364447601610516653123084412812",   
      "quoteBuyList": [  
            {  
                "category": "linear",  
                "symbol": "BTCUSDT",  
                "price": "106000"  
            }  
        ],  
        "quoteSellList":[  
            {  
                "category": "linear",  
                "symbol": "BTCUSDT",  
                "price": "126500"  
            }  
        ]  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "rfqId": "175740578143743543930777169307022",  
            "quoteId": "1757405933130044334361923221559805",  
            "quoteLinkId": "",  
            "expiresAt": "1757405993126",  
            "deskCode": "test0904",  
            "status": "Active"  
        },  
        "retExtInfo": {},  
        "time": 1757405933132  
    }  
    

[PreviousAccept non-LP Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/accept-other-quote)[NextExecute Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/execute-quote)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


