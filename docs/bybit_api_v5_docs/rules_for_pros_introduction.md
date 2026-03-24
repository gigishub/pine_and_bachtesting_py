# Introduction

> **Source:** https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/introduction

---

  * [](https://bybit-exchange.github.io/docs/)
  * Rate Limit
  * API Rate Limit Rules for PROs
  * Introduction



On this page

# Introduction

## API Rate Limit Rules for PROs​

Upcoming changes for pro account

Starting **August 13, 2025** , Bybit will roll out a new institutional API rate limit framework designed to enhance performance for high-frequency trading clients. The new system introduces a centralized institution-level rate cap with flexible per-UID configurations, enabling greater efficiency and scalability. Please refer to the [announcement](https://announcements.bybit.com/en/article/update-bybit-enhances-api-rate-limits-for-institutional-traders-bltbbbf60de757d074e/) for more information.

### UID-level rate limit​

Maximum limit for a single UID.

| Unified Account  
---|---  
Level\Product| **Futures**| **Option**| **Spot**  
Default| 10/s| 10/s| 20/s  
PRO1| 200/s| 200/s| 200/s  
PRO2| 400/s| 400/s| 400/s  
PRO3| 600/s| 600/s| 600/s  
PRO4| 800/s| 800/s| 800/s  
PRO5| 1000/s| 1000/s| 1000/s  
PRO6| 1200/s| 1200/s| 1200/s  
  
### Institutional-level rate limit​

Aggregate limit across all main and sub UIDs.

| Unified Account  
---|---  
Level\Product| **Futures**| **Option**| **Spot**  
PRO1| 10000/s| 10000/s| 10000/s  
PRO2| 20000/s| 20000/s| 20000/s  
PRO3| 30000/s| 30000/s| 30000/s  
PRO4| 40000/s| 40000/s| 40000/s  
PRO5| 50000/s| 50000/s| 50000/s  
PRO6| 60000/s| 60000/s| 60000/s  
  
instructions for API rate limit

  * All of the existing subaccounts still have their original API rate limits.
  * The default API rate limit for a new subaccount is not counted in the institutional-level API rate limit. 
  * The default API rate limit for a new sub is: 10/s for futures, 10/s for options, 20/s for spot.
  * If the aggregate institutional-level API rate limit is exceeded, you must reduce one or several account's API rate limit(s) first. After the API rate limit is less than the aggregate institutional API rate limit, you can increase the API rate limit of an account.



[PreviousAPI Rate Limit Rules for VIPs](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-vips)[NextSet Rate Limit](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-set)

  * API Rate Limit Rules for PROs
    * UID-level rate limit
    * Institutional-level rate limit


