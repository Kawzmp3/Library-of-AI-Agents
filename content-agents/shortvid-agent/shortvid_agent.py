"""
Video Agent: Convert text to speech and combine with background videos.

This agent:
1. Takes input text (either from a text file or direct input)
2. Processes video clips by:
   - Adding subtitles to videos (USE_SUBTITLES=True)
   - OR generating audio from text and combining with video (USE_SUBTITLES=False)
3. Saves the resulting videos to the final_vids directory
4. Tracks analytics on video generation

Features:
- Add subtitles to videos with customizable styles
- Use existing subtitle files if available
- Generate high-quality audio from text using ElevenLabs API
- Transcribe audio using Whisper to generate accurate subtitles
- Support for multiple video formats
- Analytics tracking for video generation

Usage:
  python shortvid_agent.py [options]

Options:
  --key API_KEY       ElevenLabs API key (required for audio generation)
  --text TEXT         Text to process directly
  --file FILE_PATH    Path to text file to use instead of default
  --all               Process all videos with Whisper transcription
  --model SIZE        Whisper model size (tiny, base, small, medium, large)
  --style STYLE       Subtitle style preset (minimal, modern, cinematic, bold)
  --lang LANGUAGE     Language for transcription (default: en)

Examples:
  # Process all videos with Whisper transcription
  python shortvid_agent.py --all
  
  # Process with custom text and modern style
  python shortvid_agent.py --text "This is a test" --style modern
  
  # Generate audio with ElevenLabs API
  python shortvid_agent.py --key YOUR_API_KEY --text "Text to speech" --style cinematic

"""

import os
import sys
import random
import time
import json
import math
import traceback
import requests
import subprocess
import re
import argparse
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
try:
    import whisper
except ImportError:
    whisper = None
    print("⚠️ OpenAI Whisper not installed. Voice transcription unavailable.")
    print("   Install with: pip install openai-whisper")

# ======== INPUT SETTINGS ========
USE_TEXT_FILE = False
INPUT_TEXT_FILE = "src/data/text_input/input.txt"
DELAY_BETWEEN_REQUESTS = 0.5  # seconds between processing requests

# ======== SUBTITLE SETTINGS ========
USE_SUBTITLES = True  # If True, add subtitles to video; if False, generate audio and combine with video
USE_EXISTING_SUBTITLES = True  # Try to use existing subtitles in video if available
SUBTITLE_POSITION = "bottom"  # Options: "top", "bottom", "middle"
SUBTITLE_FONT_SIZE = 24
SUBTITLE_STYLE_PRESET = "modern"  # Options: "minimal", "modern", "cinematic", "bold"

# ======== AUDIO SETTINGS ========
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Victor voice
MODEL_ID = "eleven_multilingual_v2"  # Model for high-quality TTS

# ======== VIDEO SETTINGS ========
MIN_VIDEO_DURATION = 10  # seconds, minimum duration for output videos
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".avi", ".mkv"]
USE_FINISHED_VIDS = False  # If True, use videos from finished_vids directory instead of raw_vids

# ======== WHISPER SETTINGS ========
USE_WHISPER = True  # Use Whisper for transcription when no subtitles are found
WHISPER_MODEL_SIZE = "base"  # Options: "tiny", "base", "small", "medium", "large"
WHISPER_LANGUAGE = "en"  # Default language for transcription
WHISPER_CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence for transcription segments

# ======== DIRECTORY SETTINGS ========
# Directories for audio files, raw videos, and finished videos
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.resolve()  # Assumed to be 2 levels up from script
DATA_DIR = PROJECT_ROOT / "data"
AUDIO_DIR = DATA_DIR / "audio"
RAW_VIDS_DIR = DATA_DIR / "raw_videos"
FINAL_VIDS_DIR = DATA_DIR / "final_videos"
FINISHED_VIDS_DIR = DATA_DIR / "finished_vids"
ANALYTICS_FILE = DATA_DIR / "analytics.csv"

# ======== CONTENT SETTINGS ========
# Minimum length for valid text input
MIN_TEXT_LENGTH = 10

# Create subtitle style presets
SUBTITLE_STYLES = {
    "minimal": {
        "FontSize": "24",
        "Alignment": "2",
        "PrimaryColour": "&HFFFFFF&",
        "OutlineColour": "&H000000&",
        "BorderStyle": "1",
        "Outline": "1",
        "Shadow": "0"
    },
    "modern": {
        "FontSize": "28",
        "Alignment": "2",
        "PrimaryColour": "&HFFFFFF&",
        "OutlineColour": "&H000000&",
        "BorderStyle": "3",
        "Outline": "1",
        "Shadow": "1",
        "BackColour": "&H80000000&"
    },
    "cinematic": {
        "FontSize": "30",
        "Alignment": "2",
        "PrimaryColour": "&HFFFFFF&",
        "OutlineColour": "&H000000&",
        "BorderStyle": "4",
        "Outline": "2",
        "Shadow": "3",
        "FontName": "Arial"
    },
    "bold": {
        "FontSize": "36",
        "Alignment": "2",
        "PrimaryColour": "&HFFFFFF&",
        "OutlineColour": "&H000000&",
        "BorderStyle": "3",
        "Outline": "3",
        "Shadow": "0",
        "Bold": "1"
    }
}

class VideoAgent:
    """Fire Dev's Video Agent 🎬"""
    
    def __init__(self, api_key=None):
        """Initialize the Video Agent"""
        global USE_SUBTITLES  # Move global declaration to the top of the method
        self.api_key = api_key
        
        # Create necessary directories
        self.audio_dir = AUDIO_DIR
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        self.raw_vids_dir = RAW_VIDS_DIR
        self.raw_vids_dir.mkdir(parents=True, exist_ok=True)
        
        self.final_vids_dir = FINAL_VIDS_DIR
        self.final_vids_dir.mkdir(parents=True, exist_ok=True)
        
        if USE_FINISHED_VIDS:
            self.finished_vids_dir = FINISHED_VIDS_DIR
            self.finished_vids_dir.mkdir(parents=True, exist_ok=True)
        
        # Create analytics file if not exists
        self.analytics_file = ANALYTICS_FILE
        self._initialize_analytics()
        
        # Initialize Whisper model if enabled
        self.whisper_model = None
        if USE_WHISPER and whisper:
            try:
                print(f"🎙️ Loading Whisper {WHISPER_MODEL_SIZE} model...")
                self.whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
                print(f"✅ Whisper model loaded successfully")
            except Exception as e:
                print(f"❌ Error loading Whisper model: {str(e)}")
                self.whisper_model = None
        
        # IMPORTANT: Check for ElevenLabs API key if not using subtitles
        if not USE_SUBTITLES and not self.api_key:
            print("⚠️ Warning: ElevenLabs API key not provided.")
            print("   Text-to-speech functionality will not work without an API key.")
            print("   Run with: python shortvid_agent.py --key YOUR_API_KEY")
            print("   Switching to subtitle mode...")
            USE_SUBTITLES = True
        
        print("🎬 Video Agent initialized!")
        print(f"📂 Audio files will be saved to: {self.audio_dir}")
        print(f"📂 Videos will be saved to: {self.final_vids_dir}")
        print(f"📊 Analytics will be saved to: {self.analytics_file}")
    
    def _initialize_analytics(self):
        """Initialize analytics file if it doesn't exist."""
        try:
            if not self.analytics_file.exists():
                # Create parent directory if it doesn't exist
                self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Create the analytics file with headers
                with open(self.analytics_file, 'w') as f:
                    f.write("timestamp,text,video_path,duration,words\n")
                print(f"✨ Created new analytics file: {self.analytics_file}")
            else:
                print(f"📊 Using existing analytics file: {self.analytics_file}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to initialize analytics file: {str(e)}")
    
    def _analyze_message(self, text):
        """Analyze message for basic statistics."""
        # Get word count
        words = len(text.split())
        
        # Return basic analytics
        return {
            "words": words,
            "chars": len(text)
        }
    
    def _save_analytics(self, message, video_path, duration):
        """Save analytics data to CSV file."""
        try:
            if not self.analytics_file.exists():
                self._initialize_analytics()
                
            # Analyze message
            analysis = self._analyze_message(message)
            
            # Create data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_preview = message[:50].replace(",", " ").replace("\n", " ")
            row = f"{timestamp},{message_preview},{video_path},{duration},{analysis['words']}\n"
            
            # Append to analytics file
            with open(self.analytics_file, 'a') as f:
                f.write(row)
                
            print(f"📊 Analytics saved")
            
        except Exception as e:
            print(f"⚠️ Warning: Failed to save analytics: {str(e)}")
    
    def _validate_content(self, text):
        """Simple validation of content - check minimum length"""
        if not text or len(text) < MIN_TEXT_LENGTH:
            print(f"❌ Content too short (minimum {MIN_TEXT_LENGTH} characters)")
            return False
        
        return True
    
    def _get_input_text(self, text=None):
        """Get input text from either file or direct input"""
        if USE_TEXT_FILE:
            try:
                print(f"📖 Reading from file: {INPUT_TEXT_FILE}")
                with open(INPUT_TEXT_FILE, 'r') as f:
                    # Read all lines and filter out empty ones
                    lines = []
                    for line in f:
                        line = line.strip()
                        # Skip empty lines, comments, or lines with just whitespace
                        if not line or line.startswith('#') or all(c in '.-_=' for c in line):
                            continue
                        # Validate content meets promotional requirements
                        if self._validate_content(line):
                            lines.append(line)
                    
                    print(f"📝 Found {len(lines)} valid promotional lines to process")
                    return lines
                    
            except Exception as e:
                print(f"❌ Error reading text file: {str(e)}")
                print("⚠️ Falling back to direct text input if provided")
                
        return [text] if text and self._validate_content(text) else []
    
    def _sanitize_filename(self, text):
        """Create a safe filename from text"""
        # Take first 30 chars of text and remove invalid filename chars
        safe_text = "".join(c if c.isalnum() else '_' for c in text[:30]).rstrip('_')
        return safe_text
    
    def _get_random_video(self):
        """Get a random video file from either raw_vids or finished_vids directory"""
        # Use finished_vids if enabled, otherwise use raw_vids
        video_dir = self.finished_vids_dir if USE_FINISHED_VIDS else self.raw_vids_dir
        
        video_files = []
        for ext in SUPPORTED_VIDEO_FORMATS:
            video_files.extend(list(video_dir.glob(f"*{ext}")))
        
        if not video_files:
            # Provide more helpful error message
            print(f"❌ No video files found in {video_dir}")
            print(f"📋 Please add video files in one of these formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}")
            print(f"Example: Add an .mp4 file to {video_dir}")
            raise ValueError(f"No video files found in {video_dir}")
        
        # Filter out empty files (some might be 0 bytes)
        valid_video_files = [f for f in video_files if f.stat().st_size > 0]
        
        if not valid_video_files:
            raise ValueError(f"❌ No valid video files found in {video_dir}. Files might be empty or corrupted.")
        
        selected_video = random.choice(valid_video_files)
        print(f"🎬 Selected video from {'finished_vids' if USE_FINISHED_VIDS else 'raw_vids'}: {selected_video.name}")
        return selected_video
    
    def _get_first_five_words(self, text):
        """Get first five words from text for filename"""
        # Split text into words and take first five
        words = text.split()[:5]
        # Join with underscores and make filename safe
        return self._sanitize_filename('_'.join(words))
    
    def _generate_audio_direct(self, text):
        """Generate audio using the ElevenLabs API directly"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.content
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            raise Exception(error_message)
    
    def _combine_audio_video(self, audio_file, video_file, text):
        """Combine audio and video files using ffmpeg with precise duration matching"""
        # Create filename from first five words of text
        video_name = self._get_first_five_words(text)
        output_file = self.final_vids_dir / f"{video_name}.mp4"
        
        try:
            # Get video duration
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 
                  'default=noprint_wrappers=1:nokey=1', str(video_file)]
            video_duration = float(subprocess.check_output(cmd).decode().strip())
            
            # Get audio duration
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                  'default=noprint_wrappers=1:nokey=1', str(audio_file)]
            audio_duration = float(subprocess.check_output(cmd).decode().strip())
            
            # Ensure minimum duration
            target_duration = max(audio_duration, MIN_VIDEO_DURATION)
            
            # If video is shorter than target duration, create precise loop
            if video_duration < target_duration:
                temp_file = self.final_vids_dir / "temp_loop.mp4"
                
                # Calculate number of full loops needed and remaining time
                full_loops = math.floor(target_duration / video_duration)
                remaining_time = target_duration % video_duration
                
                if remaining_time > 0:
                    # Create filter complex for precise loop + remaining portion
                    filter_complex = (
                        f"[0:v]loop={full_loops}:1:0[full];"  # Full loops
                        f"[0:v]trim=0:{remaining_time}[part];"  # Remaining portion
                        "[full][part]concat=n=2:v=1:a=0[v]"  # Concatenate them
                    )
                else:
                    # Just loop the exact number of times needed
                    filter_complex = f"[0:v]loop={full_loops-1}:1:0[v]"
                
                print(f"🎬 Creating precise loop: {full_loops} full + {remaining_time:.2f}s")
                
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(video_file),
                    '-filter_complex', filter_complex,
                    '-map', '[v]',
                    '-t', str(target_duration),
                    str(temp_file)
                ]
                subprocess.run(cmd, check=True)
                video_file = temp_file
            
            # Combine audio and video
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-i', str(audio_file),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True)
            
            # Clean up temp file if it exists
            if 'temp_file' in locals():
                temp_file.unlink()
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error combining audio and video: {str(e)}")
            raise
    
    def _video_exists(self, text):
        """Check if a video with these first five words already exists"""
        video_name = self._get_first_five_words(text)
        expected_path = self.final_vids_dir / f"{video_name}.mp4"
        return expected_path.exists()
    
    def _add_subtitles_to_video(self, video_file, text, output_path, subtitle_file=None):
        """Add subtitles to video using ffmpeg"""
        try:
            # If subtitle file is provided, use it; otherwise, create from text
            if subtitle_file and subtitle_file.exists():
                print(f"🎬 Adding existing subtitles with custom styling: {subtitle_file.name}")
                use_existing_subtitles = True
            else:
                # Create a temporary subtitle file in SRT format
                subtitle_file = self.final_vids_dir / "temp_subtitle.srt"
                subtitle_file_absolute = subtitle_file.absolute()
                use_existing_subtitles = False
                
                # Format the text to fit on screen (basic word wrap)
                words = text.split()
                lines = []
                current_line = []
                
                # Create lines with maximum ~40 characters each
                for word in words:
                    if len(' '.join(current_line + [word])) <= 40:
                        current_line.append(word)
                    else:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                
                # Add the last line if there's anything left
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Join lines with newlines for proper SRT format
                subtitle_text = '\\N'.join(lines)
                
                # Get video duration
                cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 
                      'default=noprint_wrappers=1:nokey=1', str(video_file)]
                video_duration = float(subprocess.check_output(cmd).decode().strip())
                
                # Create SRT content that shows the text for the entire duration
                # Calculate end time from duration (format: 00:00:00,000)
                end_time = video_duration
                end_time_formatted = self._format_timestamp(end_time)
                
                # Format the subtitle content
                subtitle_content = f"1\n00:00:00,000 --> {end_time_formatted}\n{subtitle_text}"
                
                # Write subtitle file
                with open(subtitle_file, 'w', encoding='utf-8') as f:
                    f.write(subtitle_content)
                
                print(f"📝 Created subtitle file with {len(lines)} lines")
            
            # Get style preset based on configuration
            style_preset = SUBTITLE_STYLES.get(SUBTITLE_STYLE_PRESET, SUBTITLE_STYLES["modern"])
            
            # Position settings
            position = "10" if SUBTITLE_POSITION == "bottom" else "5" if SUBTITLE_POSITION == "top" else "h-text_h/2"
            
            # Build style string from preset
            style_str = ",".join([f"{key}={value}" for key, value in style_preset.items()])
            style_str += f",MarginV={position}"
            
            # Escape the subtitle file path for ffmpeg
            escaped_subtitle_path = str(subtitle_file.absolute()).replace(':', '\\:').replace('\\', '\\\\')
            
            # Use ffmpeg to add subtitles to video
            filter_text = f"subtitles='{escaped_subtitle_path}':force_style='{style_str}'"
            
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-vf', filter_text,
                '-c:a', 'copy',
                str(output_path)
            ]
            
            print(f"🎬 Adding subtitles with ffmpeg using {SUBTITLE_STYLE_PRESET} style...")
            subprocess.run(cmd, check=True)
            
            # Clean up temp subtitle file if we created it
            if not use_existing_subtitles and subtitle_file.exists():
                subtitle_file.unlink()
                
            print(f"✅ Successfully added subtitles to video")
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error adding subtitles: {str(e)}")
            if not use_existing_subtitles and 'subtitle_file' in locals() and subtitle_file.exists():
                subtitle_file.unlink()
            raise
        except Exception as e:
            print(f"❌ Error in subtitle processing: {str(e)}")
            if not use_existing_subtitles and 'subtitle_file' in locals() and subtitle_file.exists():
                subtitle_file.unlink()
            raise
    
    def _extract_subtitles(self, video_file):
        """Extract subtitles from video file if available or transcribe using Whisper"""
        try:
            # Output path for extracted subtitles
            subtitle_file = self.final_vids_dir / f"extracted_{video_file.stem}.srt"
            
            # Use ffmpeg to extract subtitles
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-map', '0:s:0',  # First subtitle stream
                '-c:s', 'srt',
                str(subtitle_file)
            ]
            
            # Run the command - use check=False to avoid errors if no subtitles found
            process = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            # Check if subtitles were successfully extracted
            if subtitle_file.exists() and subtitle_file.stat().st_size > 0:
                print(f"✅ Successfully extracted subtitles from {video_file.name}")
                return subtitle_file
            
            # No existing subtitles found, try using Whisper if enabled
            if USE_WHISPER and self.whisper_model:
                return self._transcribe_audio_with_whisper(video_file)
            else:
                print(f"📝 No existing subtitles found in {video_file.name}")
                if USE_WHISPER and not self.whisper_model:
                    print(f"⚠️ Whisper enabled but model not loaded. Skipping transcription.")
                
                return None
                    
        except Exception as e:
            print(f"❌ Error extracting subtitles: {str(e)}")
            return None
    
    def _transcribe_audio_with_whisper(self, video_file):
        """Transcribe audio from video using Whisper"""
        try:
            print(f"🎙️ Transcribing audio using Whisper {WHISPER_MODEL_SIZE} model...")
            
            # Extract audio to temporary file
            temp_audio = self.final_vids_dir / f"temp_audio_{video_file.stem}.wav"
            
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                str(temp_audio)
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Transcribe with Whisper
            options = {
                "language": WHISPER_LANGUAGE,
                "task": "transcribe",
                "fp16": False
            }
            
            # Perform transcription
            result = self.whisper_model.transcribe(str(temp_audio), **options)
            
            # Format as SRT
            subtitle_file = self.final_vids_dir / f"whisper_{video_file.stem}.srt"
            
            # Convert segments to SRT format
            with open(subtitle_file, "w", encoding="utf-8") as f:
                for i, segment in enumerate(result["segments"], 1):
                    # Skip segments with low confidence
                    if segment["confidence"] < WHISPER_CONFIDENCE_THRESHOLD:
                        continue
                        
                    # Format start/end times as SRT format (HH:MM:SS,mmm)
                    start_time = self._format_timestamp(segment["start"])
                    end_time = self._format_timestamp(segment["end"])
                    
                    # Write SRT format: index, time range, text
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text'].strip()}\n\n")
            
            # Clean up temporary audio file
            if temp_audio.exists():
                temp_audio.unlink()
                
            print(f"✅ Successfully transcribed audio to subtitles: {subtitle_file.name}")
            return subtitle_file
            
        except Exception as e:
            print(f"❌ Error transcribing with Whisper: {str(e)}")
            traceback.print_exc()
            
            # Clean up temp files
            if 'temp_audio' in locals() and temp_audio.exists():
                temp_audio.unlink()
                
            return None
    
    def _format_timestamp(self, seconds):
        """Format seconds as SRT timestamp: HH:MM:SS,mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def process_clip(self, video_file, output_text=None):
        """Process a video clip - extract subtitles or add new ones"""
        try:
            # Create output path
            if output_text:
                safe_name = self._sanitize_filename(output_text)
            else:
                safe_name = f"processed_{video_file.stem}"
            
            output_file = self.final_vids_dir / f"{safe_name}.mp4"
            
            # Check if file already exists
            if output_file.exists():
                print(f"🔄 Skipping existing output file: {output_file.name}")
                return output_file
            
            # Check if we should try to use existing subtitles
            subtitle_file = None
            if USE_EXISTING_SUBTITLES:
                subtitle_file = self._extract_subtitles(video_file)
            
            if subtitle_file:
                # Use existing subtitles with custom styling
                print(f"🎬 Using existing subtitles with custom styling")
                return self._add_subtitles_to_video(video_file, "", output_file, subtitle_file)
            elif output_text:
                # Add new subtitles with provided text
                print(f"🎬 Adding new subtitles to video")
                return self._add_subtitles_to_video(video_file, output_text, output_file)
            else:
                # Try to extract subtitles with Whisper
                if USE_WHISPER and self.whisper_model:
                    print(f"🎬 No subtitles found, attempting to transcribe with Whisper")
                    subtitle_file = self._transcribe_audio_with_whisper(video_file)
                    if subtitle_file:
                        return self._add_subtitles_to_video(video_file, "", output_file, subtitle_file)
                
                # Just copy the video if no subtitles or text
                print(f"🎬 No subtitles, text, or transcription available, copying video")
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(video_file),
                    '-c', 'copy',
                    str(output_file)
                ]
                subprocess.run(cmd, check=True)
                print(f"✅ Copied video without changes: {output_file.name}")
                return output_file
                
        except Exception as e:
            print(f"❌ Error processing clip: {str(e)}")
            traceback.print_exc()
            return None
            
    def generate_videos(self, text=None):
        """Generate videos with subtitles instead of voice-over"""
        try:
            # Get input text lines (same as before)
            text_lines = self._get_input_text(text)
            
            # If no text provided and not using text file, process videos without text
            if not text_lines and not USE_TEXT_FILE and text is None:
                print("📝 No text provided, processing videos with existing subtitles")
                video_files = self._get_video_files()
                
                if not video_files:
                    print("❌ No video files found")
                    return None
                
                print(f"\n📊 Video Analysis:")
                print(f"Total videos to process: {len(video_files):,}")
                print("=" * 50)
                
                # Process each video
                for i, video_file in enumerate(video_files, 1):
                    print(f"\n🔄 Processing video {i}/{len(video_files)}")
                    print(f"Video: {video_file.name}")
                    
                    try:
                        final_video = self.process_clip(video_file)
                        if final_video:
                            print(f"🎞️ Processed video: {final_video.name}")
                            
                            # Save analytics
                            if hasattr(self, '_save_analytics'):
                                self._save_analytics(f"Auto-processed: {video_file.name}", 
                                                    final_video, MIN_VIDEO_DURATION)
                        
                        # Delay between processing
                        if i < len(video_files):
                            time.sleep(DELAY_BETWEEN_REQUESTS)
                            
                    except Exception as e:
                        print(f"⚠️ Error processing video {i}: {str(e)}")
                        traceback.print_exc()
                        continue
                
                print(f"\n🎉 Processing complete!")
                print(f"🎬 Final videos saved in: {self.final_vids_dir}")
                print(f"📊 Analytics saved in: {self.analytics_file}")
                return
            
            if not text_lines:
                print("❌ No valid content found")
                return None
            
            print(f"\n📊 Content Analysis:")
            print(f"Total valid lines to process: {len(text_lines):,}")
            print("=" * 50)
            
            # Process each line
            for i, line in enumerate(text_lines, 1):
                print(f"\n🔄 Processing line {i}/{len(text_lines)}")
                print(f"Text: {line[:100]}..." if len(line) > 100 else f"Text: {line}")
                
                try:
                    # Skip very short lines or likely headers
                    if len(line) < 10 or line.endswith(':'):
                        print("⏩ Skipping short line or header")
                        continue
                    
                    # Check if video already exists
                    if self._video_exists(line):
                        video_name = self._get_first_five_words(line)
                        print(f"🔄 Skipping duplicate video: {video_name}.mp4")
                        continue
                        
                    # Get random video
                    video_file = self._get_random_video()
                    print(f"🎥 Selected random video: {video_file.name}")
                    
                    # Process the clip with the text
                    final_video = self.process_clip(video_file, line)
                    
                    if final_video:
                        print(f"🎞️ Created final video with subtitles: {final_video.name}")
                        
                        # Save analytics
                        self._save_analytics(line, final_video, MIN_VIDEO_DURATION)
                    
                    # Delay between requests
                    if i < len(text_lines):
                        time.sleep(DELAY_BETWEEN_REQUESTS)
                        
                except Exception as e:
                    print(f"⚠️ Error processing line {i}: {str(e)}")
                    traceback.print_exc()
                    continue
            
            print(f"\n🎉 Processing complete!")
            print(f"🎬 Final videos saved in: {self.final_vids_dir}")
            print(f"📊 Analytics saved in: {self.analytics_file}")
            
        except Exception as e:
            print(f"❌ Error in processing: {str(e)}")
            traceback.print_exc()
            
    def _get_video_files(self):
        """Get list of video files from the appropriate directory"""
        video_dir = self.finished_vids_dir if USE_FINISHED_VIDS else self.raw_vids_dir
        video_files = []
        
        for ext in SUPPORTED_VIDEO_FORMATS:
            video_files.extend(list(video_dir.glob(f"*{ext}")))
        
        # Filter out empty files
        valid_video_files = [f for f in video_files if f.stat().st_size > 0]
        
        return valid_video_files

    def generate_audio(self, text=None):
        """Generate audio files from text input and combine with random videos"""
        # If using subtitles, use the generate_videos method instead
        if USE_SUBTITLES:
            return self.generate_videos(text)
            
        try:
            # Get input text lines
            text_lines = self._get_input_text(text)
            
            if not text_lines:
                print("❌ No valid content found")
                return None
            
            print(f"\n📊 Content Analysis:")
            print(f"Total valid lines to process: {len(text_lines):,}")
            print("=" * 50)
            
            # Process each line
            for i, line in enumerate(text_lines, 1):
                print(f"\n🔄 Processing line {i}/{len(text_lines)}")
                print(f"Text: {line[:100]}..." if len(line) > 100 else f"Text: {line}")
                
                try:
                    # Skip very short lines or likely headers
                    if len(line) < 10 or line.endswith(':'):
                        print("⏩ Skipping short line or header")
                        continue
                    
                    # Check if video already exists
                    if self._video_exists(line):
                        video_name = self._get_first_five_words(line)
                        print(f"🔄 Skipping duplicate video: {video_name}.mp4")
                        continue
                        
                    # Generate audio using direct API call
                    print(f"🔊 Generating audio for text...")
                    audio_data = self._generate_audio_direct(line)
                    
                    # Create filename from text
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    safe_name = self._sanitize_filename(line)
                    audio_filename = f"audio_{timestamp}_{safe_name}.mp3"
                    audio_filepath = self.audio_dir / audio_filename
                    
                    # Save audio file
                    with open(audio_filepath, 'wb') as f:
                        f.write(audio_data)
                    
                    print(f"✨ Generated audio: {audio_filename}")
                    
                    # Get random video and combine with audio
                    video_file = self._get_random_video()
                    print(f"🎥 Selected random video: {video_file.name}")
                    
                    final_video = self._combine_audio_video(audio_filepath, video_file, line)
                    print(f"🎞️ Created final video: {final_video.name}")
                    
                    # Save analytics
                    self._save_analytics(line, final_video, MIN_VIDEO_DURATION)
                    
                    # Delay between requests
                    if i < len(text_lines):
                        time.sleep(DELAY_BETWEEN_REQUESTS)
                        
                except Exception as e:
                    print(f"⚠️ Error processing line {i}: {str(e)}")
                    traceback.print_exc()
                    continue
            
            print(f"\n🎉 Processing complete!")
            print(f"📂 Audio files saved in: {self.audio_dir}")
            print(f"🎬 Final videos saved in: {self.final_vids_dir}")
            print(f"📊 Analytics saved in: {self.analytics_file}")
            
        except Exception as e:
            print(f"❌ Error in processing: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Video Agent: Add subtitles or generate audio for videos")
    parser.add_argument("--key", help="ElevenLabs API key (required for audio generation)")
    parser.add_argument("--text", help="Text to process directly")
    parser.add_argument("--file", help="Path to text file to use instead of default")
    parser.add_argument("--all", action="store_true", help="Process all videos with Whisper transcription")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"], 
                      default=WHISPER_MODEL_SIZE, help="Whisper model size to use")
    parser.add_argument("--style", choices=["minimal", "modern", "cinematic", "bold"],
                      default=SUBTITLE_STYLE_PRESET, help="Subtitle style preset")
    parser.add_argument("--lang", default=WHISPER_LANGUAGE, help="Language for transcription")
    
    args = parser.parse_args()
    
    # Update settings based on command line arguments
    if args.file:
        USE_TEXT_FILE = True
        INPUT_TEXT_FILE = args.file
        
    if args.model and args.model != WHISPER_MODEL_SIZE:
        WHISPER_MODEL_SIZE = args.model
        print(f"🔄 Using Whisper model: {WHISPER_MODEL_SIZE}")
        
    if args.style and args.style != SUBTITLE_STYLE_PRESET:
        SUBTITLE_STYLE_PRESET = args.style
        print(f"🔄 Using subtitle style: {SUBTITLE_STYLE_PRESET}")
        
    if args.lang and args.lang != WHISPER_LANGUAGE:
        WHISPER_LANGUAGE = args.lang
        print(f"🔄 Using language: {WHISPER_LANGUAGE}")
    
    # Create required directories
    for directory in [DATA_DIR, AUDIO_DIR, RAW_VIDS_DIR, FINAL_VIDS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    if USE_FINISHED_VIDS:
        FINISHED_VIDS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize agent with API key
    agent = VideoAgent(args.key)
    
    # Process based on arguments
    if args.all:
        print("🎬 Processing all available videos with Whisper transcription...")
        agent.generate_videos(None)
    elif args.text:
        print(f"🎬 Processing with provided text: {args.text[:50]}...")
        agent.generate_videos(args.text)
    else:
        print("🎬 No specific text provided. Using example text or text file...")
        # Example text
        example_text = "This is an example video created by the Video Agent with Whisper transcription."
        agent.generate_videos(example_text)
