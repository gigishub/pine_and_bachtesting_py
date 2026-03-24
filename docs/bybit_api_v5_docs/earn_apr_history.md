# Get APR History

> **Source:** https://bybit-exchange.github.io/docs/v5/earn/apr-history

---

  * [](https://bybit-exchange.github.io/docs/)
  * Earn
  * Get APR History



On this page

# Get APR History

info

Does not need authentication.

note

You can query up to 6 months of historical APR data.

### HTTP Request​

GET`/v5/earn/apr-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| `FlexibleSaving`,`OnChain`  
productId| **true**|  string| Product ID, from [GET /v5/earn/product](https://bybit-exchange.github.io/docs/v5/earn/product-info)  
startTime| false| integer| Start timestamp (ms). If neither `startTime` nor `endTime` is provided, the last 7 days of data is returned by default  
endTime| false| integer| End timestamp (ms). The difference between `endTime` and `startTime` must be less than or equal to 182 days  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> timestamp| string| Unix timestamp (ms) at midnight of the corresponding date  
> apr| string| APR, decimal string, e.g., `"0.055"` represents 5.5%  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/earn/apr-history?productId=8&category=OnChain HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "list": [  
                {  
                    "timestamp": "1773705600000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773619200000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773532800000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773446400000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773360000000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773273600000",  
                    "apr": "15%"  
                },  
                {  
                    "timestamp": "1773187200000",  
                    "apr": "15%"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1773741812091  
    }  
    

[PreviousGet Hourly Yield History](https://bybit-exchange.github.io/docs/v5/earn/hourly-yield)[NextSBE Basic Information](https://bybit-exchange.github.io/docs/v5/sbe/sbe-basic-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


