# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Portfolio rebalancer with two implementations:
- **Python CLI** (`script.py`): Reads portfolio data from `.env`, calculates allocations, and prints rebalancing advice
- **Web app** (`index.html`): Self-contained single-page application (HTML/CSS/JS, no frameworks) with live exchange rates, donut charts, and URL-based sharing

## Running

```bash
# Python script
source .venv/bin/activate
python script.py

# Web app (serves index.html with CORS support for Frankfurter API)
python3 -m http.server 8000
```

No build step, test suite, or linter is configured.

## Architecture

### Python (`script.py`)
Reads stock quantities and liquidity amounts from `.env` (via python-dotenv). Hardcoded asset definitions (ticker, price, target split) live in the script. `validate_split()` ensures allocations sum to 100%. Outputs total portfolio value, per-asset current vs target percentages, and buy/sell recommendations.

### Web App (`index.html`)
Everything in one file (~1000 lines). Key patterns:
- **State object** (`state`): holds assets config, exchange rates, stock quantities, and liquidity — drives all calculations
- **Reactive rendering**: any input change triggers full recalculation and DOM update
- **Frankfurter API**: fetches live EUR/USD rate from ECB; falls back to manual input on failure
- **URL sharing**: portfolio config encoded as base64 in URL hash fragment for stateless sharing
- **LocalStorage**: persists stocks and liquidity data across sessions
- **CSS variables**: dark theme palette defined at `:root`; uses Google Fonts (DM Sans, JetBrains Mono)

### Data Flow (Web App)
1. On load: fetch exchange rate → load from URL hash or localStorage → render
2. On edit: update state → recalculate totals/percentages/advice → re-render tables and donut charts
3. On share: serialize state to base64 → update URL hash

## Dependencies

- **Python**: python-dotenv (installed in `.venv`)
- **Web**: no npm/node dependencies; external: Frankfurter API, Google Fonts CDN

## Environment

`.env` stores portfolio holdings (see `.env.example` for template). Git-ignored.
