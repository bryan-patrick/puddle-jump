# Ten-day strategy replay

This is an exploration run, not evidence that the strategy will make money.

## Setup

- Trading days: 10
- Stocks per day: 10
- Price resolution: one-minute IEX bars
- News window: previous market close through one minute before market open
- News scoring: simple positive and negative headline words
- Estimated cost: 0.05% per side
- Rising prices needed: 6
- Falling prices needed: 5
- Cache retention: 30 days

## Combined result

- Strategy return: -0.2760%
- Equal-weight buy and hold: 3.2534%
- Completed trades: 16
- Profitable trades after estimated costs: 3
- Cache hits: 21
- Downloads: 0
- Expired cache files removed: 0

## Daily results

| Day | Strategy | Buy and hold | Trades | Winners |
| --- | ---: | ---: | ---: | ---: |
| 2026-07-29 | -0.0429% | -3.0084% | 2 | 0 |
| 2026-07-30 | 0.0000% | 2.6855% | 0 | 0 |
| 2026-07-31 | 0.0000% | -1.1279% | 0 | 0 |
| 2026-08-03 | 0.0000% | 2.6882% | 0 | 0 |
| 2026-08-04 | 0.0000% | 2.2769% | 0 | 0 |
| 2026-08-05 | 0.0000% | -0.8962% | 0 | 0 |
| 2026-08-06 | -0.1416% | 0.9707% | 5 | 1 |
| 2026-08-07 | -0.0181% | 0.3849% | 1 | 0 |
| 2026-08-10 | -0.0736% | -0.1586% | 8 | 2 |
| 2026-08-11 | 0.0000% | -0.4537% | 0 | 0 |

## 2026-07-29

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.33 | 2 | -0.4292% | -1.0855% |
| MSFT | -0.20 | 0 | 0.0000% | -0.7636% |
| NVDA | 0.00 | 0 | 0.0000% | -2.7798% |
| AMZN | -0.25 | 0 | 0.0000% | -0.8605% |
| META | 0.00 | 0 | 0.0000% | -0.7673% |
| TSLA | -0.20 | 0 | 0.0000% | -2.9395% |
| INTC | 0.00 | 0 | 0.0000% | -5.7222% |
| MU | 0.00 | 0 | 0.0000% | -10.4788% |
| PLTR | No news | 0 | 0.0000% | -1.4336% |
| TSM | 0.00 | 0 | 0.0000% | -3.2530% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AAPL | 09:49 | 09:56 | -0.2412% | AAPL's latest price fell at least 0.3% from its recent high. |
| AAPL | 14:03 | 14:10 | -0.1885% | AAPL's recent prices meet the falling-price rule. |

## 2026-07-30

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.09 | 0 | 0.0000% | -0.2826% |
| MSFT | 0.11 | 0 | 0.0000% | 3.7689% |
| NVDA | 0.00 | 0 | 0.0000% | 1.2866% |
| AMZN | 0.14 | 0 | 0.0000% | 1.0249% |
| META | -0.17 | 0 | 0.0000% | 1.0784% |
| TSLA | 0.00 | 0 | 0.0000% | 1.4751% |
| INTC | 0.00 | 0 | 0.0000% | 3.7408% |
| MU | 0.20 | 0 | 0.0000% | 10.3776% |
| PLTR | -1.00 | 0 | 0.0000% | 0.8365% |
| TSM | 0.00 | 0 | 0.0000% | 3.5484% |

## 2026-07-31

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.12 | 0 | 0.0000% | 1.4594% |
| MSFT | -0.07 | 0 | 0.0000% | 2.1915% |
| NVDA | -0.09 | 0 | 0.0000% | 1.4465% |
| AMZN | 0.24 | 0 | 0.0000% | 2.8515% |
| META | -0.10 | 0 | 0.0000% | 0.9044% |
| TSLA | 0.17 | 0 | 0.0000% | -0.2858% |
| INTC | 0.00 | 0 | 0.0000% | -7.1312% |
| MU | 0.00 | 0 | 0.0000% | -10.5153% |
| PLTR | 0.00 | 0 | 0.0000% | 1.4419% |
| TSM | 0.00 | 0 | 0.0000% | -3.6423% |

## 2026-08-03

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.07 | 0 | 0.0000% | -2.1700% |
| MSFT | 0.10 | 0 | 0.0000% | 1.8394% |
| NVDA | 0.00 | 0 | 0.0000% | 4.0422% |
| AMZN | 0.07 | 0 | 0.0000% | 1.7461% |
| META | 0.00 | 0 | 0.0000% | 4.5839% |
| TSLA | -0.06 | 0 | 0.0000% | 2.9395% |
| INTC | 0.00 | 0 | 0.0000% | 4.8553% |
| MU | 0.00 | 0 | 0.0000% | 6.8869% |
| PLTR | 0.00 | 0 | 0.0000% | 0.2904% |
| TSM | -0.50 | 0 | 0.0000% | 1.8678% |

## 2026-08-04

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.00 | 0 | 0.0000% | 1.7235% |
| MSFT | 0.00 | 0 | 0.0000% | 1.6942% |
| NVDA | -0.18 | 0 | 0.0000% | 0.5070% |
| AMZN | 0.00 | 0 | 0.0000% | -0.3944% |
| META | 0.00 | 0 | 0.0000% | 1.0457% |
| TSLA | 0.08 | 0 | 0.0000% | 0.5497% |
| INTC | 0.00 | 0 | 0.0000% | 5.4599% |
| MU | 0.00 | 0 | 0.0000% | 2.4515% |
| PLTR | 0.20 | 0 | 0.0000% | 9.4070% |
| TSM | 0.00 | 0 | 0.0000% | 0.3246% |

## 2026-08-05

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.00 | 0 | 0.0000% | 0.8045% |
| MSFT | 0.00 | 0 | 0.0000% | -1.9485% |
| NVDA | 0.00 | 0 | 0.0000% | 0.4662% |
| AMZN | -0.14 | 0 | 0.0000% | -3.5631% |
| META | 0.00 | 0 | 0.0000% | -1.0968% |
| TSLA | 0.11 | 0 | 0.0000% | -0.5301% |
| INTC | 0.00 | 0 | 0.0000% | 0.9184% |
| MU | 0.14 | 0 | 0.0000% | 0.2210% |
| PLTR | 0.00 | 0 | 0.0000% | -2.7630% |
| TSM | No news | 0 | 0.0000% | -1.4707% |

## 2026-08-06

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | -0.67 | 0 | 0.0000% | -0.8520% |
| MSFT | 0.00 | 0 | 0.0000% | 1.9127% |
| NVDA | 0.00 | 0 | 0.0000% | -1.0273% |
| AMZN | 0.00 | 0 | 0.0000% | -0.5346% |
| META | 0.00 | 0 | 0.0000% | 0.1700% |
| TSLA | 0.00 | 0 | 0.0000% | 0.8706% |
| INTC | No news | 0 | 0.0000% | 2.3914% |
| MU | 0.25 | 5 | -1.4161% | 4.5794% |
| PLTR | 0.00 | 0 | 0.0000% | -0.0134% |
| TSM | No news | 0 | 0.0000% | 2.2098% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| MU | 09:48 | 09:53 | -0.4843% | MU's latest price is at least 0.3% below its buy price. |
| MU | 10:09 | 10:13 | 0.3606% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 13:21 | 13:25 | -0.3914% | MU's recent prices meet the falling-price rule. |
| MU | 14:18 | 14:27 | -0.3251% | MU's latest price fell at least 0.3% from its recent high. |
| MU | 15:05 | 15:15 | -0.5812% | MU's latest price is at least 0.3% below its buy price. |

## 2026-08-07

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.00 | 0 | 0.0000% | 0.1622% |
| MSFT | 0.25 | 1 | -0.1813% | -0.3740% |
| NVDA | 0.00 | 0 | 0.0000% | 1.1421% |
| AMZN | 0.12 | 0 | 0.0000% | 0.1300% |
| META | 0.25 | 0 | 0.0000% | 0.1793% |
| TSLA | 0.00 | 0 | 0.0000% | 1.5761% |
| INTC | No news | 0 | 0.0000% | -1.6338% |
| MU | 0.00 | 0 | 0.0000% | -2.3826% |
| PLTR | 0.00 | 0 | 0.0000% | 6.1619% |
| TSM | No news | 0 | 0.0000% | -1.1126% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| MSFT | 11:41 | 11:48 | -0.1813% | MSFT's recent prices meet the falling-price rule. |

## 2026-08-10

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.09 | 0 | 0.0000% | 0.2889% |
| MSFT | 0.22 | 0 | 0.0000% | -0.4049% |
| NVDA | 0.08 | 0 | 0.0000% | -2.7384% |
| AMZN | 0.33 | 2 | -0.1803% | 0.5930% |
| META | 0.15 | 0 | 0.0000% | -0.7156% |
| TSLA | 0.10 | 0 | 0.0000% | 0.8895% |
| INTC | 0.00 | 0 | 0.0000% | 0.3475% |
| MU | 0.00 | 0 | 0.0000% | 0.1149% |
| PLTR | 0.25 | 2 | 0.2912% | 0.6902% |
| TSM | 0.25 | 4 | -0.8464% | -0.6506% |

### Trades

| Stock | Bought | Sold | Return | Exit |
| --- | --- | --- | ---: | --- |
| AMZN | 11:05 | 11:34 | 0.0058% | AMZN's latest price fell at least 0.3% from its recent high. |
| AMZN | 15:56 | 16:00 | -0.1861% | The position was marked at the market close. |
| PLTR | 10:23 | 10:56 | 0.7455% | PLTR's latest price fell at least 0.3% from its recent high. |
| PLTR | 13:07 | 13:27 | -0.4509% | PLTR's latest price is at least 0.3% below its buy price. |
| TSM | 09:49 | 09:56 | -0.3375% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 10:35 | 10:55 | -0.3455% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 11:04 | 11:27 | -0.0988% | TSM's latest price fell at least 0.3% from its recent high. |
| TSM | 11:45 | 11:59 | -0.0670% | TSM's recent prices meet the falling-price rule. |

## 2026-08-11

| Stock | Outlook | Trades | Strategy | Buy and hold |
| --- | ---: | ---: | ---: | ---: |
| AAPL | 0.00 | 0 | 0.0000% | -1.5816% |
| MSFT | 0.00 | 0 | 0.0000% | -0.2485% |
| NVDA | 0.00 | 0 | 0.0000% | -1.9553% |
| AMZN | 0.00 | 0 | 0.0000% | -1.6853% |
| META | 0.17 | 0 | 0.0000% | 0.5040% |
| TSLA | 0.00 | 0 | 0.0000% | 0.0338% |
| INTC | 0.00 | 0 | 0.0000% | 1.1322% |
| MU | 0.00 | 0 | 0.0000% | -0.2579% |
| PLTR | 0.00 | 0 | 0.0000% | -0.6847% |
| TSM | 0.00 | 0 | 0.0000% | 0.2064% |

## Reading this result

The replay gives every stock an equal share of the day and compounds the daily results. A position still open at the close is marked at the final minute price. The headline word score is intentionally basic, so this run evaluates that exact rule rather than claiming to understand the news.
