"""Generate the standalone plans page and integrate its site navigation."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import re
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
FEATURES = [
    "Quality lead generation", "Voice assistance", "AI calling",
    "Email automation", "WhatsApp automation", "SMS automation",
    "CRM and sales pipeline", "Company location insights",
    "Manpower data at no additional cost",
]
PLANS = [
    ("Essential", 600, 21000, "A focused start", "A smaller prospecting queue or one focused market."),
    ("Growth", 900, 31500, "Build your momentum", "More capacity for another location or outreach list."),
    ("Pro", 1200, 42000, "Run parallel campaigns", "Keep multiple industry or location campaigns supplied."),
    ("Business", 1500, 52500, "Broaden your coverage", "A larger prospecting pipeline for several sales queues."),
]
WHATSAPP = "https://wa.me/919999881949?text="
PLANS_URL = "https://leadgenai.rudra24secure.com/plans.html"
SALES_EMAIL = "sales@leadgenai.rudra24secure.com"
WEBSITE_URL = "https://leadgenai.rudra24secure.com/index.html"
PANELS = " ".join(f"features-{name.lower()}" for name, *_ in PLANS)
OFFER_ARROW = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'


def asset_url(name):
    """Give each exact asset version a unique URL; retain older versions for cached HTML."""
    content = (ROOT / name).read_bytes()
    source = Path(name)
    if source.suffix == ".css":
        # CSS moves two directories down; retain the original font/image locations.
        def relative_url(match):
            quote_char, url = match.groups()
            if not re.match(r"(?:[a-z][a-z0-9+.-]*:|/|#)", url, re.I):
                url = "../../" + url
            return f"url({quote_char}{url}{quote_char})"
        content = re.sub(r"url\((['\"]?)([^)'\"]+)\1\)", relative_url, content.decode()).encode()
    version = sha256(content).hexdigest()[:12]
    destination = Path("assets/generated") / f"{source.stem}.{version}{source.suffix}"
    (ROOT / destination).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / destination).write_bytes(content)
    return destination.as_posix()


def money(value, decimals=0):
    return f"₹{value:,.{decimals}f}"


def inquiry(message):
    return WHATSAPP + quote(message, safe="")


def expand_button(extra_class=""):
    return f'''<button type="button" class="plan-expand {extra_class}" data-plan-expand aria-expanded="false" aria-controls="{PANELS}" hidden><span data-expand-label>Show all features</span><span class="plan-expand-icon" aria-hidden="true"><svg viewBox="0 0 20 20" width="20" height="20"><path d="M5 10h10"/><path class="plus-stem" d="M10 5v10"/></svg></span></button>'''


def plan_card(plan):
    name, leads, base, summary, fit = plan
    gst = base * 12 // 100
    total = base + gst
    daily = leads // 30
    extra = leads - PLANS[0][1]
    capacity = f"+{extra:,} leads · +{extra * 100 // 600}% vs Essential" if extra else "Your starting lead capacity"
    features = "".join(
        f'<li><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4L19 6"></path></svg><span>{escape(feature)}</span></li>'
        for feature in FEATURES
    )
    featured = " plan-card-featured" if name == "Pro" else ""
    return f'''<article class="plan-card{featured}" id="card-{name.lower()}" aria-labelledby="plan-{name.lower()}">
      <div class="plan-title"><h2 id="plan-{name.lower()}">{name}</h2><span class="plan-fit-label" title="Equivalent across a 30-day month">{daily} / day*</span></div>
      <div class="plan-volume"><div class="plan-leads"><strong>{leads:,}</strong><span>leads / month</span></div><div class="plan-unit"><strong>{money(base / leads)}</strong><span>per lead, before GST</span></div></div>
      <div class="plan-price"><strong>{money(base)}</strong><span>/ month before GST</span></div>
      <div class="plan-billing"><span>12% GST <b>{money(gst)}</b></span><span>Monthly total <strong>{money(total)}</strong></span></div>
      <div class="plan-capacity"><span>{capacity}</span><p>{fit}</p></div>
      <a class="plan-cta" href="{inquiry(f'Hi, I would like to purchase the Rudra24 AI {name} plan. Please explain onboarding and any eligible offers.')}" target="_blank" rel="noopener noreferrer">Choose {name}<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg></a>
      <div class="plan-details">{expand_button()}<div class="plan-feature-wrap" id="features-{name.lower()}" role="region" aria-label="{name} included features"><div class="plan-feature-inner"><ul class="plan-features">{features}</ul></div></div></div>
    </article>'''


def make_page():
    cards = "\n".join(plan_card(plan) for plan in PLANS)
    picker = '<div class="plans-mobile-picker" data-plan-picker role="group" aria-label="Select a plan to compare" hidden>' + "".join(
        f'<button type="button" data-plan-choice="{index}" aria-pressed="{str(index == 0).lower()}" aria-controls="card-{name.lower()}">{name}</button>'
        for index, (name, *_rest) in enumerate(PLANS)
    ) + '</div>'
    promo_url = inquiry("Hi, please share the current promotional offers for Rudra24 AI, including eligibility and applicable terms.")
    referral_url = inquiry("Hi, I would like to know about Rudra24 AI referral discounts, eligibility and applicable terms.")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Explore plans — Rudra24 AI</title><link rel="canonical" href="{PLANS_URL}"><meta property="og:url" content="{PLANS_URL}"><meta name="description" content="Compare Rudra24 AI plans: 600–1,500 monthly leads at ₹35 per lead before GST. Explore included features, capacity and eligible offers."><meta name="theme-color" content="#FFFFEB"><link rel="icon" type="image/png" href="assets/rudra24-icon.png"><link rel="preload" href="assets/fonts/figtree-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/eb-garamond-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{asset_url("site.css")}"><link rel="stylesheet" href="{asset_url("refinement.css")}"><link rel="stylesheet" href="{asset_url("plans.css")}"><script src="{asset_url("plans.js")}" defer></script></head>
<body class="plans-page"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="Rudra24 Digital home"><img src="assets/logo/rudra24-60.png" width="30" height="30" alt=""><span class="brand-name">Rudra24 <em>Digital</em></span></a><nav class="desktop-nav" aria-label="Main navigation"><a href="product.html">Product</a><a href="use-cases.html">Use cases</a><a href="plans.html" aria-current="page">Plans</a><a class="button small" href="contact.html">Talk to us</a></nav><details class="mobile-menu"><summary>Menu</summary><nav aria-label="Mobile navigation"><a href="product.html">Product</a><a href="use-cases.html">Use cases</a><a href="plans.html" aria-current="page">Explore plans</a><a href="contact.html">Contact</a></nav></details></div></header>
<main id="main"><section class="plans-hero"><div class="wrap"><h1>Explore <em>plans.</em></h1><p>One complete sales toolkit. Choose the lead capacity your team can put to work.</p></div></section>
<section class="plans-section" aria-label="Monthly plans"><div class="wrap" data-plan-comparison><div class="plans-toolbar"><div><span class="plans-toolkit-label">All features in every plan</span><p>Monthly pricing · 12% GST shown below</p></div>{expand_button('plan-expand-global')}</div>{picker}<p class="plans-swipe-hint">Swipe to compare plans <span aria-hidden="true">→</span></p><div class="plan-grid" tabindex="0" role="region" aria-label="Compare monthly plans; scroll sideways on mobile">{cards}</div><div class="plans-value"><div><span class="value-label">Why move up?</span><p><strong>300 more leads for {money(10500)} / month.</strong> Choose more capacity for additional locations, industries or sales queues.</p></div><div><span class="value-label">One consistent cost per lead</span><p><strong>₹35 before GST · ₹39.20 including GST.</strong> At the full monthly allowance; all plans include the same features. *Daily figures use a 30-day month.</p></div></div></div></section>
<section class="plans-offers" aria-labelledby="offers-heading"><div class="wrap"><h2 id="offers-heading" class="sr-only">Promotional and referral offers</h2><div class="offers-grid"><article class="offer-card"><div><h3>Promotional savings</h3><p>Check current offers for your business.</p></div><a href="{promo_url}" target="_blank" rel="noopener noreferrer">Check offers {OFFER_ARROW}</a></article><article class="offer-card"><div><h3>Referral discounts</h3><p>Ask about referral offers and eligibility.</p></div><a href="{referral_url}" target="_blank" rel="noopener noreferrer">Ask about referrals {OFFER_ARROW}</a></article></div><p class="offers-terms">Promotional and referral discounts are subject to eligibility and terms; our team confirms eligible offers before billing.</p></div></section>
<footer class="footer"><div class="wrap plans-footer-inner"><a class="brand" href="index.html"><img src="assets/logo/rudra24-60.png" width="30" height="30" alt=""><span class="brand-name">Rudra24 <em>Digital</em></span></a><div class="plans-footer-company"><span>Rudra24 Secure Digital Solutions</span><a href="{WEBSITE_URL}">leadgenai.rudra24secure.com</a></div><div class="plans-footer-contact"><a href="contact.html">Contact us</a><a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to={SALES_EMAIL}&amp;su=Rudra24%20AI%20enquiry" target="_blank" rel="noopener noreferrer">sales<wbr>@leadgenai.rudra24secure.com</a></div></div></footer></body></html>'''


def integrate_navigation():
    for path in ROOT.glob("*.html"):
        if path.name == "plans.html":
            continue
        original = path.read_text()
        updated = re.sub(
            r'(<a href="use-cases\.html"(?: aria-current="page")?>Use cases</a>)(<details class="nav-menu contact-menu">)',
            r'\1<a href="plans.html">Explore plans</a>\2', original,
        )
        updated = updated.replace('<a href="use-cases.html">Use cases</a><a href="contact.html">Contact</a>', '<a href="use-cases.html">Use cases</a><a href="plans.html">Explore plans</a><a href="contact.html">Contact</a>')
        updated = updated.replace('<a href="recruitment.html">Recruitment</a></div><div class="footer-links">', '<a href="recruitment.html">Recruitment</a><a href="plans.html">Explore plans</a></div><div class="footer-links">')
        if updated != original:
            path.write_text(updated)


if __name__ == "__main__":
    (ROOT / "plans.html").write_text(make_page())
    integrate_navigation()
