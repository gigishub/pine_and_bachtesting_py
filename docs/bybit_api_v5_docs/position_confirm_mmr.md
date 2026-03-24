# Confirm New Risk Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/position/confirm-mmr

---

  * [](https://bybit-exchange.github.io/docs/)
  * Position
  * Confirm New Risk Limit



On this page

# Confirm New Risk Limit

It is only applicable when the user is marked as only reducing positions (please see the isReduceOnly field in the [Get Position Info](https://bybit-exchange.github.io/docs/v5/position) interface). After the user actively adjusts the risk level, this interface is called to try to calculate the adjusted risk level, and if it passes (retCode=0), the system will remove the position reduceOnly mark. You are recommended to call [Get Position Info](https://bybit-exchange.github.io/docs/v5/position) to check `isReduceOnly` field.

### HTTP Request​

POST`/v5/position/confirm-pending-mmr`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`, `inverse`  
symbol| **true**|  string| Symbol name  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/confirm-pending-mmr HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1698051123673  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 53  
      
    {  
        "category": "linear",  
        "symbol": "BTCUSDT"  
    }  
    
    
    
      
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var confirmNewRiskRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").build();  
    client.confirmPositionRiskLimit(confirmNewRiskRequest, System.out::println);  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1698051124588  
    }  
    

[PreviousGet Move Position History](https://bybit-exchange.github.io/docs/v5/position/move-position-history)[NextGet Pre-upgrade Order History](https://bybit-exchange.github.io/docs/v5/pre-upgrade/order-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


