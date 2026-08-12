# Strategy Testing

This file records what we tested, the exact settings used, and what happened.
Historical replays are experiments, not proof that the strategy will make money.

## Rules for this record

- Add a new dated entry for every meaningful strategy replay.
- Never replace an older result because a newer result looks better.
- Change existing strategy parameters before proposing new rules.
- Record the stocks, dates, price interval, market-data feed, and estimated costs.
- Record losing results as clearly as winning results.
- Keep discovery results separate from later validation results.
- End each entry with the decision we made from the evidence.

## 2026-08-12 — Three-price buy and existing sell parameters

### Question

What happens if we buy after three rising prices, and can the existing sell
parameters ignore normal price jitter without holding a clear loser too long?

### Data

- Period: 30 completed trading days from June 30 through August 11, 2026
- Stocks: AAPL, MSFT, NVDA, AMZN, META, TSLA, INTC, MU, PLTR, and TSM
- Price interval: one minute
- Feed: Alpaca IEX
- Estimated cost: 0.05% when buying and 0.05% when selling
- Parameter selection: first 20 days
- Later check: final 10 days

Three prices means three observed prices where each price is higher than the one
before it. It therefore contains two price increases.

### Existing five-price result

Settings:

- Rising prices to buy: 5
- Minimum total rise: 0.3%
- Falling prices to sell: 5
- Minimum total fall: 0.1%
- Fast drop from recent high: 0.3%
- Maximum loss from buy price: 0.3%

Result:

- Return: -12.72%
- Trades: 1,320
- Winners: 382, or 28.9%
- Median time held: 8 minutes

### Three-price result with the existing sell settings

Only the rising-price count changed from five to three.

Result:

- Return: -17.56%
- Trades: 1,998
- Winners: 30.4%
- Median time held: 6 minutes

Buying after three prices created substantially more short trades and lost more
after estimated costs.

### Best nearby existing-parameter result

Settings:

- Rising prices to buy: 3
- Minimum total rise: 0.3%
- Falling prices to sell: 7
- Minimum total fall: 0.1%
- Fast drop from recent high: 1.5%
- Maximum loss from buy price: 1.0%

Result:

- First 20 days: -6.58%
- Final 10 days: +0.07%
- All 30 days: -6.52%
- Trades: 792
- Winners: 36.2%
- Median time held: 45 minutes
- All 30 days without estimated costs: +1.13%
- All 30 days with 0.025% cost per side: -2.77%
- All 30 days with 0.05% cost per side: -6.52%

### What we learned

- The 0.3% fast-drop setting treats too much normal movement as a sell signal.
- A 1.5% fast-drop setting provides a more useful allowance for price jitter in
  this sample.
- Changing the minimum falling-trend drop between 0.05% and 0.2% made little
  difference.
- A wider 1.0% maximum loss and seven falling prices reduced unnecessary selling.
- Better sell settings reduced the loss, but did not make three-price buying
  profitable after estimated costs.
- The three-price entry produced too much turnover. Sell settings alone cannot
  repair that problem.

### Decision

Do not treat these settings as approved trading settings. The useful sell
candidate is seven falling prices, a 0.1% total fall, a 1.5% fast drop, and a
1.0% maximum loss. It needs more evaluation before changing the application
configuration.

## 2026-08-12 — User-selected three-price settings

### Question

How do the new values in `config/strategy.toml` perform over the same 30-day
replay?

### Data

- Period: 30 completed trading days from June 30 through August 11, 2026
- Stocks: AAPL, MSFT, NVDA, AMZN, META, TSLA, INTC, MU, PLTR, and TSM
- Price interval: one minute
- Feed: Alpaca IEX
- Estimated cost: 0.05% when buying and 0.05% when selling

### Settings

- Rising prices to buy: 3
- Minimum total rise: 0.5%
- Falling prices to sell: 2
- Minimum total fall: 0.5%
- Fast drop from recent high: 0.75%
- Maximum loss from buy price: 1.0%

### Result

- Strategy return: -6.07%
- Equal-weight buy-and-hold return: -0.69%
- Trades: 509
- Winners after estimated costs: 178, or 35.0%
- Average trade return: -0.12%
- Median trade return: -0.60%
- Median time held: 24 minutes

Sell reasons:

- Falling trend: 182
- Maximum loss: 172
- Market close: 121
- Fast drop: 34

### What we learned

- These settings reduced trading from 1,998 trades to 509 compared with the
  earlier three-price result.
- They improved the return from -17.56% to -6.07%.
- Falling trends and the maximum-loss rule caused most intraday sells.
- The fast-drop rule fired relatively rarely at 0.75%.
- The strategy still lost more than equal-weight buy and hold over this period.

### Decision

Record the result without changing the strategy again. The new values are a
clear improvement over the earlier three-price settings, but this replay does
not show a profitable strategy after estimated costs.

## 2026-08-12 — One-year entry and exit comparison

### Question

Does one-tick trading, longer price confirmation, greater sell tolerance, or a
simple profit-protection rule improve the strategy over a longer period?

### Data

- Period: 252 completed trading days from August 11, 2025 through August 11, 2026
- Discovery period: first 202 trading days
- Validation period: final 50 trading days
- Stocks: AAPL, MSFT, NVDA, AMZN, META, TSLA, INTC, MU, PLTR, and TSM
- Price interval: one minute
- Feed: Alpaca IEX
- Estimated cost: 0.05% when buying and 0.05% when selling

### Existing-parameter comparison

The comparison covered 64 combinations:

- Buy after one positive tick, or after three, four, or five rising prices
- Minimum entry rises from effectively zero through 0.5%
- Sell after one negative tick, or after three or four falling prices
- Minimum falling drops from effectively zero through 0.5%
- Fast-drop limits of 0.75% or 1.0%
- Maximum-loss limits of 1.0% or 1.5%

Important results:

| Strategy | Discovery | Validation | Full year | Full-year trades |
| --- | ---: | ---: | ---: | ---: |
| Current settings | -11.61% | -12.12% | -22.32% | 3,106 |
| One positive tick / one negative tick | — | -99.20% | -100.00% | 238,559 |
| Best discovery combination | -11.13% | -11.10% | -20.99% | 4,028 |

The best discovery combination bought after five rising prices and a 0.3%
total rise. It kept the existing two-price, 0.5% falling rule, 0.75% fast drop,
and 1.0% maximum loss.

Without estimated costs, that combination returned 20.20% during discovery,
-1.80% during validation, and 18.04% across the full year. The signal did not
remain profitable in validation even before estimated costs.

### Profit-protection comparison

The current and best-discovery entries were also tested with:

- Profit-taking at 0.5% or 1.0%
- Selling on the first negative tick after reaching a 0.5% profit
- Trailing the highest price by 0.25% or 0.5% after reaching a profit

None beat the existing sell rules. Early profitable exits allowed immediate
re-entry, increased trading, and made the net result worse. Some variants won
more than 60% of their trades but still lost money.

### One-trade-per-stock comparison

The profit rules were then replayed with at most one completed trade per stock
per day. The best discovery result used the current three-price, 0.5% entry and
protected a 1.0% gain with a 0.5% trail.

- Discovery return: -7.66%
- Validation return: -4.30%
- Full-year return: -11.63%
- Full-year trades: 1,461
- Full-year winners: 45.0%

### What we learned

- One-tick trading reacts to ordinary price noise and creates unusable turnover.
- Longer entry confirmation improved the discovery result only slightly and did
  not produce a positive validation result.
- Wider sell tolerance did not make the strategy profitable.
- Simple profit protection raises the winner rate but creates costly re-entry
  unless daily trading is limited.
- One trade per stock per day materially reduces the loss, but does not create a
  profitable strategy.
- Estimated trading costs are important, but the validation result was negative
  even before those costs for the best longer entry.

### Decision

Do not change `config/strategy.toml` from this experiment. Reject one-tick
trading. Longer confirmation and daily trade limits are useful evidence, but no
tested variation passed the validation period.

## 2026-08-12 — Full-pool five-day and twenty-day filter

### Question

Does the original long-term idea work when shortened to trading days: only
consider a stock when it has risen over both the previous five and twenty
completed trading days?

### Data

- Period: 252 completed trading days from August 11, 2025 through August 11, 2026
- Discovery period: first 202 trading days
- Validation period: final 50 trading days
- Stocks: all 508 stocks in the saved Puddle Jump stock pool
- Feed: Alpaca IEX daily bars
- Costs: none; this tested the filter before simulating intraday trades
- Historical membership caveat: the stock pool saved in August 2026 was applied
  to the whole period

For each stock and test day, the filter used only completed prior days. A stock
qualified when its previous close was above its close five sessions earlier and
above its close twenty sessions earlier. The following day's open-to-close move
was then measured.

### Result

| Period | Stock-days | Qualified | Average qualified per day | All stocks | Qualified stocks |
| --- | ---: | ---: | ---: | ---: | ---: |
| Discovery | 102,113 | 36,407 | 180.2 | +5.07% | -0.44% |
| Validation | 25,347 | 10,391 | 207.8 | -0.62% | -2.15% |
| Full period | 127,460 | 46,798 | 185.7 | +4.42% | -2.58% |

The percentages are compounded equal-weight daily open-to-close results.

During validation:

- All stocks averaged -0.011% from open to close
- Qualified stocks averaged -0.062% from open to close
- 49.2% of all stock-days finished above their open
- 47.8% of qualified stock-days finished above their open

### What we learned

- The five-day and twenty-day filter did not identify stocks with stronger
  intraday continuation.
- In validation, qualifying stocks performed worse than the full pool.
- A stock rising over recent days may be more likely to pause or pull back
  intraday than to continue rising immediately.
- Testing the daily filter first avoided an unnecessary full-pool minute-data
  download.

### Decision

Do not run the minute-by-minute strategy for this filter and do not change the
application strategy. Reject this exact five-day and twenty-day qualification
rule before spending more Alpaca API usage on it.

## 2026-08-12 — Intraday pullback and recovery

### Question

Instead of buying a short upward spike, can we wait for a stock to fall from the
day's open and then buy only when it begins recovering?

### Data

- Period: 252 completed trading days from August 11, 2025 through August 11, 2026
- Discovery period: first 202 trading days
- Later check: final 50 trading days
- Stocks: AAPL, MSFT, NVDA, AMZN, META, TSLA, INTC, MU, PLTR, and TSM
- Price interval: one minute
- Feed: cached Alpaca IEX prices
- New Alpaca requests: none
- Re-entry: disabled after the first completed trade for a stock each day

The experiment compared 36 entries:

- Pullbacks of 0.3%, 0.5%, 0.75%, and 1.0% from the official daily open
- Recoveries containing two, three, or four rising prices
- Minimum recovery rises of 0.1%, 0.2%, and 0.3%

Every entry used the same existing sell settings:

- Falling prices: 2
- Minimum falling drop: 0.5%
- Fast drop: 0.75%
- Maximum loss from buy price: 1.0%

### Best discovery entry

- Pullback from open: 0.3%
- Recovery: two rising prices totaling at least 0.1%
- Discovery trades: 1,594
- Discovery winners without estimated costs: 43.4%

| Estimated cost per side | Discovery | Later 50 days | Full year |
| --- | ---: | ---: | ---: |
| 0.000% | +3.38% | -4.05% | -0.81% |
| 0.005% | +1.74% | -4.44% | -2.77% |
| 0.010% | +0.13% | -4.82% | -4.69% |
| 0.025% | -4.54% | -5.96% | -10.23% |
| 0.050% | -11.86% | -7.83% | -18.76% |

The full-year result contained 1,995 trades. Without estimated costs, 41.7% of
them were winners and the median trade returned -0.35%.

### What we learned

- Waiting for a pullback improved the discovery result compared with chasing a
  short rise.
- The improvement did not continue into the later 50 days.
- The selected rule lost over the full period even before estimated execution
  costs.
- The negative median trade shows that occasional larger winners were carrying
  many smaller losing trades.
- The cached test failed early enough that broader minute-data downloads were
  unnecessary.

### Decision

Do not change the application strategy and do not spend Alpaca API requests on
new-stock validation for this exact pullback rule. It did not pass the later
period even with zero estimated costs.

## 2026-08-12 — Recent-range wave following

### Question

Can the application ride observable waves without predicting a future price by
buying a new recent high and selling when the price breaks a recent low?

### Initial cached comparison

- Period: 252 completed trading days from August 11, 2025 through August 11, 2026
- Discovery period: first 202 trading days
- Later check: final 50 trading days
- Stocks: AAPL, MSFT, NVDA, AMZN, META, TSLA, INTC, MU, PLTR, and TSM
- Price interval: one minute
- Feed: cached Alpaca IEX prices
- Entry windows: 10, 20, and 30 minutes
- Exit windows: 5, 10, and 15 minutes
- Maximum loss from buy price: 1.0%
- Re-entry: disabled after one trade for a stock each day
- Profit target: none

A new high means the current close is strictly higher than every close in the
previous entry window. A recent-low break means the current close is strictly
lower than every close in the previous exit window.

The best discovery pair used a 10-minute high and a 10-minute low.

| Estimated cost per side | Discovery | Later 50 days | Full year |
| --- | ---: | ---: | ---: |
| 0.000% | +2.42% | +2.59% | +5.07% |
| 0.005% | +0.37% | +2.07% | +2.45% |
| 0.010% | -1.64% | +1.56% | -0.10% |
| 0.025% | -7.42% | +0.05% | -7.37% |
| 0.050% | -16.31% | -2.42% | -18.34% |

This loose rule traded on all 2,520 possible original stock-days. A new
10-minute high alone was therefore too common to define a meaningful wave.

### Minimum wave size

The entry was tightened to require the new high to also be a minimum percentage
above the lowest price in that same 10-minute range. Discovery compared 0.2%,
0.3%, 0.5%, 0.75%, 1.0%, 1.25%, 1.5%, 2.0%, and 3.0% minimum rises.

The strongest discovery result used a 1.0% minimum rise. Larger requirements
produced fewer trades and worse discovery returns.

Original ten-stock result with the 1.0% wave:

| Estimated cost per side | Discovery | Later 50 days | Full year |
| --- | ---: | ---: | ---: |
| 0.000% | +4.27% | +1.11% | +5.43% |
| 0.005% | +3.36% | +0.81% | +4.20% |
| 0.010% | — | +0.52% | +2.99% |

- Full-year trades: 1,171
- Full-year raw winners: 41.0%
- Median raw trade: -0.15%
- Median time held: 14 minutes

### New-stock validation

The fixed 1.0% wave rule was then evaluated against 44 previously unused
stocks: four from each of the eleven sectors in the saved pool. Stocks were
selected with random seed `20260812`; performance was not used for selection.

- Period: the same 252 completed trading days
- Possible stock-days: 11,088
- Missing stock-days: 0
- Cached minute bars: 2,532,355
- Estimated Alpaca data pages: approximately 260
- Download pacing: 20-day batches with 30-second pauses
- Rate-limit responses: none

| Estimated cost per side | Return |
| --- | ---: |
| 0.000% | +0.99% |
| 0.005% | +0.10% |
| 0.010% | -0.79% |
| 0.025% | -3.40% |
| 0.050% | -7.60% |

- Trades: 3,913
- Raw winners: 40.5%
- Median raw trade: -0.13%
- Median time held: 14 minutes

Raw validation return by sector:

| Sector | Return |
| --- | ---: |
| Communication | +4.22% |
| Consumer Discretionary | +0.75% |
| Consumer Staples | +2.76% |
| Energy | -1.22% |
| Financials | -0.31% |
| Health Care | +0.40% |
| Industrials | +0.07% |
| Information Technology | +9.03% |
| Materials | +2.38% |
| Real Estate | -0.96% |
| Utilities | -6.23% |

### What we learned

- Recent-range breakouts are a better wave definition than consecutive rising
  prices in the original ten-stock sample.
- Requiring a 1.0% wave substantially reduced trading and improved the original
  sample.
- The direction remained slightly positive across new stocks before estimated
  execution costs, but the effect was much weaker.
- A 0.005% estimate per side consumed almost the entire broad validation return.
- Results varied substantially by sector, so the apparent original technology
  result did not generalize evenly.
- Same-bar close execution makes this replay optimistic; a real order cannot be
  assumed to fill at the exact close that reveals the signal.

### Decision

Do not change the application strategy yet. The wave rule is the first tested
idea to remain positive before costs in both the original and new-stock samples,
but its broad result is too small to establish a tradable edge after realistic
execution. Preserve it as the leading hypothesis rather than declaring it
approved.

## 2026-08-12 — Smooth wave shape

### Question

Can the 1.0% recent-range wave be improved by rejecting single-price spikes and
requiring the rise to contain several upward steps?

### Data and fixed rules

- Period: 252 completed trading days from August 11, 2025 through August 11, 2026
- Discovery period: first 202 trading days of the original ten-stock sample
- Later check: final 50 trading days of the original ten-stock sample
- Broad check: the previously cached 44-stock, eleven-sector sample
- Price interval: one minute
- Feed: cached Alpaca IEX prices
- New Alpaca requests: none
- Entry: new 10-minute high with at least a 1.0% rise from the recent low
- Exit: break below the previous 10-minute low
- Maximum loss from buy price: 1.0%
- Re-entry: disabled after one trade for a stock each day

The experiment counted upward price changes from the most recent low through
the new high. It compared minimum counts of zero, four, six, and eight upward
steps. It also compared allowing one price jump to create at most 100%, 50%, or
35% of the total wave rise.

### Discovery result

The best discovery result required eight upward steps and placed no limit on
the size of one jump.

- Raw discovery return: +4.81%
- Discovery return at 0.005% estimated cost per side: +4.18%
- Discovery trades: 604

Limiting one jump to 50% or 35% did not improve the result. This provides no
evidence that one large price change was the main problem.

### Later and broad results

| Estimated cost per side | Original later 50 days | Original full year | Broad 44 stocks |
| --- | ---: | ---: | ---: |
| 0.000% | -0.31% | +4.48% | +0.71% |
| 0.005% | -0.53% | +3.62% | +0.18% |
| 0.010% | -0.75% | +2.77% | -0.35% |
| 0.025% | -1.40% | +0.26% | -1.91% |
| 0.050% | -2.49% | -3.79% | -4.47% |

- Original full-year trades: 825
- Broad trades: 2,324
- Broad raw winners: 40.4%
- Broad median raw trade: -0.13%
- Broad median time held: 14 minutes

### What we learned

- Requiring a very smooth rise improved the discovery period and reduced trades.
- The smoothness requirement did not survive the original later period.
- The broad result remained positive before very small execution costs, but was
  too small to be meaningful after costs.
- Rejecting single-price spikes did not improve discovery, so spike shape alone
  does not explain the weak broad result.
- The smooth rule appears fitted to the original discovery period rather than a
  durable improvement.

### Decision

Do not add a smooth-wave requirement to the application. Keep the simpler 1.0%
recent-range wave as the leading research result, and record this shape filter
as an unsuccessful refinement.
