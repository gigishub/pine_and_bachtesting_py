# Introduction

> **Source:** https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/introduction

---

  * [](https://bybit-exchange.github.io/docs/)
  * Broker
  * Exchange Broker
  * Rate Limit Setup
  * Introduction



On this page

# Introduction

## API Rate Limit For Exchange Broker Client​

By default, all accounts under the Exchange Broker entity are subject to the default API rate limits. If you have special requirements based on your business needs, please contact your **account manager** to apply for a higher Exchange Broker–level cap and subaccount UID caps. Once approved, you will be able to allocate the rate limit quota across each subaccount accordingly.

instructions for API rate limit

  * All of the existing subaccounts still have their original API rate limits.
  * The default API rate limit for a new subaccount is not counted in the eb-level API rate limit. 
  * If the aggregate eb-level API rate limit is exceeded, you must reduce one or several account's API rate limit(s) first. After the API rate limit is less than the aggregate eb API rate limit cap, you can increase the API rate limit of an account.



## Default Rate limit​

| Unified Account  
---|---  
Level\Product| **Futures**| **Option**| **Spot**  
Default| 10/s| 10/s| 20/s  
  
[PreviousGet Sub Account Deposit Records](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/sub-deposit-record)[NextSet Rate Limit](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/set)

  * API Rate Limit For Exchange Broker Client
  * Default Rate limit


