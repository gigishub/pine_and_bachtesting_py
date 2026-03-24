# Demo Trading Service

> **Source:** https://bybit-exchange.github.io/docs/v5/demo

---

  * [](https://bybit-exchange.github.io/docs/)
  * Demo Trading Service



On this page

# Demo Trading Service

## Introduction​

Bybit v5 Open API supports demo trading account, but please note **not** every API is available for demo trading account because demo trading service is mainly for trading experience purpose, so that it does not have a complete function compared with the real trading service.

## Create API Key​

  1. You need to log in to your [mainnet](https://www.bybit.com/) account;
  2. Switch to `Demo Trading`, please note it is an independent account for demo trading only, and it has its own user ID;
  3. Hover the mouse on user avatar, then click "API" to generate api key and secret;



## Usage rules​

  * Basic trading rules are the same as real trading
  * Orders generated in demo trading keep **7 days**
  * Default rate limit, not upgradable



## Domain​

**Mainnet Demo Trading URL:**  
Rest API: `https://api-demo.bybit.com`  
Websocket: `wss://stream-demo.bybit.com` (note that this only supports the private streams; public data is identical to that found on mainnet with `wss://stream.bybit.com`; WS Trade is not supported)

## Tips​

  * Please note that demo trading is an isolated module. When you create the key from demo trading, please use above domain to connect.
  * By the way, it is meaningless to use demo trading service in the [testnet](https://testnet.bybit.com) website, so do not create a key from Testnet demo trading.



## Available API List​

Cateogory| Title| Endpoint  
---|---|---  
Market| All| all endpoints  
Trade| [Place Order](https://bybit-exchange.github.io/docs/v5/order/create-order)| /v5/order/create  
[Amend Order](https://bybit-exchange.github.io/docs/v5/order/amend-order)| /v5/order/amend  
[Cancel order](https://bybit-exchange.github.io/docs/v5/order/cancel-order)| /v5/order/cancel  
[Get Open Orders](https://bybit-exchange.github.io/docs/v5/order/open-order)| /v5/order/realtime  
[Cancel All Orders](https://bybit-exchange.github.io/docs/v5/order/cancel-all)| /v5/order/cancel-all  
[Get Order History](https://bybit-exchange.github.io/docs/v5/order/order-list)| /v5/order/history  
[Get Trade History](https://bybit-exchange.github.io/docs/v5/order/execution)| /v5/execution/list  
[Batch Place Order](https://bybit-exchange.github.io/docs/v5/order/batch-place)| /v5/order/create-batch (linear,option)  
[Batch Amend Order](https://bybit-exchange.github.io/docs/v5/order/batch-amend)| /v5/order/amend-batch (linear,option)  
[Batch Cancel Order](https://bybit-exchange.github.io/docs/v5/order/batch-cancel)| /v5/order/cancel-batch (linear,option)  
Position| [Get Position Info](https://bybit-exchange.github.io/docs/v5/position)| /v5/position/list  
[Set Leverage](https://bybit-exchange.github.io/docs/v5/position/leverage)| /v5/position/set-leverage  
[Switch Position Mode](https://bybit-exchange.github.io/docs/v5/position/position-mode)| /v5/position/switch-mode  
[Set Trading Stop](https://bybit-exchange.github.io/docs/v5/position/trading-stop)| /v5/position/trading-stop  
[Set Auto Add Margin](https://bybit-exchange.github.io/docs/v5/position/auto-add-margin)| /v5/position/set-auto-add-margin  
[Add Or Reduce Margin](https://bybit-exchange.github.io/docs/v5/position/manual-add-margin)| /v5/position/add-margin  
[Get Closed PnL](https://bybit-exchange.github.io/docs/v5/position/close-pnl)| /v5/position/closed-pnl  
Account| [Get Wallet Balance](https://bybit-exchange.github.io/docs/v5/account/wallet-balance)| /v5/account/wallet-balance  
[Get Borrow History](https://bybit-exchange.github.io/docs/v5/account/borrow-history)| /v5/account/borrow-history  
[Set Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/set-collateral)| /v5/account/set-collateral-switch  
[Get Collateral Info](https://bybit-exchange.github.io/docs/v5/account/collateral-info)| /v5/account/collateral-info  
[Get Coin Greeks](https://bybit-exchange.github.io/docs/v5/account/coin-greeks)| /v5/asset/coin-greeks  
[Get Account Info](https://bybit-exchange.github.io/docs/v5/account/account-info)| /v5/account/info  
[Get Transaction Log](https://bybit-exchange.github.io/docs/v5/account/transaction-log)| /v5/account/transaction-log  
[Set Margin Mode](https://bybit-exchange.github.io/docs/v5/account/set-margin-mode)| /v5/account/set-margin-mode  
[Set Spot Hedging](https://bybit-exchange.github.io/docs/v5/account/set-spot-hedge)| /v5/account/set-hedging-mode  
Asset| [Get Delivery Record](https://bybit-exchange.github.io/docs/v5/asset/delivery)| /v5/asset/delivery-record  
[Get USDC Session Settlement](https://bybit-exchange.github.io/docs/v5/asset/settlement)| /v5/asset/settlement-record  
Spot Margin Trade| [Toggle Margin Trade](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode)| /v5/spot-margin-trade/switch-mode  
[Set Leverage](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage)| /v5/spot-margin-trade/set-leverage  
[Get Status And Leverage](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status)| /v5/spot-margin-uta/status  
[WS Private](https://bybit-exchange.github.io/docs/v5/websocket/private/position)| order,execution,position,wallet,greeks| /v5/private  
  
### Request Demo Trading Funds​

> API rate limit: 1 req per minute

#### HTTP Request​

POST`/v5/account/demo-apply-money`Copy

#### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
adjustType| false| integer| `0`(default): add demo funds; `1`: reduce demo funds  
utaDemoApplyMoney| false| array|   
> coin| false| string| Applied coin, supports `BTC`, `ETH`, `USDT`, `USDC`  
> amountStr| false| string| Applied amount, the max applied amount in each request 

  * `BTC`: "15"
  * `ETH`: "200"
  * `USDT`: "100000"
  * `USDC`: "100000"

  
  
#### Request Example​
    
    
    POST /v5/account/demo-apply-money HTTP/1.1  
    Host: api-demo.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1711420489915  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "adjustType": 0,  
        "utaDemoApplyMoney": [  
            {  
                "coin": "USDT",  
                "amountStr": "109"  
            },  
            {  
                "coin": "ETH",  
                "amountStr": "1"  
            }  
        ]  
    }  
    

### Create Demo Account​

> API rate limit: 5 req per second  
>  Permission: AccountTransfer, SubMemberTransfer or SubMemberTransferList

info

  * Use product main account or sub account key to call the interface, the domain needs to be "api.bybit.com"
  * If demo account is existing, this POST request will return the existing UID directly
  * If using main account key to call, then the generated demo account is under the main account
  * If using sub account key to call, then the generated demo account is under the sub account



#### HTTP Request​

POST`/v5/user/create-demo-member`Copy

#### Request Parameters​

None

#### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subMemberId| string| Demo account ID  
  
#### Request Example​
    
    
    POST /v5/user/create-demo-member HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728460942776  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 2  
      
    {}  
    

### [Create Demo Account API Key](https://bybit-exchange.github.io/docs/v5/user/create-subuid-apikey)​

info

  * Input generated demo account uid
  * Use **production main account key** to call the interface, the domain needs to be **"api.bybit.com"**



### [Update Demo Account API Key](https://bybit-exchange.github.io/docs/v5/user/modify-sub-apikey)​

info

  * Use **production main account key** to call the interface, the domain needs to be **"api.bybit.com"**



### [Get Demo Account API Key Info](https://bybit-exchange.github.io/docs/v5/user/apikey-info)​

info

  * Use **accordingly demo account key** to call the interface, the domain needs to be **"api-demo.bybit.com"**



### [Delete Demo Account API Key](https://bybit-exchange.github.io/docs/v5/user/rm-sub-apikey)​

info

  * Use **production main account key** to call the interface, the domain needs to be **"api.bybit.com"**



[ PreviousHow To Start Copy Trading](https://bybit-exchange.github.io/docs/v5/copytrade)[NextGet System Status](https://bybit-exchange.github.io/docs/v5/system-status)

  * Introduction
  * Create API Key
  * Usage rules
  * Domain
  * Tips
  * Available API List
    * Request Demo Trading Funds
      * HTTP Request
      * Request Parameters
      * Request Example
    * Create Demo Account
      * HTTP Request
      * Request Parameters
      * Response Parameters
      * Request Example
    * Create Demo Account API Key
    * Update Demo Account API Key
    * Get Demo Account API Key Info
    * Delete Demo Account API Key


