# Clips Agent

Create short, engaging video clips from longer content. Perfect for content creators, streamers, and marketers looking to repurpose long-form content into bite-sized clips.

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=Clips+Agent" alt="Clips Agent Demo" width="600">
</p>

## ✨ Features

- **YouTube Integration**: Download and clip YouTube videos directly by URL
- **Customizable Clip Length**: Set your preferred clip duration
- **Batch Processing**: Process multiple videos in a single run
- **Transcript-based Clipping**: Use transcripts to identify interesting segments
- **Analytics Tracking**: Keep track of clip statistics
- **Organized Output**: Clean directory structure for your clips

## 🛠️ Requirements

- Python 3.8+
- FFmpeg
- yt-dlp
- moviepy
- pandas (for analytics)

## 📦 Installation

1. Install required packages:

```bash
pip install yt-dlp moviepy pandas
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
  ├── videos/           # Downloaded videos
  ├── clips/            # Generated clips
  └── transcripts/      # Transcripts of videos
```

## 🚀 Usage

### Basic Usage

```bash
# Create clips from a YouTube video
python clips_agent.py --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Create clips from a local video file
python clips_agent.py --file "/path/to/video.mp4"

# Customize clip duration
python clips_agent.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --duration 30

# Process multiple URLs from a file
python clips_agent.py --url-file "urls.txt"
```

### Command-line Options

- `--url`: YouTube URL to download and clip
- `--file`: Local video file to clip
- `--url-file`: File containing YouTube URLs (one per line)
- `--duration`: Clip duration in seconds (default: 60)
- `--output-dir`: Custom output directory for clips
- `--min-clip-length`: Minimum clip length in seconds
- `--max-clip-length`: Maximum clip length in seconds
- `--no-audio`: Create clips without audio
- `--format`: Specify output format (default: mp4)

## 📝 Examples

### Create 30-second Clips from a YouTube Video

```bash
python clips_agent.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --duration 30
```

### Process Multiple Videos from a File

```bash
python clips_agent.py --url-file "youtube_urls.txt" --duration 45
```

### Create Clips from a Local Video File

```bash
python clips_agent.py --file "my_long_video.mp4" --duration 60 --output-dir "my_clips"
```

## 🧠 How It Works

The Clips Agent follows these steps:

1. **Download** the YouTube video (if URL provided)
2. **Extract** the transcript using available subtitles or speech recognition
3. **Analyze** content to identify interesting segments
4. **Create** clips of the specified duration
5. **Save** clips to the output directory
6. **Track** clip analytics

## 📊 Analytics

The agent tracks analytics for all generated clips, including:

- Clip duration
- Source video
- Start/end timestamps
- View count potential
- Clip quality score

## 📋 Troubleshooting

- **YouTube download errors**: Check your internet connection and YouTube URL
- **FFmpeg issues**: Ensure FFmpeg is properly installed
- **No clips generated**: Check that the video downloaded successfully and has interesting content
- **Permission errors**: Check write permissions to output directories

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 💰 Monetization

Want to earn money from your clips? Here's how:

1. Create clips from trending topics and popular content
2. Upload to platforms that share ad revenue
3. Track analytics to see which clips perform best
4. Focus on high-performing content types

The Clips Agent helps you automate this process so you can focus on creating more content and growing your audience. 