'''
this ai agent will be able to take long videos and make short videos

enabling this ai agent to help you earn money while you learn to code

you get paid by most streamers to make clips of their streams

i have so much gold in my videos and things that can truly help people

if you want to learn how to code and get paid while you do it

you should just watch my videos and when you see something that you think is gold, you can make a clip out of it

and you can get paid by me for that

check out the #clips channel in discord for more info: https://discord.gg/XAw8US9aHT

examples of people crushing it with my videos:

https://www.youtube.com/@Algonomicstrades
https://www.youtube.com/@firedevonytsnips

they essentially get paid to watch my coding videos and make clips of the good parts

because i dont have time to make clips i can only stream as im building my algos

steps to your success as a Kawz's Agents clipper:
1. find good long videos on my channel: https://www.youtube.com/@firedevonyt/videos 
2. watch the video and find the parts that are good
3. make a clip out of it (5 mins-2hours in length)
4. upload the clip to your youtube channel (youtube only, no youtube shorts)
5. when you hit 10,000 views, get paid $69

Standard payout is $69 per 10,000 views but it increases based on your views per month..

10,000 views per month = $69 per 10,000 views
30,000 views per month = $89 per 10,000 views 
50,000 views per month = $100 per 10,000 views
100,000 views per month = $149 per 10,000 views

BONUS GROUP: once you hit 10,000 views per month, you get access to a private channel in discord with training on how to get more views

payments are via crypto on the 1st and 15th of every month, when you hit 10,000 views per month + just email the link, and your tracking of the views to firedevonyt@gmail.com

* if in the USA, you can only earn up to $500 per year but in the rest of the world, you can earn unlimited.

Where do you get the videos from?
1. this dropbox has a bunch of my videos that i will upload to daily: https://www.dropbox.com/scl/fo/d0rjdyus9q3pok5nbmo7b/AM9LOmUDv8KIjmH6ypTALx0?rlkey=klg4tinvneqyui46r6851liwa&st=0zxfym3w&dl=0
2. you have permission to download any of my youtube videos: https://www.youtube.com/@firedevonyt/videos

how do i clip the videos manually?
1. download capcut: https://www.capcut.com/
2. find the interesting parts of the video and make a 5 min - 2 hour clip of it
3. make an interesting thumbnail & title for the clip (you can use my thumbnails if needed, just google how to download)
4. post on youtube
5. when you hit 10,000 views email your link and stats to firedevonyt@gmail.com to get paid

how do i clip videos with this agent?
1. put in my long videos into this folder path src/data/videos/raw_clips
2. make sure to have this folder too src/data/videos/finished_vids this is the output folder
3. run the code and wait for them to output to the above folder
4. make a good thumbnail and title then upload to youtube
5. wait for 10,000 views and email the link and stats to firedevonyt@gmail.com to get paid

here is another training video, the only difference is that we only accept long youtube videos now. the below training is helpful though.

training video to learn how to clip videos: https://www.youtube.com/watch?v=nqWax0EPkcs

all of my videos you can use: https://www.dropbox.com/scl/fo/d0rjdyus9q3pok5nbmo7b/AM9LOmUDv8KIjmH6ypTALx0?rlkey=klg4tinvneqyui46r6851liwa&st=0zxfym3w&dl=0
- you can also download the videos from my channel: https://www.youtube.com/@firedevonyt/videos
'''

# Fire Dev's Video Splitter Agent🎬
import sys
from pathlib import Path
import os
import time
from termcolor import cprint
from tqdm import tqdm
import subprocess
import shutil
import random
from youtube_transcript_api import YouTubeTranscriptApi
import re
import yt_dlp
import whisper
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import argparse

# Add project root to Python path for imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Mock the model_factory module since we aren't using AI analysis in this demo
class MockModelFactory:
    def get_model(self, model_type, model_name):
        cprint(f"Using mock model: {model_type} - {model_name}", "yellow")
        return None

class models:
    class model_factory:
        @staticmethod
        def get_model(model_type, model_name):
            cprint(f"Using mock model: {model_type} - {model_name}", "yellow")
            return None

# Constants
MIN_CLIP_DURATION = 60  # 1 minute in seconds (reduced from 5 mins)
MAX_CLIP_DURATION = 120  # 2 minutes in seconds (reduced from 20 mins)
MAX_SENTENCES = 5  # Maximum number of sentences in AI response

# Processing mode
PROCESS_YOUTUBE = True  # Enable YouTube processing by default
USE_AI_ANALYSIS = False  # Disable AI analysis for this demo
USE_VOICE_GENERATION = False  # Disable voice generation by default

# AI Settings
MODEL_TYPE = "deepseek"  # Using DeepSeek API
MODEL_NAME = "deepseek-chat"  # DeepSeek's chat model

# Constants for directories
INPUT_DIR = Path("data/videos/raw_clips")
OUTPUT_DIR = Path("data/videos/finished_vids")
TEMP_DIR = Path("data/videos/temp")
YOUTUBE_MATERIALS_DIR = Path("data/videos/youtube_materials")

class ClipsAgent:
    def __init__(self):
        """Initialize the Clips Agent"""
        cprint("\n🎬 Initializing Fire Dev's Clips Agent...", "cyan")
        self._setup_directories()
        self._setup_ai()
        self._setup_whisper()
        self.current_stage = "initialized"
        self.progress = 0
        cprint("\n✅ Initialization complete!", "green")
        self._print_status()
        
    def _print_status(self):
        """Print current status of the agent"""
        status_color = "green" if self.progress == 100 else "yellow"
        cprint("\n📊 Current Status:", "cyan")
        cprint(f"Stage: {self.current_stage}", status_color)
        cprint(f"Progress: {self.progress}%", status_color)
        cprint("=" * 50, "cyan")
        
    def _setup_directories(self):
        """Ensure input and output directories exist"""
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        YOUTUBE_MATERIALS_DIR.mkdir(parents=True, exist_ok=True)
        cprint(f"📂 Input directory: {INPUT_DIR}", "cyan")
        cprint(f"📂 Output directory: {OUTPUT_DIR}", "cyan")
        cprint(f"📂 Temp directory: {TEMP_DIR}", "cyan")
        cprint(f"📂 YouTube materials directory: {YOUTUBE_MATERIALS_DIR}", "cyan")
    
    def _setup_ai(self):
        """Initialize AI model using factory"""
        if not USE_AI_ANALYSIS:
            cprint("🤖 AI initialization skipped - AI analysis disabled", "yellow")
            return
            
        try:
            self.model = models.model_factory.get_model(MODEL_TYPE, MODEL_NAME)
            if not self.model:
                cprint("⚠️ Could not initialize AI model - AI analysis will be disabled", "yellow")
                return
            cprint("🤖 AI Model initialized successfully!", "green")
        except Exception as e:
            cprint(f"⚠️ Error initializing AI model - AI analysis will be disabled: {str(e)}", "yellow")

    def _setup_whisper(self):
        """Initialize Whisper model for local video transcription"""
        try:
            cprint("🎙️ Loading Whisper model...", "cyan")
            self.whisper_model = whisper.load_model("base")
            cprint("✨ Whisper model loaded successfully!", "green")
        except Exception as e:
            cprint(f"⚠️ Could not load Whisper model: {str(e)}", "yellow")
            self.whisper_model = None

    def _is_youtube_url(self, video_path):
        """Check if the video path is a YouTube URL"""
        # Updated to specifically check for string type and common YouTube domains
        return isinstance(video_path, str) and ('youtube.com/watch?v=' in video_path or 'youtu.be/' in video_path)

    def _get_video_id(self, youtube_url):
        """Extract YouTube video ID from URL"""
        if not self._is_youtube_url(youtube_url):
            raise ValueError("Invalid YouTube URL provided.")
            
        if 'youtube.com' in youtube_url:
            video_id = re.search(r'v=([^&]+)', youtube_url)
            if video_id:
                return video_id.group(1)
        elif 'youtu.be' in youtube_url:
            video_id = youtube_url.split('/')[-1].split('?')[0] # Handle potential query params
            return video_id
        raise ValueError("Could not extract video ID from URL.")
        
    def _download_youtube_video(self, youtube_url, video_id):
        """Download YouTube video using yt-dlp to the temp directory"""
        self.current_stage = f"downloading video {video_id}"
        self.progress = 0
        self._print_status()
        
        download_path_template = TEMP_DIR / f"{video_id}.%(ext)s"
        
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',  # Prefer 720p or less
            'outtmpl': str(download_path_template),
            'quiet': False,  # Show output for debugging
            'no_warnings': False,  # Show warnings for debugging
            'progress_hooks': [self._yt_dlp_progress_hook],
            'merge_output_format': 'mp4',  # Force output to be MP4
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            # Find the actual downloaded file (yt-dlp adds the extension)
            downloaded_files = list(TEMP_DIR.glob(f"{video_id}.*"))
            if not downloaded_files:
                 raise FileNotFoundError(f"yt-dlp failed to download video {video_id}")
            
            downloaded_path = downloaded_files[0] # Assume first match is correct
            cprint(f"\n✅ Video downloaded successfully to: {downloaded_path}", "green")
            self.current_stage = "download complete"
            self.progress = 100 # Mark download as complete
            self._print_status()
            return downloaded_path
            
        except Exception as e:
            cprint(f"❌ Error downloading YouTube video: {str(e)}", "red")
            self.current_stage = "download error"
            self.progress = 0
            self._print_status()
            return None

    def _yt_dlp_progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                self.progress = int(downloaded_bytes / total_bytes * 100)
                # Update status less frequently to avoid flooding console
                if self.progress % 10 == 0: 
                    self._print_status()
        elif d['status'] == 'finished':
            self.progress = 100
            self._print_status()

    def get_transcript(self, video_id):
        """Get transcript for a YouTube video ID"""
        self.current_stage = f"transcribing {video_id}"
        self.progress = 0
        self._print_status()
        
        transcript_path = YOUTUBE_MATERIALS_DIR / video_id / f"{video_id}_transcript.txt"
        
        # Check if transcript already exists
        if transcript_path.exists():
            cprint(f"✨ Found existing transcript for {video_id}", "green")
            self.progress = 100
            self._print_status()
            with open(transcript_path, 'r') as f:
                return f.read()
        
        try:
            # Get YouTube transcript
            cprint(f"🎥 Getting YouTube transcript for {video_id}", "cyan")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            self.progress = 50
            self._print_status()
            
            full_text = []
            for entry in transcript:
                text = entry['text'].strip()
                if text:
                    full_text.append(text)
            full_text = ' '.join(full_text)
            
            # Save transcript
            os.makedirs(YOUTUBE_MATERIALS_DIR / video_id, exist_ok=True)
            with open(transcript_path, 'w') as f:
                f.write(full_text)
            
            self.progress = 100
            self._print_status()
            return full_text
            
        except Exception as e:
            cprint(f"❌ Error getting transcript: {str(e)}", "red")
            self.progress = 0
            self._print_status()
            return None

    def _get_video_files(self):
        """Get list of video files from input directory (No longer primary method)"""
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
        video_files = []
        for ext in video_extensions:
            video_files.extend(list(INPUT_DIR.glob(f'*{ext}')))
        return video_files

    def _get_video_duration(self, video_path):
        """Get video duration using ffprobe"""
        try:
            cmd = [
                'ffprobe', 
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ]
            output = subprocess.check_output(cmd).decode().strip()
            return float(output)
        except Exception as e:
            cprint(f"❌ Error getting duration: {str(e)}", "red")
            return None

    def _split_video_ffmpeg(self, video_path, start_time, duration, output_path):
        """Split video using ffmpeg directly"""
        try:
            cprint(f"🎥 Splitting video from {start_time:.2f}s for {duration:.2f}s using ffmpeg", "cyan")
            
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'libx264',  # Use H.264 video codec
                '-c:a', 'aac',      # Use AAC audio codec
                '-b:v', '2M',       # Set video bitrate
                '-strict', 'experimental',
                '-y',               # Overwrite output file if it exists
                str(output_path)
            ]
            
            # Run the command
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                cprint(f"❌ ffmpeg error (code {process.returncode}): {process.stderr}", "red")
                return False
                
            if not output_path.exists():
                cprint(f"❌ ffmpeg completed but output file not found", "red")
                return False
                
            # Verify the output file size
            if output_path.stat().st_size < 1000:  # Less than 1KB is probably an error
                cprint(f"❌ Output file too small ({output_path.stat().st_size} bytes)", "red")
                return False
                
            return True
            
        except subprocess.CalledProcessError as e:
            cprint(f"❌ ffmpeg process error: {e}", "red")
            return False
        except Exception as e:
            cprint(f"❌ Error during ffmpeg processing: {str(e)}", "red")
            return False

    def _get_random_clip_duration(self):
        """Get a random clip duration between MIN and MAX"""
        return random.randint(MIN_CLIP_DURATION, MAX_CLIP_DURATION)
    
    def clean_timestamps(self, text):
        """Clean all types of timestamps from text"""
        # Clean [MM:SS] style timestamps
        text = re.sub(r'\[\d+:\d+\]', '', text)
        # Clean MM:SS style timestamps
        text = re.sub(r'\d+:\d+', '', text)
        # Clean any remaining brackets with numbers
        text = re.sub(r'\[\d+\]', '', text)
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def download_youtube_materials(self, video_id):
        """Download transcript and thumbnail for a YouTube video ID"""
        try:
            materials_dir = YOUTUBE_MATERIALS_DIR / video_id
            materials_dir.mkdir(parents=True, exist_ok=True)
            
            # Download transcript
            transcript_path = materials_dir / f"{video_id}_transcript.txt"
            if not transcript_path.exists():
                cprint(f"🎥 Getting transcript for video ID: {video_id}", "cyan")
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                
                # Just combine the text without timestamps
                full_text = []
                for entry in transcript:
                    text = entry['text'].strip()
                    text = self.clean_timestamps(text)
                    if text:  # Only add non-empty lines
                        full_text.append(text)
                
                # Join into a single string and clean up any double spaces
                full_text = ' '.join(full_text)
                full_text = re.sub(r'\s+', ' ', full_text)
                
                # Save transcript
                with open(transcript_path, 'w') as f:
                    f.write(full_text)
                cprint("✨ Transcript downloaded and saved!", "green")
                cprint(f"📝 Cleaned transcript length: {len(full_text)} chars", "cyan")
            else:
                cprint("✨ Transcript already exists!", "green")
                with open(transcript_path, 'r') as f:
                    full_text = f.read()
            
            # Download thumbnail
            thumbnail_path = materials_dir / f"{video_id}_thumbnail.jpg"
            if not thumbnail_path.exists():
                cprint("🖼️ Downloading thumbnail...", "cyan")
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                import requests
                response = requests.get(thumbnail_url)
                if response.status_code == 200:
                    with open(thumbnail_path, 'wb') as f:
                        f.write(response.content)
                    cprint("✨ Thumbnail downloaded and saved!", "green")
                else:
                    cprint("⚠️ Could not download thumbnail, trying fallback...", "yellow")
                    # Try fallback thumbnail
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:
                        with open(thumbnail_path, 'wb') as f:
                            f.write(response.content)
                        cprint("✨ Fallback thumbnail downloaded and saved!", "green")
                    else:
                        cprint("❌ Could not download thumbnail", "red")
            else:
                cprint("✨ Thumbnail already exists!", "green")
            
            # Return the transcript text we got earlier
            return full_text 
            
        except Exception as e:
            cprint(f"❌ Error downloading YouTube materials: {str(e)}", "red")
            return None

    def process_video(self, video_path, video_id):
        """Process a single downloaded video file, using video_id for naming/transcript."""
        try:
            # Load video
            self.current_stage = f"loading video {video_id}"
            self.progress = 0
            self._print_status()
            
            if not video_path or not video_path.exists():
                 cprint(f"❌ Video file not found at {video_path}", "red")
                 return

            # Get duration using ffprobe
            duration = self._get_video_duration(video_path)
            if not duration:
                cprint(f"❌ Could not determine video duration", "red")
                return
                
            cprint(f"📊 Video duration: {duration:.2f} seconds", "cyan")
            
            self.progress = 25
            self._print_status()

            # Get transcript using video_id
            self.current_stage = f"getting transcript for {video_id}"
            # Use the video_id directly now
            transcript = self.get_transcript(video_id) 
            
            if not transcript:
                cprint("❌ Failed to get transcript, continuing with video splitting only", "yellow")
            
            # Calculate clip segments
            self.current_stage = f"calculating segments for {video_id}"
            self.progress = 50
            self._print_status()
            
            # Calculate segments between MIN_CLIP_DURATION and MAX_CLIP_DURATION
            segments = []
            current_time = 0
            while current_time < duration:
                # Random duration between MIN and MAX
                clip_duration = random.uniform(MIN_CLIP_DURATION, MAX_CLIP_DURATION)
                end_time = min(current_time + clip_duration, duration)
                
                # Only add if segment is at least MIN_CLIP_DURATION
                if end_time - current_time >= MIN_CLIP_DURATION:
                    segments.append((current_time, end_time))
                current_time = end_time
            
            cprint(f"\n📊 Will create {len(segments)} clips", "cyan")
            
            # Process each segment
            for i, (start, end) in enumerate(segments, 1):
                self.current_stage = f"processing clip {i}/{len(segments)}"
                self.progress = int((i / len(segments)) * 100)
                self._print_status()
                
                # Create subclip using ffmpeg directly
                cprint(f"\n🎬 Creating clip {i}/{len(segments)}: {start:.1f}s to {end:.1f}s", "cyan")
                
                # Output path
                output_path = OUTPUT_DIR / f"{video_id}_clip_{i}.mp4"
                
                # Split the video using ffmpeg directly
                clip_duration = end - start
                success = self._split_video_ffmpeg(video_path, start, clip_duration, output_path)
                
                if success:
                    cprint(f"✅ Saved clip to: {output_path}", "green")
                else:
                    cprint(f"❌ Failed to create clip {i}", "red")
            
            self.current_stage = f"completed {video_id}"
            self.progress = 100
            self._print_status()
            
        except Exception as e:
            cprint(f"❌ Error processing video {video_id}: {str(e)}", "red")
            self.current_stage = "error"
            self.progress = 0
            self._print_status()

    def run(self, youtube_url):
        """Main execution method - now takes a YouTube URL"""
        downloaded_path = None # Initialize to None
        try:
            if not self._is_youtube_url(youtube_url):
                 cprint(f"❌ Invalid YouTube URL provided: {youtube_url}", "red")
                 return

            cprint(f"\n▶️ Starting processing for YouTube URL: {youtube_url}", "magenta")
            
            # 1. Get Video ID
            video_id = self._get_video_id(youtube_url)
            cprint(f"📹 Video ID identified: {video_id}", "cyan")

            # 2. Download Video
            downloaded_path = self._download_youtube_video(youtube_url, video_id)
            
            if not downloaded_path:
                cprint(f"❌ Failed to download video {video_id}. Aborting.", "red")
                return

            # 3. Process Video (using downloaded path and video_id)
            self.process_video(downloaded_path, video_id)

            cprint(f"\n🎉 Finished processing for {video_id}!", "green")

        except ValueError as e:
             cprint(f"❌ Input Error: {str(e)}", "red")
        except Exception as e:
            cprint(f"❌ Error in main execution: {str(e)}", "red")
            self.current_stage = "error"
            self.progress = 0
            self._print_status()
        finally:
             # 4. Cleanup downloaded video
             if downloaded_path and downloaded_path.exists():
                 try:
                     cprint(f"\n🧹 Cleaning up temporary file: {downloaded_path}", "yellow")
                     os.remove(downloaded_path)
                 except Exception as e:
                     cprint(f"⚠️ Error during cleanup: {str(e)}", "yellow")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fire Dev's Clips Agent - Processes YouTube videos into clips.")
    parser.add_argument("youtube_url", help="The URL of the YouTube video to process.")
    
    args = parser.parse_args()

    try:
        agent = ClipsAgent()
        agent.run(args.youtube_url) # Pass the URL to the run method
    except KeyboardInterrupt:
        cprint("\n👋 Clips Agent shutting down gracefully...", "yellow")
        # Clean up temp directory if it exists on interrupt
        if TEMP_DIR.exists():
            try:
                shutil.rmtree(TEMP_DIR)
                cprint("🧹 Temp directory cleaned.", "yellow")
            except Exception as e:
                cprint(f"⚠️ Error cleaning temp directory on exit: {str(e)}", "yellow")
    except Exception as e:
        cprint(f"\n❌ Fatal error: {str(e)}", "red")
        # Also attempt temp dir cleanup on fatal error
        if TEMP_DIR.exists():
             try:
                 shutil.rmtree(TEMP_DIR)
                 cprint("🧹 Temp directory cleaned.", "yellow")
             except Exception as e_clean:
                 cprint(f"⚠️ Error cleaning temp directory on fatal error: {str(e_clean)}", "yellow")

