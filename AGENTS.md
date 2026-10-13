# Rudra24 website

## Project skills

Official public Anthropic skills are installed in `.agents/skills/`. The
catalog and pinned upstream commit are in `.agents/README.md`. Use relevant
skills by reading their `SKILL.md`; do not load every skill for every task.
For visual work, use `frontend-design` while preserving Rudra24's approved
cream and forest palette, Figtree body type and EB Garamond display type.
Use Codex tools for equivalent filesystem, shell and browser operations.
These skills do not require switching models.

## Website publishing

Run `python tools/build_plans.py` and `python tools/build_landing.py` after
changing their source assets. These scripts version browser assets. Keep
previous tracked asset versions available for cached HTML.

`python tools/publish_site.py` prepares `dist/` for Netlify. Agent skills and
development files must never be copied into the public website directory.
The full `build_site.py` generator still expects resources from the original
AI app repository; use the standalone scripts in this repository.

## Product accuracy

Website previews use fictional data. Do not describe them as the real live
AI app. The real app source, authentication setup and payment credentials
are separate requirements. Never claim WhatsApp enquiries are a payment
gateway or that a client-side success callback activates a paid plan.
