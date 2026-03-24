# Convert Guideline

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert/guideline

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert
  * Guideline



On this page

# Convert Guideline

info

  * All convert API endpoints need authentication
  * API key permission: "Exchange"



## Workflow​

### Step 1: [Get Convert Coin List](https://bybit-exchange.github.io/docs/v5/asset/convert/convert-coin-list)​

  * Query the supported coin list of convert to/from in the different account types.
  * The balance is also given when querying the convert from coin list.



### Step 2: [Request a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote)​

  * Select fromCoin, toCoin, acccountType, define the qty of fromCoin to get a quote
  * There is balance pre-check at this stage.



### Step 3: [Confirm a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert/confirm-quote)​

  * Confirm your quote in the valid time slot (15 secs). Once confirmed, the system processes your transactions.
  * This operation is async, so it can be failed if you have funds transferred out. Please check the transaction result by step 4.



### Step 4: [Get Convert Status](https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result)​

Check the final status of the coin convert.

## Error​

Code| Msg| Comment  
---|---|---  
32024| exceeds exchange threshold| If the real-time exchange rate (comfirm quote) and quoted rate (apply quote) differ by more than 0.5%, your convert will be rejected/cancelled  
790000| system error, please try again later|   
700000| parameter error|   
700001| quote fail: no deler can be used|   
700002| quote fial: not support quote type| when requestCoin=toCoin during request quote stage  
700003| order status not allowed|   
700004| order does not exit| 1\. check if quoteTxId is correct; 2. check if quoteTxId is matched with accountType  
700005| Your available balance is insufficient or wallet does not exist|   
700006| Low amount limit| the request amount cannot be smaller than minFromCoinLimit  
700007| Large amount limit| the request amount cannot be larger than maxFromCoinLimit  
700008| quote fail: price time out| 1\. the quote is expired; 2. The quoteTxId does not exist  
700009| quoteTxId has already been used| get this error when you call confirm quote more than once before expiry time  
700010| INS loan user cannot perform conversion|   
700011| illegal operation| when request a quote with user A, but confirm the quote with user B  
  
## API Rate Limit​

Method| Path| Limit| Upgradable  
---|---|---|---  
GET| /v5/asset/exchange/query-coin-list| 100 req/s| N  
POST| /v5/asset/exchange/quote-apply| 50 req/s| N  
POST| /v5/asset/exchange/convert-execute| 50 req/s| N  
GET| /v5/asset/exchange/convert-result-query| 100 req/s| N  
GET| /v5/asset/exchange/query-convert-history| 100 req/s| N  
  
[PreviousCancel Withdrawal](https://bybit-exchange.github.io/docs/v5/asset/withdraw/cancel-withdraw)[NextGet Convert Coin List](https://bybit-exchange.github.io/docs/v5/asset/convert/convert-coin-list)

  * Workflow
    * Step 1: Get Convert Coin List
    * Step 2: Request a Quote
    * Step 3: Confirm a Quote
    * Step 4: Get Convert Status
  * Error
  * API Rate Limit


