# Podcast Show-Notes Pipeline

Transcribes podcast episodes, detects chapters, and generates shownotes.

Uses: [podcast-ad-cleaner](https://github.com/adamc199/podcast-ad-cleaner) (MIT)

## Setup

```bash
cd pipelines/podcast
git clone https://github.com/adamc199/podcast-ad-cleaner.git repo
cd repo
chmod +x install.sh
./install.sh
```

## Usage

```bash
# Step 1: Download, transcribe, and detect chapters
cd pipelines/podcast/repo
bash podcast-cleaner.sh "podcast name"

# Step 2: Generate shownotes from transcription
python3 pipelines/podcast/generate_shownotes.py --vtt ~/cleaned-podcasts/*.vtt
```

## Output

- Clean MP3 with embedded chapters
- VTT transcript with timestamps
- JSON chapter markers
- Processing report

## Requirements

- Linux (Ubuntu/Arch/Fedora)
- Ollama (for AI ad detection + chapter generation)
- ffmpeg
- Python 3.8+
