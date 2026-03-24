# Get Leveraged Token Market

> **Source:** https://bybit-exchange.github.io/docs/v5/lt/leverage-token-reference

---

On this page

# Get Leveraged Token Market

Get leverage token market information

### HTTP Request​

GET`/v5/spot-lever-token/reference`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
ltCoin| **true**|  string| Abbreviation of the LT, such as BTC3L  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
ltCoin| string| Abbreviation of the LT, such as BTC3L  
nav| string| net value  
navTime| string| Update time for net asset value (in milliseconds and UTC time zone)  
circulation| string| Circulating supply in the secondary market  
basket| string| basket  
leverage| string| Real leverage calculated by last traded price  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/spot-lever-token/reference?ltCoin=BTC3S HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_leveraged_token_market(  
        ltCoin="BTC3L",  
    ))  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "basket": "-132.460000082171973364",  
            "circulation": "30097.901900052619091704",  
            "leverage": "-2.666924651755770729",  
            "ltCoin": "BTC3S",  
            "nav": "27.692082719770373048",  
            "navTime": "1672991679858"  
        },  
        "retExtInfo": {},  
        "time": 1672991679937  
    }  
    

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


