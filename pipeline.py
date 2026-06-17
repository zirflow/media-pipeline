#!/usr/bin/env python3
"""
Media Pipeline — Unified Content-as-Code Pipeline

Usage:
  python3 pipeline.py --run <step> [--param key=value ...]
  python3 pipeline.py --project <project.yaml>
  python3 pipeline.py --init "Topic" --tone professional

Examples:
  python3 pipeline.py --run script-factcheck --param topic="AI Tools"
  python3 pipeline.py --run cover --param type=youtube --param title="Hello"
  python3 pipeline.py --project projects/example.yaml
"""

import argparse
import json
import os
import subprocess
import sys
import yaml
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.resolve()
PIPELINES = ROOT / "pipelines"
CONFIG_ENV = ROOT / "config.env"


def load_config():
    """Load credentials from config.env into environment."""
    if CONFIG_ENV.exists():
        with open(CONFIG_ENV) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def load_llm_config() -> dict:
    """Get LLM connection details from environment."""
    return {
        "base_url": os.environ.get("LLM_API_BASE_URL", "http://192.168.31.4:3001/v1"),
        "api_key": os.environ.get("LLM_API_KEY", ""),
        "model": os.environ.get("LLM_MODEL", "auto"),
    }


# ── Available Pipeline Steps ──────────────────────────────────────

STEPS = {}


def register(name: str):
    """Decorator to register a pipeline step."""
    def decorator(fn):
        STEPS[name] = fn
        return fn
    return decorator


@register("script-factcheck")
def run_script_factcheck(params: dict) -> dict:
    """Step 1: Script outline generation + fact-checking."""
    topic = params.get("topic", "")
    if not topic:
        return {"error": "Missing --param topic=..."}
    
    result = subprocess.run(
        [sys.executable, str(PIPELINES / "script-factcheck" / "pipeline.py"),
         "--topic", topic, "--output", "-"],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    
    return {"step": "script-factcheck", "topic": topic, "output": result.stdout}


@register("cover")
def run_cover(params: dict) -> dict:
    """Step 4: Render thumbnail from Remotion."""
    cover_type = params.get("type", "youtube")
    title = params.get("title", "Untitled")
    
    broll_dir = PIPELINES / "broll-cover"
    composition = f"{cover_type}-cover"
    output_file = ROOT / "output" / f"{cover_type}-cover.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    result = subprocess.run(
        ["npx", "remotion", "still", "src/index.ts", composition, str(output_file)],
        cwd=str(broll_dir), capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    
    return {"step": "cover", "type": cover_type, "output": str(output_file)}


@register("podcast")
def run_podcast(params: dict) -> dict:
    """Step 7: Podcast transcription + chapters + shownotes."""
    url = params.get("url", "")
    if not url:
        return {"error": "Missing --param url=..."}
    
    cleaner_dir = PIPELINES / "podcast" / "repo"
    if not cleaner_dir.exists():
        return {"error": "podcast-ad-cleaner not cloned. Run: cd pipelines/podcast && git clone https://github.com/adamc199/podcast-ad-cleaner.git repo"}
    
    result = subprocess.run(
        ["bash", "podcast-cleaner.sh", url],
        cwd=str(cleaner_dir), capture_output=True, text=True, timeout=600
    )
    
    # Generate shownotes from VTT
    shownotes_script = PIPELINES / "podcast" / "generate_shownotes.py"
    vtt_files = list(Path.home().glob("cleaned-podcasts/*.vtt"))
    if vtt_files and shownotes_script.exists():
        subprocess.run(
            [sys.executable, str(shownotes_script), "--vtt", str(vtt_files[-1])],
            capture_output=True, text=True, timeout=30
        )
    
    return {"step": "podcast", "status": "ok" if result.returncode == 0 else "partial"}


# ── Main Pipeline Runner ──────────────────────────────────────────


def run_project(project_path: Path):
    """Execute all steps defined in a project YAML."""
    with open(project_path) as f:
        project = yaml.safe_load(f)
    
    title = project.get("title", "Untitled Project")
    print(f"\n{'='*50}")
    print(f" Pipeline: {title}")
    print(f"{'='*50}\n")
    
    results = {}
    for step_name in project.get("steps", []):
        if step_name not in STEPS:
            print(f"  ⚠️  Unknown step: {step_name}, skipping")
            continue
        
        print(f"  ▶ [{step_name}]")
        params = project.get("params", {}).get(step_name, {})
        params.setdefault("topic", title)
        
        result = STEPS[step_name](params)
        if "error" in result:
            print(f"  ❌ Failed: {result['error']}")
        else:
            print(f"  ✅ Done")
        results[step_name] = result
        print()
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Media Pipeline — Content-as-Code")
    parser.add_argument("--run", help="Run a single pipeline step")
    parser.add_argument("--param", action="append", default=[], help="Parameters (key=value)")
    parser.add_argument("--project", help="Run a project YAML file")
    parser.add_argument("--list", action="store_true", help="List available steps")
    parser.add_argument("--init", help="Initialize a new project with topic")
    parser.add_argument("--tone", default="professional", help="Content tone")
    
    args = parser.parse_args()
    load_config()
    
    if args.list:
        print("Available pipeline steps:")
        for name in sorted(STEPS.keys()):
            print(f"  {name}")
        return
    
    if args.init:
        topic = args.init
        projects_dir = ROOT / "projects"
        projects_dir.mkdir(exist_ok=True)
        
        safe_name = topic.lower().replace(" ", "-")[:30]
        yaml_path = projects_dir / f"{safe_name}.yaml"
        
        config = {
            "title": topic,
            "tone": args.tone,
            "steps": list(STEPS.keys()),
            "params": {},
        }
        
        with open(yaml_path, "w") as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"✅ Created {yaml_path}")
        print(f"   Run: python3 pipeline.py --project {yaml_path}")
        return
    
    if args.project:
        results = run_project(Path(args.project))
        failed = [k for k, v in results.items() if "error" in v]
        if failed:
            print(f"\n⚠️  Steps with errors: {', '.join(failed)}")
        else:
            print(f"\n✅ All steps completed successfully")
        return
    
    if args.run:
        params = {}
        for p in args.param:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
        
        if args.run not in STEPS:
            print(f"Unknown step: {args.run}")
            print(f"Available: {', '.join(sorted(STEPS.keys()))}")
            return
        
        result = STEPS[args.run](params)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ {json.dumps(result, ensure_ascii=False, indent=2)}")
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
