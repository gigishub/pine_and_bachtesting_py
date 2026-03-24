# Get Reference Price

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/reference-price

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Get Reference Price



On this page

# Get Reference Price

### HTTP Request​

GET`/v5/fiat/reference-price`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
symbol| **true**|  string| Coin Pair, such as EUR-USDT  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Array of quotes  
> symbol| string| Trading pair symbol  
> fiat| string| Fiat currency of the trading pair (e.g: "EUR")  
> crypto| string| Cryptocurrency of the trading pair (e.g:"USDT")  
> timestamp| string| Unix timestamp  
> buys| array| Array of buy quote objects  
>> unitPrice| string| unitPrice: 1 crypto=x fiat  
>> paymentMethod| string| From coin type. `fiat` or `crypto`  
> sells| array| Array of sell quote objects  
>> unitPrice| string| unitPrice: 1 crypto=x fiat  
>> paymentMethod| string| From coin type. `fiat` or `crypto`  
  
### Request Example​

  * HTTP


    
    
    GET /v5/fiat/reference-price HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720074159814  
    X-BAPI-RECV-WINDOW: 5000  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "symbol": "EUR-USDT",  
            "fiat": "EUR",  
            "crypto": "USDT",  
            "timestamp": "1765181161",  
            "buys": [  
                {  
                    "unitPrice": "0.8581",  
                    "paymentMethod": "Cash Balance"  
                },  
                {  
                    "unitPrice": "0.9297487",  
                    "paymentMethod": "Credit Card"  
                },  
                {  
                    "unitPrice": "0.9807915",  
                    "paymentMethod": "Apple Pay"  
                },  
                {  
                    "unitPrice": "0.8631747",  
                    "paymentMethod": "Google Pay"  
                }  
            ],  
            "sells": [  
                {  
                    "unitPrice": "0.8581",  
                    "paymentMethod": "Cash Balance"  
                },  
                {  
                    "unitPrice": "0.9297487",  
                    "paymentMethod": "Credit Card"  
                },  
                {  
                    "unitPrice": "0.9807915",  
                    "paymentMethod": "Apple Pay"  
                },  
                {  
                    "unitPrice": "0.8631747",  
                    "paymentMethod": "Google Pay"  
                },  
                {  
                    "unitPrice": "0.8584759",  
                    "paymentMethod": "SEPA"  
                }  
            ]  
        }  
    }  
    

[PreviousGet Trading Pair List](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-coin-list)[NextRequest a Quote](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/quote-apply)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


