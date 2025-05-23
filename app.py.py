import os
import streamlit as st
import yt_dlp
import tempfile
import subprocess
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="English Accent Analyzer",
    page_icon="🎙️",
    layout="wide"
)

# App title and description
st.title("English Accent Analyzer")
st.markdown("""
This app analyzes English accents from YouTube videos using keyword analysis.
Enter a YouTube URL below to get started.
""")

# Function to download audio
def download_audio(url: str) -> str:
    """Download audio from YouTube URL"""
    try:
        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        output_path = Path(temp_dir) / f"accent_analyzer_temp.mp3"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_path),
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return str(output_path)
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# Function to analyze the YouTube video
def analyze_video(url: str) -> dict:
    """Analyze YouTube video based on title, description, comments, etc."""
    try:
        # Get video info with yt-dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,  # Don't download the video
            'getcomments': True,    # Get comments
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # Extract useful information
        title = info.get('title', '')
        description = info.get('description', '')
        
        # Combine text for analysis
        text_to_analyze = (title + " " + description).lower()
        
        # Perform accent analysis
        return classify_accent(text_to_analyze)
    except Exception as e:
        st.error(f"Error analyzing video: {e}")
        return {
            "accent": "Unknown",
            "confidence": 0.0,
            "note": f"Error analyzing video: {str(e)}",
            "confidence_details": "Could not analyze video content"
        }

# Function to classify accent
def classify_accent(text: str) -> dict:
    """Classify the accent based on keywords in the text"""
    text = text.lower()
    
    # Accent feature detection with comprehensive word lists
    australian_words = ["mate", "aussie", "bloody", "no worries", "g'day", "arvo", "barbie", "reckon", "crikey", 
                        "australian", "australia", "sydney", "melbourne", "brisbane", "perth"]
    
    british_words = ["innit", "cheers", "trousers", "bloody", "blimey", "quid", "rubbish", "proper", "mum", "whilst",
                    "british", "britain", "uk", "london", "manchester", "liverpool", "england", "scotland", "wales"]
    
    american_words = ["dude", "awesome", "gotta", "wanna", "guys", "totally", "mom", "bucks", "elevator", "apartment",
                     "american", "america", "usa", "united states", "new york", "california", "los angeles", "chicago"]
    
    indian_words = ["only yaar", "i am telling", "what is your good name", "itself", "kindly", "do the needful", "prepone",
                   "indian", "india", "mumbai", "delhi", "bangalore", "hyderabad", "chennai", "kolkata"]
    
    # Count occurrences
    australian_count = sum(1 for word in australian_words if word in text)
    british_count = sum(1 for word in british_words if word in text)
    american_count = sum(1 for word in american_words if word in text)
    indian_count = sum(1 for word in indian_words if word in text)
    
    # Add base confidence to prevent zeros
    accent_scores = {
        "Australian": australian_count + 0.1,
        "British": british_count + 0.1, 
        "American": american_count + 0.1,
        "Indian English": indian_count + 0.1
    }
    
    # If no strong indicators, slightly favor American as default
    if sum(accent_scores.values()) < 1.5:
        accent_scores["American"] += 0.3
    
    # Find the accent with highest score
    top_accent = max(accent_scores, key=accent_scores.get)
    
    # Calculate confidence (normalize to percentage)
    total = sum(accent_scores.values())
    for accent in accent_scores:
        accent_scores[accent] = (accent_scores[accent] / total) * 100
    
    # Prepare notes
    notes = {
        "Australian": "Australian expressions or locations detected.",
        "British": "British vocabulary and expressions identified.",
        "American": "American expressions or locations detected.",
        "Indian English": "Indian English patterns or locations detected."
    }
    
    if sum(1 for score in accent_scores.values() if score > 30) > 1:
        note = f"Mixed accent with {top_accent} being dominant."
    else:
        note = notes.get(top_accent, "No strong regional indicators found.")
    
    # Prepare confidence details
    confidence_details = "\n".join([f"{accent}: {score:.1f}%" for accent, score in 
                                   sorted(accent_scores.items(), key=lambda x: x[1], reverse=True)])
    
    return {
        "accent": top_accent,
        "confidence": accent_scores[top_accent],
        "note": note,
        "confidence_details": confidence_details
    }

# Main app logic
url_input = st.text_input("Enter a YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
analyze_button = st.button("Analyze Accent")

if analyze_button and url_input:
    # Process video
    with st.status("Processing video...") as status:
        status.update(label="Analyzing video...")
        result = analyze_video(url_input)
            
        status.update(label="Analysis complete!", state="complete")
    
    # Display results in a nice layout
    st.success("Analysis completed successfully!")
    
    # Create columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Accent Analysis")
        st.metric("Detected Accent", result["accent"])
        st.metric("Confidence", f"{result['confidence']:.1f}%")
        st.info(result["note"])
    
    with col2:
        st.subheader("Detailed Confidence Scores")
        st.code(result["confidence_details"])
    
# Add info about the tool
st.markdown("---")
st.markdown("""
### About this tool
This tool uses:
- **yt-dlp** to analyze YouTube video metadata
- **Keyword analysis** to determine accent patterns

Note: This simple version analyzes video title and description rather than audio transcription.
For more accurate results, install SpeechRecognition and use the full version.

### Installation for full version
To use the speech recognition version, install these packages:
```bash
pip install streamlit yt-dlp SpeechRecognition
```
""")