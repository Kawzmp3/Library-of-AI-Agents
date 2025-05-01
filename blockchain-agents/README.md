# Blockchain AI Agents

This collection contains AI agents focused on blockchain analysis, crypto monitoring, and on-chain data processing.

## Available Agents

### Sniper Agent
Monitors and identifies new token launches for early investing opportunities.

### TX Agent
Tracks transactions from specific wallets and identifies notable on-chain movements.

### Solana Agent
Specialized in Solana blockchain analysis, token evaluation, and opportunity detection.

### Chart Analysis Agent
Analyzes price charts and technical indicators to identify trading patterns.

### RBI Agent (Research-Based Investment)
Conducts deep research on tokens and projects to identify investment opportunities.

## Installation

Each agent has its own dependencies and requirements. Navigate to the specific agent's folder for detailed setup instructions.

## Common Requirements

- Python 3.8+
- Web3.py
- Blockchain-specific libraries
- Data analysis tools (pandas, numpy)

## Usage

Most blockchain agents follow a similar pattern:

```python
# Import the agent
from sniper_agent import TokenScanner

# Initialize
scanner = TokenScanner()

# Run monitoring
scanner.monitor_new_launches()
```

See each agent's README for specific usage instructions and configuration options. 