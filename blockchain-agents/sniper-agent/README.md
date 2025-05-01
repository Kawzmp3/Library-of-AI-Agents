# Sniper Agent

An AI agent that monitors and identifies new token launches for early investing opportunities.

## Features

- Real-time monitoring of new token launches
- Alerts with token details and links
- Historical tracking of discovered tokens
- Customizable filters for token quality
- Visual alerts and sound notifications

## Requirements

- Python 3.8+
- pandas
- requests
- rich (for terminal UI)
- playsound (for audio alerts)

## Installation

```bash
pip install pandas requests rich playsound
```

## Usage

```python
from sniper_agent import TokenScanner

# Initialize the scanner
scanner = TokenScanner()

# Start monitoring for new token launches
scanner.monitor_new_launches()

# Or view previously identified tokens
scanner.show_past_tokens()
```

## Configuration

The agent can be configured by modifying the parameters at the top of the `sniper_agent.py` file:

- Scan interval
- Display settings
- Filtering criteria
- Alert settings

## Disclaimer

This agent is provided for educational purposes only. Newly launched tokens can be extremely volatile and risky. Many new tokens may be scams or have security vulnerabilities. Always conduct thorough research before investing in any token, especially new launches. 