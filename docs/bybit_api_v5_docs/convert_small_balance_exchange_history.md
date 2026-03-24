# Get Exchange History

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/exchange-history

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert Small Balances
  * Get Exchange History



On this page

# Get Exchange History

info

  * API key permission: `Convert`
  * API rate limit: `10 req /s`
  * You can query all small-balance exchange records made via API or web/app from both the Unified and Funding wallets.



### HTTP Request​

GET`/v5/asset/covert/small-balance-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
accountType| false| string| `eb_convert_uta`, `eb_convert_funding`  
quoteId| false| string| Quote ID, highest priority when querying  
startTime| false| string| The start timestamp (ms)  
endTime| false| string| The end timestamp (ms)  
cursor| false| string| Page number  
size| false| string| Page size, default is 50, maximum is 100  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
cursor| string| Current page number  
size| string| Curreng page size  
lastPage| string| Last page number  
totalCount| string| Total number of records  
records| array<object>|   
> accountType| string| `eb_convert_uta`: unified wallet, `eb_convert_funding`: funding wallet  
> exchangeTxId| string| Exchange transaction ID  
> toCoin| string| Target currency  
> toAmount| string| Actual total amount received  
> subRecords| array<object>| details  
>> fromCoin| string| Source currency  
>> fromAmount| string| Source currency amount  
>> toCoin| string| Target currency  
>> toAmount| string| Actual amount received  
>> feeCoin| string| Exchange fee currency  
>> feeAmount| string| Exchange fee  
>> status| string| `init`, `processing`, `success`, `failure`, `partial_fulfillment`  
>> taxFeeInfo| object|   
>>> totalAmount| string| Tax fee amount  
>>> feeCoin| string| Tax fee currency  
>>> taxFeeItems| array| Tax fee items  
> status| string| `init`, `processing`, `success`, `failure`, `partial_fulfillment`  
> createdAt| string| Quote created timestamp  
> exchangeSource| string| Exchange source `small_asset_uta`, `small_asset_funding`  
> feeCoin| string| Exchange fee currency  
> totalFeeAmount| string| Total exchange fee amount  
> totalTaxFeeInfo| object|   
>> totalAmount| string| Total tax fee amount  
>> feeCoin| string| Tax fee currency  
>> taxFeeItems| array| Tax fee items  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/covert/small-balance-history?quoteId=1010075157602517596339322880&accountType=eb_convert_uta HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1766134218672  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_exchange_history_small_balance(  
        quoteId="1010075157602517596339322880",  
        accountType="eb_convert_uta",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "cursor": "1",  
            "size": "50",  
            "lastPage": "1",  
            "totalCount": "1",  
            "records": [  
                {  
                    "accountType": "eb_convert_uta",  
                    "exchangeTxId": "1010075157602517596339322880",  
                    "toCoin": "USDC",  
                    "toAmount": "0.000728325793503221",  
                    "subRecords": [  
                        {  
                            "fromCoin": "SOL",  
                            "fromAmount": "0.000003",  
                            "toCoin": "USDC",  
                            "toAmount": "0.000363439538230885",  
                            "feeCoin": "USDC",  
                            "feeAmount": "0.000007417133433283",  
                            "status": "success",  
                            "taxFeeInfo": {  
                                "totalAmount": "0",  
                                "feeCoin": "",  
                                "taxFeeItems": []  
                            }  
                        },  
                        {  
                            "fromCoin": "XRP",  
                            "fromAmount": "0.0002",  
                            "toCoin": "USDC",  
                            "toAmount": "0.000364886255272336",  
                            "feeCoin": "USDC",  
                            "feeAmount": "0.000007446658270864",  
                            "status": "success",  
                            "taxFeeInfo": {  
                                "totalAmount": "0",  
                                "feeCoin": "",  
                                "taxFeeItems": []  
                            }  
                        }  
                    ],  
                    "status": "success",  
                    "createdAt": "1766128195000",  
                    "exchangeSource": "small_asset_uta",  
                    "feeCoin": "USDC",  
                    "totalFeeAmount": "0.000014863791704147",  
                    "totalTaxFeeInfo": {  
                        "totalAmount": "0",  
                        "feeCoin": "",  
                        "taxFeeItems": []  
                    }  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1766129394948  
    }  
    

[PreviousConfirm a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/confirm-quote)[NextGet Trading Pair List](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-coin-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


