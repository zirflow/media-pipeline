# WeChat Article Publishing Pipeline

Publishes Markdown articles to WeChat Official Account drafts via the official API.

Uses: [wechat_artical_publisher_skill](https://github.com/aximof/wechat_artical_publisher_skill)

## Setup

```bash
# Clone the publisher
cd pipelines/wechat-publish
git clone https://github.com/aximof/wechat_artical_publisher_skill.git repo

# Configure credentials
cp repo/.env.example repo/.env
# Edit repo/.env with your WeChat AppID and AppSecret
```

## Usage

```bash
cd pipelines/wechat-publish/repo
python3 publish.py article.md
```

## Prerequisites

1. WeChat Official Account (服务号 or 订阅号)
2. AppID & AppSecret from WeChat Admin Panel
3. Server IP whitelisted in WeChat Admin Panel
