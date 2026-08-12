# Ten-day strategy replay

This is an exploration run, not evidence that the strategy will make money.

## Setup

- Trading days: 10
- Stocks per day: 10
- Price resolution: one-minute IEX bars
- Buy input: price movement only
- Estimated cost: 0.05% per side
- Rising prices needed: 6
- Falling prices needed: 5
- Cache retention: 30 days

## Combined result

- Strategy return: -2.0560%
- Equal-weight buy and hold: 3.2534%
- Completed trades: 291
- Profitable trades after estimated costs: 88
- Cache hits: 11
- Downloads: 0
- Expired cache files removed: 0

## Daily results

| Day | Strategy | Buy and hold | Trades | Winners |
| --- | ---: | ---: | ---: | ---: |
| 2026-07-29 | 0.3250% | -3.0084% | 32 | 12 |
| 2026-07-30 | -0.2470% | 2.6855% | 41 | 14 |
| 2026-07-31 | -0.3071% | -1.1279% | 40 | 12 |
| 2026-08-03 | -0.3648% | 2.6882% | 33 | 11 |
| 2026-08-04 | -0.3600% | 2.2769% | 26 | 8 |
| 2026-08-05 | -0.2790% | -0.8962% | 27 | 10 |
| 2026-08-06 | -0.6660% | 0.9707% | 26 | 4 |
| 2026-08-07 | -0.0902% | 0.3849% | 24 | 7 |
| 2026-08-10 | 0.0482% | -0.1586% | 24 | 7 |
| 2026-08-11 | -0.1312% | -0.4537% | 18 | 3 |

## 2026-07-29

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 2 | -0.4292% | -1.0855% |
| MSFT | 3 | -0.6352% | -0.7636% |
| NVDA | 1 | -0.0948% | -2.7798% |
| AMZN | 3 | -0.6367% | -0.8605% |
| META | 4 | -0.3153% | -0.7673% |
| TSLA | 2 | 0.5095% | -2.9395% |
| INTC | 5 | 2.4526% | -5.7222% |
| MU | 5 | 2.2891% | -10.4788% |
| PLTR | 2 | 0.0260% | -1.4336% |
| TSM | 5 | 0.0842% | -3.2530% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 09:49 | 09:56 | -0.2412% | AAPL's latest price fell at least 0.3% from its recent high. |
| AAPL | 14:03 | 14:10 | -0.1885% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 13:22 | 13:26 | -0.4307% | MSFT's latest price is at least 0.3% below its buy price. |
| MSFT | 14:02 | 14:15 | 0.0044% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 14:48 | 15:00 | -0.2099% | MSFT's latest price fell at least 0.3% from its recent high. |
| NVDA | 10:53 | 11:12 | -0.0948% | NVDA's latest price fell at least 0.3% from its recent high. |
| AMZN | 12:27 | 12:35 | -0.0520% | AMZN's recent prices meet the falling-price rule. |
| AMZN | 14:03 | 14:24 | -0.4727% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 14:31 | 15:05 | -0.1129% | AMZN's latest price fell at least 0.3% from its recent high. |
| META | 10:19 | 10:25 | -0.4225% | META's latest price is at least 0.3% below its buy price. |
| META | 12:23 | 13:26 | 0.6465% | META's latest price fell at least 0.3% from its recent high. |
| META | 14:05 | 14:10 | -0.3759% | META's latest price fell at least 0.3% from its recent high. |
| META | 14:53 | 15:00 | -0.1601% | META's latest price fell at least 0.3% from its recent high. |
| TSLA | 13:15 | 13:25 | -0.3811% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 14:40 | 15:05 | 0.8940% | TSLA's latest price fell at least 0.3% from its recent high. |
| INTC | 12:20 | 12:35 | 0.9516% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 12:52 | 13:19 | 1.3320% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 13:51 | 13:56 | -0.1474% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 14:03 | 14:05 | -0.4632% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 14:40 | 14:49 | 0.7673% | INTC's latest price fell at least 0.3% from its recent high. |
| MU | 11:17 | 11:20 | -0.7495% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:22 | 12:32 | 0.9053% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:04 | 13:18 | 0.1707% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:52 | 13:55 | -0.3155% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 14:38 | 14:49 | 2.2856% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 10:35 | 10:37 | -0.4130% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 12:52 | 13:29 | 0.4409% | PLTR's latest price fell at least 0.3% from its recent high. |
| TSM | 10:03 | 10:09 | -0.2349% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 12:01 | 12:05 | -0.3893% | TSM's recent prices meet the falling-price rule. |
| TSM | 13:14 | 13:31 | -0.4324% | TSM's latest price is at least 0.3% below its buy price. |
| TSM | 13:52 | 14:20 | 0.8507% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 14:41 | 15:05 | 0.2961% | TSM's latest price fell at least 0.3% from its recent high. |

## 2026-07-30

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 3 | -0.2529% | -0.2826% |
| MSFT | 4 | 0.4163% | 3.7689% |
| NVDA | 5 | -0.2264% | 1.2866% |
| AMZN | 3 | 1.7374% | 1.0249% |
| META | 5 | -1.7255% | 1.0784% |
| TSLA | 2 | -1.2074% | 1.4751% |
| INTC | 4 | -0.1376% | 3.7408% |
| MU | 7 | -0.7546% | 10.3776% |
| PLTR | 4 | -1.2822% | 0.8365% |
| TSM | 4 | 0.9628% | 3.5484% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 10:10 | 10:13 | -0.4196% | AAPL's latest price is at least 0.3% below its buy price. |
| AAPL | 10:40 | 10:59 | 0.0343% | AAPL's recent prices meet the falling-price rule. |
| AAPL | 12:19 | 14:05 | 0.1331% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 09:36 | 09:39 | -0.7216% | MSFT's latest price is at least 0.3% below its buy price. |
| MSFT | 10:00 | 10:04 | -0.2820% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 10:28 | 10:52 | -0.0566% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 11:35 | 12:43 | 1.4897% | MSFT's latest price fell at least 0.3% from its recent high. |
| NVDA | 09:47 | 10:08 | 1.0822% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 11:06 | 11:08 | -0.4071% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 12:06 | 12:41 | -0.5325% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 13:48 | 14:20 | -0.4270% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 15:42 | 16:00 | 0.0668% | The position was marked at the market close. |
| AMZN | 09:37 | 10:04 | 1.2144% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 11:35 | 12:19 | 0.3923% | AMZN's recent prices meet the falling-price rule. |
| AMZN | 15:13 | 15:25 | 0.1240% | AMZN's recent prices meet the falling-price rule. |
| META | 09:46 | 09:48 | -0.5440% | META's latest price is at least 0.3% below its buy price. |
| META | 10:41 | 10:44 | -0.4238% | META's latest price is at least 0.3% below its buy price. |
| META | 11:05 | 11:18 | -0.4998% | META's latest price is at least 0.3% below its buy price. |
| META | 14:56 | 15:31 | -0.1523% | META's latest price fell at least 0.3% from its recent high. |
| META | 15:45 | 15:54 | -0.1167% | META's recent prices meet the falling-price rule. |
| TSLA | 09:37 | 09:38 | -0.9481% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 11:37 | 12:00 | -0.2617% | TSLA's recent prices meet the falling-price rule. |
| INTC | 09:47 | 09:53 | 0.3126% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 12:15 | 12:21 | -0.3361% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 14:47 | 14:51 | -0.3180% | INTC's recent prices meet the falling-price rule. |
| INTC | 15:03 | 15:23 | 0.2055% | INTC's latest price fell at least 0.3% from its recent high. |
| MU | 09:52 | 09:53 | -0.6635% | MU's latest price is at least 0.3% below its buy price. |
| MU | 10:24 | 10:32 | 1.0960% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 11:06 | 11:08 | -0.8665% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:05 | 12:11 | -0.0720% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 12:37 | 12:42 | -0.4683% | MU's latest price is at least 0.3% below its buy price. |
| MU | 13:08 | 13:23 | 0.7260% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:35 | 13:50 | -0.4922% | MU's latest price is at least 0.3% below its buy price. |
| PLTR | 09:46 | 09:49 | -0.5538% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 11:35 | 11:53 | -0.0917% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 12:05 | 12:32 | -0.3543% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 15:13 | 15:19 | -0.2880% | PLTR's latest price fell at least 0.3% from its recent high. |
| TSM | 09:43 | 10:07 | 1.1200% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 10:20 | 10:31 | 0.5706% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 12:05 | 12:10 | -0.3006% | TSM's recent prices meet the falling-price rule. |
| TSM | 15:13 | 15:26 | -0.4226% | TSM's latest price is at least 0.3% below its buy price. |

## 2026-07-31

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 3 | 1.0889% | 1.4594% |
| MSFT | 2 | 1.2339% | 2.1915% |
| NVDA | 6 | -0.5255% | 1.4465% |
| AMZN | 5 | 0.0771% | 2.8515% |
| META | 8 | -1.0146% | 0.9044% |
| TSLA | 4 | -1.4084% | -0.2858% |
| INTC | 3 | -0.6876% | -7.1312% |
| MU | 3 | 0.2816% | -10.5153% |
| PLTR | 2 | -0.6048% | 1.4419% |
| TSM | 4 | -1.5114% | -3.6423% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 10:23 | 10:31 | -0.3374% | AAPL's latest price fell at least 0.3% from its recent high. |
| AAPL | 14:14 | 15:40 | 0.9956% | AAPL's latest price fell at least 0.3% from its recent high. |
| AAPL | 15:45 | 15:56 | 0.4313% | AAPL's latest price fell at least 0.3% from its recent high. |
| MSFT | 11:20 | 12:05 | 1.2179% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 14:14 | 14:39 | 0.0157% | MSFT's recent prices meet the falling-price rule. |
| NVDA | 10:32 | 10:56 | 0.1151% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 11:39 | 11:47 | -0.4354% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 11:53 | 12:08 | -0.1432% | NVDA's recent prices meet the falling-price rule. |
| NVDA | 12:25 | 13:08 | 0.2896% | NVDA's recent prices meet the falling-price rule. |
| NVDA | 15:19 | 15:25 | -0.0276% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 15:46 | 16:00 | -0.3234% | NVDA's latest price fell at least 0.3% from its recent high. |
| AMZN | 09:36 | 09:40 | -0.2060% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 09:50 | 09:53 | -0.1317% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 10:27 | 10:40 | 0.2408% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 11:15 | 11:18 | -0.5230% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 11:53 | 12:29 | 0.7013% | AMZN's recent prices meet the falling-price rule. |
| META | 10:09 | 10:12 | -0.3176% | META's latest price fell at least 0.3% from its recent high. |
| META | 10:18 | 10:26 | -0.3869% | META's latest price fell at least 0.3% from its recent high. |
| META | 10:42 | 11:09 | 0.4606% | META's latest price fell at least 0.3% from its recent high. |
| META | 11:36 | 11:49 | -0.0256% | META's recent prices meet the falling-price rule. |
| META | 14:18 | 14:40 | -0.1599% | META's recent prices meet the falling-price rule. |
| META | 14:49 | 15:09 | -0.1226% | META's recent prices meet the falling-price rule. |
| META | 15:37 | 15:41 | -0.4120% | META's latest price is at least 0.3% below its buy price. |
| META | 15:56 | 16:00 | -0.0524% | The position was marked at the market close. |
| TSLA | 10:19 | 10:20 | -0.5000% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 10:49 | 10:53 | -0.4906% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 11:39 | 11:42 | -0.6143% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 15:22 | 15:58 | 0.1909% | TSLA's latest price fell at least 0.3% from its recent high. |
| INTC | 10:51 | 10:55 | -0.7138% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 13:27 | 13:40 | 0.4785% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 14:19 | 14:26 | -0.4500% | INTC's latest price is at least 0.3% below its buy price. |
| MU | 10:51 | 10:55 | -0.5776% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:31 | 12:38 | -0.0103% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:13 | 13:40 | 0.8746% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 15:19 | 15:26 | -0.3518% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 15:50 | 16:00 | -0.2540% | The position was marked at the market close. |
| TSM | 10:51 | 10:55 | -0.5874% | TSM's latest price is at least 0.3% below its buy price. |
| TSM | 11:53 | 12:16 | -0.4752% | TSM's latest price is at least 0.3% below its buy price. |
| TSM | 12:31 | 13:49 | -0.1073% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 15:22 | 15:26 | -0.3495% | TSM's recent prices meet the falling-price rule. |

## 2026-08-03

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 1 | -0.0102% | -2.1700% |
| MSFT | 1 | -0.0804% | 1.8394% |
| NVDA | 3 | 0.4881% | 4.0422% |
| AMZN | 3 | -1.4304% | 1.7461% |
| META | 5 | -0.0594% | 4.5839% |
| TSLA | 3 | 0.7928% | 2.9395% |
| INTC | 3 | -0.3636% | 4.8553% |
| MU | 8 | -1.5746% | 6.8869% |
| PLTR | 4 | -1.3486% | 0.2904% |
| TSM | 2 | -0.0612% | 1.8678% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 12:29 | 12:46 | -0.0102% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 11:31 | 11:51 | -0.0804% | MSFT's latest price fell at least 0.3% from its recent high. |
| NVDA | 09:56 | 10:03 | 0.6808% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 10:36 | 11:30 | 0.2546% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 15:02 | 15:14 | -0.4449% | NVDA's latest price is at least 0.3% below its buy price. |
| AMZN | 09:42 | 09:50 | -0.7381% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 10:30 | 10:34 | -0.5298% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 14:44 | 15:05 | -0.1686% | AMZN's latest price fell at least 0.3% from its recent high. |
| META | 09:49 | 10:00 | 0.6346% | META's latest price fell at least 0.3% from its recent high. |
| META | 10:07 | 10:12 | -0.3208% | META's latest price fell at least 0.3% from its recent high. |
| META | 10:45 | 10:52 | -0.3429% | META's latest price fell at least 0.3% from its recent high. |
| META | 11:03 | 11:34 | 0.2424% | META's latest price fell at least 0.3% from its recent high. |
| META | 14:25 | 14:37 | -0.2690% | META's recent prices meet the falling-price rule. |
| TSLA | 09:56 | 10:01 | -0.3368% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 10:38 | 11:13 | 0.8309% | TSLA's recent prices meet the falling-price rule. |
| TSLA | 14:39 | 15:08 | 0.3000% | TSLA's recent prices meet the falling-price rule. |
| INTC | 10:51 | 11:10 | -0.4087% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 12:19 | 12:25 | -0.4189% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 13:49 | 14:15 | 0.4662% | INTC's recent prices meet the falling-price rule. |
| MU | 10:00 | 10:01 | -0.4688% | MU's latest price is at least 0.3% below its buy price. |
| MU | 10:53 | 10:57 | -0.6235% | MU's latest price is at least 0.3% below its buy price. |
| MU | 11:34 | 11:38 | -0.6336% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:19 | 12:22 | -0.4756% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:32 | 12:43 | -0.4004% | MU's latest price is at least 0.3% below its buy price. |
| MU | 13:14 | 13:26 | -0.4621% | MU's latest price is at least 0.3% below its buy price. |
| MU | 13:31 | 14:14 | 0.8489% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 15:30 | 15:55 | 0.6418% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 09:40 | 09:44 | 0.0272% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 11:01 | 11:04 | -0.5414% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 12:10 | 12:12 | -0.4105% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 12:29 | 12:49 | -0.4298% | PLTR's latest price is at least 0.3% below its buy price. |
| TSM | 10:51 | 11:07 | -0.4017% | TSM's latest price is at least 0.3% below its buy price. |
| TSM | 13:35 | 14:21 | 0.3418% | TSM's recent prices meet the falling-price rule. |

## 2026-08-04

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 3 | -0.5963% | 1.7235% |
| MSFT | 2 | 0.6829% | 1.6942% |
| NVDA | 2 | -0.6756% | 0.5070% |
| AMZN | 4 | -0.3654% | -0.3944% |
| META | 2 | 0.1486% | 1.0457% |
| TSLA | 3 | -0.7870% | 0.5497% |
| INTC | 3 | 0.3758% | 5.4599% |
| MU | 3 | -0.6951% | 2.4515% |
| PLTR | 3 | -1.0946% | 9.4070% |
| TSM | 1 | -0.5937% | 0.3246% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 10:18 | 10:41 | -0.4437% | AAPL's latest price is at least 0.3% below its buy price. |
| AAPL | 11:38 | 12:20 | -0.3215% | AAPL's recent prices meet the falling-price rule. |
| AAPL | 12:52 | 13:23 | 0.1688% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 09:49 | 10:22 | 0.9322% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 10:35 | 10:50 | -0.2470% | MSFT's latest price fell at least 0.3% from its recent high. |
| NVDA | 10:08 | 10:16 | -0.4745% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 10:30 | 10:41 | -0.2021% | NVDA's recent prices meet the falling-price rule. |
| AMZN | 10:03 | 10:17 | 0.6737% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 11:27 | 11:45 | -0.4628% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 13:04 | 13:58 | -0.3291% | AMZN's recent prices meet the falling-price rule. |
| AMZN | 15:35 | 15:51 | -0.2436% | AMZN's latest price fell at least 0.3% from its recent high. |
| META | 11:25 | 12:21 | -0.4353% | META's latest price is at least 0.3% below its buy price. |
| META | 13:05 | 13:53 | 0.5865% | META's recent prices meet the falling-price rule. |
| TSLA | 10:06 | 10:20 | -0.2324% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 11:41 | 12:15 | 0.0048% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 13:25 | 13:51 | -0.5607% | TSLA's latest price is at least 0.3% below its buy price. |
| INTC | 09:36 | 09:44 | 0.4046% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 10:06 | 10:18 | 0.4513% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 12:49 | 12:56 | -0.4779% | INTC's latest price is at least 0.3% below its buy price. |
| MU | 10:30 | 10:31 | -0.5224% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:21 | 12:53 | 0.0888% | MU's recent prices meet the falling-price rule. |
| MU | 13:39 | 13:51 | -0.2622% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 09:43 | 09:45 | -0.4488% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 10:10 | 10:12 | -0.6455% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 12:10 | 12:19 | -0.0032% | PLTR's recent prices meet the falling-price rule. |
| TSM | 09:53 | 09:57 | -0.5937% | TSM's latest price is at least 0.3% below its buy price. |

## 2026-08-05

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 1 | 0.5979% | 0.8045% |
| MSFT | 3 | -0.4257% | -1.9485% |
| NVDA | 4 | -0.4711% | 0.4662% |
| AMZN | 1 | -0.2609% | -3.5631% |
| META | 3 | -0.4952% | -1.0968% |
| TSLA | 2 | -1.0944% | -0.5301% |
| INTC | 6 | 0.6041% | 0.9184% |
| MU | 3 | 0.2142% | 0.2210% |
| PLTR | 2 | -0.9921% | -2.7630% |
| TSM | 2 | -0.4663% | -1.4707% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 10:43 | 11:15 | 0.5979% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 10:26 | 11:04 | 0.0429% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 11:25 | 11:36 | -0.5191% | MSFT's latest price is at least 0.3% below its buy price. |
| MSFT | 14:13 | 15:23 | 0.0510% | MSFT's recent prices meet the falling-price rule. |
| NVDA | 09:40 | 09:43 | -0.1926% | NVDA's latest price fell at least 0.3% from its recent high. |
| NVDA | 12:05 | 12:09 | -0.3727% | NVDA's recent prices meet the falling-price rule. |
| NVDA | 12:16 | 13:31 | 0.3817% | NVDA's recent prices meet the falling-price rule. |
| NVDA | 15:02 | 15:12 | -0.2866% | NVDA's recent prices meet the falling-price rule. |
| AMZN | 15:57 | 16:00 | -0.2609% | The position was marked at the market close. |
| META | 09:43 | 09:44 | -0.4402% | META's latest price is at least 0.3% below its buy price. |
| META | 10:16 | 10:19 | -0.4055% | META's latest price is at least 0.3% below its buy price. |
| META | 15:17 | 16:00 | 0.3517% | The position was marked at the market close. |
| TSLA | 09:42 | 09:43 | -0.4559% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 10:07 | 10:13 | -0.6414% | TSLA's latest price is at least 0.3% below its buy price. |
| INTC | 09:45 | 09:51 | 0.4836% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 10:09 | 10:12 | -0.4832% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 11:10 | 11:14 | -0.1957% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 11:21 | 11:52 | 0.7937% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 12:19 | 12:34 | 0.4670% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 15:05 | 15:45 | -0.4554% | INTC's latest price is at least 0.3% below its buy price. |
| MU | 10:08 | 10:20 | 0.4883% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 11:32 | 11:35 | -0.6420% | MU's latest price is at least 0.3% below its buy price. |
| MU | 12:19 | 12:32 | 0.3716% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 11:40 | 11:50 | -0.4644% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 15:41 | 15:55 | -0.5302% | PLTR's latest price is at least 0.3% below its buy price. |
| TSM | 09:43 | 09:52 | -0.0244% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 12:30 | 12:56 | -0.4420% | TSM's latest price is at least 0.3% below its buy price. |

## 2026-08-06

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 0 | 0.0000% | -0.8520% |
| MSFT | 3 | -0.9909% | 1.9127% |
| NVDA | 2 | -0.8731% | -1.0273% |
| AMZN | 2 | -0.8509% | -0.5346% |
| META | 1 | -0.1346% | 0.1700% |
| TSLA | 3 | -0.9335% | 0.8706% |
| INTC | 4 | -1.1766% | 2.3914% |
| MU | 5 | -1.4161% | 4.5794% |
| PLTR | 3 | 0.1803% | -0.0134% |
| TSM | 3 | -0.4649% | 2.2098% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| MSFT | 10:19 | 10:24 | -0.2306% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 10:45 | 11:13 | -0.3558% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 15:57 | 15:59 | -0.4077% | MSFT's latest price is at least 0.3% below its buy price. |
| NVDA | 09:38 | 09:40 | -0.4533% | NVDA's latest price is at least 0.3% below its buy price. |
| NVDA | 09:50 | 09:55 | -0.4217% | NVDA's latest price is at least 0.3% below its buy price. |
| AMZN | 10:34 | 10:42 | -0.4501% | AMZN's latest price is at least 0.3% below its buy price. |
| AMZN | 10:59 | 11:08 | -0.4025% | AMZN's latest price is at least 0.3% below its buy price. |
| META | 10:34 | 10:42 | -0.1346% | META's latest price fell at least 0.3% from its recent high. |
| TSLA | 10:59 | 11:04 | -0.3514% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 12:52 | 13:20 | -0.4364% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 15:56 | 16:00 | -0.1484% | The position was marked at the market close. |
| INTC | 09:48 | 09:53 | 0.2427% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 10:45 | 10:46 | -0.4893% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 11:01 | 11:03 | -0.5750% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 12:41 | 12:47 | -0.3582% | INTC's latest price fell at least 0.3% from its recent high. |
| MU | 09:48 | 09:53 | -0.4843% | MU's latest price is at least 0.3% below its buy price. |
| MU | 10:09 | 10:13 | 0.3606% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:21 | 13:25 | -0.3914% | MU's recent prices meet the falling-price rule. |
| MU | 14:18 | 14:27 | -0.3251% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 15:05 | 15:15 | -0.5812% | MU's latest price is at least 0.3% below its buy price. |
| PLTR | 10:00 | 10:04 | 0.4587% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 11:29 | 11:46 | 0.0533% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 13:20 | 13:27 | -0.3303% | PLTR's latest price fell at least 0.3% from its recent high. |
| TSM | 09:44 | 09:54 | -0.1384% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 10:09 | 10:27 | -0.0572% | TSM's recent prices meet the falling-price rule. |
| TSM | 12:41 | 13:42 | -0.2700% | TSM's latest price fell at least 0.3% from its recent high. |

## 2026-08-07

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 1 | 0.1809% | 0.1622% |
| MSFT | 1 | -0.1813% | -0.3740% |
| NVDA | 1 | -0.0173% | 1.1421% |
| AMZN | 2 | -0.4773% | 0.1300% |
| META | 0 | 0.0000% | 0.1793% |
| TSLA | 5 | -0.1145% | 1.5761% |
| INTC | 4 | 0.3356% | -1.6338% |
| MU | 4 | 0.1244% | -2.3826% |
| PLTR | 4 | -1.4657% | 6.1619% |
| TSM | 2 | 0.7134% | -1.1126% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 10:21 | 10:51 | 0.1809% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 11:41 | 11:48 | -0.1813% | MSFT's recent prices meet the falling-price rule. |
| NVDA | 15:57 | 16:00 | -0.0173% | The position was marked at the market close. |
| AMZN | 14:06 | 14:10 | -0.2016% | AMZN's recent prices meet the falling-price rule. |
| AMZN | 15:50 | 16:00 | -0.2762% | AMZN's recent prices meet the falling-price rule. |
| TSLA | 10:20 | 10:30 | 0.5903% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 11:06 | 11:12 | -0.4590% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 11:23 | 11:35 | 0.1999% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 15:02 | 15:35 | -0.4286% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 15:57 | 16:00 | -0.0132% | The position was marked at the market close. |
| INTC | 11:05 | 11:16 | -0.1501% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 11:21 | 11:36 | 1.2211% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 15:02 | 15:31 | -0.3268% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 15:54 | 15:56 | -0.4004% | INTC's latest price is at least 0.3% below its buy price. |
| MU | 11:05 | 11:37 | 1.2822% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:20 | 13:27 | -0.3723% | MU's recent prices meet the falling-price rule. |
| MU | 14:34 | 14:35 | -0.4003% | MU's latest price is at least 0.3% below its buy price. |
| MU | 15:02 | 15:32 | -0.3749% | MU's latest price fell at least 0.3% from its recent high. |
| PLTR | 09:56 | 09:57 | -0.5943% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 10:33 | 10:35 | -0.7894% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 11:07 | 11:09 | -0.5063% | PLTR's latest price is at least 0.3% below its buy price. |
| PLTR | 12:36 | 13:34 | 0.4206% | PLTR's recent prices meet the falling-price rule. |
| TSM | 10:49 | 12:25 | 0.7913% | TSM's recent prices meet the falling-price rule. |
| TSM | 13:07 | 13:54 | -0.0774% | TSM's recent prices meet the falling-price rule. |

## 2026-08-10

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 1 | -0.3211% | 0.2889% |
| MSFT | 3 | 0.6790% | -0.4049% |
| NVDA | 1 | 0.1796% | -2.7384% |
| AMZN | 2 | -0.1803% | 0.5930% |
| META | 1 | 1.5336% | -0.7156% |
| TSLA | 3 | -0.8949% | 0.8895% |
| INTC | 4 | 0.6789% | 0.3475% |
| MU | 3 | -0.6373% | 0.1149% |
| PLTR | 2 | 0.2912% | 0.6902% |
| TSM | 4 | -0.8464% | -0.6506% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 09:57 | 10:09 | -0.3211% | AAPL's recent prices meet the falling-price rule. |
| MSFT | 09:45 | 10:36 | 1.1853% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 12:59 | 13:04 | -0.2906% | MSFT's latest price fell at least 0.3% from its recent high. |
| MSFT | 15:56 | 16:00 | -0.2104% | The position was marked at the market close. |
| NVDA | 13:09 | 13:27 | 0.1796% | NVDA's recent prices meet the falling-price rule. |
| AMZN | 11:05 | 11:34 | 0.0058% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 15:56 | 16:00 | -0.1861% | The position was marked at the market close. |
| META | 09:56 | 10:50 | 1.5336% | META's latest price fell at least 0.3% from its recent high. |
| TSLA | 10:01 | 10:09 | -0.3406% | TSLA's latest price fell at least 0.3% from its recent high. |
| TSLA | 11:45 | 12:44 | -0.4207% | TSLA's latest price is at least 0.3% below its buy price. |
| TSLA | 15:57 | 16:00 | -0.1362% | The position was marked at the market close. |
| INTC | 09:59 | 10:15 | 0.6596% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 11:55 | 12:05 | -0.4703% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 12:49 | 12:59 | -0.0498% | INTC's latest price fell at least 0.3% from its recent high. |
| INTC | 14:12 | 15:04 | 0.5419% | INTC's recent prices meet the falling-price rule. |
| MU | 11:45 | 12:07 | -0.1523% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 12:49 | 13:20 | -0.0733% | MU's recent prices meet the falling-price rule. |
| MU | 14:36 | 15:06 | -0.4128% | MU's latest price is at least 0.3% below its buy price. |
| PLTR | 10:23 | 10:56 | 0.7455% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 13:07 | 13:27 | -0.4509% | PLTR's latest price is at least 0.3% below its buy price. |
| TSM | 09:49 | 09:56 | -0.3375% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 10:35 | 10:55 | -0.3455% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 11:04 | 11:27 | -0.0988% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 11:45 | 11:59 | -0.0670% | TSM's recent prices meet the falling-price rule. |

## 2026-08-11

| Stock | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: |
| AAPL | 0 | 0.0000% | -1.5816% |
| MSFT | 1 | -0.1277% | -0.2485% |
| NVDA | 1 | -0.2588% | -1.9553% |
| AMZN | 1 | -0.0633% | -1.6853% |
| META | 2 | 1.2649% | 0.5040% |
| TSLA | 1 | -0.3890% | 0.0338% |
| INTC | 5 | -1.6488% | 1.1322% |
| MU | 2 | 0.2826% | -0.2579% |
| PLTR | 2 | 0.1800% | -0.6847% |
| TSM | 3 | -0.5521% | 0.2064% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| MSFT | 15:56 | 16:00 | -0.1277% | The position was marked at the market close. |
| NVDA | 10:56 | 11:01 | -0.2588% | NVDA's latest price fell at least 0.3% from its recent high. |
| AMZN | 14:46 | 15:18 | -0.0633% | AMZN's recent prices meet the falling-price rule. |
| META | 09:57 | 10:23 | 1.5210% | META's latest price fell at least 0.3% from its recent high. |
| META | 11:23 | 11:31 | -0.2523% | META's recent prices meet the falling-price rule. |
| TSLA | 10:44 | 10:59 | -0.3890% | TSLA's latest price fell at least 0.3% from its recent high. |
| INTC | 10:03 | 10:05 | -0.4410% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 11:15 | 11:21 | -0.3504% | INTC's recent prices meet the falling-price rule. |
| INTC | 12:40 | 13:14 | -0.4014% | INTC's latest price is at least 0.3% below its buy price. |
| INTC | 14:52 | 15:08 | -0.1976% | INTC's recent prices meet the falling-price rule. |
| INTC | 15:14 | 15:43 | -0.2691% | INTC's latest price fell at least 0.3% from its recent high. |
| MU | 13:18 | 13:25 | -0.3176% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:30 | 14:58 | 0.6021% | MU's recent prices meet the falling-price rule. |
| PLTR | 10:44 | 10:54 | -0.3200% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 12:41 | 14:19 | 0.5016% | PLTR's recent prices meet the falling-price rule. |
| TSM | 09:42 | 09:46 | -0.3553% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 10:49 | 11:13 | -0.0622% | TSM's recent prices meet the falling-price rule. |
| TSM | 15:51 | 16:00 | -0.1354% | The position was marked at the market close. |

## Reading this result

The replay gives every stock an equal share of the day and compounds the daily results. A position still open at the close is marked at the final minute price. This replay uses the current short rising-price rule; the planned 30-minute rule is not included.
