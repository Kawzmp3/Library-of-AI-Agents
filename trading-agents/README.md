# Trading AI Agents

This collection contains AI agents focused on trading, financial analysis, market monitoring, and investment strategies.

## Available Agents

### Trading Agent
Advanced portfolio management and allocation agent that analyzes market data and executes trades.

### CopyBot Agent
Monitors and copies successful trading strategies from high-performance wallets.

### Risk Agent
Manages portfolio risk by monitoring positions, enforcing risk limits, and protecting capital.

### Strategy Agent
Evaluates trading signals and develops allocation strategies based on market conditions.

### Whale Agent
Monitors large movements in open interest and market patterns to detect whale activity.

### Funding Agent
Analyzes funding rates across exchanges to identify arbitrage opportunities.

### Liquidation Agent
Tracks liquidation events and market impact to identify trading opportunities.

### Funding Arbitrage Agent
Specialized agent for executing funding rate arbitrage strategies between exchanges.

### CoinGecko Agent
Multi-agent system that analyzes coin market data from CoinGecko API.

### Listing Arbitrage Agent
Identifies new token listings on exchanges for potential arbitrage opportunities.

### New/Top Agent
Scans for newly listed tokens and top gainers to identify early investment opportunities.

## Installation

Each agent has its own dependencies and requirements. Navigate to the specific agent's folder for detailed setup instructions.

## Common Requirements

- Python 3.8+
- Pandas
- Requests
- Various exchange APIs

## Usage

Most trading agents follow a similar pattern:

```python
# Import the agent
from trading_agent import TradingAgent

# Initialize
agent = TradingAgent()

# Run a single monitoring cycle
agent.run_monitoring_cycle()

# Or run continuously
agent.run()
```

See each agent's README for specific usage instructions and configuration options. 