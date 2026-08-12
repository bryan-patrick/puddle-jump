# Puddle Jump Agent Guide

## Project direction

Puddle Jump is a Python trading and backtesting project. Keep the system small, testable, and consistent between simulation and real-time operation.

The initial product starts with a broad pool of eligible stocks, finds stocks with recent upward price momentum, and produces simple buy, sell, or no-action decisions.

## Technology

- Use Python 3.14 as the primary language.
- Manage Python versions, environments, and dependencies with `uv`.
- Use `ruff` for linting and formatting.
- Prefer Polars for tabular data processing and analysis.
- Use SQLite for initial application state and structured operational data.
- Use Parquet for large historical market datasets.
- Produce daily reports in Markdown.
- Use React with TypeScript and TSX for the user interface. It must not contain trading logic.
- Use Alpaca's official `alpaca-py` package for stock data and Alpaca paper trading.

## Architecture

- Maintain one Python core for signals, strategies, risk, execution, and events.
- Run the same strategy and risk code against historical replay and live or paper market events.
- Keep market-data and broker integrations behind adapters so operating mode does not change core decisions.
- Begin with paper trading. Live execution must remain disabled until it is explicitly enabled and the strategy has passed replay and paper-trading validation.
- Put a thin Python HTTP boundary between the Python application and the React UI. Do not move domain logic into that boundary.
- Never duplicate trading logic between backtests and live or paper execution.
- Treat any divergence between simulated and real-time behavior as an architectural defect unless it models a documented real-world constraint.

## Alpaca integration

- Use Alpaca's personal Trading API and Market Data API. Do not use the Broker API.
- Load the paper API key and secret from `.env`. Never store recovery codes, print secrets, or expose credentials to the React application.
- Create the Alpaca trading client with `paper=True`. Do not create a live trading client without a new explicit decision from the project owner.
- Keep Trades Suspended enabled in Alpaca until the project owner deliberately enables paper orders at the approved pull-request step.
- Start current-price collection with `StockHistoricalDataClient` and one `StockSnapshotRequest` for the daily watchlist using the IEX feed.
- Start with simple HTTP requests on the configured interval. Do not add WebSocket streaming unless polling becomes inadequate.
- Read Alpaca's market clock before submitting an order. Initial orders run during regular market hours only.
- Read the paper account and open positions from Alpaca before making paper-order decisions.
- Use simple day market orders. Buy by a configured dollar amount so fractional trading can be used; sell the owned share quantity.
- Record the Alpaca order ID, status, filled quantity, filled price, failure reason, and request ID when available.
- Do not use options, short selling, margin, extended-hours trading, or PTP entries.

## Daily inputs and records

- Keep an eligible stock pool containing every S&P 500 constituent security plus an explicit list of major technology stocks outside the index.
- Record the source and date of every stock-pool snapshot because index membership changes.
- Keep the full stock pool separate from the smaller set currently being watched or traded.
- Select stocks from price movement only. Do not fetch, score, or use news as a trading input.
- Store symbols separately from changing prices.
- Before paper trading, use Alpaca to confirm that a selected stock is active, tradable, and eligible for the planned fractional order.
- Record each observed stock price with its symbol and timezone-aware timestamp, keeping observations in chronological order for each stock.
- Organize human-inspectable daily inputs and reports under a `YYYY-MM-DD` trading-day directory based on the relevant exchange timezone. Use unambiguous ISO 8601 timestamps with offsets for updates made during the day.
- Keep `watchlist.json` at the trading-day root.
- Keep live operational state and event records in SQLite, larger price histories in Parquet, and the daily summary in Markdown.
- Keep Alpaca market-data downloads local and ignored by Git unless Alpaca gives written permission to redistribute them.
- Cache downloaded historical prices locally for 30 days by default. Keep the retention period configurable and never commit the cache.

## Daily scorecard

- Create a `report.md` inside every trading-day directory, including days when no trades occur.
- Record starting and ending cash, starting and ending account value, daily profit or loss in dollars and percent, trades made, results by stock, open positions, decisions and reasons, risk limits triggered, errors, and short notes.
- Generate report numbers from recorded events and positions rather than entering totals by hand.
- Keep the report easy to scan in plain language. It should answer: What did we do, why did we do it, and how did we do?

## Initial strategy

- Run one simple, configurable loop for the daily watchlist. A roughly 30-second interval is a reasonable starting point, not a hard-coded rule.
- The strategy is price-only. Do not make buy or sell decisions from news.
- The current exploration rule buys when every price in the latest configured number of observations is higher than the one before it and the total move meets the configured minimum percentage.
- The next entry rule to evaluate measures the total rise over 30 minutes, compares it with QQQ over the same window, and confirms the stock is still higher than it was five minutes ago. Treat those values as configurable hypotheses.
- Sell immediately when the price reaches the configured maximum loss below its actual buy price, regardless of recent jitter.
- Also sell immediately when the current price falls by the configured fast-drop percentage from the highest price in the recent sell window.
- Otherwise, sell on a falling trend only when every price in the recent sell window is lower than the one before it and the total decline meets the configured minimum percentage.
- Start with five prices, a 0.1% falling-trend decline, a 0.3% fast drop, and a 0.3% maximum loss. These are hypotheses to test, not assumed truths.
- Return exactly one explicit decision: `BUY`, `SELL`, or `NO_ACTION`. Include a readable reason with every decision.
- Keep intervals, trend windows, and other strategy values in configuration rather than scattering constants through the code.
- Make every decision explainable from its recorded inputs.
- Enforce configurable maximum position size, maximum total exposure, and daily loss limits before submitting any order.
- Provide an emergency stop that prevents new orders and cancels pending orders without depending on the UI.

## User interface

- Render results with React and TSX, backed by a thin HTTP interface to the Python application.
- Show the watchlist, current prices, recent momentum, open position, latest decision, and the reason for that decision.
- Keep calculations and order decisions out of UI components. The UI displays state and sends explicit user commands only.

## Modularity and organization

- Keep application code flat inside the single top-level `puddle_jump` package while the project is small.
- Organize behavior into focused modules with plain names and cohesive responsibilities.
- Keep concerns such as strategies, risk, execution, market data, storage, and reporting separate.
- Avoid catch-all modules, miscellaneous utility files, hidden coupling, and circular dependencies.
- Do not create one-file subpackages or repeat names such as `stock_prices/stock_prices.py`.
- Create a subpackage only when an area has grown into several substantial modules and grouping them makes the project easier to navigate.

## Project structure

Use this as the initial shape. Keep directory names plain and change them when ownership becomes clearer.

```text
puddle-jump/
├── config/
│   ├── stock_pool.json
│   └── strategy.toml
├── data/
│   ├── trading-days/YYYY-MM-DD/
│   ├── replay-results/
│   └── market/
├── src/puddle_jump/
│   ├── __init__.py
│   ├── main.py
│   ├── stock_pool.py
│   ├── daily_watchlist.py
│   ├── stock_prices.py
│   ├── rising_prices.py
│   ├── falling_prices.py
│   ├── decisions.py
│   ├── decision_replay.py
│   ├── alpaca_data.py
│   ├── check_alpaca_data.py
│   ├── history_cache.py
│   ├── strategy_history.py
│   ├── replay_history.py
│   └── ...
└── ui/src/
```

- Keep generated trading data out of source directories.
- Start paper trading with a direct `buy_stocks()` operation. Add a separate `sell_stocks()` operation when needed instead of prematurely creating a generic order-execution framework.

## Coding style

- Do not sound lame. Ever. Write like a person: direct, natural, and plain. Avoid corporate filler, canned phrases, forced enthusiasm, and marketing language.
- Beginner readability is a project requirement. Clever code that is harder to follow is not an improvement.
- Follow the spirit of the owner's `codewars-challenges` solutions: direct, readable, and easy to trace from input to output.
- Use plain everyday language in directory names, files, functions, variables, logs, comments, reports, and UI text.
- Name functions after the action they perform, such as `check_prices()`, `decide_trades()`, `buy_stocks()`, and `write_daily_report()`.
- Name values after what they contain, such as `stocks_to_watch`, `stock_prices`, and `daily_profit`. Avoid vague names such as `data`, `item`, `obj`, `handler`, or `processor` when a specific name is available.
- Avoid abbreviations unless the abbreviated form is the normal domain term and is clearer than spelling it out.
- Prefer clear loops, conditionals, descriptive intermediate variables, and small focused functions over clever or compressed code.
- Prefer pure functions for calculations and trading decisions: pass values in, initialize an explicit result, and return the result without hidden side effects.
- For non-trivial logic, favor a visible `result` variable and an explicit return over a compressed expression.
- Add docstrings or short comments around trading rules and non-obvious decisions. Explain purpose and reasoning rather than narrating obvious syntax.
- Avoid dense one-liners, unnecessary metaprogramming, deep inheritance, premature generalization, and abstraction for its own sake.
- Use built-ins and library helpers selectively. If chaining them obscures the algorithm, write the logic explicitly.
- Do not reimplement well-tested standard, numerical, or data-processing primitives without a concrete reason.
- Optimize first for correctness, readability, and debuggability; optimize performance when measurement or system requirements justify it.

## Working practices

- Treat this file as a living team agreement. Raise concerns, challenge weak decisions, and propose concrete alternatives when new evidence changes a tradeoff.
- Add type hints to new Python code.
- Keep domain logic independent of storage, transport, and UI concerns.
- Prefer simple, explicit designs; introduce additional services or databases only for a demonstrated need.
- Build one small feature at a time and give each feature its own pull request.
- Keep every pull request focused on one purpose and leave the project working when merged.
- Do not mix unrelated cleanup, refactoring, or future scaffolding into a feature pull request.
- Create directories and shared records only when the current feature needs them. Do not generate the full planned tree up front.
- Do not add automated unit tests or testing dependencies during the initial exploration. Historical strategy replay commands are useful evaluation tools and are not unit tests.
- Revisit automated testing only after an explicit decision by the project owner.
- Evaluate the trading idea against real historical inputs before building simulated accounts, order execution, or the user interface.
- Historical evaluation must use only prices available at each simulated time, include estimated spread and slippage, and keep exploration periods separate from final evaluation periods.
- Agree on the viability measures before viewing final results. Stop after the viability report so the project owner can decide whether to continue, change the strategy, or end the project.
- The project owner handles Git: branches, commits, pushes, pull requests, merges, tags, and releases.
- Agents may inspect Git state but must not change it unless the project owner explicitly asks for a specific Git action.
- After completing one build step, stop and report the changed files, checks run, and a suggested pull-request title and summary for the owner to use.
- Before starting a build step, agree with the project owner on that step's behavior and acceptance checks. Do not assume details belonging to later steps.

## Pull request plan

The project owner creates and manages the pull requests. Build these one at a time in order, then stop for review. Revisit later steps when earlier work teaches us something; the list is a guide, not permission to build ahead.

### Baseline

The project owner established `main` with this agreement, the chosen project icon, `.env.example`, and a practical `.gitignore`. This one-time baseline was not a feature pull request.

### Repository introduction

1. **Brief README:** Add a very short `README.md` for repository visitors with the project logo and a one-sentence description.

### Python application

2. **Python project setup:** Add Python 3.14 metadata, `uv`, the importable `puddle_jump` package, `ruff`, and one simple command that proves the package runs.
3. **Stock pool:** Save a dated S&P 500 snapshot plus the agreed extra technology stocks in `config/stock_pool.json`, add `load_stock_pool()`, and print the totals.
4. **Daily watchlist:** Save and load a small, manually selected watchlist for one trading day and reject symbols outside the eligible stock pool.
5. **Strategy settings:** Add `config/strategy.toml` and `load_strategy_settings()` with simple validation for the initial interval, trend windows, and thresholds.
6. **Stock price observations:** Add the small price record and collect ordered price observations for each watched stock.
7. **Rising-price check:** Add one pure function that decides whether a stock has risen for the configured number of observations and minimum percentage.
8. **Falling-price check:** Add pure functions that detect a steady decline over the configured sell window and a fast drop from the recent high.
9. **Buy decision:** Return `BUY` only when the rising-price rule passes and the stock is not already owned; otherwise return `NO_ACTION` with a reason.
10. **Sell decision:** Return `SELL` when an owned stock reaches its maximum loss, drops quickly from its recent high, or passes the falling-price rule; otherwise return `NO_ACTION` with a reason.
11. **Decision replay:** Feed fixed example prices through the same buy and sell decision functions and verify the resulting decisions. Do not simulate money or trades yet.

### Early viability checkpoint

12. **Alpaca historical data access:** Add `alpaca-py` and the small `.env` loader, confirm they work with Python 3.14, and create the read-only stock-price client. Stop and discuss rather than silently changing Python if compatibility fails.
13. **Historical replay inputs:** Cache one-minute prices for ten stocks across ten completed trading days. Keep the 30-day local cache out of Git and reuse it between runs.
14. **Historical viability report:** Replay the actual buy and sell rules, include estimated costs, and report returns, trade count, winners, and an equal-weight baseline.
15. **Thirty-minute entry rule:** Replace the short consecutive-price buy rule with the agreed 30-minute rise, QQQ comparison, and five-minute confirmation, then compare it with the existing replay result.

Stop after the thirty-minute comparison. The project owner must explicitly decide whether to continue, change the strategy, or end the project before the remaining work begins.

### Simulated trading

16. **Simulated account:** Track starting cash, available cash, owned stocks, share counts, and account value without connecting to Alpaca.
17. **Trading limits:** Check the agreed position, exposure, and daily loss limits before allowing a simulated trade.
18. **Simulated buy:** Update the simulated account for a buy and prevent repeat buys while the stock is already owned.
19. **Simulated sell:** Update the simulated account for a sell and update cash and ownership.
20. **Trade history:** Record simulated buys, sells, decisions, reasons, and account changes in SQLite.
21. **Daily scorecard:** Generate `report.md` from the recorded trade history and account state.
22. **Trading loop:** Check the daily watchlist on the configured interval, make decisions, update the simulated account, and record what happened.
23. **Simulated trading day:** Run the complete loop against fixed prices and verify the decisions, simulated trades, ending account, trade history, and daily scorecard together.

### Alpaca paper integration

24. **Current stock prices:** Request one IEX snapshot for the daily watchlist and translate the response into the project's plain stock-price records.
25. **Market clock:** Read Alpaca's clock and report whether the regular stock market is open, plus the next open and close.
26. **Paper account status:** Create the forced-paper trading client and read cash, buying power, account value, blocked status, and the user-controlled Trades Suspended status without changing them.
27. **Paper positions:** Read current Alpaca paper positions and translate them into the project's plain position records.

Before the next pull request, stop so the project owner can review the read-only integration and deliberately turn off Trades Suspended.

28. **Buy stocks through Alpaca:** Add `buy_stocks()` using a fractional day market order for the configured dollar amount, forced through `TradingClient(..., paper=True)`.
29. **Sell stocks through Alpaca:** Add `sell_stocks()` using a day market order for the currently owned share quantity, forced through the paper client.
30. **Order results:** Read submitted Alpaca orders until they are filled, rejected, canceled, or otherwise finished, then return the result in plain language.
31. **Alpaca trade history:** Save Alpaca order IDs, results, fills, reasons, and account changes through the existing SQLite trade-history code.

### User interface

32. **Read-only Python API:** Expose the watchlist, prices, account, decisions, and daily results without adding trading logic.
33. **React application shell:** Set up the TypeScript and TSX application, routing, formatting, and the project icon.
34. **Trading dashboard:** Display the current watchlist, prices, momentum, positions, latest decisions, reasons, and daily result.
35. **Daily history view:** Let the user select a previous trading day and read its scorecard and activity.

### Later work

36. **Paper-trading review:** Compare replay and paper results, document differences, and decide whether the strategy is ready for further work.
37. **Live trading:** Plan this only after an explicit team decision; it is not authorized by this roadmap alone.
