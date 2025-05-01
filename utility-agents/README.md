# Utility AI Agents

This collection contains general-purpose utility agents that provide foundational functionality and automation tools.

## Available Agents

### Phone Agent
Creates a voice-activated phone system with natural language understanding and response.

### Code Runner Agent
Automates code execution and testing with IDE integration.

### Million Agent
A question-answering agent based on the Million book knowledge base.

### Base Agent
Core functionality and parent class for creating new agents.

## Installation

Each agent has its own dependencies and requirements. Navigate to the specific agent's folder for detailed setup instructions.

## Common Requirements

- Python 3.8+
- Various utility libraries
- Language model access

## Usage

Utility agents have varied usage patterns depending on their specific purpose:

```python
# Base Agent Example
from base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__('custom_agent_type')
        
    def run(self):
        # Custom implementation
        pass
```

See each agent's README for specific usage instructions and configuration options. 