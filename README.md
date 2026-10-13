# xurrent-agent-fleet

Version: repo-v1.0.0 (2026-10-13)

This repository is the source of truth for Luke Eubanks' agent fleet skills. claude.ai installs them from here as plugins, so a change merged into `main` is a deploy.

## What's inside

- `.claude-plugin/marketplace.json` lists the six plugins.
- `plugins/<name>/.claude-plugin/plugin.json` holds each plugin's name and version.
- `plugins/<name>/skills/<name>/SKILL.md` is the skill itself. call-to-onepager also carries its build script, template, fonts, and logo.

| Plugin | Skill version |
|---|---|
| lynn | v1.5.0 |
| greg | v1.11.0 |
| danny | v1.3.0 |
| brand | v1.11.0 |
| call-to-onepager | v3.4.1 |
| xurrent-brand-guidelines | v1.0.0 |

## How a change ships

1. Every change happens on a branch and arrives as a pull request. Nobody edits `main` directly.
2. Each change bumps two numbers to the same value: `version` in the skill's `SKILL.md` and `version` in its `plugin.json`. claude.ai only delivers a plugin when its version changes.
3. Luke reviews the pull request and merges it. With Sync automatically on, claude.ai picks up the new version from `main`.

## Rules for Lynn

- Work on `claude/` branches and open a pull request. Never merge.
- Any change to a claim, a customer quote, or one of Luke's rulings is a question for Luke first, not an edit.
- Log every merged change in the Lynn registry in Google Drive.
