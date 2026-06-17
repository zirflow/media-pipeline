# Script Outline + Fact-Check Pipeline

Generates a structured video script outline with automated fact-checking via LLM.

## Usage

```bash
# Basic
python3 pipeline.py --topic "Your Topic"

# With options
python3 pipeline.py --topic "AI Tools" --tone casual --output script.md

# Skip fact-checking (faster, for drafts)
python3 pipeline.py --topic "Quick Idea" --no-factcheck
```

## Requirements

- LLM API configured in `config.env` (see root README)
