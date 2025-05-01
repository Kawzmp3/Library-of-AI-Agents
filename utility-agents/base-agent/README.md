# Base Agent

The foundational parent class for creating new AI agents. This provides core functionality that can be extended for specialized agent implementations.

## Features

- Common initialization logic
- Standardized agent type tracking
- Timestamp management
- Abstract run method for consistent implementation

## Requirements

- Python 3.8+
- pandas (for data handling)
- datetime (included in standard library)
- pathlib (included in standard library)

## Installation

```bash
pip install pandas
```

## Usage

The Base Agent is intended to be extended by more specialized agents:

```python
from base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        # Initialize with a type identifier
        super().__init__('custom_agent_type')
        # Add custom initialization
        self.my_custom_property = "value"
    
    def run(self):
        # Required implementation of abstract method
        print(f"Agent of type {self.type} running since {self.start_time}")
        # Add custom logic here
```

## Extending the Base Agent

When creating a new agent that extends BaseAgent:

1. Always call the parent `__init__` method with your agent's type identifier
2. Implement the required `run()` method
3. Add your specialized functionality as additional methods
4. Use the built-in properties like `start_time` when needed

## Available Properties

- `type`: The agent type identifier
- `start_time`: The datetime when the agent was initialized 