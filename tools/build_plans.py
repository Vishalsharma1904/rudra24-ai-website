from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
FEATURES = [
    "Quality lead generation",
    "Voice assistance",
    "AI calling",
    "Email automation",
    "WhatsApp automation",
    "SMS automation",
    "CRM and sales pipeline",
    "Company location insights",
    "Manpower data at no additional cost",
]
PLANS = [
    ("Essential", 600, 21000, 2520, 23520, "A focused start for a growing team."),
    ("Growth", 900, 31500, 3780, 35280, "More room to build a steady pipeline."),
    ("Pro", 1200, 42000, 5040, 47040, "For teams ready to scale their outreach."),
    ("Business", 1500, 52500, 6300, 58800, "Higher lead volume for ambitious teams."),
]
WHATSAPP = "https://wa.me/919999881949?text="


def money(value):
    return f"₹{value:,}"


def plan_card(plan, index):
    name, leads, base, gst, total, summary = plan
    message = quote(f"Hi, I would like to purchase the Rudra24 AI {name} plan.", safe="")
    features = "".join(
        f'<li><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"></path></svg><span>{escape(feature)}</span></li>'
        for feature in FEATURES
    )
    featured = " plan-card-featured" if name == "Pro" else ""
    badge = ""
    return f'''<article class="plan-card{featured}">
      {badge}<span class="plan-number">Plan 0{index}</span><h2>{escape(name)}</h2>
      <p class="plan-summary">{escape(summary)}</p>
      <div class="plan-leads"><strong>{leads:,}</strong><span>leads each month</span></div>
      <div class="plan-price"><strong>{money(base)}<span> / month</span></strong></div>
      <p class="plan-tax">12% GST {money(gst)} · <b>Total {money(total)} / month</b></p>
      <a class="plan-cta" href="{WHATSAPP}{message}" target="_blank" rel="noopener noreferrer">Ask about {escape(name)} <span aria-hidden="true">↗</span></a>
      <details class="plan-details"><summary>See all included features <span class="plan-details-icon" aria-hidden="true">+</span></summary>
        <div class="plan-feature-wrap"><ul class="plan-features">{features}</ul></div>
      </details>
    </article>'''


def make_page():
    cards = "\n".join(plan_card(plan, i) for i, plan in enumerate(PLANS, 1))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Explore plans — Rudra24 AI</title><meta name="description" content="Compare Rudra24 AI plans, monthly lead volumes and GST-inclusive pricing."><meta name="theme-color" content="#FFFFEB"><link rel="icon" type="image/png" href="assets/rudra24-icon.png"><link rel="preload" href="assets/fonts/figtree-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/eb-garamond-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="refinement.css"><link rel="stylesheet" href="plans.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Rudra24 Digital home"><img src="assets/logo/rudra24-60.png" width="30" height="30" alt=""><span class="brand-name">Rudra24 <em>Digital</em></span></a><nav class="desktop-nav" aria-label="Main navigation"><a href="product.html">Product</a><a href="use-cases.html">Use cases</a><a href="plans.html" aria-current="page">Plans</a><a class="button small" href="contact.html">Talk to us</a></nav><details class="mobile-menu"><summary>Menu</summary><nav aria-label="Mobile navigation"><a href="product.html">Product</a><a href="use-cases.html">Use cases</a><a href="plans.html" aria-current="page">Explore plans</a><a href="contact.html">Contact</a></nav></details></div></header>
<main id="main"><section class="plans-hero"><div class="wrap"><span class="plan-index">01</span><span class="eyebrow">Plans for your next stage</span><h1>Explore <em>plans.</em></h1><p class="subcopy">A clearer view of what your team can do with Rudra24 AI. Choose the lead volume that fits your next move.</p><div class="plans-note"><span class="plans-note-mark">AI</span><span>Every plan includes the complete Rudra24 AI toolkit <i>·</i> no feature add-ons</span></div></div></section>
<section class="plans-section"><div class="wrap"><div class="plans-intro"><div><span class="eyebrow">Simple, transparent pricing</span><h2>More conversations.<br><em>Less guesswork.</em></h2></div><p>Choose a monthly lead allowance. GST is shown separately, with your total payable amount displayed before you get in touch.</p></div><div class="plan-grid">{cards}</div><p class="plans-footnote">Prices shown per month. 12% GST is added to the base price. For onboarding, referrals or a tailored requirement, <a href="contact.html">talk with our team</a>.</p></div></section>
<section class="plans-cta-band"><div class="wrap"><div><span class="eyebrow">Not sure where to begin?</span><h2>Let’s find your <em>fit.</em></h2><p>Share what your team needs and we’ll help you choose a plan.</p></div><div class="actions"><a class="button" href="https://wa.me/919999881949?text=Hi%2C%20please%20help%20me%20choose%20a%20Rudra24%20AI%20plan." target="_blank" rel="noopener noreferrer">Talk to our team</a></div></div></section></main>
<footer class="footer"><div class="wrap"><div class="footer-main"><div class="footer-brand"><a class="brand" href="index.html"><img src="assets/logo/rudra24-60.png" width="30" height="30" alt=""><span class="brand-name">Rudra24 <em>Digital</em></span></a><p>Your AI partner for finding leads, starting conversations and keeping business moving.</p></div><div class="footer-links"><h3>Explore</h3><a href="product.html">Product overview</a><a href="plans.html">Explore plans</a><a href="use-cases.html">Use cases</a><a href="contact.html">Talk to the team</a></div></div></div></footer></body></html>'''


def integrate_navigation():
    desktop_old = '<a href="use-cases.html">Use cases</a><details class="nav-menu contact-menu">'
    desktop_new = '<a href="use-cases.html">Use cases</a><a href="plans.html">Explore plans</a><details class="nav-menu contact-menu">'
    mobile_old = '<a href="use-cases.html">Use cases</a><a href="contact.html">Contact</a>'
    mobile_new = '<a href="use-cases.html">Use cases</a><a href="plans.html">Explore plans</a><a href="contact.html">Contact</a>'
    footer_old = '<a href="recruitment.html">Recruitment</a></div><div class="footer-links">'
    footer_new = '<a href="recruitment.html">Recruitment</a><a href="plans.html">Explore plans</a></div><div class="footer-links">'
    for path in ROOT.glob("*.html"):
        if path.name == "plans.html":
            continue
        original = path.read_text()
        updated = original.replace(desktop_old, desktop_new)
        updated = updated.replace(mobile_old, mobile_new)
        updated = updated.replace(footer_old, footer_new)
        path.write_text(updated)


if __name__ == "__main__":
    (ROOT / "plans.html").write_text(make_page())
    integrate_navigation()
