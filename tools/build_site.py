"""Author the standalone static site. No build tool is needed to view its output."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import shutil
import json
import re

SITE = Path(__file__).resolve().parents[1]
REPO = SITE.parents[1]

ICONS = {}

def icon(name, extra=''):
    return f'<svg class="icon {extra}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

# Reuse the app's Feather geometry, without importing its runtime or settings.
app_icons = json.loads(re.search(r'var ICONS = (\{.*?\});', (REPO/'clavis-icons.js').read_text(encoding='utf-8'), re.S)[1])
for site_name, app_name in {'assistant':'aperture','search':'briefcase','people':'users','crm':'trello','message':'message-circle','phone':'phone-call','mail':'mail','calendar':'calendar','download':'download','check':'check','clock':'clock','pin':'map-pin','chart':'bar-chart-2','file':'file-text','memory':'database','connect':'link','mic':'mic','task':'check-square','shield':'shield','menu':'menu','play':'play','arrow':'arrow-right','chevron':'chevron-down','grid':'grid','zap':'zap','settings':'settings','sidebar':'sidebar','book':'book-open','map':'map','navigation':'navigation','layers':'layers','plus':'plus','minus':'minus','external':'external-link','send':'arrow-up','sound':'volume-2','muted':'volume-x','close':'x','copy':'copy','globe':'globe','filter':'filter','route':'git-commit'}.items():
    ICONS[site_name] = app_icons[app_name]

CLIPS = {
    # key: (category, headline, one plain line, start offset inside the clip in seconds, [(second, moment, detail)])
    'leads': ('Lead generation', 'Find businesses that need your service.', 'Tell Run Agent who you serve and where. It searches Google Maps and job listings for you — no spreadsheets, no copy-paste.', 0,
              [(0,'Choose where to look','A state, a city or a single locality — anywhere in India.'),(4,'Narrow it down','Here the search is set to Haryana → Gurugram → Sector 29.'),(8,'Let it search','Run Agent starts finding matching businesses on Google Maps.')]),
    'calling': ('AI voice calling', 'An AI caller that speaks Hindi and English.', 'Set up your calling agent once. She calls through your list in the hours you choose, so your team only talks to interested leads.', 0,
              [(0,'Build your agent','Give her a name, a role and a natural Hindi + English voice.'),(4,'Describe your business','What you offer, what makes you different and the goal of each call.'),(7,'Set calling hours','She works through the call queue, one call at a time.')]),
    'outreach': ('WhatsApp & email', 'Personal messages you approve before sending.', 'Connect your official WhatsApp Business number once. Every lead gets a personal message — and nothing is sent until you approve it.', 0,
              [(0,'Connect your number','Your official WhatsApp Business account, set up once.'),(4,'A message for every lead','Each one is personalised, with your brochure attached.'),(8,'You review the batch','Check every message first, then send when you are ready.')]),
    'crm': ('CRM & follow-ups', 'Know every client and what comes next.', 'Every deal, conversation and follow-up in one place — from the first call to the confirmed client.', 2,
              [(2,'Your numbers at a glance','Open deals, confirmed clients and follow-ups due this week.'),(5,'Deals by stage','See how many leads are new, qualified or waiting on a follow-up.'),(8,'Move deals forward','The pipeline board keeps every client moving to the next step.')]),
    'assistant': ('AI assistant', 'Ask in Hindi or English. Get work started.', 'Type the way you speak. Your assistant writes the message, script or search for you — ready to review and send.', 4,
              [(4,'Ask the way you speak','“Gurugram ke hotels ke liye ek follow-up message likho.”'),(6.5,'Get a ready draft','A polite, personal follow-up, written in seconds.'),(8.5,'Send or refine','Send it on WhatsApp, copy it, or ask for changes.')]),
}

def feature_film(key):
    category, title, desc, start, moments = CLIPS[key]
    steps = ''.join(f'<li data-at="{at}"><button type="button" data-clip-seek="{at}" data-js-control><span>{n+1:02}</span><b>{m}</b><small>{d}</small></button></li>' for n,(at,m,d) in enumerate(moments))
    return f'''<section class="section rule feature-film" id="film-{key}"><div class="wrap split film-split"><div class="film-explain reveal"><span class="eyebrow">Inside the app · {category}</span><h2>{title}</h2><p class="subcopy">{desc}</p><p class="film-moments-label">What happens in this clip</p><ol class="film-moments">{steps}</ol></div><figure class="film-frame reveal" data-clip-player data-clip="{key}" data-start="{start}"><video controls muted playsinline preload="metadata" poster="assets/video/{key}-poster.jpg" width="1920" height="1080" aria-label="{category}: {title} — a short, silent clip from the app"><source src="assets/video/{key}.mp4" type="video/mp4"></video><figcaption><span class="film-live" aria-hidden="true"><i></i>Plays by itself · silent</span><button type="button" data-clip-toggle data-js-control>Pause</button></figcaption><div class="film-progress" aria-hidden="true"><i></i></div></figure></div></section>'''

def wa(label='Talk to us on WhatsApp', topic='', classes='button'):
    text = 'Hi, I would like to know more about Rudra24 AI' + (f' for {topic}' if topic else '') + '.'
    return f'<a class="{classes}" href="https://wa.me/919999881949?text={quote(text)}" target="_blank" rel="noopener noreferrer">{escape(label)}{icon("arrow")}</a>'

def link(label, href, classes='text-link'):
    return f'<a class="{classes}" href="{href}">{label}{icon("arrow")}</a>'

PAGES = [
    ('index', 'Home', 'Your sales team’s new AI partner.', 'Find the right leads, start better conversations and keep every customer’s next step in view with Rudra24 AI.'),
    ('product', 'Product', 'One workspace. A little less work.', 'Explore the Rudra24 AI assistant, voice tools, memory, lead research, outreach, CRM and integrations.'),
    ('lead-generation', 'Lead generation', 'Find the right businesses. Start there.', 'Research business leads by location and industry, review contacts, and export useful results with Rudra24 AI.'),
    ('crm', 'CRM & follow-ups', 'Every conversation. A clear next step.', 'Manage customer records, deals, follow-ups, meetings, reports, clients and contracts in Rudra24 AI.'),
    ('outreach', 'Outreach & calling', 'A thoughtful first hello. A better follow-up.', 'Prepare email, WhatsApp, SMS and calling workflows with Rudra24 AI. Review drafts and connect your providers.'),
    ('recruitment', 'Recruitment', 'Find people. Keep the process clear.', 'Search candidates, organise your shortlist and manage recruitment data with Rudra24 AI.'),
    ('use-cases', 'Use cases', 'Made for the way small teams work.', 'See Rudra24 AI workflows for service businesses, security and housekeeping agencies, sales and staffing teams.'),
    ('contact', 'Contact', 'Let’s make room for better work.', 'Talk to the Rudra24 team on WhatsApp about a product walkthrough, business needs and setup.'),
]

FEATURE_NAV = [('product','assistant','Product overview','Everything, in one workspace'),('lead-generation','search','Lead generation','Find and organise businesses'),('crm','crm','CRM & follow-ups','Keep the next step in view'),('outreach','message','Outreach & calling','Prepare better conversations'),('recruitment','people','Recruitment','Build a useful shortlist')]

def logo(size):
    widths = (20, 24, 30, 32, 40, 48, 60, 64, 80, 90, 96, 120, 144, 180, 270)
    files = ', '.join(f'assets/logo/rudra24-{w}.png {w}w' for w in widths)
    fallback = next(w for w in widths if w >= min(size * 2, widths[-1]))
    return f'<img src="assets/logo/rudra24-{fallback}.png" srcset="{files}" sizes="{size}px" width="{size}" height="{size}" alt="">'

def brand_mark(size, home_label=True):
    label = ' aria-label="Rudra24 Digital home"' if home_label else ''
    return f'<a class="brand" href="index.html"{label}>{logo(size)}<span class="brand-name">Rudra24 <em>Digital</em></span></a>'

MENU_MORE = [('product.html#assistant','assistant','AI assistant'),('product.html#integrations','connect','Connected tools'),('outreach.html#calling','phone','Voice calling'),('crm.html#contracts','file','Clients & contracts'),('crm.html#reports','chart','Reports'),('lead-generation.html#exports','download','Data exports')]

def header(current):
    menu = ''.join(f'<a href="{slug}.html"{(" aria-current=\"page\"" if current == slug else "")}>{icon(ico)}<span><b>{label}</b><small>{desc}</small></span></a>' for slug,ico,label,desc in FEATURE_NAV)
    more = ''.join(f'<a href="{href}">{icon(ico)}<span>{label}</span></a>' for href,ico,label in MENU_MORE)
    panel = f'<div class="menu-panel mega"><div class="mega-cols"><div class="mega-col mega-main"><span class="mega-label">Product</span>{menu}</div><div class="mega-col"><span class="mega-label">Inside the workspace</span>{more}</div></div><div class="mega-foot"><span>Every page has a hands-on demo with fictional data.</span><a class="mega-foot-link" href="use-cases.html">{icon("people")}Use cases</a></div></div>'
    mobile = ''.join(f'<a class="sub" href="{slug}.html">{label}</a>' for slug,_,label,_ in FEATURE_NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
    <header class="site-header"><div class="wrap header-inner">
      {brand_mark(30)}
      <nav class="desktop-nav" aria-label="Main navigation"><details class="nav-menu product-menu"><summary>Product {icon('chevron','chevron')}</summary>{panel}</details>
      <a href="use-cases.html"{(' aria-current="page"' if current=='use-cases' else '')}>Use cases</a><details class="nav-menu contact-menu"><summary{(' class="is-current"' if current=='contact' else '')}>Contact {icon('chevron','chevron')}</summary><div class="menu-panel mega mini"><div class="mega-col"><span class="mega-label">Talk to us</span><a href="https://wa.me/919999881949" target="_blank" rel="noopener noreferrer">{icon("message")}<span><b>WhatsApp</b><small>Usually the quickest reply</small></span></a><a href="tel:+919999881949">{icon("phone")}<span><b>+91 99998 81949</b><small>Vishal Sharma · Marketing</small></span></a><a href="mailto:sales@leadgenai.rudra24secure.com">{icon("mail")}<span><b>Email the team</b><small>sales@leadgenai.rudra24secure.com</small></span></a><a href="contact.html#walkthrough">{icon("pin")}<span><b>Head office</b><small>{escape(ADDRESS)}</small></span></a></div><div class="mega-foot"><a class="mega-foot-link" href="contact.html">{icon("file")}Open the contact page</a></div></div></details>{wa('Let’s talk',classes='button small')}</nav>
      <details class="mobile-menu"><summary>Menu {icon('menu')}</summary><nav aria-label="Mobile navigation"><a href="product.html">Explore the product</a>{mobile}<a href="use-cases.html">Use cases</a><a href="contact.html">Contact</a>{wa()}</nav></details>
    </div></header>'''

COMPANIES = [
    ('Rudra24 Secure Digital Solutions', 'sales@leadgenai.rudra24secure.com', 'https://leadgenai.rudra24secure.com/index.html', 'leadgenai.rudra24secure.com'),
    ('Rudra24 Secure', 'rudra24securegroup@gmail.com', 'https://rudra24secure.com', 'rudra24secure.com'),
    ('Rudra24 Jobs', 'Rudra24Jobs@gmail.com', 'https://rudra24jobs.com', 'rudra24jobs.com'),
]
ADDRESS_LINES = ['Rudra House', 'Plot No. 72, Street No. 2', 'Sunita Vihar, Loni, Ghaziabad', 'Uttar Pradesh, India 201102']
ADDRESS = ', '.join(ADDRESS_LINES)
MAP_URL = 'https://www.google.com/maps/search/?api=1&query=' + quote(ADDRESS)

def site_link(url, label):
    ext = url.startswith('http')
    return f'<a href="{url}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{label}{icon("arrow") if ext else ""}</a>'

def company_list():
    return ''.join(f'<li><b>{name}</b><a href="mailto:{mail}">{mail.replace("@", "<wbr>@")}</a>{site_link(url, label)}</li>' for name, mail, url, label in COMPANIES)

DIRECTIONS_URL = 'https://www.google.com/maps/dir/?api=1&destination=' + quote(ADDRESS)

def office():
    """Head-office address as text; the map itself lives in the Visit us section above the footer."""
    lines = '<br>'.join(ADDRESS_LINES)
    return f'<address class="office"><span class="office-label">Head office</span><p>{lines}</p><a href="#visit">See it on the map{icon("arrow")}</a></address>'

def visit_section():
    """Visit us: the app's map with our head-office pin. Clicking the pin opens a card with address, phone and email."""
    lines = '<br>'.join(ADDRESS_LINES)
    card = f'''<div class="visit-card" id="visit-card" data-visit-card role="group" aria-label="Rudra24 head office"><button type="button" class="visit-close" data-visit-close aria-label="Close" data-js-control>{icon('close')}</button><div class="visit-card-head">{logo(40)}<div><b>Rudra24 Digital</b><small>Head office · Loni, Ghaziabad</small></div></div><address>{lines}</address><ul class="visit-lines"><li>{icon('phone')}<a href="tel:+919999881949">+91 99998 81949</a></li><li>{icon('mail')}<a href="mailto:sales@leadgenai.rudra24secure.com">sales@leadgenai.rudra24secure.com</a></li></ul><div class="visit-actions"><a class="button" href="{DIRECTIONS_URL}" target="_blank" rel="noopener noreferrer">Get directions{icon('navigation')}</a>{wa('WhatsApp', classes='button secondary')}</div><small class="visit-note">The pin marks our area in Loni. Directions use the full address.</small></div>'''
    views = ''.join(f'<button type="button" data-map-view="{v}" aria-pressed="{str(v == "map").lower()}" data-js-control>{label}</button>' for v, label in [('map', 'Map'), ('satellite', 'Satellite'), ('3d', '3D')])
    details = f'''<div class="visit-details reveal"><span class="eyebrow">Head office</span><address>{lines}</address><p>Planning a visit? Contact our team so we can make time for you.</p><ul class="visit-lines"><li>{icon('phone')}<a href="tel:+919999881949">+91 99998 81949</a></li><li>{icon('mail')}<a href="mailto:sales@leadgenai.rudra24secure.com">sales@leadgenai.rudra24secure.com</a></li></ul><div class="actions"><a class="button" href="{DIRECTIONS_URL}" target="_blank" rel="noopener noreferrer">Get directions{icon('navigation')}</a>{wa('WhatsApp', classes='button secondary')}</div></div>'''
    return f'''<section class="section visit" id="visit"><div class="wrap">{head('Visit us', 'Come and meet us <em>in Loni.</em>', 'Find our head office, get directions or contact the team before your visit.')}<div class="visit-layout">{details}<div class="visit-map reveal" data-visit-map data-lat="{OFFICE_POINT[0]}" data-lng="{OFFICE_POINT[1]}"><div class="visit-canvas" data-visit-canvas role="region" aria-label="Map of our head office area in Loni, Ghaziabad. Ctrl and scroll to zoom."></div><p class="map-fallback"><span class="map-loading-dot" aria-hidden="true"></span><span class="map-fallback-wait">Opening the map…</span><span class="map-fallback-fail">The live map needs an internet connection. Our address and phone number are beside the map.</span></p><div class="map-views visit-views" role="group" aria-label="Map view">{views}</div>{card}<button type="button" class="visit-pin" data-visit-pin aria-expanded="false" aria-controls="visit-card" data-js-control><span class="visit-pin-dot">{logo(22)}</span><span class="visit-pin-label">Rudra House · Head office</span></button></div></div></div></section>'''

def footer():
    products = ''.join(f'<a href="{slug}.html">{label}</a>' for slug,_,label,_ in FEATURE_NAV)
    return f'''<footer class="footer"><div class="wrap"><div class="footer-main">
    <div class="footer-brand">{brand_mark(40, False)}<p>Your AI partner for finding leads, starting conversations and keeping business moving.</p><div class="footer-companies"><h3>Our companies</h3><ul class="company-list">{company_list()}</ul></div></div>
    <div class="footer-links"><h3>Explore</h3>{products}</div><div class="footer-links"><h3>Stay in touch</h3><a href="use-cases.html">Use cases</a><a href="contact.html">Talk to the team</a><a href="https://wa.me/919999881949" target="_blank" rel="noopener noreferrer">WhatsApp</a><a href="mailto:sales@leadgenai.rudra24secure.com">Email us</a></div>
    <div class="footer-visit">{office()}</div></div>
    <div class="footer-bottom"><span>© 2026 Rudra24 Digital</span><span>Built for small teams. Designed for everyday work.</span></div></div></footer>'''

def closing(topic='your business'):
    return f'''<section class="closing"><div class="wrap reveal"><span class="eyebrow" style="justify-content:center">Your next step</span><h2>Less to juggle.<br><em>More room to grow.</em></h2><p>Tell us how your team works. We’ll walk you through the parts of Rudra24 AI that fit.</p><div class="actions">{wa(topic=topic)}{link('Meet the workspace','product.html','button secondary')}</div></div></section>'''

def faq(items, title='Questions, <em>answered.</em>', num=''):
    rows = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
    return f'<section class="section rule" id="questions"><div class="wrap">{head('Questions', title, 'Short answers about languages, your data and what this website does.', num=num)}<div class="faq-list reveal">{rows}</div></div></section>'

def page_hero(eyebrow, title, desc, topic='', center=False):
    return f'''<section class="page-hero {'center' if center else ''}"><div class="wrap"><span class="eyebrow hero-title">{eyebrow}</span><h1 class="hero-title">{title}</h1><p class="subcopy hero-copy">{desc}</p><div class="actions hero-copy">{wa(topic=topic)}{link('See how it works','#walkthrough','button secondary')}</div></div></section>'''

LEADS_ON_MAP = [
    ('Oakfield Suites','Hotel','Connaught Place, Delhi',28.6315,77.2167),
    ('Northgate Residency','Hotel','Karol Bagh, Delhi',28.6519,77.1909),
    ('The Grand Atrium','Hotel','Aerocity, Delhi',28.5530,77.1210),
    ('Willow Care Centre','Hospital','Sector 18, Noida',28.5700,77.3260),
    ('Lotus Heart Clinic','Hospital','Dwarka, Delhi',28.5920,77.0460),
    ('Cedar Business Park','Office','Cyber City, Gurugram',28.4950,77.0890),
    ('Maple Tech Tower','Office','Sector 62, Noida',28.6270,77.3730),
    ('Sunrise Public School','School','Indirapuram, Ghaziabad',28.6460,77.3690),
    ('Brightpath Academy','School','Rohini, Delhi',28.7360,77.1130),
]
OFFICE_POINT = (28.7316, 77.3008)  # Loni, Ghaziabad (approximate; "Open in Maps" uses the full address)

def lead_map_section():
    data = json.dumps([{'name':n,'kind':k,'area':a,'lat':la,'lng':ln} for n,k,a,la,ln in LEADS_ON_MAP]).replace('"','&quot;')
    chips = ''.join(f'<button type="button" data-map-filter="{k}" aria-pressed="{str(k=="All").lower()}" data-js-control>{k if k=="All" else k+"s"}</button>' for k in ['All','Hotel','Hospital','Office','School'])
    items = ''.join(f'<li><button type="button" data-map-item="{i}" data-js-control><b>{n}</b><span>{k} · {a}</span></button></li>' for i,(n,k,a,_,_) in enumerate(LEADS_ON_MAP))
    feats = points([
        ('Every lead, where it is','Search results land on the map, so you can see at a glance which businesses are close to you or your team.'),
        ('Filter by industry','Show only hotels, hospitals, offices or schools. Pins and the list update together.'),
        ('Street, satellite or 3D','Switch views like in the app — read street names, check the building from above or tilt into 3D.'),
        ('Plan the visit','Add stops from any pin and see them joined in order, with the total distance. Open any place in Google Maps.')], 'points-4')
    return f'''<section class="section lead-map-section" id="lead-map"><div class="wrap">{head('Lead map','See your leads <em>on a map.</em>','Every business becomes a pin. Filter by industry, open any pin and plan which ones to visit.', num='03')}
    <div class="lead-map reveal" data-lead-map data-leads="{data}"><div class="map-toolbar"><div class="map-chips" role="group" aria-label="Filter the map">{chips}</div><div class="map-views" role="group" aria-label="Map view"><button type="button" data-map-view="map" aria-pressed="true" data-js-control>Map</button><button type="button" data-map-view="satellite" aria-pressed="false" data-js-control>Satellite</button><button type="button" data-map-view="3d" aria-pressed="false" data-js-control>3D</button></div></div><p class="map-status" data-map-status aria-live="polite">9 sample businesses in Delhi NCR</p>
    <div class="map-stage"><div class="map-canvas" data-map-canvas role="region" aria-label="Map of fictional sample businesses in Delhi NCR"><p class="map-fallback"><span class="map-loading-dot" aria-hidden="true"></span><span class="map-fallback-wait">Opening the map…</span><span class="map-fallback-fail">The live map needs an internet connection. The list beside it shows every sample business.</span></p></div>
    <div class="map-side"><ol class="map-list" data-map-list>{items}</ol><div class="map-route" data-map-route><div class="map-route-head"><b>Visit plan</b><button type="button" data-map-route-clear data-js-control>Clear</button></div><p data-map-route-text>Open a pin and choose “Add to visit” to plan a route.</p></div></div></div>
    <p class="map-note">Fictional sample businesses. Same map engine and layers as the app — OpenFreeMap / OpenStreetMap streets and Esri satellite imagery. Ctrl + scroll to zoom.</p></div>
    {feats}</div></section>'''

def head(label, title, definition, extra='', num=''):
    """Centred chapter heading: a short section name, the tagline, then one plain-language line."""
    number = f'<i>{num}</i>' if num else ''
    return f'<div class="section-head chapter reveal"><span class="eyebrow">{number}{label}</span><h2>{title}</h2><p>{definition}</p>{extra}</div>'

def points(items, extra_class=''):
    """Numbered explanations under a thin rule — the way claude.com explains a section."""
    cells = ''.join(f'<article class="point"><small>{i+1:02}</small><h3>{t}</h3><p>{d}</p></article>' for i,(t,d) in enumerate(items))
    return f'<div class="points reveal {extra_class}">{cells}</div>'

def frame(body, label='Product preview', sidebar=False):
    side = ''
    return f'''<div class="demo-frame"><div class="demo-bar"><div class="demo-bar-label"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span>{logo(18)}Rudra24 AI <span aria-hidden="true">/</span> {label}</div><span class="sample-label">Fictional demo data</span></div><div class="{'demo-shell' if sidebar else ''}">{side}{body}</div></div>'''

def lead_pane():
    companies = [('O','Oakfield Suites','Hotel','Delhi','Oakfield Suites · Hotel · Delhi. Sample contact record selected. Review the contact source before outreach.'),('W','Willow Care Centre','Healthcare','Noida','Willow Care Centre · Healthcare · Noida. Sample contact record selected. No real contact details are used in this preview.'),('C','Cedar Business Park','Offices','Gurugram','Cedar Business Park · Offices · Gurugram. Sample contact record selected. Save the record to keep its next step in view.')]
    rows = ''.join(f'<tr><td><div class="company"><span class="initial">{initial}</span><span><b>{name}</b><small>{kind}</small></span></div></td><td>{area}</td><td><button class="lead-open" type="button" data-js-control data-lead-open="{detail}" aria-label="View {name}" aria-pressed="false">View {icon("arrow")}</button></td></tr>' for initial,name,kind,area,detail in companies)
    return f'''<div data-lead-demo><div class="prompt">{icon('assistant')}Find 3 business leads in Delhi NCR<span class="prompt-arrow" aria-hidden="true">{icon('arrow')}</span></div><div class="sample-meta"><span>3 sample businesses</span><span>Review before outreach</span></div><div class="table-scroll" tabindex="0" role="region" aria-label="Sample business leads"><table class="lead-table"><caption class="sr-only">Fictional business leads for the product preview</caption><thead><tr><th scope="col">Business</th><th scope="col">Area</th><th scope="col"><span class="sr-only">Details</span></th></tr></thead><tbody>{rows}</tbody></table></div><div class="lead-detail">{icon('pin')}<span data-lead-detail aria-live="polite">Choose a sample business to see its details. Real searches can include company information, contact sources and map locations.</span></div><div class="demo-bottom"><p>Sample data. No live search runs here.</p><button class="tiny-button" type="button" data-js-control data-export-sample>{icon('download')}Export sample CSV</button></div></div>'''

def draft_pane():
    return f'''<div data-draft-demo><div class="channel-select" aria-label="Sample draft channel" data-js-control><button type="button" data-channel="email" aria-pressed="true">Email</button><button type="button" data-channel="whatsapp" aria-pressed="false">WhatsApp</button><button type="button" data-channel="call" aria-pressed="false">Call script</button></div><div class="draft"><div class="draft-meta" data-draft-meta>Email draft · Review before sending</div><div class="draft-copy" data-draft-copy>Subject: Housekeeping support for Oakfield Suites

Hello,

We provide housekeeping support for hospitality teams. I would like to understand whether Oakfield Suites is reviewing its staffing needs.

Would a short conversation next week be useful?

Thank you,
Your team</div></div><div class="demo-bottom"><p>Preparation only. Nothing is sent.</p><span class="sample-label">You review the next step</span></div></div>'''

def crm_pane():
    columns = ''
    for i,stage in enumerate(['New','Contacted','Follow-up']):
        card = '<article class="deal" data-deal><b>Oakfield Suites</b><p>Housekeeping enquiry</p><span class="tag">Ready to review</span></article>' if i==0 else ''
        columns += f'<div class="kanban-column" data-stage="{stage}"><h4>{stage}<span data-count>{1 if i==0 else 0}</span></h4>{card}</div>'
    return f'<div data-crm-demo><div class="kanban">{columns}</div><div class="demo-bottom"><p data-crm-status aria-live="polite">One sample enquiry, ready to review.</p><button class="tiny-button" type="button" data-js-control data-move-deal>Move to Contacted</button></div><div class="lead-detail">{icon("check")}<span>The next step stays with the record, alongside your notes and activity.</span></div></div>'

def followup_pane():
    return f'''<div class="followup-grid"><div class="note-card">{icon('calendar')}<h4>A time to<br>follow up.</h4><p>Oakfield Suites<br>Review the housekeeping enquiry.</p><small>Example reminder · Tuesday, 11:00</small></div><div class="note-card">{icon('file')}<h4>The details,<br>still together.</h4><p>Company introduction, conversation notes and the next step, attached to one record.</p><small>Meeting time confirmed by you</small></div></div><div class="lead-detail">{icon('clock')}<span>Calendar actions depend on your connected account and confirmed meeting details.</span></div>'''

def app_nav(icon_name, label, view=None, tab=None, current=False):
    data = (f' data-app-view="{view}"' if view else '') + (f' data-tab-target="{tab}"' if tab else '')
    return f'<button type="button" class="app-nav-item"{data}{" aria-current=\"true\"" if current else ""} title="{label}" aria-label="{label}">{icon(icon_name)}<span>{label}</span></button>'

def app_view_dashboard():
    stats = ''.join(f'<div class="app-stat"><span>{label}</span><b>{value}</b><small>{note}</small></div>' for label,value,note in [('Leads this week','1,248','+18% vs last week'),('Contacted','412','33% of new leads'),('Follow-ups due','96','24 due today')])
    sources = ''.join(f'<div class="app-bar-row"><span>{name}</span><i style="--w:{pct}%"></i><b>{pct}%</b></div>' for name,pct in [('Google Maps',62),('Google Jobs',23),('LinkedIn Jobs',15)])
    activity = ''.join(f'<li>{icon(ic)}<span>{text}</span><small>{when}</small></li>' for ic,text,when in [('message','WhatsApp message delivered to Oakfield Suites','2 min'),('phone','AI call completed — demo booked','14 min'),('search','42 new leads found in Gurugram','1 h')])
    return f'<div class="app-view" data-view="dashboard" hidden><div class="app-view-head"><div><h3>Good evening, Vishal.</h3><p>Here is your sales workspace today.</p></div><span class="app-badge">Sample numbers</span></div><div class="app-stats">{stats}</div><div class="app-two"><div class="app-panel"><h4>Lead sources</h4>{sources}</div><div class="app-panel"><h4>Recent activity</h4><ul class="app-activity">{activity}</ul></div></div></div>'

def app_view_candidates():
    rows = ''.join(f'<tr><td><span class="initial">{n[0]}</span><span><b>{n}</b><small>{r}</small></span></td><td>{c}</td><td><span class="app-pill">{st}</span></td></tr>' for n,r,c,st in [('Aarav Mehta','Security supervisor','Noida','Shortlisted'),('Priya Nair','Front office executive','Gurugram','Interview'),('Rohit Verma','Housekeeping lead','Delhi','New')])
    return f'<div class="app-view" data-view="candidates" hidden><div class="app-view-head"><div><h3>Candidate DB</h3><p>Every applicant, organised by role and stage.</p></div><span class="app-badge">Fictional people</span></div><div class="table-scroll" tabindex="0" role="region" aria-label="Sample candidates"><table class="lead-table app-table"><thead><tr><th scope="col">Candidate</th><th scope="col">City</th><th scope="col">Stage</th></tr></thead><tbody>{rows}</tbody></table></div></div>'

def app_view_analytics():
    bars = ''.join(f'<div class="app-col"><i style="--h:{h}%"></i><span>{d}</span></div>' for d,h in [('Mon',42),('Tue',58),('Wed',51),('Thu',74),('Fri',88),('Sat',63),('Sun',35)])
    return f'<div class="app-view" data-view="analytics" hidden><div class="app-view-head"><div><h3>Analytics</h3><p>New leads found each day this week.</p></div><span class="app-badge">Sample numbers</span></div><div class="app-panel app-chart">{bars}</div></div>'

def app_view_settings():
    rows = ''.join(f'<label class="app-setting"><span><b>{t}</b><small>{d}</small></span><input type="checkbox" disabled{" checked" if on else ""}><i aria-hidden="true"></i></label>' for t,d,on in [('Hindi & English voice','Your assistant speaks and listens in both languages.',True),('Review before sending','Every message waits for your approval.',True),('Daily summary email','A short report of yesterday’s work.',False)])
    return f'<div class="app-view" data-view="settings" hidden><div class="app-view-head"><div><h3>Settings</h3><p>Shown for preview — change these inside the app.</p></div><span class="app-badge">Preview only</span></div><div class="app-panel">{rows}</div></div>'

def workspace():
    labels = [('leads','Find leads',lead_pane()),('draft','Prepare outreach',draft_pane()),('crm','Track in CRM',crm_pane()),('followup','Follow up',followup_pane())]
    tabs = ''.join(f'<button id="workflow-tab-{key}" type="button" data-tab="{key}" aria-selected="{str(i==0).lower()}">{label}</button>' for i,(key,label,_) in enumerate(labels))
    panels = ''.join(f'<div id="workflow-panel-{key}" class="demo-pane" data-panel="{key}"{(" hidden" if i else "")}>{body}</div>' for i,(key,_,body) in enumerate(labels))
    workflow = f'<div class="app-view demo-body" data-view="workflow" data-tabs><div class="demo-heading"><div><h3>From a lead to a next step.</h3><p>A small tour of your everyday workspace.</p></div>{icon("assistant")}</div><div class="demo-tabs" data-tablist aria-label="Business workflow">{tabs}</div>{panels}<span class="sr-only" data-tab-status aria-live="polite"></span></div>'
    nav = (app_nav('grid','Dashboard',view='dashboard')
        + '<span class="app-nav-group">Data Hub</span>'
        + app_nav('search','All Leads',tab='leads',current=True) + app_nav('people','Candidate DB',view='candidates') + app_nav('chart','Analytics',view='analytics')
        + '<span class="app-nav-group">Automation</span>'
        + app_nav('zap','Run Agent',tab='leads') + app_nav('mail','Email Auto',tab='draft') + app_nav('message','WhatsApp Auto',tab='draft') + app_nav('crm','CRM',tab='crm') + app_nav('calendar','Follow-ups',tab='followup')
        + '<span class="app-nav-group">System</span>'
        + app_nav('settings','Settings',view='settings'))
    return f'''<div class="demo-frame app-window" data-app-shell><div class="demo-bar app-titlebar"><div class="demo-bar-label"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><button type="button" class="app-icon-button" data-app-collapse aria-controls="workspace-sidebar" aria-expanded="true" aria-label="Collapse sidebar" data-js-control>{icon("sidebar")}</button>{logo(18)}Rudra24 AI <span aria-hidden="true">/</span> <span data-app-crumb>All Leads</span></div><div class="app-titlebar-tools"><span class="app-tool">{icon("clock")}History</span><span class="app-tool">{icon("book")}Manual</span><button type="button" class="app-run" data-tab-target="leads" data-js-control>{icon("zap")}Run Agent</button></div></div><div class="demo-shell app-shell-body"><aside id="workspace-sidebar" class="app-sidebar" aria-label="App navigation (preview)"><nav class="app-side-nav">{nav}</nav><div class="app-side-foot">{icon("connect")}<span>Connected tools</span></div></aside><div class="app-main">{workflow}{app_view_dashboard()}{app_view_candidates()}{app_view_analytics()}{app_view_settings()}</div></div></div>'''

def standalone_preview(title, desc, pane, label):
    return frame(f'<div class="demo-body"><div class="demo-heading"><div><h3>{title}</h3><p>{desc}</p></div>{icon("assistant")}</div>{pane}</div>',label)

ASSISTANT_CHAT = [
    # A fictional chat the assistant window plays on a loop: English first, then Hinglish — Rudra answers in the same language.
    ('you', 'Find 20 hotel leads in Gurugram.'),
    ('rudra', 'Done — 20 hotels in Gurugram, 14 with a phone number. They are saved in your Data Hub.'),
    ('you', 'Inke liye ek WhatsApp intro likho.'),
    ('rudra', 'Ye raha draft: “Namaste! Hum hotels ko trained security aur housekeeping staff dete hain.” Bhejne se pehle ek baar check kar lijiye.'),
    ('you', 'Kal 11 baje follow-up yaad dila dena.'),
    ('rudra', 'Ho gaya — kal subah 11 baje ka follow-up CRM me add kar diya.'),
]

def assistant_preview():
    """The assistant window: the app's orb on the left, a short chat that plays itself on the right (site.js)."""
    bubbles = ''.join(f'<div class="chat-msg {who}"><span class="chat-who">{"You" if who == "you" else "Rudra"}</span><p>{text}</p></div>' for who, text in ASSISTANT_CHAT)
    return f'''<div class="demo-frame assistant-window" data-assistant-demo data-state="idle"><div class="demo-bar"><div class="demo-bar-label"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span>{logo(18)}Rudra24 AI <span aria-hidden="true">/</span> AI assistant</div><div class="assistant-bar-tools"><button type="button" class="assistant-sound" data-assistant-sound aria-pressed="true" data-js-control>{icon('sound','is-on')}{icon('muted','is-off')}<span data-assistant-sound-label>Tap for sound</span></button><span class="sample-label">Fictional demo data</span></div></div><div class="assistant-body"><div class="assistant-stage"><div class="assistant-orb-wrap"><div class="assistant-orb" data-assistant-orb role="img" aria-label="Rudra, the Rudra24 AI assistant" tabindex="-1"></div></div><p class="assistant-state"><i aria-hidden="true"></i><span data-assistant-state>Ready when you are</span></p><p class="assistant-langs">Hindi · English · Hinglish</p></div><div class="assistant-chat"><div class="assistant-thread" data-assistant-thread>{bubbles}</div><div class="assistant-composer" aria-hidden="true"><span class="composer-field"><span class="composer-typed" data-assistant-typing></span><span class="composer-placeholder">Ask Rudra in Hindi or English…</span></span><span class="composer-mic">{icon('mic')}</span><span class="composer-send">{icon('send')}</span></div></div></div></div>'''

def cards(items):
    html = ''
    categories = {'search':'Lead generation','crm':'CRM & follow-ups','phone':'AI voice calling','message':'WhatsApp & email','assistant':'AI assistant','people':'AI assistant'}
    for i,(ico,title,desc,href,label) in enumerate(items):
        clip = ['leads','crm','calling','outreach','assistant'][i]
        key = ['leads','crm','calling','outreach','assistant'][i]
        html += experience_card(key, ico, title, desc, href, i, clip, categories.get(ico,'Product'))
    return '<div class="feature-grid">'+html+'</div>'

def demo_field(label, name, options=None, value='', kind='text'):
    if options:
        control = '<select name="'+name+'">'+''.join(f'<option>{escape(item)}</option>' for item in options)+'</select>'
    elif kind == 'textarea':
        control = f'<textarea name="{name}" required maxlength="600" rows="3">{escape(value)}</textarea>'
    else:
        bounds = ' min="1" max="20" step="1"' if kind=='number' else ' maxlength="100"'
        control = f'<input type="{kind}" name="{name}" value="{escape(value)}" required{bounds}>'
    return f'<label><span>{label}</span>{control}</label>'

def experience_pane(key):
    if key=='crm': return crm_pane()
    if key=='outreach': return draft_pane()
    if key in ['leads','client','candidates']:
        candidate = key=='candidates'
        fields = demo_field('Your request · review the search settings below','request',value='Find 3 hotel leads in Sector 29, Gurugram.',kind='textarea') if key=='client' else ''
        fields += demo_field('Role' if candidate else 'Industry','industry', ['Security guards','Housekeeping staff','Office staff'] if candidate else ['Hotels & Hospitality','Hospitals & Healthcare','IT Parks & Tech','Banks & Corporate','Factories & Manufacturing','Warehouses & Logistics','Schools & Colleges','Residential Societies'])
        fields += demo_field('City','city',['Gurugram','Delhi','Noida','Mumbai','Bengaluru','Jaipur'])+demo_field('Locality','area',value='Sector 29')+demo_field('Requested count · 1–20 in this demo','count',value='3',kind='number')
        if not candidate: fields += demo_field('Source','source',['Google Maps','Google Jobs','LinkedIn Jobs'])
        action = 'Find sample candidates' if candidate else 'Generate sample leads'
        intro = '<div class="demo-request">Start with your request, then confirm the search settings.<br><small>This sample search uses the settings you choose below.</small></div>' if key=='client' else ''
        return intro+f'<form data-experience="{key}" class="experience-form"><fieldset disabled data-experience-fields><div class="experience-fields">{fields}</div><div class="actions"><button class="button" type="submit">{action}{icon("arrow")}</button><button class="button secondary" type="button" data-search-stop hidden>Stop search</button></div></fieldset><p role="status" data-experience-status>Choose your search. All results here are fictional.</p><div data-experience-results></div><button type="button" class="button secondary" data-demo-export hidden>Export these samples</button><button type="button" class="button secondary" data-demo-save hidden>Add samples to CRM</button></form>'
    if key in ['data','dashboard','reports']:
        return f'<div data-data-view="{key}"><div class="experience-metrics"><div><b data-total-leads>3</b><span>Sample leads</span></div><div><b data-total-crm>1</b><span>CRM records</span></div><div><b data-total-tasks>0</b><span>Planned follow-ups</span></div></div><p>Run a sample search or save a follow-up in another card. Your demo overview updates here.</p><label class="experience-filter">View records<select data-data-filter><option>All records</option><option>CRM records</option><option>Candidate records</option></select></label><div data-data-results></div><button class="button secondary" type="button" data-data-export>Export visible samples</button><p data-data-status role="status">Fictional records, kept only for this visit.</p></div>'
    definitions = {
        'assistant': ('Prepare a plan', [demo_field('What do you need help with?','request',value='Help me introduce our housekeeping services to a hotel.',kind='textarea')]),
        'voice': ('Preview a conversation', [demo_field('Language','language',['English','Hindi']),demo_field('Conversation goal','request',value='Introduce our housekeeping services',kind='textarea')]),
        'calling': ('Prepare a call script', [demo_field('Company name','company',value='Example Service Team'),demo_field('Business to contact','recipient',value='Oakfield Suites'),demo_field('Service','service',value='Housekeeping support'),demo_field('Language','language',['English','Hindi'])]),
        'email': ('Prepare email draft', [demo_field('From business','company',value='Example Service Team'),demo_field('Recipient business','recipient',value='Oakfield Suites'),demo_field('Service','service',value='Housekeeping support')]),
        'whatsapp': ('Prepare WhatsApp draft', [demo_field('From business','company',value='Example Service Team'),demo_field('Recipient business','recipient',value='Oakfield Suites'),demo_field('Service','service',value='Security staffing')]),
        'sms': ('Prepare SMS draft', [demo_field('From business','company',value='Example Service Team'),demo_field('Recipient business','recipient',value='Oakfield Suites'),demo_field('Service','service',value='Housekeeping support')]),
        'calendar': ('Save sample follow-up', [demo_field('Customer','recipient',value='Oakfield Suites'),demo_field('Date','date',value='2026-10-20',kind='date'),demo_field('Time','time',value='11:00',kind='time'),demo_field('Next step','request',value='Review the company introduction',kind='textarea')]),
        'contracts': ('Save sample contract', [demo_field('Client','recipient',value='Oakfield Suites'),demo_field('Service','service',value='Housekeeping support'),demo_field('Renewal date','date',value='2027-01-20',kind='date')]),
        'settings': ('Apply to this preview', [demo_field('Company name','company',value='Example Service Team'),demo_field('Services','service',value='Security and housekeeping'),demo_field('Language','language',['English','Hindi'])]),
        'accounts': ('Preview account setup', [demo_field('Account','provider',['Gmail','Google Sheets','Google Calendar','WhatsApp']),demo_field('Workflow','request',['Email drafts','Spreadsheet exports','Meeting reminders','WhatsApp preparation'])]),
        'connectors': ('Preview connection checklist', [demo_field('Connection','provider',['Google Workspace','WhatsApp','Voice provider','AI provider'])]),
        'plugins': ('Preview workflow setup', [demo_field('Workflow','provider',['Google Sheets sync','Email automation','Calling integration'])]),
        'keys': ('Show provider requirements', [demo_field('Provider type','provider',['AI provider','Lead sourcing','Voice and telephony'])]),
    }
    action, fields = definitions[key]
    return f'<form class="experience-form" data-experience="{key}"><fieldset disabled data-experience-fields><div class="experience-fields">{"".join(fields)}</div><button class="button" type="submit">{action}{icon("arrow")}</button></fieldset><p data-experience-status role="status">Try the form. This preview does not send messages, connect accounts or make calls.</p><div data-experience-results></div></form>'

HOW = {
    'leads':'Choose the industry, city, locality, source and number of leads. Run the search, open a result, then export it or add it to the sample CRM. Stop keeps the results already returned.',
    'client':'Start with a plain-language request. Review the industry and area, choose the count, and run the sample search. The real Client AI uses your configured AI and sourcing providers.',
    'crm':'Move the enquiry from New to Contacted to Follow-up. In the app, add customer notes, record what actually happened and plan the next activity.',
    'outreach':'Switch between email, WhatsApp and a call script. Review the introduction before using it. The app needs a configured sender or calling provider for delivery.',
    'assistant':'Describe the task in your own words. Review the suggested steps and keep useful company context, memory and tasks together. This demo uses prepared responses.',
    'voice':'Choose a language and a goal to read an example conversation. In the app, voice requires a provider and microphone permission. This website does not record audio.',
    'calling':'Enter your company, the customer and your service. Prepare a script and review the opening. Real calling also needs a backend, credentials and a telephony connection.',
    'candidates':'Choose the role and location, then run the sample search. Open a candidate to review the fictional record. Real recruitment results need review and a sourcing setup.',
    'data':'Review your sample leads and CRM records. Filter the list and export a CSV. In the app, the Data Hub also includes the candidate database and Excel manager.',
    'dashboard':'Use the overview to see your lead and follow-up totals. Choose a record view to inspect the data behind the numbers.',
    'reports':'Review recorded work, then inspect the records behind a total. These demo totals come from your actions here; they are not business performance claims.',
    'email':'Enter the business and service, then prepare an editable email draft. Review it before sending through your configured email account in the app.',
    'whatsapp':'Prepare an introduction for a reviewed contact. Edit the draft and check the details. The website prepares text only; real sending needs the app’s account setup.',
    'sms':'Prepare a short service introduction. Review the text and recipient in the app before sending through a configured messaging provider.',
    'calendar':'Choose the customer, date, time and next step. Save a sample reminder. The app can use a connected calendar after the meeting details are confirmed.',
    'contracts':'Keep a confirmed client’s service and renewal date together. Save a sample record here. This preview does not create a legal agreement.',
    'settings':'Set the company context used by this preview. In the app, review company details, language, appearance and provider settings in Settings.',
    'accounts':'Select an account and the work it supports. Review the setup steps. Real accounts are connected inside the app; this demo does not ask for sign-in.',
    'connectors':'Choose a connection to see what it needs and what it supports. Review permissions before connecting an account in the app.',
    'plugins':'Choose a workflow to see its setup requirements. Use the app’s configured integration; this website does not install anything.',
    'keys':'Choose a provider type to understand the setup. API credentials belong in the app’s authenticated settings. Do not enter any secret on this demo website.',
}

def experience_card(key, ico, title, desc, href, index, clip='', category='Product'):
    hover = f' data-feature-clip="{clip}"' if clip else ''
    return f'''<details class="feature-card experience-card reveal" data-experience-card="{key}"><summary{hover}><span class="card-top"><span class="card-category">{icon(ico)}{category}</span><span class="card-index">{index+1:02}</span></span><span class="card-title">{title}</span><span class="card-description">{desc}</span><span class="card-open">Try this feature {icon('chevron')}</span></summary><div class="feature-content"><div class="feature-instructions"><span class="eyebrow">How to use it</span><h3>See the next step.</h3><p>{HOW[key]}</p>{link('Read the full feature guide',href)}<p class="setup-note">Interactive demo · Fictional data. Nothing is sent or called.</p></div><div class="experience-shell"><div class="experience-rail"><span class="window-dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="rail-brand">{logo(20)}Rudra24 AI</span><span class="rail-tab">{icon(ico)}{category}</span><span class="rail-status">Demo · fictional data</span></div><div class="experience-workspace"><p class="workspace-kicker">Rudra24 AI · {category}</p><h4>{category}</h4>{experience_pane(key)}</div></div></div></details>'''

def experience_directory():
    entries = [
        ('client','message','Client AI (Chat)','Turn your request into a focused lead search.','lead-generation.html','leads'),
        ('voice','mic','Voice Calling AI','Preview a Hindi or English conversation.','outreach.html#calling','calling'),
        ('calling','phone','Voice Calling','Prepare a script and understand calling setup.','outreach.html#calling','calling'),
        ('candidates','people','Candidate AI','Research a role and build a sample shortlist.','recruitment.html',''),
        ('crm','crm','CRM & pipeline','Move a record and keep its next step visible.','crm.html','crm'),
        ('calendar','calendar','Follow-ups & meetings','Save a customer reminder with a date and time.','crm.html',''),
        ('contracts','file','Clients & contracts','Keep the service and renewal date together.','crm.html#contracts',''),
        ('reports','chart','Reports','See the records behind your demo totals.','crm.html#reports',''),
        ('dashboard','chart','Dashboard','Review leads, CRM records and planned follow-ups.','product.html',''),
        ('data','memory','Data Hub & exports','Filter records and download your sample CSV.','lead-generation.html#exports',''),
        ('leads','search','Run Agent','Choose industry, area, source and exact count.','lead-generation.html','leads'),
        ('email','mail','Email Auto','Prepare and edit a business introduction.','outreach.html','outreach'),
        ('whatsapp','message','WhatsApp Auto','Prepare a short message for a reviewed contact.','outreach.html','outreach'),
        ('sms','message','Text messages','Prepare a concise service introduction.','outreach.html',''),
        ('assistant','assistant','AI assistant & memory','Describe a task and review a prepared plan.','product.html#assistant','assistant'),
        ('accounts','connect','Accounts','Understand the account setup for your workflow.','product.html#integrations',''),
        ('connectors','connect','Connectors','See connection requirements before you start.','product.html#integrations',''),
        ('plugins','connect','Plugins','Explore how integrations support your work.','product.html#integrations',''),
        ('keys','shield','API keys & providers','Understand the providers your setup needs.','product.html#integrations',''),
        ('settings','task','Settings & company','Set the context used in this visit’s demo.','product.html',''),
    ]
    return '<div class="feature-grid experience-directory">'+''.join(experience_card(key,ico,title,desc,href,i,clip,title) for i,(key,ico,title,desc,href,clip) in enumerate(entries))+'</div>'

def benefits(items):
    return '<div class="wrap benefit-strip">'+''.join(f'<div>{icon(ico)}<h3>{title}</h3><p>{desc}</p></div>' for ico,title,desc in items)+'</div>'

def detail_section(kicker,title,desc,items,anchor=''):
    blocks = ''.join(f'<article>{icon(ico)}<h3>{heading}</h3><p>{copy}</p></article>' for ico,heading,copy in items)
    return f'<section class="section"{(" id=\""+anchor+"\"" if anchor else "")}><div class="wrap detail-grid"><div class="reveal"><span class="eyebrow">{kicker}</span><h2>{title}</h2><p class="subcopy">{desc}</p></div><div class="detail-blocks reveal">{blocks}</div></div></section>'

def related(items):
    content = ''.join(f'<a href="{href}"><h3>{title}</h3><p>{desc}</p>{icon("arrow")}</a>' for href,title,desc in items)
    return f'<section class="section rule"><div class="wrap"><div class="section-head reveal"><h2>Keep it<br><em>connected.</em></h2><p>Explore the next part of the workflow.</p></div><div class="related-links reveal">{content}</div></div></section>'

def steps_section(items, title='Three steps <em>from search to client.</em>', label='How it works', definition='Ask for what you need, review what comes back and choose the next step. You stay in control.', num=''):
    content = points(items)
    return f'<section class="section rule" id="walkthrough"><div class="wrap">{head(label, title, definition, num=num)}{content}</div></section>'

def film_player():
    return '''<video id="launch-film" tabindex="0" muted loop controls playsinline preload="none" poster="assets/video/launch-mobile-poster.jpg" width="1920" height="1080" aria-label="Rudra24 AI launch film. Click or press Enter to toggle sound." aria-describedby="film-hint"><source src="assets/video/launch-mobile.mp4#t=19.5" media="(max-width: 760px)" type="video/mp4"><source src="assets/video/launch-film.mp4#t=19.5" type="video/mp4"><p>Your browser cannot play this film. <a href="assets/video/launch-film.mp4">Open the MP4</a>.</p></video><div class="film-caption"><span id="film-hint">The workspace in action · Hover for sound</span><div class="film-actions"><button type="button" data-film-expand data-js-control>Expand film</button><button type="button" data-film-toggle data-js-control>Pause video</button></div></div><dialog class="film-dialog" aria-label="Full-size launch film"><button type="button" data-film-close class="button secondary">Close full-size view</button><div data-film-slot></div><p>Use the player controls for full screen on your phone. Tap the video to enable sound.</p></dialog><p class="film-status" data-film-status role="status" hidden></p><a href="assets/video/launch-film.mp4" class="film-error-link" target="_blank" rel="noopener noreferrer" data-film-fallback hidden>Open the launch film directly</a>'''

def home():
    features = [('search','Find businesses that need your service.','Choose an industry and an area. Get a scored list of companies with contacts and a map — ready to call.','lead-generation.html','Explore lead generation'),('crm','Know every client and what comes next.','Clients, conversations and follow-ups live together, so no deal is forgotten and every client has a clear next step.','crm.html','Explore the CRM'),('phone','An AI caller that speaks Hindi and English.','Set up your calling agent once — name, voice and your business. Connect your calling provider and it works through your list.','outreach.html#calling','Explore voice calling'),('message','Personal messages you approve before sending.','A tailored WhatsApp message or email for every lead, with your brochure attached. Nothing goes out until you say so.','outreach.html','Explore outreach'),('assistant','Ask in Hindi or English. Get work started.','Ask for leads, a follow-up message or candidates. Your assistant prepares it and keeps it in your data hub.','product.html','Explore the workspace')]
    return f'''<section class="hero launch-hero landing-centered"><div class="wrap launch-grid"><div class="launch-copy"><span class="eyebrow hero-title">Rudra24 AI · Your business workspace</span><h1 class="hero-title">From first lead<br><span>to <em>lasting client.</em></span></h1><p class="subcopy hero-copy">Find the right businesses, start better conversations and keep every follow-up in one workspace.</p><div class="actions hero-copy">{wa('Talk to us')}{link('Watch demo','#film','button secondary')}</div><p class="hero-note hero-copy">For small businesses, service teams and growing agencies.</p></div><div class="launch-media hero-preview" id="film">{film_player()}</div></div></section>
    <nav class="wrap chapter-nav" aria-label="On this page"><a href="#film-summary">{icon('grid')}Features</a><a href="#workspace">{icon('sidebar')}Live preview</a><a href="#lead-map">{icon('pin')}Lead map</a><a href="#assistant-home">{icon('assistant')}AI assistant</a><a href="#walkthrough">{icon('task')}How it works</a><a href="#use-cases-home">{icon('people')}Use cases</a><a href="#questions">{icon('message')}Questions</a></nav>
    <section class="section" id="film-summary"><div class="wrap">{head('Features','Find, call, message and track — <em>in one app.</em>','Five tools your team uses every day. Open any card to try it with sample data.', num='01')}{cards(features)}<div class="actions">{link('Try every app tab','product.html#walkthrough','button secondary')}</div></div></section>
    <section class="section workspace-tour" id="workspace"><div class="wrap">{head('Live app preview','Try the app <em>right here.</em>','A working copy of Rudra24 AI. Click the sidebar and the tabs to follow one lead from search to follow-up.', num='02')}<div class="reveal">{workspace()}<div class="below-demo"><span>{icon('check')}Choose a tab to explore each step.</span><span>Fictional demo data. No messages or calls.</span></div></div>{points([('Same layout as the app','Dashboard, Data Hub, Automation and System — the sidebar you see after signing in. Collapse it with the button in the title bar.'),('One lead, start to finish','Find a business, prepare an email or WhatsApp draft, move it through the CRM and plan the follow-up.'),('Safe to explore','Every record here is fictional. Nothing on this page sends a message, makes a call or saves your data.')])}</div></section>
    {lead_map_section()}
    <section class="section assistant-story" id="assistant-home"><div class="wrap">{head('AI assistant','Just ask — <em>in Hindi or English.</em>','Your assistant prepares messages, finds businesses and starts tasks, using what is already in your workspace.', num='04')}<div class="split"><div class="reveal">{points([('Hindi and English','Speak or type the way you talk. The assistant answers in the same language.'),('Knows your workspace','It works with your leads, CRM records and drafts, so you never repeat yourself.'),('Starts the task','Ask for leads, a message or a follow-up — it prepares the next step for you to review.')], 'points-stack')}<div class="actions">{link('Meet your assistant','product.html#assistant','button secondary')}</div></div><div class="reveal">{assistant_preview()}</div></div></div></section>
    {steps_section([('Tell it what you need.','Choose the industry, location and task. Start with a plain-language request.'),('Review the useful details.','Look through company records, candidate results or prepared drafts. Keep what fits.'),('Choose the next step.','Prepare outreach, add a follow-up or export the results. You stay in control.')], num='05')}
    <section class="section rule" id="use-cases-home"><div class="wrap">{head('Use cases','Made for teams <em>that sell services.</em>','Service businesses, agencies and staffing teams use Rudra24 AI from the first lead to the signed client.', link('See all use cases','use-cases.html'), num='06')}<article class="usecase-row reveal"><div><h3>For service businesses.</h3><p>Your next customer and your next conversation, connected.</p></div><div><p>Find businesses in your area, prepare a relevant introduction and keep the follow-up with the customer record.</p><div class="workflow"><span>Find a lead</span>{icon('arrow')}<span>Prepare outreach</span>{icon('arrow')}<span>Track the next step</span></div></div></article><article class="usecase-row reveal"><div><h3>For agencies and staffing teams.</h3><p>Keep client opportunities and candidate research organised.</p></div><div><p>Research hotels, hospitals and offices, organise potential client conversations and build a candidate shortlist.</p><div class="workflow"><span>Research clients</span>{icon('arrow')}<span>Shortlist people</span>{icon('arrow')}<span>Keep work organised</span></div></div></article></div></section>
    {faq([('What does Rudra24 AI bring together?','Lead research, your AI assistant, recruitment, CRM, exports and outreach preparation. Connected accounts and providers enable additional workflows.'),('Can I use Hindi and English?','The assistant includes Hindi and English voice workflows. Voice availability depends on the selected provider, microphone permissions and account setup.'),('Does this website make calls or send messages?','No. The interactive previews use fictional examples. Real calling and messaging happen in the app after the required provider and account setup.'),('How do I see what fits my business?','Talk to us on WhatsApp. Tell us your industry and the work you want to simplify, and ask for a walkthrough of the relevant features.')], num='07')}{closing()}'''

def product():
    grid = experience_directory()
    return f'''{page_hero('The product','One workspace.<br><em>A little less work.</em>','The assistant, the customer record and the next follow-up, all close at hand. Rudra24 AI brings the working day together.',center=True)}
    <div class="wrap page-preview hero-preview compact-demo">{workspace()}<p class="preview-caption">Explore a sample workflow. All records shown here are fictional.</p></div>
    {benefits([('assistant','Ask in plain language','Start with the work, not a complicated menu.'),('connect','Bring useful tools together','Connect the accounts your workflow needs.'),('task','Keep context close','Research, drafts and next steps stay easier to find.')])}
    <section class="section" id="assistant"><div class="wrap split"><div class="reveal"><span class="eyebrow">Your everyday assistant</span><h2>Talk it through.<br><em>Put it to work.</em></h2><p class="subcopy">Ask a business question, prepare a message, or start lead research. The assistant gives your request a clear place to begin.</p><ul class="quiet-list"><li>{icon('mic')}Hindi-English voice and text conversations</li><li>{icon('memory')}Saved business context and conversation history</li><li>{icon('task')}Task progress, results and next steps</li></ul><p class="setup-note">Voice needs a configured provider and microphone permission. Saved memory can be reviewed and managed in the app.</p></div><div class="reveal">{assistant_preview()}</div></div></section>
    <section class="section rule" id="walkthrough"><div class="wrap"><div class="section-head reveal"><h2>The whole picture.<br><em>Without the clutter.</em></h2><p>Open a card to try its form, review a sample result and see how that part of the app works.</p></div>{grid}</div></section>
    <section class="section soft-section" id="integrations"><div class="wrap split"><div class="reveal"><span class="eyebrow">Connected tools</span><h2>Your tools.<br><em>In the same conversation.</em></h2><p class="subcopy">Bring account-based workflows into the app. Your email, spreadsheet, calendar and communication setup determines what you can use.</p></div><div class="reveal"><h3>Connections that support the work.</h3><div class="integration-list"><span>Google Gmail</span><span>Google Sheets</span><span>Google Calendar</span><span>WhatsApp</span><span>Voice providers</span><span>AI providers</span></div><p class="setup-note">Some connections require sign-in, provider credentials, approvals or paid usage. Ask us to walk you through your setup. Phone calls need a configured backend and telephony connection.</p></div></div></section>{closing()}'''

def leads():
    return f'''{page_hero('Lead generation','Find the right businesses.<br><em>Start there.</em>','Research leads by industry and location. Review the details, keep useful records and give your next conversation a better starting point.',topic='lead generation')}
    <div class="wrap page-preview compact-demo hero-preview">{standalone_preview('A useful place to begin.','Choose your search and try the process.', '<div class="experience-workspace">'+experience_pane('leads')+'</div>','Run Agent')}<p class="preview-caption">Fictional companies and sample areas. This is a preview, not a live search.</p></div>
    {benefits([('pin','Keep the location precise','Research the area you actually want to cover.'),('search','Choose the scope','Specify your industry and requested lead count.'),('download','Use the results','Save, organise or export the useful records.')])}
    {detail_section('From a request to a record','A clearer search.<br><em>A more useful result.</em>','Start with what your business needs. The app keeps the request and the results connected.',[('search','Industry and area','Look for hotels, hospitals, offices and other business categories in your selected location.'),('people','The count you asked for','Set how many leads you want. When fewer are available, review the actual returned results.'),('file','Company and contact context','Review business details and contact sources. Website enrichment can help fill gaps when information is available.'),('pin','Company information on maps','Keep the location in view while reviewing a business and planning your coverage.')])}
    {steps_section([('Make a focused request.','For example: find hotel leads in Delhi for a housekeeping introduction.'),('Review the returned records.','Check the company, location and available contact details. Keep useful results and review missing information.'),('Take the work forward.','Save records, prepare outreach, add CRM follow-ups or export your list.')])}
    <section class="section soft-section" id="exports"><div class="wrap split"><div class="reveal"><span class="eyebrow">Your data, ready to use</span><h2>Keep it in the app.<br><em>Or take it with you.</em></h2><p class="subcopy">Use the lead database to organise your records. Export to Excel or CSV, or use Google Sheets with a configured connection.</p><ul class="quiet-list"><li>{icon('download')}Excel and CSV exports</li><li>{icon('connect')}Google Sheets sync with account setup</li><li>{icon('task')}Partial results remain useful when a search stops</li></ul></div><div class="reveal"><div class="note-card">{icon('file')}<h4>From research<br>to your next task.</h4><p>Company · Category · Area · Contact source<br>A list that your team can review and work with.</p><small>Contact availability varies by source.</small></div></div></div></section>
    {faq([('Will every business have a phone number?','No. Public contact availability varies. Review the source and use website enrichment where available; a missing contact should stay missing until there is a real source.'),('What happens if I stop a search?','The app can retain returned partial results for preview and export. The number available depends on what the search returned before it stopped.'),('Can I move a lead into the CRM?','Yes. The CRM keeps lead records, activities and next steps together. Review the record and choose the workflow you want to start.')])}
    {related([('outreach.html','Prepare the introduction','Put relevant company information into a clear first message.'),('crm.html','Keep the follow-up','Give the useful lead a record and a next step.'),('use-cases.html','See a working example','Explore a client-research workflow for your business.')])}{closing('lead research')}'''

def crm():
    return f'''{page_hero('CRM & follow-ups','Every conversation.<br><em>A clear next step.</em>','Customer records, notes, deal stages and reminders, kept together. Spend less time remembering where the conversation left off.',topic='CRM and follow-ups')}
    <div class="wrap page-preview compact-demo hero-preview">{standalone_preview('A pipeline you can follow.','Move the sample enquiry through its next steps.',crm_pane(),'CRM pipeline')}<p class="preview-caption">A fictional enquiry. Moving a sample card does not contact anyone.</p></div>
    {benefits([('crm','A place for each record','Customer details and deal stages stay together.'),('clock','A visible next step','Keep notes, activities and follow-ups with the lead.'),('chart','Review what happened','Reports draw on the records and activities you enter.')])}
    {detail_section('Customer context','The details matter.<br><em>Keep them close.</em>','A pipeline is useful when the story behind each record is easy to find.',[('people','Customer records','Keep company details, conversation notes and recorded outcomes with the customer.'),('crm','Deal stages','Move an enquiry through your pipeline as its status changes. Record what actually happened.'),('task','Activities and follow-ups','Track attempts, replies and the next action. Give the follow-up a clear owner and place.'),('calendar','Meetings and calendars','Save confirmed meeting details. Calendar and meeting-email actions need connected accounts.')])}
    {steps_section([('Bring in the record.','Start from a useful lead or a customer record you want to organise.'),('Record the conversation.','Add the channel, notes and actual outcome. Review suggestions before saving them.'),('Choose the next action.','Set a follow-up, confirm a meeting or update the pipeline when the status changes.')])}
    <section class="section soft-section" id="contracts"><div class="wrap split"><div class="reveal"><span class="eyebrow">Clients & contracts</span><h2>After the first yes.<br><em>Keep the work in view.</em></h2><p class="subcopy">Keep confirmed clients, contract details and renewal dates organised. A won deal becomes a relationship worth keeping track of.</p></div><div class="reveal"><div class="note-card">{icon('file')}<h4>A client record.<br>A contract. A renewal.</h4><p>Keep the dates and details your team enters in a dedicated client and contract workspace.</p><small>Confirmed outcomes, recorded by your team.</small></div></div></div></section>
    {detail_section('Reports & overview','See the progress.<br><em>Understand the context.</em>','Review pipeline and activity data without separating the numbers from the records behind them.',[('chart','Interactive reports','Open the records behind supported report views and explore the period you need.'),('file','Business outcomes','Review confirmed clients, contract information and recorded outcomes.'),('task','Activity history','Keep the trail of follow-ups and updates available for your team.'),('clock','Renewal states','Review contract dates and renewals using the information entered in the app.')],anchor='reports')}
    {related([('lead-generation.html','Start with useful leads','Bring new business opportunities into the workspace.'),('outreach.html','Continue the conversation','Prepare outreach with the customer context nearby.'),('use-cases.html','See the complete workflow','Explore a small-team sales workflow.')])}{closing('CRM and customer follow-ups')}'''

def outreach():
    return f'''{page_hero('Outreach & calling','A thoughtful first hello.<br><em>A better follow-up.</em>','Prepare an introduction that makes sense for the business you are contacting. Keep the message, the conversation and the next step connected.',topic='outreach and calling')}
    <div class="wrap page-preview compact-demo hero-preview">{standalone_preview('Make it relevant.','Try a sample email, WhatsApp draft or call script.',draft_pane(),'Outreach preparation')}<p class="preview-caption">Example drafts only. No message is sent and no call is made.</p></div>
    {benefits([('file','Prepare with context','Use the company information you have reviewed.'),('message','Choose the channel','Email, WhatsApp, SMS and calling have their own setup.'),('check','Review the next action','Keep message preparation separate from delivery.')])}
    {detail_section('A message with a purpose','The right words.<br><em>A clear reason to reach out.</em>','From a short introduction to a follow-up, start with the customer and the conversation you want to have.',[('mail','Email workflows','Prepare messages and work with connected email accounts. Account authorisation is required for sending.'),('message','WhatsApp tools','Prepare messages and use configured WhatsApp workflows. Cloud messaging needs an authorised business sender and the required Meta setup.'),('phone','Text messages','Prepare SMS communication and use the configured provider. Provider access and sending charges can apply.'),('file','Pitch documents','Keep company introductions and pitch documents close to your outreach workflow.')])}
    <section class="section soft-section" id="calling"><div class="wrap split"><div class="reveal"><span class="eyebrow">Voice & calling</span><h2>Prepare the conversation.<br><em>Then connect the setup.</em></h2><p class="subcopy">Use calling tools to configure an agent, organise its knowledge and prepare a script. Review supported recordings, transcripts and outcomes after a conversation.</p><p class="setup-note">Real calls require a configured backend, provider credentials and an active phone or SIP connection. An API key alone is not a working phone line. Provider availability and call charges vary.</p></div><div class="reveal"><div class="note-card">{icon('phone')}<h4>A better-prepared<br>conversation.</h4><p>Agent setup → Script and knowledge → Authorised calling connection → Conversation review</p><small>Calling features depend on your provider setup.</small></div></div></div></section>
    {steps_section([('Start from a reviewed record.','Use the business details that are relevant to your introduction.'),('Prepare and review the message.','Choose a channel, edit the draft and confirm the sender and account setup.'),('Record the actual outcome.','Keep the reply, call review or follow-up with the CRM record. Opening a chat does not prove delivery.')])}
    {faq([('Will the app send a message just because I drafted it?','Drafting and delivery are different steps. Review your message and use the authorised account workflow. Manual WhatsApp sharing still needs you to send and confirm the message.'),('What do I need for real calling?','A working backend, supported voice and telephony providers, credentials and a provisioned phone/SIP connection. We can walk you through the setup requirements.'),('Are provider calls and messages included for free?','Provider plans, quotas and usage charges vary. Ask for the current setup and costs before using paid calling or messaging.')])}
    {related([('crm.html','Keep the outcome','Save conversation notes and agree on a follow-up.'),('lead-generation.html','Find a relevant starting point','Research the businesses you want to reach.'),('contact.html','Discuss your setup','Talk through the channels your team needs.')])}{closing('outreach and calling setup')}'''

def candidates():
    people = [('A','A. Mehta','Security','Delhi','security'),('R','R. Shah','Housekeeping','Noida','housekeeping'),('S','S. Kumar','Supervisor','Gurugram','supervisor')]
    cards_ = ''.join(f'<article class="candidate-card" data-candidate-role="{role}"><span class="initial">{initial}</span><h4>{name}</h4><p>{title} · {area}</p><span class="candidate-tag">Sample candidate</span></article>' for initial,name,title,area,role in people)
    return f'<div data-candidate-demo><div class="channel-select" aria-label="Sample candidate role" data-js-control><button type="button" data-candidate-filter="all" aria-pressed="true">All roles</button><button type="button" data-candidate-filter="security" aria-pressed="false">Security</button><button type="button" data-candidate-filter="housekeeping" aria-pressed="false">Housekeeping</button></div><div class="candidate-list">{cards_}</div><div class="demo-bottom"><p data-candidate-status aria-live="polite">3 fictional candidates shown.</p><span class="sample-label">Review before contact</span></div></div>'

def recruitment():
    return f'''{page_hero('Recruitment','Find people.<br><em>Keep the process clear.</em>','Candidate research, a useful shortlist and organised records. Bring staffing work into the same workspace as your client opportunities.',topic='candidate research and recruitment')}
    <div class="wrap page-preview compact-demo hero-preview">{standalone_preview('A shortlist with a purpose.','Choose a role and try the search.', '<div class="experience-workspace">'+experience_pane('candidates')+'</div>','Candidate AI')}<p class="preview-caption">Invented records for demonstration. No personal candidate data is used.</p></div>
    {benefits([('search','Start with a focused request','Describe the role and location you need.'),('people','Review the candidates','Look through the returned records before contact.'),('download','Keep a usable shortlist','Organise candidate data and supported exports.')])}
    {detail_section('Staffing workflows','The right context.<br><em>For the next conversation.</em>','Keep candidate research clear and separate from a hiring decision.',[('assistant','Recruiter assistant','Start a candidate-research task with the role and location your agency needs.'),('people','Candidate database','Keep returned candidate records in a dedicated place for review.'),('search','Useful filters','Search and organise the available records to work through your shortlist.'),('download','Data exports','Use supported spreadsheet exports to keep recruitment records useful for your team.')])}
    {steps_section([('Describe your staffing need.','Specify the role, location and scope of the candidate search.'),('Review the available records.','Check the returned information. Research results are a starting point, not a hiring recommendation.'),('Build your next step.','Organise a shortlist and prepare the questions your team wants to ask.')])}
    {related([('lead-generation.html','Find client opportunities','Research the businesses your staffing team serves.'),('use-cases.html','See the agency workflow','Explore client and candidate research together.'),('contact.html','Discuss recruitment needs','Tell us the roles and locations your team covers.')])}{closing('staffing and recruitment')}'''

CASES = [
    ('services','Service businesses','Find the next customer. Keep the next step.','For teams offering business services, a useful lead is only the beginning. Keep the research, introduction and follow-up in one workflow.','A reviewed business list and a clear follow-up, ready for your team.', [('Research your area.','Choose the industry, location and lead count that fit your service.'),('Prepare a relevant introduction.','Use reviewed company details to explain why you are reaching out.'),('Keep the next step.','Add notes and follow-ups to the CRM rather than leaving them in separate lists.')]),
    ('agencies','Security & housekeeping','New client conversations. Less scattered work.','Research hotels, hospitals, offices and other businesses that may be relevant to your services. Keep a company introduction and client records nearby.','A focused client-research and follow-up workflow.', [('Choose your territory.','Research the business categories and precise locations your agency covers.'),('Prepare your pitch.','Draft a service introduction or call script and keep your company document ready.'),('Track the relationship.','Record the actual reply, confirmed meeting or next follow-up in the CRM.')]),
    ('sales','Sales teams','Keep the conversation moving.','Small sales teams need a clear view of which records are new, which conversations happened and which follow-ups are due.','A pipeline with context behind each next action.', [('Start with the record.','Bring a useful lead into the customer workspace.'),('Record what happened.','Keep notes and factual outcomes with the deal.'),('Plan the follow-up.','Review activities and confirmed meeting details, then choose the next step.')]),
    ('staffing','Staffing teams','People and opportunities. In the same picture.','Bring client research and candidate research into one working day, while keeping the two kinds of records clearly organised.','A candidate shortlist and client opportunities your team can review.', [('Understand the requirement.','Describe the role and location your staffing team needs to research.'),('Review a candidate list.','Organise the available records and prepare your own interview questions.'),('Keep client work connected.','Research prospective clients and track the relevant conversations separately in CRM.')]),
]

def usecases():
    tabs = ''.join(f'<button id="case-tab-{key}" type="button" data-tab="{key}" aria-selected="{str(i==0).lower()}">{label}</button>' for i,(key,label,*_) in enumerate(CASES))
    panels = ''
    for i,(key,label,title,desc,result,steps_) in enumerate(CASES):
        content = ''.join(f'<article class="story-step"><span>0{j+1}</span><div><h3>{heading}</h3><p>{copy}</p></div></article>' for j,(heading,copy) in enumerate(steps_))
        panels += f'<section id="case-panel-{key}" class="case-panel demo-pane" data-panel="{key}"{(" hidden" if i else "")}><div><h3>{title}</h3><p class="subcopy">{desc}</p><p class="result">{result}</p><div class="actions">{wa("Discuss this workflow",label)}</div></div><div>{content}</div></section>'
    static = ''.join(f'<article class="usecase-row reveal"><div><h3>{label}</h3><p>{title}</p></div><div><p>{desc}</p><div class="workflow">'+''.join(f'<span>{heading}</span>' for heading,_ in steps_)+'</div></div></article>' for _,label,title,desc,_,steps_ in CASES)
    return f'''{page_hero('Use cases','Made for the way<br><em>small teams work.</em>','Different businesses. Familiar busywork. Find a workflow that gives your team a clearer place to start.',topic='a business workflow',center=True)}
    <section class="section rule" id="walkthrough"><div class="wrap" data-tabs><div class="demo-tabs usecase-tabs" data-tablist aria-label="Business use cases">{tabs}</div>{panels}<span class="sr-only" data-tab-status aria-live="polite"></span></div></section>
    <section class="section soft-section"><div class="wrap"><div class="section-head reveal"><h2>Find your starting point.<br><em>Build from there.</em></h2><p>Each workflow uses the same connected product, with a different task at the centre.</p></div>{static}</div></section>
    {related([('product.html','Explore the whole product','See the tools behind these workflows.'),('crm.html','Connect the next step','Keep the customer record and activity together.'),('contact.html','Walk through your own case','Tell us what your team is trying to simplify.')])}{closing('your team’s workflow')}'''

def contact():
    return f'''<section class="page-hero"><div class="wrap"><span class="eyebrow hero-title">Talk to the team</span><h1 class="hero-title">Let’s make room<br><em>for better work.</em></h1><p class="subcopy hero-copy">Tell us about your business and the tasks you want to simplify. We’ll start with a conversation.</p></div></section>
    <section class="wrap contact-layout" id="walkthrough"><div class="contact-info reveal"><p>Ask for a product walkthrough, discuss your workflow, or understand the accounts and providers your setup needs.</p><div class="contact-person"><span class="eyebrow">Your first point of contact</span><h3>Vishal Sharma</h3><p>Marketing contact · Rudra24</p><a href="tel:+919999881949">+91 99998 81949</a><div class="actions">{wa()}</div></div><div class="contact-person"><h3>Prefer email?</h3><p>Write to the team that fits your enquiry.</p><ul class="company-list">{company_list()}<li><b>General enquiries</b><a href="mailto:sales@leadgenai.rudra24secure.com">sales@leadgenai.rudra24secure.com</a></li></ul></div><div class="contact-person">{office()}</div></div>
    <form class="contact-form reveal" data-contact-form><h3>A little context helps.</h3><p>Prepare an enquiry, then review and send it in WhatsApp. No information is submitted to this website.</p><fieldset data-contact-fields disabled><legend class="sr-only">Prepare a WhatsApp enquiry</legend><label class="form-field">Your name <span class="optional">(optional)</span><input name="name" autocomplete="name" maxlength="100" placeholder="How should we address you?"></label><label class="form-field">Business name <span class="optional">(optional)</span><input name="business" autocomplete="organization" maxlength="150" placeholder="Your business or team"></label><label class="form-field">What would you like to explore?<select name="interest"><option value="a product walkthrough">A product walkthrough</option><option value="lead generation">Lead generation</option><option value="CRM and follow-ups">CRM and follow-ups</option><option value="outreach and calling">Outreach and calling</option><option value="recruitment">Recruitment</option><option value="provider and account setup">Provider and account setup</option></select></label><label class="form-field">Anything else? <span class="optional">(optional)</span><textarea name="message" maxlength="1200" placeholder="Tell us what your team needs."></textarea></label><button class="button" type="submit" data-js-control>Prepare my enquiry {icon('arrow')}</button></fieldset><p class="form-note">Your details stay in this page until you choose to open WhatsApp.</p><p class="thanks-note" data-enquiry-status aria-live="polite"></p><a class="button" href="https://wa.me/919999881949" target="_blank" rel="noopener noreferrer" data-prepared-enquiry hidden>Open my enquiry in WhatsApp {icon('arrow')}</a><noscript><p class="form-note">JavaScript is off. You can still contact the team directly:</p>{wa()}</noscript></form></section>
    {faq([('Can I see the app before deciding?','Ask for a product walkthrough on WhatsApp. Tell us your business type and the features you want to see.'),('What should I share about my business?','Your industry, the locations you cover and the tasks your team wants to simplify are a useful starting point. Do not send passwords or API keys.'),('How does pricing work?','Contact the team for the current product offer. Third-party AI, calling and messaging providers may have separate plans or usage charges.'),('What is needed for calling and account integrations?','It depends on the workflow. Calling needs backend and telephony setup; email, calendar, Sheets and WhatsApp need their respective authorised accounts or provider configuration.')])}'''

GMAIL_SUBJECT = quote('Enquiry from the Rudra24 website')

def gmail_links(html):
    """Turn mailto: links into Gmail compose links that open in a new tab."""
    return re.sub(r'href="mailto:([^"?]+)"',
        lambda m: f'href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to={m.group(1)}&amp;su={GMAIL_SUBJECT}" target="_blank" rel="noopener noreferrer"', html)

def write_page(slug, label, title, desc, body):
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{escape(label)} — Rudra24 AI</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="theme-color" content="#FFFFEB"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:site_name" content="Rudra24 AI"><link rel="icon" type="image/png" href="assets/rudra24-icon.png"><link rel="preload" href="assets/fonts/figtree-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/eb-garamond-latin-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="refinement.css"><script src="assets/vendor/lenis.min.js" defer></script><script src="map.js" defer></script><script src="media.js" defer></script><script src="site.js" defer></script><script src="experience.js" defer></script></head>
<body data-page="{slug}">{header(slug)}<main id="main">{body}{visit_section()}</main>{footer()}</body></html>'''
    (SITE / f'{slug}.html').write_text(gmail_links(html),encoding='utf-8')

def main():
    fonts = SITE / 'assets/fonts'
    fonts.mkdir(parents=True,exist_ok=True)
    for name in ['figtree-latin-variable.woff2','geist-latin-wght-normal.woff2','eb-garamond-latin-variable.woff2','eb-garamond-latin-italic-variable.woff2','LICENSE-figtree.txt','LICENSE-ebgaramond.txt','LICENSE-Geist.txt']:
        shutil.copy2(REPO/'fonts'/name,fonts/name)
    # The square app PNG is resized once for the site; the ICO contains a wider mark.
    builders = [home,product,leads,crm,outreach,recruitment,usecases,contact]
    for page,builder in zip(PAGES,builders):
        body = builder()
        clips = {'product':['assistant'],'lead-generation':['leads'],'crm':['crm'],'outreach':['calling','outreach']}.get(page[0], [])
        if clips:
            body = body.replace(closing(), ''.join(feature_film(key) for key in clips) + closing()) if page[0]=='product' else body
            if page[0]!='product':
                pos = body.rfind('<section class="closing">')
                body = body[:pos] + ''.join(feature_film(key) for key in clips) + body[pos:]
        write_page(*page,body)
        print(f'Built {page[0]}.html')
    from build_landing import build_landing
    build_landing()

if __name__=='__main__':
    main()



