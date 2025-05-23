# English Accent Analyzer

A Streamlit web application that analyzes English accents from YouTube videos using keyword analysis of video metadata.

## Features

- Analyzes YouTube video titles and descriptions to detect accent patterns
- Supports detection of multiple English accents:
  - American English
  - British English
  - Australian English
  - Indian English
- Provides confidence scores and detailed analysis
- Simple and intuitive web interface

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install streamlit yt-dlp
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Open your web browser to the displayed URL (typically http://localhost:8501)
3. Enter a YouTube URL and click "Analyze Accent"
4. View the results showing:
   - Detected accent
   - Confidence score
   - Analysis notes
   - Detailed confidence breakdown

## How It Works

The analyzer uses keyword analysis to detect accent patterns by:
1. Extracting video metadata using yt-dlp
2. Analyzing text for region-specific words and expressions
3. Calculating confidence scores based on keyword matches
4. Providing detailed analysis of detected accent patterns

## Requirements

- Python 3.6+
- streamlit
- yt-dlp
- FFmpeg (for audio processing)

## Future Improvements

- Audio transcription support using SpeechRecognition
- More accent varieties
- Enhanced pattern detection
- Machine learning-based classification

## License

MIT License
