# B-roll Animation + Cover Generation

Programmatic video rendering using Remotion. Generates:

- **B-roll**: Animated background transitions and motion graphics
- **Covers**: YouTube thumbnails (16:9) and Xiaohongshu/Douyin covers (9:16)

## Quick Start

```bash
# Install dependencies
cd pipelines/broll-cover
npm install

# List available compositions
npx remotion compositions src/index.ts

# Render a YouTube thumbnail
npx remotion still src/index.ts youtube-cover yt-cover.png

# Render a vertical cover (小红书/抖音)
npx remotion still src/index.ts xhs-cover xhs-cover.png

# Start the Remotion Studio (visual editor)
npx remotion studio src/index.ts

# Render B-roll animation
npx remotion render src/index.ts broll out.mp4
```

## Customization

Edit `src/Root.tsx` to customize:
- Background gradients and colors
- Text styles and positioning
- Animation duration and effects
- Add new composition templates

## Requirements

- Node.js 18+
- npm
