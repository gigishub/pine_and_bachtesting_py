# Introduction

> **Source:** https://bybit-exchange.github.io/docs/v5/intro

---

On this page

# Introduction

## Overview​

The V5 API brings uniformity and efficiency to Bybit's product lines, unifying Spot, Derivatives, and Options in one set of specifications.

## Current API Coverage​

OpenAPI Version| Account Type| Linear| Inverse| Spot| Options  
---|---|---|---|---|---  
**USDT Perpetual**| **USDC Perpetual**| **USDT Futures**| **Perpetual**| **Futures**  
V5| Unified trading account| ✓| ✓| ✓| ✓| ✓| ✓| ✓  
  
## Key Upgrades​

### Product Lines Alignment​

V5 unifies the APIs of various trading products into one, providing users the capability to trade Spot, Derivatives and Options contracts with a single API by distinguishing transactions through different order parameters. Consequently, there is no need to switch between multiple interfaces when building different products – regardless of tasks such as order management or querying wallet data – as the same API can be used to request and return results.

The global dictionary in V5 is uniquely defined to avoid scenarios where different terms are used for the same purposes, or where a single term has multiple references. This simplifies the troubleshooting process for users.

For example, when creating an order with `POST /v5/order/create`, users can specify `category=spot/linear/inverse/option` to create multiple orders across different products.

### Enhance Capital Efficiency​

V5 provides users the ability to upgrade accounts to a unified account, allowing for sharing and cross-utilization of funds across Spot, USDT Perpetual, USDC Perpetual and Options contracts. Users are also able to offset profit and losses across different positions, thus further enhancing capital efficiency.

### Unified Account Borrowing​

API V5 supports borrowing across a unified account mode. Users can pledge multiple assets as collateral to obtain margin for trading across different products.

_For example_ : Trader Alice opens a USDT-settled BTCUSDT contract position while holding only BTC assets. If a floating loss is incurred, a debt will be recorded and interest will be charged hourly.

### Portfolio Margin Mode​

Unified Accounts now support combined margin between Inverse Perpetuals, Inverse Futures, USDT Perpetual, USDC Perpetual, USDC Futures and Options.

### API Interface Naming Standard​

API V5 offers clearer path definitions for improved clarity and reduced ambiguity. The new version divides the API path into market data, order management, position management, account management, asset management, and more modules.

> {host}/{version}/{product}/{module}  
>  Example: api.bybit.com/v5/market/recent-trade

Address Segment| Description  
---|---  
v5/market/| Candlestick, orderbook, ticker, platform transaction data, underlying financial rules, risk control rules  
v5/order/| Order management  
v5/position/| Position management  
v5/account/| Single account operations only – unified funding account, rates, etc.  
v5/asset/| Operations across multiple accounts – asset management, fund management, etc.  
v5/spot-lever-token/| Obtain quotes from Leveraged Tokens on Spot, and to exercise purchase and redeem functions  
v5/spot-margin-trade/| Manage Margin Trading on Spot  
  
### Cancellation of Orders by Settlement Currency​

Users can cancel all Derivatives orders settled by the same currency with `settleCoin`.

### Addition of Insurance Fund Interface​

This interface addition allows for queries of the insurance pool, which users can use to check for any insurance fund updates on the Bybit platform.

### Readability Improvements to API Documentation​

The API documentation has been revised and proofread to improve clarity and reduce confusion. Any parts of the previous documentation that were not clear have been revised to provide better explanations.

  * Overview
  * Current API Coverage
  * Key Upgrades
    * Product Lines Alignment
    * Enhance Capital Efficiency
    * Unified Account Borrowing
    * Portfolio Margin Mode
    * API Interface Naming Standard
    * Cancellation of Orders by Settlement Currency
    * Addition of Insurance Fund Interface
    * Readability Improvements to API Documentation


