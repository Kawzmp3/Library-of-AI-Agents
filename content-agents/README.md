# Content AI Agents

This collection contains AI agents focused on content creation, media processing, analysis, and distribution.

## Available Agents

### ShortVid Agent
Adds beautiful subtitles to videos using Whisper transcription or generates voiceovers with ElevenLabs.

### Clips Agent
Creates engaging clips from longer videos, perfect for social media and content repurposing.

### Sentiment Agent
Analyzes sentiment from social media and market data to gauge public opinion.

### Chat Agent
Interactive chat bot that responds to user queries with AI-powered responses.

### Focus Agent
Monitors and improves productivity by analyzing work sessions and providing feedback.

### Compliance Agent
Analyzes content for compliance with guidelines and regulations.

### Tweet Agent
Generates engaging Twitter/X content from longer text.

### TikTok Agent
Automates interactions with TikTok content for analysis and engagement.

### Research Agent
Generates research ideas and content based on trending topics and user interests.

## Installation

Each agent has its own dependencies and requirements. Navigate to the specific agent's folder for detailed setup instructions.

## Common Requirements

- Python 3.8+
- FFmpeg (for video processing)
- OpenAI Whisper (for speech recognition)
- Various content APIs

## Usage

Most content agents follow a similar pattern:

```python
# Import the agent
from shortvid_agent import VideoAgent

# Initialize
agent = VideoAgent()

# Process content
agent.generate_videos("Your text here")

# Or run with command line options
# python shortvid_agent.py --text "Add this text as subtitles" --style modern
```

See each agent's README for specific usage instructions and configuration options. 