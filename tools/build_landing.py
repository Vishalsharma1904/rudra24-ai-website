"""Apply the standalone landing layout and version shared browser assets."""
from pathlib import Path
import re
from build_plans import asset_url

ROOT = Path(__file__).resolve().parents[1]
HERO_COPY = "Find the right businesses, start better conversations and keep every follow-up in one workspace."
OLD_COPY = "Find the right businesses, start better conversations and keep every customer’s next step in view — one calm workspace for your whole team."
MOBILE_SOURCE = '<source src="assets/video/launch-mobile.mp4#t=19.5" media="(max-width: 760px)" type="video/mp4">'


def build_landing():
    home = ROOT / "index.html"
    html = home.read_text()
    html = html.replace('class="hero launch-hero"', 'class="hero launch-hero landing-centered"')
    html = html.replace(OLD_COPY, HERO_COPY)
    html = html.replace('>Talk to us<svg', '>Explore plans<svg', 1)
    # The first hero action leads directly to the published pricing page.
    hero_start = html.index('<div class="actions hero-copy">')
    hero_end = html.index('</div>', hero_start)
    hero_actions = html[hero_start:hero_end]
    hero_actions = re.sub(r'href="https://wa.me/[^\"]+" target="_blank" rel="noopener noreferrer"', 'href="plans.html"', hero_actions, count=1)
    html = html[:hero_start] + hero_actions + html[hero_end:]
    html = re.sub(r'<div class="film-stage-heading">.*?</div>', '', html, count=1)
    html = html.replace('Live app preview', 'Interactive workspace demo')
    html = html.replace('Live preview</a>', 'Workspace demo</a>')
    html = html.replace('A working copy of Rudra24 AI. Click the sidebar and the tabs to follow one lead from search to follow-up.', 'Explore the workflow with fictional data. Use the sidebar and tabs to follow a lead from search to follow-up.')
    # Only the hero's first CTA pair changes; later calls to action retain their labels.
    html = html.replace('>Talk to our team<svg', '>Talk to us<svg', 1)
    html = html.replace('class="button secondary" href="#workspace">Explore the workspace', 'class="button secondary" href="#film">Watch demo', 1)
    html = html.replace('tabindex="0" autoplay muted loop controls playsinline preload="metadata"', 'tabindex="0" muted loop controls playsinline preload="none"')
    html = html.replace('poster="assets/video/launch-poster.jpg"', 'poster="assets/video/launch-mobile-poster.jpg"', 1)
    source = '<source src="assets/video/launch-film.mp4#t=19.5" type="video/mp4">'
    if MOBILE_SOURCE not in html:
        html = html.replace(source, MOBILE_SOURCE + source, 1)
    html = html.replace('Original 1080p film · Hover for sound. Click the video if your browser needs a gesture.', 'Use the player controls for full screen on your phone. Tap the video to enable sound.')
    if 'rel="canonical"' not in html:
        html = html.replace('<title>Home — Rudra24 AI</title>', '<title>Home — Rudra24 AI</title><link rel="canonical" href="https://leadgenai.rudra24secure.com/index.html">', 1)
    if not re.search(r'href="(?:landing\.css|assets/generated/landing\.[a-f0-9]+\.css)"', html):
        html = html.replace('</head>', '<link rel="stylesheet" href="landing.css"></head>', 1)
    home.write_text(html)
    names = ("site.css", "refinement.css", "site.js", "media.js")
    for path in ROOT.glob("*.html"):
        if path.name == "plans.html":
            continue
        html = path.read_text()
        for name in (*names, "landing.css") if path.name == "index.html" else names:
            stem, suffix = name.rsplit(".", 1)
            pattern = r'(href|src)="(?:' + re.escape(name) + r'|assets/generated/' + re.escape(stem) + r'\.[a-f0-9]+\.' + suffix + r')"'
            versioned = asset_url(name)
            html = re.sub(pattern, lambda match: f'{match[1]}="{versioned}"', html)
        if html != path.read_text():
            path.write_text(html)


if __name__ == "__main__":
    build_landing()
