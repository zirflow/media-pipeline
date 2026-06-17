# Media Pipeline — 内容即代码

> **Content-as-Code** — AI 驱动的内容生产流水线。输入主题或原始素材，自动输出脚本、字幕、B-roll 动画、封面、公众号文章和播客 Show-Notes。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Repo](https://img.shields.io/badge/GitHub-zirflow%2Fmedia--pipeline-blue)](https://github.com/zirflow/media-pipeline)

---

## 痛点

独立创作者 80% 的时间花在**重复性机械工作**上——写大纲、校字幕、设计封面、跨平台排版、转录播客。创意的 20%（选题、判断、审美）反而被挤占。

这个管线把 80% 自动化。

## 七步流程

```
输入（主题 / 音频 / 视频）
│
├─▶ [1] 脚本大纲打磨 + Fact-Check ─── LLM 生成 → 联网核实
├─▶ [2] 字幕整理捉虫 ──────────────── Whisper 转写 → 校对 → 多格式导出
├─▶ [3] B-roll 动画生成 ─────────────── Remotion 编程式视频
├─▶ [4] 封面生成 ──────────────────── 横版(16:9) + 竖版(9:16) 批量渲染
├─▶ [5] 多平台分发 ─────────────────  公众号(官方API) / 小红书(无API)
├─▶ [6] 公众号排版上传 ────────────── Markdown → 微信 HTML → 发布
└─▶ [7] 播客 Show-Notes ──────────── 转录 → 章节检测 → 摘要生成
```

每步**独立可选**，按需运行。

## 快速开始

```bash
# 克隆（含子模块）
git clone --recurse-submodules https://github.com/zirflow/media-pipeline.git
cd media-pipeline

# 安装依赖
make install

# 1. 为主题生成脚本大纲
python3 pipeline.py --run script-factcheck --param topic="AI 自媒体创作"

# 2. 渲染 YouTube 封面
python3 pipeline.py --run cover --param type=youtube --param title="视频标题"

# 3. 处理播客
python3 pipeline.py --run podcast --param url="播客名称"

# 完整项目
python3 pipeline.py --project projects/example.yaml
```

## 各步骤详解

| # | 步骤 | 功能 | 技术栈 | 上游依赖 | 状态 |
|:-:|------|------|--------|---------|:----:|
| 1 | **脚本大纲+Fact-Check** | LLM 生成大纲 → 逐条事实核查 → 润色 | Python + 任意 LLM API | 无 | ✅ |
| 2 | **字幕整理捉虫** | Whisper 语音转写 → SubtitleEdit 校对 → SRT/VTT/ASS | SubtitleEdit + Whisper | [SubtitleEdit](https://github.com/SubtitleEdit/subtitleedit) (GPL) | ✅ |
| 3 | **B-roll 动画** | 编程式运动图形 — 转场/数据可视化/动态背景 | Remotion (React) | [Remotion](https://github.com/remotion-dev/remotion) (源码可用) | ✅ |
| 4 | **封面生成** | 横版 1280×720 / 竖版 1080×1920 批量渲染 | Remotion still | [Remotion](https://github.com/remotion-dev/remotion) | ✅ |
| 5 | **多平台分发** | 公众号(官方API) / 小红书(无公开API) | Python | — | ⚠️ |
| 6 | **公众号排版上传** | Markdown → 微信HTML → 自动传图 → 发布 | wechat_artical_publisher_skill | [aximof/skill](https://github.com/aximof/wechat_artical_publisher_skill) (MIT) | ✅ |
| 7 | **播客 Show-Notes** | Whisper 转录 → 章节检测 → 摘要 → VTT | podcast-ad-cleaner + LLM | [podcast-ad-cleaner](https://github.com/adamc199/podcast-ad-cleaner) (MIT) | ✅ |

## 上游依赖管理

本项目的上游依赖以 **git submodule + 包管理器 + Dependabot** 三层方式管理：

| 依赖 | 管理方式 | 自动更新 |
|------|---------|---------|
| Remotion | npm (`package.json` 锁定版本) | ✅ Dependabot 每周检查 |
| podcast-ad-cleaner | git submodule | ✅ Dependabot + GitHub Actions |
| wechat_artical_publisher_skill | git submodule | ✅ Dependabot + GitHub Actions |
| SubtitleEdit | apt 包管理器 | ❌ 系统包管理器 |
| OpenAI Whisper | pip (`requirements.txt`) | ✅ Dependabot 每周检查 |

### 手动同步上游

```bash
# 更新所有 submodule 到最新
git submodule update --remote --recursive

# 查看更新了什么
git diff --submodule

# 更新 npm 依赖
cd pipelines/broll-cover && npm update

# 更新 pip 依赖
pip install --upgrade -r requirements.txt
```

## 项目配置

创建项目 YAML 文件：

```yaml
# projects/my-video.yaml
title: "AI Tools for Content Creators"
tone: professional
steps:
  - script-factcheck
  - cover
  - wechat-publish
audio: ./recording.mp3
```

然后运行 `python3 pipeline.py --project projects/my-video.yaml`。

## 上游项目致谢

- **[Remotion](https://github.com/remotion-dev/remotion)** — 编程式视频框架（v4.0.478，源码可用协议）
- **[SubtitleEdit](https://github.com/SubtitleEdit/subtitleedit)** — 跨平台字幕编辑器（13k+ stars，GPL）
- **[podcast-ad-cleaner](https://github.com/adamc199/podcast-ad-cleaner)** — 本地播客处理工具（MIT）
- **[wechat_artical_publisher_skill](https://github.com/aximof/wechat_artical_publisher_skill)** — 公众号发布器（MIT）
- **[OpenAI Whisper](https://github.com/openai/whisper)** — 语音识别（MIT）

## 协议

MIT — 详见 [LICENSE](LICENSE)

---

*为独立创作者打造。把时间花在想法的打磨上，而不是格式的复制粘贴上。*
