# Website review — 13 October 2026

## Changes

Centered hero retained with direct plans CTA, framed walkthrough, quieter feature cards, tinted workspace section and forest closing section. Original typography and palette retained. Interactive workspace accurately described as a fictional-data demo.

14 official Apache-licensed Anthropic skill directories installed with original licenses and resources. Source commit and exclusions are recorded in `.agents/README.md`. Skill availability in a future picker requires project rediscovery; documented runtime dependencies are not all installed.

Netlify now prepares a public-only `dist/` folder; tools, skills and notes are excluded from hosting.

## Evidence

- All nine pages reviewed in local Chromium at 1440×900 and 390×844 from the generated hosting folder.
- No horizontal overflow or page JavaScript exceptions in those 18 layouts.
- Home additionally inspected at 320×700; video remains inside first screen on tested phone sizes.
- Plans: all five expansion controls synchronize; Business selection updates and scrolls; collapse restores all five controls.
- Home: primary action opens plans.html; video dialog opens and closes.
- All local HTML asset/link targets exist.
- All 14 installed skills have Apache licenses; hosting directory excludes `.agents/` and `tools/`.
- git diff --check clean.

## Limits

These checks cover local static website behavior. They do not verify live hosting, authentication, real AI execution or payment settlement. The actual AI app repository is still unidentified. Payment credentials and authentication database setup remain pending. Purchase buttons contact the team.
