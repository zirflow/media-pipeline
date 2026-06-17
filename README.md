# Media Pipeline

> **Content-as-Code** — An AI-powered content creation pipeline that takes your topic or raw footage and produces finished assets: scripts, subtitles, B-roll animations, covers, WeChat articles, and podcast shownotes.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Repo](https://img.shields.io/badge/GitHub-zirflow%2Fmedia--pipeline-blue)](https://github.com/zirflow/media-pipeline)

---

## The Problem

Solo creators spend 80% of their time on **repetitive mechanical work** — writing outlines, correcting subtitles, designing thumbnails, reformatting for different platforms, transcribing podcasts. The creative 20% (ideas, judgment, taste) gets squeezed.

This pipeline automates the 80%.

## The Pipeline

```
INPUT (topic / audio / video)
│
├─▶ [1] Script Outline + Fact-Check ─── LLM writes + verifies
├─▶ [2] Subtitle Correction ─────────── Whisper → SubtitleEdit
├─▶ [3] B-roll Animation ────────────── Remotion (programmatic video)
├─▶ [4] Cover Generation ────────────── Horizontal + vertical (Remotion)
├─▶ [5] Multi-platform Distribution ─── WeChat (via official API)
├─▶ [6] WeChat Article Formatting ───── Markdown → WeChat HTML → publish
└─▶ [7] Podcast Show-Notes ──────────── Transcription + chapters + summary
```

Each step is **independent and optional**. Run what you need.

## Quick Start

```bash
# Clone (with submodules)
git clone --recurse-submodules https://github.com/zirflow/media-pipeline.git
cd media-pipeline

# Or if already cloned:
git submodule update --init --recursive

# Install dependencies
make install

# 1. Generate a script outline for a topic
python3 pipeline.py --run script-factcheck --param topic="AI for content creators"

# 2. Render a YouTube thumbnail
python3 pipeline.py --run cover --param type=youtube --param title="My Video Title"

# 3. Process a podcast
python3 pipeline.py --run podcast --param url="https://example.com/episode.mp3"

# Full pipeline from a project file
python3 pipeline.py --project projects/example.yaml
```

## Keeping Upstream Dependencies Updated

```bash
# Check all upstream projects for new versions
make update

# Or manually:
git submodule update --remote --recursive   # update podcast-ad-cleaner & wechat publisher
cd pipelines/broll-cover && npm update      # update Remotion
pip install --upgrade -r requirements.txt   # update Whisper
```

Dependabot runs weekly and GitHub Actions auto-creates PRs when upstream repos change.

## Pipeline Details

| # | Step | What it does | Tech | Status |
|---|------|-------------|------|--------|
| 1 | **Script Outline + Fact-Check** | LLM generates a video script outline, then fact-checks each claim against web sources | Python + FreeLLMAPI / OpenAI | ✅ |
| 2 | **Subtitle Correction** | Whisper transcribes audio; SubtitleEdit batch-corrects spelling & timing; exports SRT/VTT/ASS | SubtitleEdit + Whisper | ✅ |
| 3 | **B-roll Animation** | Programmatic motion graphics — transitions, data viz, animated backgrounds — rendered as MP4 | Remotion (React) | ✅ |
| 4 | **Cover Generation** | Renders 16:9 (YouTube) and 9:16 (Xiaohongshu/Douyin) thumbnails from templates, batch-ready | Remotion stills | ✅ |
| 5 | **Multi-platform Distribution** | (WeChat ✓ via official API; Xiaohongshu ✗ — no public API available) | Python + WeChat API | ⚠️ |
| 6 | **WeChat Article Publishing** | Markdown → formatted WeChat HTML → auto-upload images → publish to drafts | wechat_artical_publisher_skill | ✅ |
| 7 | **Podcast Show-Notes** | Whisper transcription → auto chapter detection → summary generation → timestamped VTT | podcast-ad-cleaner + LLM | ✅ |

## Requirements

- **Python 3.8+**
- **Node.js 18+** (for Remotion covers & B-roll)
- **ffmpeg** (for audio/subtitle processing)
- **WeChat Official Account** (for steps 5-6; AppID + AppSecret needed)

Optional:
- **Ollama** (for fully-local podcast ad detection & chapter generation)
- **SubtitleEdit** (for subtitle batch correction)

## Project Configuration

Create a project file:

```yaml
# projects/my-video.yaml
title: "AI Tools for Content Creators"
tone: professional
steps:
  - script-factcheck
  - cover
  - wechat-publish
audio: ./recording.mp3        # optional: for subtitles + podcast
```

Then run:

```bash
python3 pipeline.py --project projects/my-video.yaml
```

## Credits

This pipeline integrates several excellent open-source projects:

- **[Remotion](https://github.com/remotion-dev/remotion)** — Programmatic video framework (source-available)
- **[SubtitleEdit](https://github.com/SubtitleEdit/subtitleedit)** — Cross-platform subtitle editor (GPL)
- **[podcast-ad-cleaner](https://github.com/adamc199/podcast-ad-cleaner)** — Local podcast processing (MIT)
- **[wechat_artical_publisher_skill](https://github.com/aximof/wechat_artical_publisher_skill)** — WeChat article publisher (MIT)
- **[OpenAI Whisper](https://github.com/openai/whisper)** — Speech-to-text (MIT)

## License

MIT — see [LICENSE](LICENSE).

---

*Built for solo creators who'd rather spend time on ideas than on formatting.*
