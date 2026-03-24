# Trade Notify

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/trade-notify

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Trade Notify



On this page

# Trade Notify

## Trade Notify​

### Webhook URL​

  * **Webhook_url** : Provided in the [trade-execute](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/confirm-quote) API.



### Webhook Method​

  * **HTTP Method** : `POST`



### Authentication​

  * Share the **IP whitelist** with each other.



### Headers​
    
    
    Content-Type: application/json  
    timestamp: xxx  
    publicKey: xxx  
    

* * *

### Request Body​

The request body is in **JSON** format with the following fields:

Field Name| Type| Description  
---|---|---  
`tradeNo`| string| Trade order number  
`status`| string| Trade status: `processing`, `success`, or `failed`  
`quoteTxId`| string| Quote transaction ID. System generated, used to confirm the quote  
`exchangeRate`| string| Exchange rate  
`fromCoin`| string| Convert from coin (coin to sell)  
`fromCoinType`| string| Coin type of `fromCoin`, either `fiat` or `crypto`  
`toCoin`| string| Convert to coin (coin to buy)  
`toCoinType`| string| Coin type of `toCoin`, either `fiat` or `crypto`  
`fromAmount`| string| From coin amount (amount to sell)  
`toAmount`| string| To coin amount (amount to buy according to the exchange rate)  
`createdAt`| string| Trade created time  
      
    
      
    

[PreviousGet Balance](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/balance-query)[NextSign Agreement](https://bybit-exchange.github.io/docs/v5/user/sign-agreement)

  * Trade Notify
    * Webhook URL
    * Webhook Method
    * Authentication
    * Headers
    * Request Body


