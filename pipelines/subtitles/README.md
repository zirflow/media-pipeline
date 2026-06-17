# Subtitle Correction Pipeline

Automates subtitle generation and correction:
1. **Whisper** — Speech-to-text transcription
2. **SubtitleEdit** — Batch spell-checking and format conversion

## Usage

```bash
# Process an audio file
./auto-subtitle.sh audio.mp3

# Output in output-audio/
```

## Requirements

- `whisper` (`pip install openai-whisper`)
- `subtitleeditor` (apt/brew)
- `ffmpeg`
