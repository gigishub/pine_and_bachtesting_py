# Get Product Info

> **Source:** https://bybit-exchange.github.io/docs/v5/earn/product-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Earn
  * Get Product Info



On this page

# Get Product Info

info

Does not need authentication.

[Bybit Saving FAQ](https://www.bybit.com/en/help-center/article/FAQ-Bybit-Savings)

### HTTP Request​

GET`/v5/earn/product`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| `FlexibleSaving`,`OnChain`  
**Remarks** : currently, only flexible savings and on chain is supported  
coin| false| string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> category| string| `FlexibleSaving`,`OnChain`  
> estimateApr| string| Estimated APR, e.g., `3%`, `4.25%`  
**Remarks** : 1)The Est. APR provides a dynamic preview of your potential returns, updated every 10 minutes in response to market conditions.   
2) Please note that this is an estimate and may differ from the actual APR you will receive.  
3) Platform Reward APRs are not shown  
> coin| string| Coin name  
> minStakeAmount| string| Minimum stake amount  
> maxStakeAmount| string| Maximum stake amount  
> precision| string| Amount precision  
> productId| string| Product ID  
> status| string| `Available`, `NotAvailable`  
> bonusEvents| Array| Bonus  
>> apr| string| Yesterday's Rewards APR  
>> coin| string| Reward coin  
>> announcement| string| Announcement link  
> minRedeemAmount| string| Minimum redemption amount. Only has value in Onchain LST mode (coin != swapCoin)  
> maxRedeemAmount| string| Maximum redemption amount. Only has value in Onchain LST mode (coin != swapCoin)  
> duration| string| `Fixed`,`Flexible`. Product Type  
> term| int| Unit: Day. Only when duration = `Fixed` for OnChain  
> swapCoin| string| swap coin. Only has value in Onchain LST mode (coin != swapCoin)  
> swapCoinPrecision| string| swap coin precision. Only has value in Onchain LST mode (coin != swapCoin)  
> stakeExchangeRate| string| Estimated stake exchange rate. Only has value in Onchain LST mode (coin != swapCoin)  
> redeemExchangeRate| string| Estimated redeem exchange rate. Only has value in Onchain LST mode (coin != swapCoin)  
> rewardDistributionType| string| `Simple`: Simple interest, `Compound`: Compound interest, `Other`: LST. Only has value for Onchain  
> rewardIntervalMinute| int| Frequency of reward distribution (minutes)  
> redeemProcessingMinute| string| Estimated redemption minutes  
> stakeTime| string| Staking on-chain time, in milliseconds  
> interestCalculationTime| string| Interest accrual time, in milliseconds  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/earn/product?category=FlexibleSaving&coin=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_earn_product_info(  
        category="FlexibleSaving",  
        coin="BTC",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "list": [  
                {  
                    "category": "FlexibleSaving",  
                    "estimateApr": "3%",  
                    "coin": "BTC",  
                    "minStakeAmount": "0.001",  
                    "maxStakeAmount": "10",  
                    "precision": "8",  
                    "productId": "430",  
                    "status": "Available",  
                    "bonusEvents": [],  
                    "minRedeemAmount": "",  
                    "maxRedeemAmount": "",  
                    "duration": "",  
                    "term": 0,  
                    "swapCoin": "",  
                    "swapCoinPrecision": "",  
                    "stakeExchangeRate": "",  
                    "redeemExchangeRate": "",  
                    "rewardDistributionType": "",  
                    "rewardIntervalMinute": 0,  
                    "redeemProcessingMinute": 0,  
                    "stakeTime": "",  
                    "interestCalculationTime": ""  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1739935669110  
    }  
    

[PreviousGet Issued Voucher](https://bybit-exchange.github.io/docs/v5/broker/reward/get-issue-voucher)[NextStake / Redeem](https://bybit-exchange.github.io/docs/v5/earn/create-order)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


