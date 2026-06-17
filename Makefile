.PHONY: install status update script cover broll subtitle podcast wechat-publish push

SHELL := /bin/bash
ROOT := $(shell pwd)

## Install all dependencies
install:
	@echo "=== Installing Dependencies ==="
	@pip install pyyaml openai-whisper 2>&1 | tail -1
	@cd $(ROOT)/pipelines/broll-cover && npm install --legacy-peer-deps 2>&1 | tail -1
	@echo "✅ Install complete"

## Check pipeline status
status:
	@echo "=== Media Pipeline — Status ==="
	@echo ""
	@echo "[pipeline.py]"
	@python3 $(ROOT)/pipeline.py --list
	@echo ""
	@echo "[broll-cover]"
	@cd $(ROOT)/pipelines/broll-cover && npx remotion compositions src/index.ts 2>&1 | grep -E "^[a-z]"
	@echo ""
	@echo "[subtitles]"
	@which subtitleeditor >/dev/null 2>&1 && echo "  ✅ subtitleeditor" || echo "  ⚠️  subtitleeditor not installed"
	@pip show openai-whisper >/dev/null 2>&1 && echo "  ✅ whisper" || echo "  ⚠️  whisper not installed"
	@echo ""
	@echo "[wechat-publish]"
	@test -d $(ROOT)/pipelines/wechat-publish/repo && echo "  ✅ repo cloned" || echo "  ⚠️  run: cd pipelines/wechat-publish && git clone https://github.com/aximof/wechat_artical_publisher_skill.git repo"
	@echo ""
	@echo "[podcast]"
	@test -d $(ROOT)/pipelines/podcast/repo && echo "  ✅ repo cloned" || echo "  ⚠️  run: cd pipelines/podcast && git clone https://github.com/adamc199/podcast-ad-cleaner.git repo"
	@echo ""
	@du -sh $(ROOT) 2>/dev/null

## Initialize submodules (clone upstream repos)
clone:
	@echo "=== Initializing Submodules ==="
	git submodule update --init --recursive
	@echo "✅ Submodules initialized"
	@echo "   podcast-ad-cleaner → pipelines/podcast/repo"
	@echo "   wechat_artical_publisher_skill → pipelines/wechat-publish/repo"

## Check for upstream updates
update:
	@echo "=== Checking Upstream Updates ==="
	@python3 $(ROOT)/scripts/check-updates.py
	@echo ""
	@echo "=== Syncing Submodules ==="
	git submodule update --remote --recursive 2>&1 | grep -v "^$" || echo "  Already up to date"
	@echo ""
	@echo "=== Syncing npm ==="
	cd $(ROOT)/pipelines/broll-cover && npm update 2>&1 | tail -2
	@echo ""
	@echo "=== Syncing pip ==="
	pip install --upgrade -r $(ROOT)/requirements.txt 2>&1 | tail -1

## Generate script outline + fact-check
script:
	@test -n "$(TOPIC)" || (echo "Usage: make script TOPIC='Your topic'" && exit 1)
	python3 $(ROOT)/pipeline.py --run script-factcheck --param topic="$(TOPIC)"

## Render cover thumbnail
cover:
	@test -n "$(TYPE)" || (echo "Usage: make cover TYPE=youtube|xhs TITLE='Title'" && exit 1)
	python3 $(ROOT)/pipeline.py --run cover --param type=$(TYPE) --param title="$(TITLE)"

## Start Remotion Studio for B-roll editing
broll:
	cd $(ROOT)/pipelines/broll-cover && npx remotion studio src/index.ts

## Process subtitles from audio
subtitle:
	@test -n "$(FILE)" || (echo "Usage: make subtitle FILE=audio.mp3" && exit 1)
	cd $(ROOT)/pipelines/subtitles && bash auto-subtitle.sh "$(FILE)"

## Process podcast
podcast:
	@test -n "$(URL)" || (echo "Usage: make podcast URL='podcast name or URL'" && exit 1)
	python3 $(ROOT)/pipeline.py --run podcast --param url="$(URL)"

## Run a full project
project:
	@test -n "$(FILE)" || (echo "Usage: make project FILE=projects/example.yaml" && exit 1)
	python3 $(ROOT)/pipeline.py --project $(FILE)

## Init a new project
init:
	@test -n "$(TOPIC)" || (echo "Usage: make init TOPIC='Your topic'" && exit 1)
	python3 $(ROOT)/pipeline.py --init "$(TOPIC)"

## Push to GitHub
push:
	git add -A
	git status
	@echo ""
	@read -p "Commit message: " MSG; \
	git commit -m "$$MSG" && git push origin main
