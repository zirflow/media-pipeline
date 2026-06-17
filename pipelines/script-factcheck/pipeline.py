#!/usr/bin/env python3
"""
Script Outline + Fact-Check Pipeline
Generates video script outlines with automated fact-checking.

Usage:
  python3 pipeline.py --topic "Your Topic" [--tone professional] [--output file.md]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def call_llm(prompt: str, system: str = "You are a professional content creator.") -> str:
    """Call the configured LLM API."""
    api_base = os.environ.get("LLM_API_BASE_URL", "http://192.168.31.4:3001/v1")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "auto")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 2000,
        "temperature": 0.7,
    }

    req = urllib.request.Request(
        f"{api_base}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]


def generate_outline(topic: str) -> str:
    """Step 1: Generate a structured video script outline."""
    prompt = (
        f"Create a video script outline for the topic: 「{topic}」\n\n"
        "Include:\n"
        "1. Opening hook (background + problem statement)\n"
        "2. Main content (3 key points + examples)\n"
        "3. Practical tips (if applicable)\n"
        "4. Summary + call to action\n\n"
        "Describe each section in 1-2 sentences."
    )
    return call_llm(prompt, "You are an experienced content strategist.")


def fact_check(script: str) -> str:
    """Step 2: Fact-check claims in the script."""
    prompt = (
        f"Fact-check the following script content. "
        f"Flag any potentially inaccurate or exaggerated claims:\n\n{script[:3000]}\n\n"
        "For each claim, mark as:\n"
        "✅ Verified / ⚠️ Needs verification / ❌ Inaccurate\n"
        "For ⚠️ and ❌ items, suggest corrections."
    )
    return call_llm(prompt, "You are a rigorous fact-checker.")


def polish(outline: str, tone: str) -> str:
    """Step 3: Polish the script for delivery."""
    prompt = (
        f"Rewrite the following script outline in a {tone} tone, "
        f"suitable for video narration.\n\n{outline}\n\n"
        "Make it conversational, add emotional cues [surprise] [empathy] [insight], "
        "and ensure each segment is 30-60 seconds when spoken."
    )
    return call_llm(prompt, "You are a professional script editor.")


def main():
    parser = argparse.ArgumentParser(description="Script Outline + Fact-Check Pipeline")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument("--tone", default="professional", choices=["professional", "casual", "dramatic", "empathetic"])
    parser.add_argument("--output", "-o", default=None, help="Output file path")
    parser.add_argument("--no-factcheck", action="store_true", help="Skip fact-check step")
    args = parser.parse_args()

    print(f"Script Outline + Fact-Check", flush=True)
    print(f"Topic: {args.topic}  |  Tone: {args.tone}\n", flush=True)

    outline = generate_outline(args.topic)
    print("=== Outline ===\n" + outline + "\n", flush=True)

    if not args.no_factcheck:
        checks = fact_check(outline)
        print("=== Fact-Check ===\n" + checks + "\n", flush=True)
    else:
        checks = "Skipped"

    final_script = polish(outline, args.tone)
    print("=== Polished Script ===\n" + final_script + "\n", flush=True)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"# {args.topic}\n\n## Outline\n\n{outline}\n\n")
            f.write(f"## Fact-Check\n\n{checks}\n\n## Script\n\n{final_script}\n")
        print(f"Saved to: {args.output}", flush=True)


if __name__ == "__main__":
    main()
