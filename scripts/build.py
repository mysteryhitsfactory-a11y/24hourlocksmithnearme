# -*- coding: utf-8 -*-
"""24 Hour Locksmith (24hourlocksmithnearme.us) — static site generator.
Midnight/amber 'open late' design. 230+ unique pages: 50 states + 163 cities.
White-hat: no fake reviews, no time guarantees, no license claims, no 'nationwide' copy."""
import os, hashlib, html
from data import STATES, SERVICES, COMBO_SERVICES, PHONE, PHONE_RAW, DOMAIN, BRAND, GSC_TOKEN

OUT = os.path.join(os.path.dirname(__file__), "..", "site")

def seed(s): return int(hashlib.md5(s.encode()).hexdigest(), 16)
def pick(bank, key, n=1, offset=0):
    s = seed(key) + offset; out, used = [], set()
    for i in range(n):
        idx = (s // (7 ** (i + 1)) + i * 13) % len(bank)
        while idx in used: idx = (idx + 1) % len(bank)
        used.add(idx); out.append(bank[idx])
    return out if n > 1 else out[0]

SVC = {s[0]: s for s in SERVICES}
ALL_CITIES = [(st, c) for st in STATES for c in st[4]]  # (state_tuple, city_tuple)
def city_path(st, c): return f"/locksmith-{c[0]}-{st[2].lower()}/"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=Bebas+Neue&display=swap" rel="stylesheet">'

CSS = """
:root{--ink:#0b0e14;--ink2:#121826;--panel:#1a2234;--amber:#ffb703;--amber2:#fb8500;--ice:#8ecae6;--paper:#f6f7f9;--mist:#e9edf2;--txt:#22293a;--dim:#5b6474;--line:rgba(11,14,20,.12)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Archivo',system-ui,sans-serif;color:var(--txt);background:var(--paper);line-height:1.65;font-size:17px}
h1,h2,h3,h4{font-family:'Archivo',sans-serif;font-weight:800;line-height:1.15;color:var(--ink)}
a{color:#0d6e9e;text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.big{font-family:'Bebas Neue',sans-serif;letter-spacing:.02em}
/* header */
header{background:var(--ink);position:sticky;top:0;z-index:50;border-bottom:3px solid var(--amber)}
.hd{display:flex;align-items:center;justify-content:space-between;padding:12px 22px;max-width:1120px;margin:0 auto;gap:14px}
.logo{display:flex;align-items:center;gap:11px;color:#fff}
.logo .mk{width:42px;height:42px;flex:none}
.logo b{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;font-weight:400;letter-spacing:.06em;color:#fff}
.logo b em{color:var(--amber);font-style:normal}
.logo small{display:block;font-size:.64rem;letter-spacing:.3em;text-transform:uppercase;color:var(--ice)}
nav{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
nav a{color:#c9d3e0;font-size:.93rem;font-weight:500}
nav a:hover{color:var(--amber)}
.call{background:var(--amber);color:var(--ink)!important;padding:10px 20px;border-radius:8px;font-weight:800;white-space:nowrap;box-shadow:0 0 0 0 rgba(255,183,3,.5)}
.call:hover{background:#ffc733}
/* hero */
.hero{background:radial-gradient(900px 500px at 80% -20%,rgba(142,202,230,.14),transparent 55%),radial-gradient(700px 420px at 10% 120%,rgba(255,183,3,.12),transparent 55%),linear-gradient(170deg,var(--ink),var(--ink2) 70%);color:#e8edf4;padding:72px 0 64px;position:relative}
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:.75rem;letter-spacing:.28em;text-transform:uppercase;color:var(--amber);margin-bottom:16px}
.eyebrow:before{content:"";width:9px;height:9px;border-radius:50%;background:var(--amber);box-shadow:0 0 12px var(--amber)}
.hero h1{color:#fff;font-size:clamp(1.9rem,4.4vw,3.15rem);max-width:840px;text-wrap:balance}
.hero p.lead{max-width:640px;margin:18px 0 28px;color:#b9c4d4;font-size:1.07rem}
.cta-row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;padding:14px 28px;border-radius:10px;font-weight:800;font-size:1.02rem}
.btn.primary{background:var(--amber);color:var(--ink)}
.btn.primary:hover{background:#ffc733}
.btn.ghost{border:2px solid var(--ice);color:var(--ice)}
.btn.ghost:hover{background:rgba(142,202,230,.12)}
.hero .sub{margin-top:20px;font-size:.9rem;color:#7e8ba0;letter-spacing:.04em}
/* sections */
section{padding:56px 0}
section.alt{background:var(--mist)}
section.dark{background:var(--ink);color:#dbe3ee}
section.dark h2,section.dark h3{color:#fff}
h2{font-size:clamp(1.5rem,3vw,2.1rem);margin-bottom:14px;text-wrap:balance}
.sec-intro{max-width:720px;margin-bottom:30px;color:var(--dim)}
section.dark .sec-intro{color:#a9b6c9}
.rule{width:64px;height:4px;background:linear-gradient(90deg,var(--amber),var(--amber2));border-radius:2px;margin-bottom:22px}
/* cards */
.grid{display:grid;gap:18px}
.grid.c3{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.grid.c4{grid-template-columns:repeat(auto-fit,minmax(235px,1fr))}
.card{background:#fff;border-radius:12px;padding:24px 22px;border:1px solid var(--line);border-left:4px solid var(--amber);box-shadow:0 2px 10px rgba(11,14,20,.05)}
.card h3{font-size:1.1rem;margin-bottom:8px}
.card p{font-size:.94rem;color:var(--dim)}
.card a.more{font-weight:700;font-size:.9rem;display:inline-block;margin-top:10px}
/* chips */
.chips{display:flex;flex-wrap:wrap;gap:9px}
.chips a{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 15px;font-size:.9rem;color:var(--ink);font-weight:500}
.chips a:hover{border-color:var(--amber2);color:var(--amber2)}
section.dark .chips a{background:var(--panel);border-color:rgba(255,255,255,.12);color:#dbe3ee}
/* steps */
.steps{counter-reset:st}
.step{display:flex;gap:18px;padding:17px 0;border-bottom:1px dashed rgba(255,255,255,.16);align-items:flex-start}
.step:last-child{border-bottom:0}
.step .n{counter-increment:st;flex:none;width:46px;height:46px;border-radius:10px;background:var(--panel);color:var(--amber);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:1.5rem;border:1px solid rgba(255,183,3,.4)}
.step .n:before{content:counter(st)}
.step h3{font-size:1.05rem;margin-bottom:4px}
.step p{font-size:.94rem;color:#a9b6c9}
/* faq */
details{background:#fff;border:1px solid var(--line);border-radius:10px;margin-bottom:11px;overflow:hidden}
summary{cursor:pointer;padding:15px 20px;font-weight:600;color:var(--ink);list-style:none;position:relative;padding-right:44px}
summary:after{content:"+";position:absolute;right:18px;top:11px;font-size:1.4rem;color:var(--amber2)}
details[open] summary:after{content:"–"}
details .a{padding:0 20px 17px;color:var(--dim);font-size:.95rem}
/* prose */
.prose{max-width:760px}
.prose p{margin-bottom:16px}
.prose h2{margin-top:32px}
.prose ul{margin:0 0 16px 22px}
/* callout */
.callout{background:var(--ink);color:#e8edf4;border-radius:14px;padding:32px 30px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px;border-top:3px solid var(--amber)}
.callout h3{color:#fff;font-size:1.28rem;margin:0}
.callout p{color:#a9b6c9;margin:6px 0 0;font-size:.95rem}
/* footer */
footer{background:var(--ink);color:#8f9cb0;padding:52px 0 28px;font-size:.92rem;border-top:3px solid var(--amber)}
footer h4{color:#fff;font-size:.98rem;margin-bottom:13px}
footer a{color:#8f9cb0}
footer a:hover{color:var(--amber)}
.fgrid{display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-bottom:32px}
.fbot{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;font-size:.82rem}
footer ul{list-style:none}
footer li{margin-bottom:7px}
/* fx */
.fxblk{opacity:0;transform:translateY(20px);transition:opacity .6s ease,transform .6s ease}
.fxlit{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.fxblk{opacity:1;transform:none;transition:none}}
.crumbs{font-size:.84rem;padding:15px 0 0;color:#75809245}
.crumbs,.crumbs a{color:#75808f}
@media(max-width:760px){nav{display:none}section{padding:44px 0}}
.mnav{display:none}
@media(max-width:760px){.mnav{display:flex;gap:14px;flex-wrap:wrap;background:var(--ink2);padding:10px 22px}.mnav a{color:#c9d3e0;font-size:.85rem}}
"""

FX = """<script>(function(){function lit(){var els=document.querySelectorAll('.fxblk');var vh=window.innerHeight;els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<vh*0.92&&r.bottom>0)e.classList.add('fxlit');});}
if(matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('.fxblk').forEach(function(e){e.classList.add('fxlit')});return;}
window.addEventListener('scroll',lit,{passive:true});window.addEventListener('load',lit);document.addEventListener('DOMContentLoaded',lit);setTimeout(lit,60);})();</script>"""

LOGO_SVG = """<svg class="mk" viewBox="0 0 42 42" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="42" height="42" rx="10" fill="#ffb703"/><circle cx="21" cy="21" r="13.5" fill="#0b0e14"/><line x1="21" y1="21" x2="21" y2="12.5" stroke="#ffb703" stroke-width="2.6" stroke-linecap="round"/><line x1="21" y1="21" x2="27.5" y2="24.5" stroke="#8ecae6" stroke-width="2.2" stroke-linecap="round"/><circle cx="21" cy="21" r="1.8" fill="#ffb703"/></svg>"""

FAVICON = '<link rel="icon" type="image/svg+xml" href="/favicon.svg">'

def nav_html():
    return f"""<header><div class="hd">
<a class="logo" href="/">{LOGO_SVG}<span><b>24 HOUR <em>LOCKSMITH</em></b><small>Open All Night · Every Night</small></span></a>
<nav><a href="/services/">Services</a><a href="/locations/">Locations</a><a href="/car-key-replacement/">Car Keys</a><a href="/about/">About</a><a href="/contact/">Contact</a><a class="call" href="tel:{PHONE_RAW}">☎ {PHONE}</a></nav>
</div><div class="mnav"><a href="/services/">Services</a><a href="/locations/">Locations</a><a href="/about/">About</a><a href="/contact/">Contact</a></div></header>"""

def footer_html():
    svc = "".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES[:7])
    sts = "".join(f'<li><a href="/locksmith-{st[0]}/">{st[1]}</a></li>' for st in STATES[:7])
    return f"""<footer><div class="wrap"><div class="fgrid">
<div><h4>24 Hour Locksmith</h4><p>A live dispatcher and mobile locksmiths, around the clock. Cars, homes and businesses.</p><p style="margin-top:12px"><a class="call" style="display:inline-block" href="tel:{PHONE_RAW}">☎ {PHONE}</a></p></div>
<div><h4>Services</h4><ul>{svc}<li><a href="/services/">All services →</a></li></ul></div>
<div><h4>Locations</h4><ul>{sts}<li><a href="/locations/">All locations →</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div><div class="fbot"><span>© 24 Hour Locksmith · 24hourlocksmithnearme.us</span><span>Open 24 hours, 7 days a week.</span></div></div></footer>"""

def shell(title, desc, path, body, schema=""):
    canonical = DOMAIN + path
    og = f"""<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="{BRAND}">"""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="google-site-verification" content="{GSC_TOKEN}">
{og}{FAVICON}{FONTS}<style>{CSS}</style>{schema}</head><body>
{nav_html()}
{body}
{footer_html()}{FX}</body></html>"""

def biz_schema(place=None):
    area = f", serving {place}" if place else ""
    return f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Locksmith","name":"{BRAND}","telephone":"+1{PHONE_RAW}","url":"{DOMAIN}/","description":"24-hour mobile locksmith dispatch{area}. Car lockouts, house lockouts, car key replacement, rekeying and commercial locksmith work.","openingHours":"Mo-Su 00:00-23:59","priceRange":"$$"}}</script>"""

def faq_schema(faqs):
    items = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q.replace('"','\\"'), a.replace('"','\\"')) for q, a in faqs)
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}</script>'

def crumbs(items):
    lis = "".join(f' › <a href="{u}">{t}</a>' if u else f' › {t}' for t, u in items)
    return f'<div class="wrap crumbs"><a href="/">Home</a>{lis}</div>'

def callout(t, sub):
    return f"""<div class="callout fxblk"><div><h3>{t}</h3><p>{sub}</p></div><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div>"""

TRUST = [
 "The price is agreed before the work starts: a realistic range on the phone, and the exact figure confirmed by the technician in person before any tool comes out.",
 "Every call starts with a straight answer — dispatch quotes an honest range up front, and the final price is confirmed on-site before work begins.",
 "You approve the number first. A range over the phone, a firm price in person, and only then does the job start.",
]
DAMAGE = [
 "Non-destructive entry comes first, every time. Picks, bypass tools and decoders open the vast majority of lockouts with the original lock left exactly as it was.",
 "Drilling is a last resort, not a shortcut — most doors open without damage and without replacing anything.",
 "Locks get opened the patient way; destructive entry happens only with your explicit approval when there's truly no alternative.",
]
FAQS = [
 ("How fast can a locksmith get to me?","It depends on where the nearest available technician is and local traffic, so we don't promise a fixed number of minutes. Dispatch answers immediately, tells you honestly how far the closest tech is, and keeps you updated on the way."),
 ("How much does a locksmith cost?","It depends on the job and the hour. You'll hear a realistic range on the phone before anyone is dispatched, and the technician confirms the exact price in person before starting."),
 ("Will my lock or car be damaged?","No — non-destructive methods come first. Vehicles are opened with proper tools that protect paint, seals and electronics; drilling a lock is a genuine last resort done only with your approval."),
 ("Are you really open 24 hours?","Yes — dispatch answers around the clock, every day of the year. Late-night and holiday calls can carry an after-hours rate, always stated up front."),
 ("Do I need to show ID?","Yes. Before opening a home, business or vehicle we verify you have the right to be inside — a driver's license, registration or lease settles it in seconds, and it protects you as much as anyone."),
 ("Can you make a key if I lost every copy?","Usually, yes. Keys are cut and programmed on-site for most makes and models — transponder keys and proximity fobs included — even with no original to copy."),
 ("Should I rekey or replace?","If the hardware is solid, rekeying is the smarter buy: same locks, new pins, old keys dead. If the lock is worn or outdated, the technician will say so and explain why replacement wins."),
 ("What payment do you take?","Cards and cash on completion. The job is done and tested in front of you first."),
]

CITY_OPEN = [
 "Locked out in {city}? {brand} dispatch answers around the clock and routes the nearest available mobile locksmith to you — whether it's 2 PM or 2 AM.",
 "{city} — {fact} — doesn't stop at sundown, and neither do lockouts. One call reaches a live dispatcher, day or night, and puts a mobile technician on the way.",
 "A lockout in {city} never checks the clock first. {brand} keeps dispatch open 24 hours so a locksmith can head your way the moment you call.",
 "From downtown to the edges of town, {brand} covers {city} around the clock — car lockouts, house lockouts and lost keys handled at your location.",
]
CITY_MID = [
 "{state} means {region}, and {city} — {fact} — is exactly the kind of place our mobile units are built for: the truck carries key machines, programmers, picks and hardware, so most jobs finish in one visit.",
 "Being {fact}, {city} keeps locksmiths busy — and our technicians arrive ready, with cutting and programming equipment on board for most makes, models and door hardware.",
 "In {state} — {region} — {city} calls get the same treatment as everywhere we work: honest pricing before dispatch, damage-free methods first, and a technician who finishes the job on the first trip whenever possible.",
]

def city_page(st, c):
    stslug, stname, abbr, region, _ = st
    cslug, cname, fact = c
    key = f"city|{cslug}|{abbr}"
    fmt = dict(city=cname, state=stname, region=region, fact=fact, brand=BRAND)
    p1 = pick(CITY_OPEN, key).format(**fmt)
    p2 = pick(CITY_MID, key, offset=5).format(**fmt)
    trust = pick(TRUST, key, offset=9); dmg = pick(DAMAGE, key, offset=13)
    faqs = pick(FAQS, key, n=4, offset=17)
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in faqs)
    cards = "".join(f'<div class="card fxblk"><h3>{SVC[s][1]}</h3><p>{SVC[s][2]}</p><a class="more" href="/{s}/">Details →</a></div>' for s in COMBO_SERVICES + ["lock-rekey"])
    sibs = [x for x in st[4] if x[0] != cslug]
    near = "".join(f'<a href="{city_path(st, n)}">{n[1]}</a>' for n in sibs)
    other = "".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES if s[0] not in COMBO_SERVICES + ["lock-rekey"])
    title = f"24 Hour Locksmith in {cname}, {abbr} | {BRAND}"
    desc = f"24-hour locksmith in {cname}, {stname}: car lockouts, house lockouts, car keys made on-site. Live dispatch, up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">{cname}, {abbr} · Open Now</div>
<h1>24 Hour Locksmith in {cname}</h1>
<p class="lead">Car lockouts, house lockouts and lost keys in {cname} — a live dispatcher answers any hour and sends the nearest mobile technician.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/services/">All services</a></div>
<div class="sub">Up-front pricing · Damage-free first · Cars · Homes · Businesses</div></div></div>
{crumbs([("Locations","/locations/"),(stname,f"/locksmith-{stslug}/"),(cname,None)])}
<section><div class="wrap prose"><div class="rule"></div>
<p class="fxblk">{p1}</p><p class="fxblk">{p2}</p><p class="fxblk">{trust}</p><p class="fxblk">{dmg}</p></div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">Most-called services in {cname}</h2><div class="grid c4">{cards}</div>
<div style="margin-top:24px"><h3 style="margin-bottom:11px">Also available</h3><div class="chips fxblk">{other}</div></div></div></section>
<section><div class="wrap"><h2 class="fxblk">{cname} locksmith questions</h2>{faq_html}</div></section>
<section class="alt"><div class="wrap">{callout(f"Locked out in {cname} right now?","One call reaches live dispatch — any hour, any day.")}
<div style="margin-top:30px"><h3 style="margin-bottom:11px">More {stname} coverage</h3><div class="chips fxblk">{near}<a href="/locksmith-{stslug}/">All of {stname} →</a></div></div></div></section>"""
    return title, desc, city_path(st, c), body, biz_schema(f"{cname}, {abbr}") + faq_schema(faqs)

STATE_OPEN = [
 "{state} is {region} — and {brand} keeps a 24-hour dispatch line open for all of it. Wherever you're standing when the door clicks shut, one call starts the fix.",
 "Across {state}, lockouts don't keep business hours. {brand} answers around the clock and connects you with mobile locksmith service where you are.",
 "{brand} covers {state} the way it should be covered: a live dispatcher any hour, honest pricing before anyone rolls, and damage-free methods first.",
]
def state_page(st):
    stslug, stname, abbr, region, cities = st
    key = "state|" + stslug
    p1 = pick(STATE_OPEN, key).format(state=stname, region=region, brand=BRAND)
    trust = pick(TRUST, key, offset=3); dmg = pick(DAMAGE, key, offset=7)
    city_cards = "".join(f'<div class="card fxblk"><h3>{c[1]}</h3><p>{c[2][0].upper()+c[2][1:]}.</p><a class="more" href="{city_path(st, c)}">24 hour locksmith in {c[1]} →</a></div>' for c in cities)
    svc_chips = "".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES)
    faqs = pick(FAQS, key, n=3, offset=11)
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in faqs)
    others = [x for x in STATES if x[0] != stslug][seed(key) % (len(STATES)-8):][:7]
    near = "".join(f'<a href="/locksmith-{o[0]}/">{o[1]}</a>' for o in others)
    title = f"24 Hour Locksmith in {stname} | {BRAND}"
    desc = f"24-hour locksmith service in {stname}: lockouts, car keys, rekeying and more. Live dispatch with up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">{stname} · Open Now</div>
<h1>24 Hour Locksmith in {stname}</h1>
<p class="lead">Live dispatch around the clock for cars, homes and businesses across {stname}.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/locations/">All locations</a></div>
<div class="sub">Up-front pricing · Damage-free first · Live dispatch</div></div></div>
{crumbs([("Locations","/locations/"),(stname,None)])}
<section><div class="wrap prose"><div class="rule"></div>
<p class="fxblk">{p1}</p><p class="fxblk">{trust}</p><p class="fxblk">{dmg}</p></div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">{stname} cities we cover</h2><div class="grid c3">{city_cards}</div></div></section>
<section><div class="wrap"><h2 class="fxblk">Every service, any hour</h2><div class="chips fxblk">{svc_chips}</div>
<div style="margin-top:34px"><h2 class="fxblk">Common questions</h2>{faq_html}</div></div></section>
<section class="alt"><div class="wrap">{callout(f"Need a locksmith in {stname}?","A live dispatcher answers 24/7 — tell them where you are.")}
<div style="margin-top:30px"><h3 style="margin-bottom:11px">Nearby coverage</h3><div class="chips fxblk">{near}</div></div></div></section>"""
    return title, desc, f"/locksmith-{stslug}/", body, biz_schema(stname) + faq_schema(faqs)

def service_page(s):
    slug, name, short, cat, blurb = s
    key = "svc|" + slug
    faqs = pick(FAQS, key, n=4, offset=19)
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in faqs)
    extra = {
      "auto":"Most makes and models on American roads are covered — domestic, Japanese, Korean and European — with cutting and programming equipment on the truck. For an unusual vehicle, give dispatch the year, make and model and they'll confirm before rolling.",
      "residential":"Houses, condos, townhomes and apartments get the same standard: honest advice on repair versus rekey versus replace, quality hardware from names like Schlage, Kwikset and Yale, and doors that close right when the job is done.",
      "commercial":"Storefronts, offices, restaurants and warehouses need hardware that survives daily abuse. Commercial-grade locks, exit devices and key control are installed and serviced — with key assignments documented when you want them tracked.",
      "emergency":"Emergency work is the core of the operation: dispatch answers around the clock, technicians rotate on call overnight, and after-hours rates are stated before anyone is sent.",
    }[cat]
    others = [x for x in SERVICES if x[0] != slug][seed(key) % 8:][:4]
    rel = "".join(f'<div class="card fxblk"><h3>{o[1]}</h3><p>{o[2]}</p><a class="more" href="/{o[0]}/">Learn more →</a></div>' for o in others)
    st_chips = "".join(f'<a href="/locksmith-{st[0]}/">{st[1]}</a>' for st in STATES)
    title = f"{name} — 24 Hours | {BRAND}"
    desc = f"{short} Live dispatch around the clock, up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">Open 24 Hours</div>
<h1>{name}, Any Hour</h1><p class="lead">{short}</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/locations/">Where we work</a></div>
<div class="sub">Up-front pricing · Damage-free first · Live dispatch</div></div></div>
{crumbs([("Services","/services/"),(name,None)])}
<section><div class="wrap prose"><div class="rule"></div>
<p class="fxblk">{blurb}</p><p class="fxblk">{extra}</p>
<p class="fxblk">{pick(TRUST,key)}</p><p class="fxblk">{pick(DAMAGE,key,offset=3)}</p></div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">Find {name.lower()} near you</h2><p class="sec-intro">Pick your state to see local coverage:</p><div class="chips fxblk">{st_chips}</div></div></section>
<section><div class="wrap"><h2 class="fxblk">Common questions</h2>{faq_html}</div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">Related services</h2><div class="grid c4">{rel}</div></div></section>"""
    return title, desc, f"/{slug}/", body, biz_schema() + faq_schema(faqs)

def home_page():
    svc_cards = "".join(f'<div class="card fxblk"><h3>{s[1]}</h3><p>{s[2]}</p><a class="more" href="/{s[0]}/">Details →</a></div>' for s in SERVICES[:8])
    st_chips = "".join(f'<a href="/locksmith-{st[0]}/">{st[1]}</a>' for st in STATES)
    title = "24 Hour Locksmith Near Me — Lockouts & Car Keys, Any Hour | " + PHONE
    desc = f"Searching '24 hour locksmith near me'? Live dispatch answers around the clock: car lockouts, house lockouts, car keys made on-site. Up-front pricing. {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">Live Dispatch · Open Now</div>
<h1>The locksmith that's awake when you need one.</h1>
<p class="lead">Car lockouts, house lockouts, lost keys, rekeying — a live dispatcher answers 24 hours a day and sends the nearest mobile locksmith, with the price agreed before the work starts.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/locations/">Find your city</a></div>
<div class="sub">Damage-free methods first · Cars · Homes · Businesses</div></div></div>
<section><div class="wrap"><div class="rule"></div>
<h2 class="fxblk">What we handle</h2><p class="sec-intro fxblk">Every truck is a rolling locksmith shop — key machines, programmers, picks and hardware — so most jobs finish in one visit.</p>
<div class="grid c4">{svc_cards}</div>
<p style="margin-top:20px" class="fxblk"><a class="btn ghost" style="border-color:var(--amber2);color:var(--amber2)" href="/services/">See all services →</a></p></div></section>
<section class="dark"><div class="wrap"><h2 class="fxblk">How a call works</h2><div class="steps prose">
<div class="step fxblk"><span class="n"></span><div><h3>Tell dispatch where you are</h3><p>A live person — not a menu — takes your location and what happened, 24 hours a day.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Hear a real price range</h3><p>An honest range before anyone is dispatched. After-hours rates stated up front.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>The nearest tech rolls</h3><p>The closest available mobile locksmith heads your way with the right tools.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Approve, then work starts</h3><p>Exact price confirmed in person first. Job done, tested, and you're back inside.</p></div></div>
</div></div></section>
<section><div class="wrap"><h2 class="fxblk">Find a locksmith near you</h2>
<p class="sec-intro fxblk">Pick your state, then your city:</p>
<div class="chips fxblk">{st_chips}</div></div></section>
<section class="alt"><div class="wrap">{callout("Locked out right now?","Skip the scrolling — a live dispatcher answers any hour.")}</div></section>"""
    return title, desc, "/", body, biz_schema()

def services_index():
    cats = [("auto","Automotive"),("residential","Residential"),("commercial","Commercial"),("emergency","Emergency")]
    secs = ""
    for ckey, label in cats:
        cards = "".join(f'<div class="card fxblk"><h3>{s[1]}</h3><p>{s[2]}</p><a class="more" href="/{s[0]}/">Details →</a></div>' for s in SERVICES if s[3] == ckey)
        secs += f'<h2 class="fxblk" style="margin-top:28px">{label}</h2><div class="grid c3">{cards}</div>'
    title = f"Locksmith Services, 24 Hours a Day | {BRAND}"
    desc = f"Every service we run around the clock: automotive, residential, commercial and emergency locksmith work. Call {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Full service menu</div><h1>Services That Never Sleep</h1>
<p class="lead">Twelve services, one number, every hour of the year.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Services",None)])}
<section><div class="wrap">{secs}</div></section>
<section class="alt"><div class="wrap">{callout("Not sure what you need?","Describe the problem — dispatch will tell you what it takes and what it costs.")}</div></section>"""
    return title, desc, "/services/", body, biz_schema()

def locations_index():
    st_cards = "".join(f'<a href="/locksmith-{st[0]}/">{st[1]}</a>' for st in STATES)
    big = "".join(f'<a href="{city_path(st, c)}">{c[1]}, {st[2]}</a>' for st, c in ALL_CITIES[:0])
    majors = [("new-york-city","New York, NY","/locksmith-new-york-city-ny/"),("los-angeles","Los Angeles, CA","/locksmith-los-angeles-ca/"),("chicago","Chicago, IL","/locksmith-chicago-il/"),("houston","Houston, TX","/locksmith-houston-tx/"),("phoenix","Phoenix, AZ","/locksmith-phoenix-az/"),("philadelphia","Philadelphia, PA","/locksmith-philadelphia-pa/"),("miami","Miami, FL","/locksmith-miami-fl/"),("atlanta","Atlanta, GA","/locksmith-atlanta-ga/"),("dallas","Dallas, TX","/locksmith-dallas-tx/"),("denver","Denver, CO","/locksmith-denver-co/"),("seattle","Seattle, WA","/locksmith-seattle-wa/"),("las-vegas","Las Vegas, NV","/locksmith-las-vegas-nv/")]
    big_chips = "".join(f'<a href="{u}">{n}</a>' for _, n, u in majors)
    title = f"Locations — Find a 24 Hour Locksmith | {BRAND}"
    desc = f"Find 24-hour locksmith coverage where you are — pick your state or jump to a major city. Live dispatch: {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Coverage</div><h1>Find a Locksmith Where You Are</h1>
<p class="lead">Pick your state, or jump straight to a major city.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Locations",None)])}
<section><div class="wrap"><h2 class="fxblk">Major cities</h2><div class="chips fxblk">{big_chips}</div>
<h2 class="fxblk" style="margin-top:34px">Browse by state</h2><div class="chips fxblk">{st_cards}</div></div></section>
<section class="alt"><div class="wrap">{callout("Don't see your town?","Call anyway — dispatch will tell you straight if we can reach you.")}</div></section>"""
    return title, desc, "/locations/", body, biz_schema()

def about_page():
    title = f"About {BRAND}"
    desc = f"What 24 Hour Locksmith is: live dispatch around the clock, honest pricing before work starts, damage-free methods first. {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Who we are</div><h1>Built for the 3 AM Phone Call</h1>
<p class="lead">Part of the 24/7 Locksmith family — a dispatch-first locksmith service that answers when others don't.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("About",None)])}
<section><div class="wrap prose"><div class="rule"></div>
<p class="fxblk">Most lockouts happen at the worst possible time — after the shops close, before they open, in a parking lot at midnight. That's the moment this service was built for. Dispatch is staffed around the clock, and mobile technicians carry key machines, programmers, entry tools and hardware so nearly every job can finish in a single visit.</p>
<h2 class="fxblk">Three rules on every job</h2>
<p class="fxblk">First: the price is agreed before the work starts — a realistic range on the phone, an exact figure confirmed in person. Second: non-destructive methods come first, and drilling is a last resort. Third: authorization is verified before anything is opened, because that's what protects every honest customer.</p>
<h2 class="fxblk">What we work on</h2>
<p class="fxblk">Cars (lockouts, lost keys, fobs, ignitions), homes (lockouts, rekeying, lock changes, smart locks) and businesses (commercial hardware, key control, safes). Trusted brands like Schlage, Kwikset, Yale, Medeco and Mul-T-Lock.</p>
<h2 class="fxblk">Where</h2>
<p class="fxblk"><a href="/locations/">Browse coverage by state and city</a> — or just call and tell dispatch where you're standing.</p></div></section>
<section class="alt"><div class="wrap">{callout("Save the number","The best time to find a locksmith is before you need one.")}</div></section>"""
    return title, desc, "/about/", body, biz_schema()

def contact_page():
    title = f"Contact — {BRAND}"
    desc = f"Reach a live dispatcher any hour: {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">24 hours · 7 days</div><h1>Contact</h1>
<p class="lead">One number, answered by a person, every hour of the year.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Contact",None)])}
<section><div class="wrap prose"><div class="rule"></div>
<h2 class="fxblk">Call — it's the fastest way</h2>
<p class="fxblk">For lockouts and emergencies, calling beats any form: <a href="tel:{PHONE_RAW}"><b>{PHONE}</b></a>. Dispatch can usually give you a price range in under two minutes.</p>
<h2 class="fxblk">Have ready</h2>
<ul class="fxblk"><li>Your location — address or cross-streets</li><li>What happened (lockout, lost keys, broken lock…)</li><li>For vehicles: year, make and model</li><li>A callback number</li></ul></div></section>
<section class="alt"><div class="wrap">{callout("Locked out right now?","Stop reading — call. A dispatcher is awake.")}</div></section>"""
    return title, desc, "/contact/", body, biz_schema()

def faq_page():
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in FAQS)
    title = f"Locksmith FAQ | {BRAND}"
    desc = f"Straight answers on pricing, timing, ID checks, car keys and rekeying. Call {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Straight answers</div><h1>Questions, Answered Honestly</h1>
<p class="lead">Everything people ask before they call.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("FAQ",None)])}
<section><div class="wrap">{faq_html}</div></section>
<section class="alt"><div class="wrap">{callout("Question not here?","Ask a human — dispatch answers 24/7.")}</div></section>"""
    return title, desc, "/faq/", body, biz_schema() + faq_schema(FAQS)

def write(path, content):
    fs = os.path.join(OUT, path.strip("/"))
    if path.endswith("/") or path == "/":
        fs = os.path.join(fs, "index.html")
    os.makedirs(os.path.dirname(fs), exist_ok=True)
    with open(fs, "w") as f: f.write(content)

def main():
    pages = []
    for gen in (home_page, services_index, locations_index, about_page, contact_page, faq_page):
        t, d, p, b, sc = gen(); write(p, shell(t, d, p, b, sc)); pages.append(p)
    for s in SERVICES:
        t, d, p, b, sc = service_page(s); write(p, shell(t, d, p, b, sc)); pages.append(p)
    for st in STATES:
        t, d, p, b, sc = state_page(st); write(p, shell(t, d, p, b, sc)); pages.append(p)
        for c in st[4]:
            t, d, p, b, sc = city_page(st, c); write(p, shell(t, d, p, b, sc)); pages.append(p)
    fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 42"><rect width="42" height="42" rx="10" fill="#ffb703"/><circle cx="21" cy="21" r="13.5" fill="#0b0e14"/><line x1="21" y1="21" x2="21" y2="12.5" stroke="#ffb703" stroke-width="2.6" stroke-linecap="round"/><line x1="21" y1="21" x2="27.5" y2="24.5" stroke="#8ecae6" stroke-width="2.2" stroke-linecap="round"/><circle cx="21" cy="21" r="1.8" fill="#ffb703"/></svg>"""
    with open(os.path.join(OUT, "favicon.svg"), "w") as f: f.write(fav)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc></url>" for p in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print(f"Built {len(pages)} pages")

if __name__ == "__main__":
    main()
