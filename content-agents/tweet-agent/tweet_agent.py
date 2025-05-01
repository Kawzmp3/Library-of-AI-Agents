"""
🐦 Fire Dev's Tweet Generator (Demo Version)
Built with love by Fire Dev 🚀

This agent takes text input and generates tweets based on the content.
This is a demo version that doesn't require API keys.

To use with real API keys:
1. Set your API keys in the .env file
2. Change DEMO_MODE to False
3. Configure the model and settings as needed
"""

# Configuration Settings
DEMO_MODE = True  # Set to False to use real API keys
MAX_CHUNK_SIZE = 10000  # Maximum characters per chunk
TWEETS_PER_CHUNK = 5    # Number of tweets to generate per chunk
USE_TEXT_FILE = True    # Whether to use og_tweet_text.txt by default
OG_TWEET_FILE = "src/data/tweets/mcp_transcript.txt"
USE_TEST_MODE = True    # Set to True for a quick test with only 1 chunk

import os
import time
from datetime import datetime
from pathlib import Path
import sys
import traceback
import math
from termcolor import colored, cprint
import random

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Example tweet templates for demo purposes
EXAMPLE_TWEETS = [
    "model context protocol (mcp) is gaining critical mass as open ai officially backs it. this standardizes how ai agents connect to external services.",
    "mcp reduces the complexity of building ai agents. no more manually configuring every single connection - just connect to the mcp server.",
    "launched by anthropic in november 2023, mcp is now reaching wide market penetration. a protocol is only as valuable as its adoption.",
    "with mcp, you don't need to manually configure calendar tools. connect to one mcp server and get access to create, delete, update, and get events.",
    "in n8n, an mcp flow replaces multiple nodes with just one connection to an mcp server, giving your ai agent access to all tools in that family.",
    "soon there will be mcp compass - a high-level node that selects the family of nodes you need, then selects the specific sub-node to call.",
    "the current way to build ai agents: configure each tool separately. the mcp way: connect to a family of tools with one authorization.",
    "mcp servers for airbnb, apify, and other services are already being created. the ecosystem is growing with community contributions.",
    "mcp is still early days but adoption is accelerating. right now, best to experiment internally rather than implementing in client projects.",
    "mcp is like an ai wrapper around apis, standardizing how ai agents interact with external services for improved accuracy and reliability.",
]

# Color settings for terminal output
TWEET_COLORS = [
    {'text': 'white', 'bg': 'on_green'},
    {'text': 'white', 'bg': 'on_blue'},
    {'text': 'white', 'bg': 'on_red'}
]

class TweetAgent:
    """Fire Dev's Tweet Generator 🐦 (Demo Version)"""
    
    def __init__(self):
        """Initialize the Tweet Agent"""
        print("🤖 Running Tweet Agent (Demo Version)")
        print("⚠️ Note: This is a demo that generates example tweets without API calls")
        
        # Create tweets directory if it doesn't exist
        self.tweets_dir = Path(PROJECT_ROOT) / "src" / "data" / "tweets"
        self.tweets_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = self.tweets_dir / f"generated_tweets_{timestamp}.txt"
        print(f"📝 Output will be saved to: {self.output_file}")
        
    def _chunk_text(self, text):
        """Split text into chunks of MAX_CHUNK_SIZE characters"""
        return [text[i:i + MAX_CHUNK_SIZE] 
                for i in range(0, len(text), MAX_CHUNK_SIZE)]
    
    def _get_input_text(self, text=None):
        """Get input text from either file or direct input"""
        if USE_TEXT_FILE:
            try:
                with open(OG_TWEET_FILE, 'r') as f:
                    return f.read()
            except Exception as e:
                print(f"❌ Error reading text file: {str(e)}")
                print("⚠️ Falling back to direct text input if provided")
                
        return text
    
    def _print_colored_tweet(self, tweet, color_idx):
        """Print tweet with color based on its position"""
        color_settings = TWEET_COLORS[color_idx % len(TWEET_COLORS)]
        cprint(tweet, color_settings['text'], color_settings['bg'])
        print()  # Add spacing between tweets
    
    def _generate_demo_tweets(self, chunk_number, num_tweets=3):
        """Generate example tweets for demo purposes"""
        # Pick random tweets from templates without repeats
        available_tweets = EXAMPLE_TWEETS.copy()
        random.shuffle(available_tweets)
        
        # Make sure we don't request more tweets than we have templates
        num_tweets = min(num_tweets, len(available_tweets))
        
        # Take the first num_tweets
        selected_tweets = available_tweets[:num_tweets]
        
        # Ensure we don't have duplicates across chunks
        for i, tweet in enumerate(selected_tweets):
            # Add a chunk identifier to make each tweet slightly unique
            # but only if we're processing multiple chunks
            if not USE_TEST_MODE and chunk_number > 1:
                selected_tweets[i] = tweet.rstrip('.') + f" #{chunk_number}."
        
        return selected_tweets
    
    def generate_tweets(self, text=None):
        """Generate tweets from text input or file"""
        try:
            # Get input text
            input_text = self._get_input_text(text)
            
            if not input_text:
                print("❌ No input text provided and couldn't read from file")
                return None
            
            # For test mode, limit text to the first chunk size
            if USE_TEST_MODE:
                print("🧪 Running in test mode - limited to 1 chunk")
                input_text = input_text[:MAX_CHUNK_SIZE]
            
            # Calculate and display text stats
            total_chars = len(input_text)
            total_chunks = math.ceil(total_chars / MAX_CHUNK_SIZE)
            total_tweets = total_chunks * TWEETS_PER_CHUNK
            
            print(f"\n📊 Text Analysis:")
            print(f"Total characters: {total_chars:,}")
            print(f"Chunk size: {MAX_CHUNK_SIZE:,}")
            print(f"Number of chunks: {total_chunks:,}")
            print(f"Tweets per chunk: {TWEETS_PER_CHUNK}")
            print(f"Total tweets to generate: {total_tweets:,}")
            print("=" * 50)
            
            # Split text into chunks if needed
            chunks = self._chunk_text(input_text)
            all_tweets = []
            
            for i, chunk in enumerate(chunks, 1):
                print(f"\n🔄 Processing chunk {i}/{total_chunks} ({len(chunk):,} characters)")
                
                # Generate example tweets for demo
                chunk_tweets = self._generate_demo_tweets(i, TWEETS_PER_CHUNK)
                
                # Print tweets with colors to terminal
                print("\n🐦 Generated tweets for this chunk:")
                for idx, tweet in enumerate(chunk_tweets):
                    self._print_colored_tweet(tweet, idx)
                
                all_tweets.extend(chunk_tweets)
                
                # Write tweets to file with paragraph spacing (clean format)
                with open(self.output_file, 'a') as f:
                    for tweet in chunk_tweets:
                        f.write(f"{tweet}\n\n")  # Double newline for paragraph spacing
                
                # Small delay between chunks to simulate API calls
                if i < total_chunks:
                    time.sleep(1)
            
            return all_tweets
            
        except Exception as e:
            print(f"❌ Error generating tweets: {str(e)}")
            traceback.print_exc()
            return None

if __name__ == "__main__":
    agent = TweetAgent()
    
    # Example usage with direct text
    test_text = """Bitcoin showing strong momentum with increasing volume. 
    Price action suggests accumulation phase might be complete. 
    Key resistance at $69,000 with support holding at $65,000."""
    
    # If USE_TEXT_FILE is True, it will use the file instead of test_text
    tweets = agent.generate_tweets(test_text)
    
    if tweets:
        print(f"\nTweets have been saved to: {agent.output_file}")
