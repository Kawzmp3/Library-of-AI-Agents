# Sentiment Agent

An AI agent that analyzes sentiment from social media and market data to gauge public opinion on various topics, particularly in cryptocurrency and financial markets.

## Features

- Real-time sentiment analysis of social media content
- Historical sentiment tracking and change detection
- Automated alerts for significant sentiment shifts
- Support for multiple data sources
- Visualization of sentiment trends

## Requirements

- Python 3.8+
- pandas
- requests
- transformers (for sentiment analysis)
- asyncio (for concurrent processing)
- API access for social media platforms

## Installation

```bash
pip install pandas requests transformers asyncio
```

## Usage

```python
from sentiment_agent import SentimentAgent

# Initialize the agent
agent = SentimentAgent()

# Run sentiment analysis once
agent.analyze_and_announce_sentiment(tweets)

# Or run continuously
agent.run()
```

## Configuration

The agent can be configured by modifying the parameters at the top of the `sentiment_agent.py` file:

- Social media sources
- Sentiment thresholds
- Polling frequency
- Alert settings

## How It Works

1. The agent collects data from configured social media sources
2. Content is analyzed using a fine-tuned sentiment analysis model
3. Results are aggregated to determine overall sentiment
4. Significant changes trigger alerts
5. Historical data is maintained for trend analysis

## Disclaimer

This agent is provided for educational purposes only. Sentiment analysis should not be the sole basis for investment decisions. Always combine multiple sources of information and conduct thorough research before making financial decisions. 