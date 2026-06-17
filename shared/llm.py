#!/usr/bin/env python3
"""
Shared LLM client — unified interface for all pipeline LLM calls.
Loads config from config.env.
"""

import json
import os
import urllib.request
from pathlib import Path
from typing import Optional


def load_config():
    """Load config.env into environment."""
    config_path = Path(__file__).parent.parent / "config.env"
    if config_path.exists():
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def get_config() -> dict:
    """Get LLM connection parameters."""
    load_config()
    return {
        "base_url": os.environ.get(
            "LLM_API_BASE_URL", "http://192.168.31.4:3001/v1"
        ),
        "api_key": os.environ.get("LLM_API_KEY", ""),
        "model": os.environ.get("LLM_MODEL", "auto"),
    }


def chat(
    messages: list,
    system: Optional[str] = None,
    max_tokens: int = 2000,
    temperature: float = 0.7,
    timeout: int = 60,
) -> str:
    """
    Send a chat completion request to the configured LLM.

    Args:
        messages: List of {role, content} dicts
        system: Optional system prompt (prepended to messages)
        max_tokens: Maximum output tokens
        temperature: Sampling temperature
        timeout: Request timeout in seconds

    Returns:
        Generated response text
    """
    config = get_config()

    if system:
        messages = [{"role": "system", "content": system}] + messages

    payload = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    req = urllib.request.Request(
        f"{config['base_url']}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['api_key']}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"LLM API error {e.code}: {body}") from e


def prompt(
    user_prompt: str,
    system: Optional[str] = None,
    **kwargs,
) -> str:
    """Convenience: send a single user prompt."""
    return chat([{"role": "user", "content": user_prompt}], system=system, **kwargs)
