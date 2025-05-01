# ShortVid Agent

A powerful video processing agent that can add subtitles to videos, transcribe audio using Whisper, and generate audio from text.

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=ShortVid+Agent" alt="ShortVid Agent Demo" width="600">
</p>

## ✨ Features

- **Automatic Transcription**: Use OpenAI's Whisper to transcribe video audio into accurate subtitles
- **Beautiful Subtitle Styles**: Choose from multiple subtitle styles (minimal, modern, cinematic, bold)
- **Text-to-Speech**: Generate high-quality voiceovers using ElevenLabs API
- **Batch Processing**: Process entire directories of videos at once
- **Analytics Tracking**: Keep track of processed videos and statistics
- **Multi-language Support**: Process videos in various languages with Whisper

## 🛠️ Requirements

- Python 3.8+
- FFmpeg
- OpenAI Whisper
- ElevenLabs API key (only for text-to-speech functionality)

## 📦 Installation

1. Install required packages:

```bash
pip install openai-whisper requests pandas
```

2. Install FFmpeg:

```bash
# MacOS (with Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows (with Chocolatey)
choco install ffmpeg
```

3. Set up directory structure:

```
data/
  ├── audio/                # Generated audio files
  ├── raw_videos/           # Input video files
  ├── final_videos/         # Output processed videos
  └── text_input/           # Input text files
      └── input.txt
```

## 🚀 Usage

### Basic Usage

```bash
# Process with specific text
python shortvid_agent.py --text "This is a test" --style modern

# Process all videos with Whisper transcription
python shortvid_agent.py --all

# Use a text file for input
python shortvid_agent.py --file path/to/text_file.txt

# Generate audio using ElevenLabs (requires API key)
python shortvid_agent.py --key YOUR_API_KEY --text "Text to speech" --style cinematic
```

### Command-line Options

- `--key`: ElevenLabs API key (required for audio generation)
- `--text`: Text to process directly
- `--file`: Path to text file to use instead of default
- `--all`: Process all videos with Whisper transcription
- `--model`: Whisper model size (tiny, base, small, medium, large)
- `--style`: Subtitle style preset (minimal, modern, cinematic, bold)
- `--lang`: Language for transcription (default: en)

## 🎨 Subtitle Styles

| Style | Description |
|-------|-------------|
| **minimal** | Clean, simple subtitles with minimal styling |
| **modern** | Modern look with slight background and shadow |
| **cinematic** | Movie-like subtitles with stronger outline and shadow |
| **bold** | Bold text for maximum readability |

## 🌐 Whisper Model Sizes

| Model | Speed | Accuracy | RAM Usage |
|-------|-------|----------|-----------|
| **tiny** | Fastest | Lowest | ~1GB |
| **base** | Fast | Good | ~1GB |
| **small** | Medium | Better | ~2GB |
| **medium** | Slow | High | ~5GB |
| **large** | Slowest | Highest | ~10GB |

## 📝 Examples

### Add Modern Style Subtitles to All Videos

```bash
python shortvid_agent.py --all --style modern
```

### Process Videos in Japanese

```bash
python shortvid_agent.py --all --lang ja --model medium
```

### Process a Text File with Bold Subtitles

```bash
python shortvid_agent.py --file src/data/my_text.txt --style bold
```

## 📊 Analytics

The agent tracks basic analytics for all processed videos in the `data/analytics.csv` file, including:

- Timestamp
- Text content
- Video path
- Duration
- Word count

## 📋 Troubleshooting

- **No video files found**: Make sure to add video files to the `data/raw_videos/` directory
- **Whisper not installed**: Run `pip install openai-whisper`
- **FFmpeg errors**: Ensure FFmpeg is properly installed and available in your PATH

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests. 