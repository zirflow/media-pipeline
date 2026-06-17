#!/usr/bin/env python3
"""
Upstream Update Checker — checks all referenced projects for new versions.
Run: python3 scripts/check-updates.py
"""

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent

def check_npm(package: str, current: str) -> dict:
    """Check latest version of an npm package."""
    try:
        req = urllib.request.Request(
            f"https://registry.npmjs.org/{package}/latest",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            latest = data.get("version", "unknown")
            return {
                "package": package,
                "current": current,
                "latest": latest,
                "update": latest != current,
            }
    except Exception as e:
        return {"package": package, "current": current, "error": str(e)}


def check_submodule(path: str) -> dict:
    """Check if a git submodule has unpushed upstream commits."""
    try:
        result = subprocess.run(
            ["git", "-C", path, "log", "..origin/main", "--oneline"],
            capture_output=True, text=True, timeout=10
        )
        commits = result.stdout.strip().splitlines() if result.stdout.strip() else []
        return {
            "path": path,
            "behind": len(commits),
            "updates": commits[:5],
        }
    except Exception as e:
        return {"path": path, "error": str(e)}


def check_pip(package: str) -> dict:
    """Check latest version of a pip package."""
    try:
        req = urllib.request.Request(
            f"https://pypi.org/pypi/{package}/json",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            latest = data["info"]["version"]
        # Get current version
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True, text=True, timeout=10
        )
        current = "not installed"
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    current = line.split(":")[1].strip()
        return {
            "package": package,
            "current": current,
            "latest": latest,
            "update": latest != current if current != "not installed" else True,
        }
    except Exception as e:
        return {"package": package, "error": str(e)}


def main():
    print("=" * 50)
    print("  Media Pipeline — Upstream Update Checker")
    print("=" * 50)

    # 1. NPM packages
    print("\n📦 NPM / Remotion:")
    npm_result = check_npm("remotion", "4.0.478")
    status = "⚠️ Update available" if npm_result.get("update") else "✅ Up to date"
    print(f"  remotion: {npm_result.get('current','?')} → {npm_result.get('latest','?')}  {status}")
    if npm_result.get("error"):
        print(f"  ❌ Error: {npm_result['error']}")

    # 2. Pip packages
    print("\n📦 Pip / Whisper:")
    pip_result = check_pip("openai-whisper")
    status = "⚠️ Update available" if pip_result.get("update") else "✅ Up to date"
    print(f"  openai-whisper: {pip_result.get('current','?')} → {pip_result.get('latest','?')}  {status}")

    # 3. Submodules
    print("\n🔗 Git Submodules:")
    for sm_path in ["pipelines/podcast/repo", "pipelines/wechat-publish/repo"]:
        full_path = str(ROOT / sm_path)
        if not (Path(full_path) / ".git").exists():
            print(f"  {sm_path}: ⚠️ not initialized (run git submodule update --init)")
            continue
        result = check_submodule(full_path)
        if "error" in result:
            print(f"  {sm_path}: ❌ {result['error']}")
        elif result["behind"] > 0:
            print(f"  {sm_path}: ⚠️ {result['behind']} commits behind")
            for c in result["updates"]:
                print(f"    {c}")
        else:
            print(f"  {sm_path}: ✅ Up to date")

    # 4. Summary
    print("\n" + "=" * 50)
    print("  Run: git submodule update --remote --recursive")
    print("       cd pipelines/broll-cover && npm update")
    print("       pip install --upgrade -r requirements.txt")
    print("=" * 50)


if __name__ == "__main__":
    main()
