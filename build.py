#!/usr/bin/env python3
"""Generate the multi-page Grace Distribution site from the section blocks."""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / "_sections.html").read_text()  # snapshot of the old single-page body

# --- extract each section block by its comment marker ---
parts = re.findall(r'<!-- ===== (.*?) ===== -->(.*?)(?=<!-- ===== |\Z)', SRC, re.S)
S = {name.strip(): block for name, block in parts}

def fix_links(html):
    repl = {
        'href="#home"': 'href="index.html"',
        'href="#about"': 'href="about.html"',
        'href="#services"': 'href="services.html"',
        'href="#gallery"': 'href="gallery.html"',
        'href="#team"': 'href="team.html"',
        'href="#pricing"': 'href="pricing.html"',
        'href="#customers"': 'href="clients.html"',
        'href="#contact"': 'href="contact.html"',
    }
    for a, b in repl.items():
        html = html.replace(a, b)
    return html

NAV = [("index.html","Home"),("about.html","About"),("services.html","Services"),
       ("gallery.html","Gallery"),("pricing.html","Supply"),("team.html","Team"),
       ("clients.html","Clients"),("contact.html","Contact")]

def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="https://unpkg.com/aos@2.3.4/dist/aos.css" />
  <link rel="stylesheet" href="css/style.css" />
  <link rel="icon" href="images/logo-original.png" />
</head>
<body>
'''

def header(active):
    links = "\n        ".join(
        f'<a href="{href}"{" class=\"active\"" if href==active else ""}>{label}</a>'
        for href, label in NAV)
    return f'''
  <!-- TOP BAR -->
  <div class="topbar">
    <div class="container topbar__inner">
      <ul class="topbar__info">
        <li><i class="fa-solid fa-location-dot"></i> Mardan, Khyber Pakhtunkhwa, Pakistan</li>
        <li><a href="mailto:kashifyousafzai0001@gmail.com"><i class="fa-solid fa-envelope"></i> kashifyousafzai0001@gmail.com</a></li>
        <li class="hide-md"><a href="tel:+923005895573"><i class="fa-solid fa-phone"></i> 0300-5895573</a></li>
      </ul>
      <div class="topbar__social">
        <span>Follow Us</span>
        <a href="#" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
        <a href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        <a href="https://wa.me/923005895573" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
      </div>
    </div>
  </div>

  <!-- HEADER -->
  <header class="header" id="header">
    <div class="container header__inner">
      <a href="index.html" class="brand">
        <svg class="brand__mark" viewBox="0 0 64 64" width="44" height="44" aria-hidden="true">
          <defs><linearGradient id="drop" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#ffe680"/><stop offset="0.55" stop-color="#f7b500"/><stop offset="1" stop-color="#b87f00"/>
          </linearGradient></defs>
          <path d="M32 6c-13 19-19 25-19 34a19 19 0 0 0 38 0c0-9-6-15-19-34Z" fill="url(#drop)"/>
          <ellipse cx="26" cy="30" rx="4" ry="9" fill="#fff" opacity="0.65"/>
        </svg>
        <span class="brand__text"><strong>GRACE</strong><span>DISTRIBUTION</span></span>
      </a>
      <nav class="nav" id="nav">
        {links}
      </nav>
      <a href="contact.html" class="btn btn--accent header__cta">Get A Quote <i class="fa-solid fa-arrow-right"></i></a>
      <button class="nav-toggle" id="navToggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </header>
'''

def banner(title, crumb, img):
    return f'''
  <!-- PAGE BANNER -->
  <section class="pagebanner" style="background-image:url('images/{img}')">
    <div class="pagebanner__ov"></div>
    <div class="container pagebanner__inner" data-aos="fade-up">
      <h1>{title}</h1>
      <p class="crumb"><a href="index.html">Home</a> <i class="fa-solid fa-angle-right"></i> {crumb}</p>
    </div>
  </section>
'''

FOOT = fix_links("\n  <!-- ===== FOOTER ===== -->" + S["FOOTER"]).rstrip()
SCRIPTS = '''
  <a href="https://wa.me/923005895573" class="wa-float" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
  <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
  <script src="js/script.js"></script>
</body>
</html>
'''

def page(filename, active, title, desc, banner_html, *section_names):
    body = "".join(fix_links(S[name]) for name in section_names)
    html = head(title, desc) + header(active) + banner_html + body + FOOT + SCRIPTS
    (ROOT / filename).write_text(html)
    print("wrote", filename)

BASE = "Grace Distribution — Excellence in Fuel Distribution Network"

# HOME (hero, not banner)
home_top = fix_links(S["HERO (slider)"] + S["FUEL PRODUCT STRIP"] + S["FEATURES"] +
                     S["ABOUT"] + S["COUNTERS"] + S["VIDEO / CTA BANNER"] + S["QUALITY CTA BAND"])
(ROOT / "index.html").write_text(
    head(f"{BASE} | High Speed Diesel Supply Pakistan",
         "Grace Petroleum (SMC-Private) Limited — premier High Speed Diesel supply, free doorstep delivery & 24/7 service across Pakistan.")
    + header("index.html") + home_top + FOOT + SCRIPTS)
print("wrote index.html")

page("about.html","about.html", f"About Us | {BASE}",
     "About Grace Distribution — trusted High Speed Diesel distributor across Pakistan, partner of PSO, Shell, Total & Chevron.",
     banner("About Us","About Us","station-pumps.jpg"),
     "ABOUT","FACILITY / CAPABILITIES","COUNTERS")

page("services.html","services.html", f"Our Services | {BASE}",
     "Fuel distribution services — High Speed Diesel supply, free doorstep delivery, quality & calibration, bulk supply, 24/7 support.",
     banner("Our Services","Services","station-night.jpg"),
     "SERVICES","FACILITY / CAPABILITIES","QUALITY CTA BAND")

page("gallery.html","gallery.html", f"Gallery | {BASE}",
     "Grace Distribution fuel distribution network gallery — stations, tankers and supply operations.",
     banner("Gallery","Gallery","pump-day.jpg"),
     "GALLERY","VIDEO / CTA BANNER")

page("pricing.html","pricing.html", f"Supply Solutions | {BASE}",
     "Fuel supply solutions for every requirement — High Speed Diesel, Light Diesel Oil, Petrol and Lubricants.",
     banner("Supply Solutions","Supply","refuel.jpg"),
     "SUPPLY SOLUTIONS (Pricing layout)","QUALITY CTA BAND")

page("team.html","team.html", f"Our Team | {BASE}",
     "Meet the Grace Distribution management team.",
     banner("Our Team","Team","station-pumps.jpg"),
     "TEAM","COUNTERS")

page("clients.html","clients.html", f"Our Clients | {BASE}",
     "Grace Distribution valued customers — trusted by leading brands, banks, hospitals and industries across Pakistan.",
     banner("Our Valued Customers","Clients","g5.jpg"),
     "VALUED CUSTOMERS","BRAND PARTNERS","TESTIMONIALS")

page("contact.html","contact.html", f"Contact Us | {BASE}",
     "Contact Grace Distribution for diesel supply, bulk orders and partnership enquiries — 24/7.",
     banner("Contact Us","Contact","station-night.jpg"),
     "CONTACT","FAQ")

print("DONE")
