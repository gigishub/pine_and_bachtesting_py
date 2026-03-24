# Create RFQ

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/create-rfq

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Create RFQ



On this page

# Create RFQ

Create RFQ. **Up to 50 requests** per second.

info

  * Only supports UTA2.0 accounts
  * Only supports full position and combined margin mode
  * Not supported by demo users
  * Cannot choose oneself as the bidder



### HTTP Request​

POST`/v5/rfq/create-rfq`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
counterparties| **true**|  array| Spread combination symbol name  
rfqLinkId| false| string| Custom RFQ ID

  * The length should be between 1-32 bits 
  * Combination of letters (case sensitive) and numbers
  * An rfqLinkId expires after three months – after which it can be reused
  * Open orders must have a unique ID whereas orders that have reached a final/terminated status do not have to be unique. 

  
anonymous| false| boolean| Whether or not it is anonymous inquiry. The default value is `false`. When it is `true` the identity of the inquiring party will not be revealed even after the transaction is concluded.  
strategyType| false| string| Strategy type, if it is a custom inquiry, strategyType is `custom`, if it is a product combination provided by the system, it is the combination type; the default is `custom`; non-custom combinations have rate optimization, currently 50%; the transaction rate between LPs is currently 30%  
list| **true**|  array of objects| Combination transaction list 

  * Use [Get RFQ Configuration](https://bybit-exchange.github.io/docs/v5/rfq/trade/rfq-config) to confirm the maximum length of the combination (`maxLegs`)
  * The base coin and settle coin of all combinations must be the same
  * Symbols under the same category must be unique

  
> category| **true**|  string| Product type: Unified account: `spot`, `linear`,`option`  
> symbol| **true**|  string| Name of the transaction contract. No inquiries are allowed in the last 30 minutes before contract settlement  
> side| **true**|  string| Inquiry transaction direction: `Buy` , `Sell`  
> qty| **true**|  string| If the number of transactions exceeds the position size, the position will then open in the reverse direction  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Order ID  
list| array of objects|   
> rfqId| string| Inquiry ID  
> rfqLinkId| string| Custom inquiry ID  
> status| string| Status of the RFQ: `Active` `Canceled` `Filled` `Expired` `Failed`  
> expiresAt| string| The inquiry's expiration time (ms)  
> deskCode| string| Inquiring party's unique identification code  
  
### Request Example​
    
    
    POST /v5/rfq/create-rfq HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
      
    {  
        "counterparties": ["LP4","LP5"],  
        "rfqLinkId":"rfq00993",  
        "anonymous": false,  
        "strategyType": "custom",  
        "list": [  
            {  
                "category": "linear",  
                "symbol": "BTCUSDT",  
                "side":"buy",  
                "qty":"2"  
            },  
            {  
                "category": "spot",  
                "symbol": "BTCUSDT",  
                "side":"buy",  
                "qty":"2"  
            },  
            {  
                "category": "option",  
                "symbol": "BTCUSDT",  
                "side":"sell",  
                "qty":"2"  
            }  
        ]  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "rfqId": "17526315514105706281",  
            "rfqLinkId": "rfq00993",  
            "status": "Active",  
            "expiresAt": "1752632151414",  
            "deskCode": "LP2"  
        },  
        "retExtInfo": {},  
        "time": 1752631551419  
    }  
    

[PreviousBasic Workflow](https://bybit-exchange.github.io/docs/v5/rfq/basic-workflow)[NextGet RFQ Configuration](https://bybit-exchange.github.io/docs/v5/rfq/trade/rfq-config)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


