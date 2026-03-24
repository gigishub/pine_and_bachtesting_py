# Get Announcement

> **Source:** https://bybit-exchange.github.io/docs/v5/announcement

---

  * [](https://bybit-exchange.github.io/docs/)
  * Get Announcement



On this page

# Get Announcement

### HTTP Request​

GET`/v5/announcements/index`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[locale](https://bybit-exchange.github.io/docs/v5/enum#locale)| **true**|  string| Language symbol  
[type](https://bybit-exchange.github.io/docs/v5/enum#announcementtype)| false| string| Announcement type  
[tag](https://bybit-exchange.github.io/docs/v5/enum#announcementtag)| false| string| Announcement tag  
page| false| integer| Page number. Default: `1`  
limit| false| integer| Limit for data size per page. Default: `20`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
total| integer| Total records  
list| array| Object  
> title| string| Announcement title  
> description| string| Announcement description  
> type| Object|   
>> title| string| The title of announcement type  
>> [key](https://bybit-exchange.github.io/docs/v5/enum#announcementtype)| string| The key of announcement type  
> [tags](https://bybit-exchange.github.io/docs/v5/enum#announcementtag)| array<string>| The tag of announcement  
> url| string| Announcement url  
> dateTimestamp| number| Timestamp that author fills  
> startDataTimestamp| number| The start timestamp (ms) of the event, only valid when `list.type.key == "latest_activities"`  
> endDataTimestamp| number| The end timestamp (ms) of the event, only valid when `list.type.key == "latest_activities"`  
> publishTime| number| The published timestamp for the announcement  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Java


    
    
    GET /v5/announcements/index?locale=en-US&limit=1 HTTP/1.1  
    Host: api.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_announcement(  
        locale="en-US",  
        limit=1,  
    ))  
    
    
    
    import com.bybit.api.client.domain.announcement.LanguageSymbol;  
    import com.bybit.api.client.domain.market.request.MarketDataRequest;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncMarketDataRestClient();  
    var announcementInfoRequest = MarketDataRequest.builder().locale(LanguageSymbol.EN_US).build();  
    client.getAnnouncementInfo(announcementInfoRequest, System.out::println);  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "total": 735,  
            "list": [  
                {  
                    "title": "New Listing: Arbitrum (ARB) — Deposit, Trade and Stake ARB to Share a 400,000 USDT Prize Pool!",  
                    "description": "Bybit is excited to announce the listing of ARB on our trading platform!",  
                    "type": {  
                        "title": "New Listings",  
                        "key": "new_crypto"  
                    },  
                    "tags": [  
                        "Spot",  
                        "Spot Listings"  
                    ],  
                    "url": "https://announcements.bybit.com/en-US/article/new-listing-arbitrum-arb-deposit-trade-and-stake-arb-to-share-a-400-000-usdt-prize-pool--bltf662314c211a8616/",  
                    "dateTimestamp": 1679045608000,  
                    "startDateTimestamp": 1679045608000,  
                    "endDateTimestamp": 1679045608000  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1679415136117  
    }  
    

[PreviousIntegration Guidance](https://bybit-exchange.github.io/docs/v5/guide)[NextSelf Match Prevention](https://bybit-exchange.github.io/docs/v5/smp)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


