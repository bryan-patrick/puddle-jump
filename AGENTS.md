# Puddle Jump Agent Guide

## Project direction

Puddle Jump is a Python trading and backtesting project. Keep the system small, testable, and consistent between simulation and real-time operation.

The initial product starts with a broad pool of eligible stocks, selects a smaller daily watchlist from the news, observes price momentum on a relaxed interval, and produces simple buy, sell, or no-action decisions.

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
- Use `NewsClient` for historical news and keep it separate from stock-price requests.
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
- Keep the full stock pool separate from the smaller daily watchlist selected from the news.
- Start with a manually selected daily watchlist. Automate the news scan only after the format and selection process are understood.
- Store symbols separately from changing daily outlooks and prices.
- Before paper trading, use Alpaca to confirm that a selected stock is active, tradable, and eligible for the planned fractional order.
- Record a daily initial outlook for every watched stock. Use a score from `-1.0` to `1.0`, where negative is unfavorable, zero is neutral, and positive is favorable.
- Include the symbol, score, readable label, explanation, sources, and timestamp in every outlook entry.
- Allow manual and automated news analysis to produce the same outlook format so either can be used without changing the strategy.
- Record the stock's daily reference price separately from its news-outlook weight; do not overload one value with both meanings.
- Record each observed stock price with its symbol and timezone-aware timestamp, keeping observations in chronological order for each stock.
- Organize human-inspectable daily inputs and reports under a `YYYY-MM-DD` trading-day directory based on the relevant exchange timezone. Use unambiguous ISO 8601 timestamps with offsets for updates made during the day.
- Preserve the initial outlook and append timestamped revisions instead of silently overwriting history.
- Keep `watchlist.json` at the trading-day root and timestamped outlook files under `outlooks/`.
- Keep live operational state and event records in SQLite, larger price histories in Parquet, and the daily summary in Markdown.
- Keep Alpaca market data and news downloads local and ignored by Git unless Alpaca gives written permission to redistribute them. Commit the replay plan, source links, and manually assigned outlooks so the inputs can be recreated with the owner's credentials.

## Daily scorecard

- Create a `report.md` inside every trading-day directory, including days when no trades occur.
- Record starting and ending cash, starting and ending account value, daily profit or loss in dollars and percent, trades made, results by stock, open positions, decisions and reasons, risk limits triggered, errors, and short notes.
- Generate report numbers from recorded events and positions rather than entering totals by hand.
- Keep the report easy to scan in plain language. It should answer: What did we do, why did we do it, and how did we do?

## Initial strategy

- Run one simple, configurable loop for the daily watchlist. A roughly 30-second interval is a reasonable starting point, not a hard-coded rule.
- Buy only when the daily news outlook is favorable, every price in the latest configured number of observations is higher than the one before it, and the total move from first to last meets the configured minimum percentage.
- Sell when the price falls below its daily reference value or every price in the latest configured sell window is lower than the one before it. Half the buy window is a starting hypothesis to test, not an assumed truth.
- Return exactly one explicit decision: `BUY`, `SELL`, or `NO_ACTION`. Include a readable reason with every decision.
- Keep intervals, trend windows, outlook thresholds, and other strategy values in configuration rather than scattering constants through the code.
- Make every decision explainable from its recorded inputs.
- Enforce configurable maximum position size, maximum total exposure, and daily loss limits before submitting any order.
- Provide an emergency stop that prevents new orders and cancels pending orders without depending on the UI.

## User interface

- Render results with React and TSX, backed by a thin HTTP interface to the Python application.
- Show the watchlist, daily outlook, reference and current prices, recent momentum, open position, latest decision, and the reason for that decision.
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
│   ├── replay-inputs/YYYY-MM-DD/
│   └── market/
├── src/puddle_jump/
│   ├── __init__.py
│   ├── main.py
│   ├── stock_pool.py
│   ├── daily_watchlist.py
│   ├── daily_outlook.py
│   ├── trading_day_files.py
│   ├── stock_prices.py
│   ├── rising_prices.py
│   ├── falling_prices.py
│   ├── decisions.py
│   ├── decision_replay.py
│   ├── alpaca_data.py
│   ├── check_alpaca_data.py
│   ├── historical_inputs.py
│   ├── save_historical_inputs.py
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
- Name values after what they contain, such as `stocks_to_watch`, `stock_prices`, `daily_outlook`, and `daily_profit`. Avoid vague names such as `data`, `item`, `obj`, `handler`, or `processor` when a specific name is available.
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
- Do not add automated tests or testing dependencies during the initial exploration. Manually run the current feature and report what was checked.
- Revisit automated testing only after an explicit decision by the project owner.
- Evaluate the trading idea against real historical inputs before building simulated accounts, order execution, or the user interface.
- Historical evaluation must use only news and prices available at each simulated time, include estimated spread and slippage, and keep exploration periods separate from final evaluation periods.
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
6. **Daily outlook:** Add the plain daily outlook record plus functions to write and read the agreed JSON format.
7. **Trading-day files:** Create the `YYYY-MM-DD` directory for a chosen exchange date and preserve timestamped outlook updates.
8. **Stock price observations:** Add the small price record and collect ordered price observations for each watched stock.
9. **Rising-price check:** Add one pure function that decides whether a stock has risen for the configured number of observations and minimum percentage.
10. **Falling-price check:** Add one pure function that decides whether a stock is falling for the configured sell window.
11. **Buy decision:** Return `BUY` only when the outlook and rising-price rules pass and the stock is not already owned; otherwise return `NO_ACTION` with a reason.
12. **Sell decision:** Return `SELL` when an owned stock falls below its initial price or passes the falling-price rule; otherwise return `NO_ACTION` with a reason.
13. **Decision replay:** Feed fixed example prices through the same buy and sell decision functions and verify the resulting decisions. Do not simulate money or trades yet.

### Early viability checkpoint

14. **Alpaca historical data access:** Add `alpaca-py` and the small `.env` loader, confirm they work with Python 3.14, and create read-only stock-price and news clients. Stop and discuss rather than silently changing Python if compatibility fails.
15. **Historical replay inputs:** Lock a small set of past stocks and dates, save the news and prices that were available at each simulated time, and manually assign outlooks without viewing later prices.
16. **Historical viability report:** Replay the actual buy and sell rules, include estimated spread and slippage, compare exploration and evaluation periods, and report returns, losses, trade count, and simple baselines.

Stop after the viability report. The project owner must explicitly decide whether to continue, change the strategy, or end the project before the remaining work begins.

### Simulated trading

17. **Simulated account:** Track starting cash, available cash, owned stocks, share counts, and account value without connecting to Alpaca.
18. **Trading limits:** Check the agreed position, exposure, and daily loss limits before allowing a simulated trade.
19. **Simulated buy:** Update the simulated account for a buy and prevent repeat buys while the stock is already owned.
20. **Simulated sell:** Update the simulated account for a sell and update cash and ownership.
21. **Trade history:** Record simulated buys, sells, decisions, reasons, and account changes in SQLite.
22. **Daily scorecard:** Generate `report.md` from the recorded trade history and account state.
23. **Trading loop:** Check the daily watchlist on the configured interval, make decisions, update the simulated account, and record what happened.
24. **Simulated trading day:** Run the complete loop against fixed prices and verify the decisions, simulated trades, ending account, trade history, and daily scorecard together.

### Alpaca paper integration

25. **Current stock prices:** Request one IEX snapshot for the daily watchlist and translate the response into the project's plain stock-price records.
26. **Market clock:** Read Alpaca's clock and report whether the regular stock market is open, plus the next open and close.
27. **Paper account status:** Create the forced-paper trading client and read cash, buying power, account value, blocked status, and the user-controlled Trades Suspended status without changing them.
28. **Paper positions:** Read current Alpaca paper positions and translate them into the project's plain position records.

Before the next pull request, stop so the project owner can review the read-only integration and deliberately turn off Trades Suspended.

29. **Buy stocks through Alpaca:** Add `buy_stocks()` using a fractional day market order for the configured dollar amount, forced through `TradingClient(..., paper=True)`.
30. **Sell stocks through Alpaca:** Add `sell_stocks()` using a day market order for the currently owned share quantity, forced through the paper client.
31. **Order results:** Read submitted Alpaca orders until they are filled, rejected, canceled, or otherwise finished, then return the result in plain language.
32. **Alpaca trade history:** Save Alpaca order IDs, results, fills, reasons, and account changes through the existing SQLite trade-history code.

### User interface

33. **Read-only Python API:** Expose the watchlist, outlooks, prices, account, decisions, and daily results without adding trading logic.
34. **React application shell:** Set up the TypeScript and TSX application, routing, formatting, and the project icon.
35. **Trading dashboard:** Display the current watchlist, prices, outlooks, positions, latest decisions, reasons, and daily result.
36. **Daily history view:** Let the user select a previous trading day and read its scorecard and activity.

### Later work

37. **Automated news outlook:** Scan news across the stock pool, select the daily watchlist, and write the same outlook format already accepted from manual input.
38. **Paper-trading review:** Compare replay and paper results, document differences, and decide whether the strategy is ready for further work.
39. **Live trading:** Plan this only after an explicit team decision; it is not authorized by this roadmap alone.
