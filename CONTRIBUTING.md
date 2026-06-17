# Contributing to Media Pipeline

Thanks for your interest! This project is designed for solo creators but we welcome contributions.

## How to contribute

### Report issues

Open a GitHub issue. Include:
- What you were trying to do
- What happened
- Expected behavior
- Your OS and Python/Node versions

### Submit changes

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Run `make install` to verify
5. Submit a PR

### Code style

- Python: Keep it simple. stdlib first, minimal dependencies.
- TypeScript/React: Follow Remotion conventions.
- Scripts: Bash for simple wrappers, Python for logic.

### Adding a new pipeline step

1. Create `pipelines/<step-name>/pipeline.py` with a CLI entry point
2. Register it in `pipeline.py` by adding a `@register("<step-name>")` function
3. Add a `README.md` with usage docs
4. Update the top-level README table

### Upstream dependencies

We track upstream changes via:
- **git submodules** for cloned repos (podcast-ad-cleaner, wechat_artical_publisher_skill)
- **npm/pip versions** for package dependencies (Remotion, Whisper)
- **Dependabot** for automated update checks

When a submodule has updates:
```bash
git submodule update --remote --recursive
git add pipelines/*/repo
git commit -m "chore: sync upstream submodules"
```

## License

This project is MIT. Your contributions will be MIT too.
