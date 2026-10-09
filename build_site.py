"""Builds the IronLog landing page in every language: ./index.html (English) and ./<code>/index.html.
Run: python build_site.py
When the iOS app is live on the App Store, set APP_STORE_LIVE = True and rebuild."""
import html, json, glob
from pathlib import Path
from strings import LANGS

HERE = Path(__file__).resolve().parent
SITE = "https://ahmeddilshadshah.github.io/ironlog-app"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.ahmeddilshadshah.ironlog"
APPLE_URL = "https://apps.apple.com/app/id6820042796"
APP_STORE_LIVE = False

SCRIPT = {"en": "latin", "es": "latin", "fr": "latin", "pt": "latin", "de": "latin", "id": "latin", "tr": "latin",
          "ru": "cyr", "ar": "arab", "ur": "arab", "hi": "indic", "bn": "indic", "ja": "cjk", "ko": "cjk", "zh": "cjk"}
ORDER = ["en", "ar", "bn", "de", "es", "fr", "hi", "id", "ja", "ko", "pt", "ru", "tr", "ur", "zh"]

icons = json.load(open(HERE / "store_icons.json", encoding="utf-8"))


def glyph_svg(name):
    g = icons[name]
    x0, y0, x1, y1 = g["bounds"]
    return (f'<svg class="ico" viewBox="{x0} {-y1} {x1 - x0} {y1 - y0}" aria-hidden="true" focusable="false">'
            f'<path transform="scale(1,-1)" fill="currentColor" d="{g["d"]}"/></svg>')


APPLE_ICO, PLAY_ICO = glyph_svg("apple"), glyph_svg("google-play")
GLOBE = ('<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/></svg>')

E = lambda s: html.escape(s, quote=True)

CSS = """
@font-face{font-family:"Bebas Neue";src:url("@@P@@assets/BebasNeue-Regular.ttf") format("truetype");font-display:swap}
@font-face{font-family:"Oswald";src:url("@@P@@assets/Oswald-Bold.ttf") format("truetype");font-weight:700;font-display:swap}
:root{
  --bg:#0c0e11; --bg-raise:#14181d; --line:#232a31; --text:#eef2f5; --muted:#97a3ae;
  --accent:#4fc3d9; --accent-ink:#06222a; --white:#fff;
  --display:"Bebas Neue","Arial Narrow",Impact,sans-serif;
  --body:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
[data-script=cyr]{--display:"Oswald","Arial Narrow",Impact,sans-serif}
[data-script=arab]{--display:"Segoe UI","Noto Naskh Arabic","Noto Sans Arabic",Tahoma,system-ui,sans-serif}
html:lang(hi),html:lang(bn){--display:"Noto Sans Devanagari","Noto Sans Bengali","Nirmala UI","Kohinoor Devanagari","Kohinoor Bangla",system-ui,sans-serif}
html:lang(ja){--display:"Hiragino Sans","Yu Gothic UI","Noto Sans JP",Meiryo,system-ui,sans-serif}
html:lang(ko){--display:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif}
html:lang(zh){--display:"PingFang SC","Microsoft YaHei UI","Noto Sans SC",system-ui,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--body);line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit}
.wrap{width:100%;max-width:1120px;margin-inline:auto;padding-inline:20px}
.skip{position:absolute;inset-inline-start:-999px;top:8px;background:var(--accent);color:var(--accent-ink);padding:8px 14px;border-radius:8px;z-index:30}
.skip:focus{inset-inline-start:12px}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:6px}

/* header */
header{position:sticky;top:0;z-index:20;background:rgba(12,14,17,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:14px}
.brand{display:flex;align-items:center;gap:12px;flex:0 0 auto}
.brand img{height:26px;width:auto}
.brand img.app-icon{height:38px;width:38px}
.tools{display:flex;align-items:center;gap:12px}
nav{display:flex;align-items:center;gap:22px;font-size:.95rem}
nav a{text-decoration:none;color:var(--muted);padding:6px 0;white-space:nowrap}
nav a:hover{color:var(--text)}
nav a.nav-cta{background:var(--accent);color:var(--accent-ink);font-weight:700;padding:9px 16px;border-radius:10px}
nav a.nav-cta:hover{color:var(--accent-ink);filter:brightness(1.08)}
@media (max-width:640px){nav a:not(.nav-cta){display:none}}
@media (max-width:470px){.brand img:not(.app-icon){display:none}.tools{gap:8px}}

/* language menu */
.lang{position:relative}
.lang summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:8px 12px;border:1px solid var(--line);border-radius:10px;color:var(--muted);font-size:.9rem;user-select:none}
.lang summary::-webkit-details-marker{display:none}
.lang summary:hover,.lang[open] summary{color:var(--text);border-color:#3a444d}
.globe{width:18px;height:18px;flex:0 0 auto}
.lang ul{position:absolute;inset-inline-end:0;top:calc(100% + 8px);margin:0;padding:6px;list-style:none;background:var(--bg-raise);border:1px solid var(--line);border-radius:14px;min-width:200px;max-height:72vh;overflow:auto;box-shadow:0 24px 60px -20px rgba(0,0,0,.85)}
.lang li a{display:block;padding:9px 12px;border-radius:9px;text-decoration:none;color:var(--text);font-size:.95rem;font-family:system-ui,"Segoe UI","Noto Sans",sans-serif}
.lang li a:hover{background:rgba(255,255,255,.06)}
.lang li a[aria-current]{background:rgba(79,195,217,.14);color:var(--accent)}
@media (max-width:640px){.lang summary .lang-name{display:none}.lang summary{padding:9px 10px}}

/* hero */
.hero{padding-block:clamp(40px,7vw,96px) clamp(48px,7vw,88px);background:radial-gradient(900px 520px at 78% 30%,rgba(79,195,217,.13),transparent 70%)}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(24px,5vw,64px);align-items:center}
.app-id{display:flex;align-items:center;gap:16px;margin:0 0 22px}
.app-icon{border-radius:22.4%;box-shadow:0 10px 30px -8px rgba(0,0,0,.7),0 0 0 1px rgba(255,255,255,.06)}
.app-id b{display:block;font-family:"Bebas Neue","Arial Narrow",Impact,sans-serif;font-weight:400;font-size:1.9rem;line-height:1;letter-spacing:.02em}
.app-id span{color:var(--muted);font-size:.92rem}
.get-head{display:flex;align-items:center;gap:18px;margin-bottom:12px}
.get-head h2{margin:0}
h1{font-family:var(--display);font-weight:400;font-size:clamp(3rem,7.4vw,5.9rem);line-height:.94;margin:0 0 22px;text-wrap:balance;letter-spacing:.01em}
h1 em{font-style:normal;color:var(--accent)}
.lede{font-size:clamp(1.05rem,2vw,1.25rem);color:var(--muted);max-width:34em;margin:0 0 28px}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.btn{display:inline-flex;align-items:center;gap:12px;padding:12px 22px;border-radius:12px;font-weight:700;text-decoration:none;font-size:1rem;border:1px solid transparent;min-height:54px}
.btn .ico{width:26px;height:26px;flex:0 0 auto}
.btn small{display:block;font-weight:500;font-size:.72rem;opacity:.8;line-height:1.2}
.btn b{display:block;line-height:1.15}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-primary:hover{filter:brightness(1.08)}
.btn-store{background:transparent;border-color:#3a444d;color:var(--text)}
.btn-store:hover{border-color:var(--accent);color:var(--accent)}
.btn-soon{background:transparent;border-color:var(--line);color:var(--muted);cursor:default}
.qr-soon{width:132px;height:132px;border-radius:12px;border:1px dashed var(--line);display:grid;place-items:center;text-align:center;color:var(--muted);font-size:.8rem;padding:10px}
.facts{display:flex;flex-wrap:wrap;gap:8px 20px;padding:0;margin:0;list-style:none;color:var(--muted);font-size:.95rem}
.facts li::before{content:"";display:inline-block;width:7px;height:7px;border-radius:2px;background:var(--accent);margin-inline-end:9px;vertical-align:middle}

.hero-art{position:relative;min-height:520px;display:flex;justify-content:center}
.phone{border-radius:34px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px -20px rgba(0,0,0,.7)}
.phone img{width:100%;height:auto}
.hero-art .p1{position:absolute;width:min(56%,270px);inset-inline-start:2%;top:36px;transform:rotate(-5deg);opacity:.9}
[dir=rtl] .hero-art .p1{transform:rotate(5deg)}
.hero-art .p2{position:relative;width:min(62%,300px);margin-inline-start:18%;z-index:1}
@media (max-width:860px){.hero .wrap{grid-template-columns:1fr}.hero-art{min-height:440px;order:2}}

/* sections */
section{padding-block:clamp(48px,7vw,88px)}
h2{font-family:var(--display);font-weight:400;font-size:clamp(2.2rem,5vw,3.6rem);line-height:1;margin:0 0 12px;letter-spacing:.01em}
.sub{color:var(--muted);max-width:40em;margin:0 0 34px}

/* gallery */
.gallery{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;list-style:none;margin:0;padding:6px max(20px,calc((100% - 1120px) / 2 + 20px)) 24px;scroll-padding-inline:max(20px,calc((100% - 1120px) / 2 + 20px));scrollbar-color:var(--line) transparent;-webkit-overflow-scrolling:touch}
.gallery li{flex:0 0 auto;width:min(66vw,270px);scroll-snap-align:start;list-style:none}
.gallery .phone{border-radius:30px}

/* features */
.features{display:grid;grid-template-columns:repeat(2,1fr);gap:0 clamp(28px,6vw,80px);list-style:none;padding:0;margin:0}
.features li{padding:22px 0;border-top:1px solid var(--line)}
.features h3{font-family:var(--display);font-weight:400;font-size:1.7rem;letter-spacing:.02em;margin:0 0 6px;color:var(--white)}
.features p{margin:0;color:var(--muted)}
@media (max-width:720px){.features{grid-template-columns:1fr}}

/* download */
.get{background:var(--bg-raise);border-block:1px solid var(--line)}
.stores{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.store{border:1px solid var(--line);border-radius:20px;padding:26px;display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;background:var(--bg)}
.store img.qr{width:132px;height:132px;border-radius:12px;background:#fff}
.store h3{font-family:"Bebas Neue","Arial Narrow",Impact,sans-serif;font-weight:400;font-size:1.9rem;margin:0 0 4px;letter-spacing:.02em}
.store p{margin:0 0 14px;color:var(--muted);font-size:.95rem}
@media (max-width:860px){.stores{grid-template-columns:1fr}}
@media (max-width:420px){.store{grid-template-columns:1fr;justify-items:start}}

footer{padding-block:34px 48px;color:var(--muted);font-size:.92rem}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px 28px;justify-content:space-between;align-items:center}
footer ul{display:flex;flex-wrap:wrap;gap:6px 22px;list-style:none;padding:0;margin:0}
footer a{text-decoration:none}
footer a:hover{color:var(--text);text-decoration:underline}

/* scripts other than Latin: no all-caps display face, so use weight and calmer sizes */
[data-script=cyr] h1{font-weight:700;font-size:clamp(2.5rem,6.2vw,4.9rem);line-height:1.04;letter-spacing:0}
[data-script=cyr] h2{font-weight:700;font-size:clamp(1.9rem,4.4vw,3rem);letter-spacing:0}
[data-script=cyr] .features h3{font-weight:700;font-size:1.35rem;letter-spacing:0}
[data-script=arab] h1,[data-script=indic] h1,[data-script=cjk] h1{font-weight:800;font-size:clamp(2.3rem,5.8vw,4.4rem);line-height:1.2;letter-spacing:0}
[data-script=arab] h2,[data-script=indic] h2,[data-script=cjk] h2{font-weight:800;font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.25;letter-spacing:0}
[data-script=arab] .features h3,[data-script=indic] .features h3,[data-script=cjk] .features h3{font-weight:800;font-size:1.3rem;letter-spacing:0}
[data-script=cjk] h1{font-size:clamp(2rem,4.5vw,3.5rem);word-break:auto-phrase;line-break:strict}
[data-script=cjk] h2{word-break:auto-phrase}
html:lang(ko) h1,html:lang(ko) h2,html:lang(ko) p,html:lang(ko) h3{word-break:keep-all}
[data-script=arab] .lede,[data-script=indic] .lede{line-height:1.85}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

REDIRECT = """<script>
(function(){try{
var codes=%s,pick=localStorage.getItem('ironlog-lang')||((navigator.language||'en').toLowerCase().split('-')[0]);
if(codes.indexOf(pick)>-1)location.replace(pick+'/'+location.hash);
}catch(e){}})();
</script>"""

MENU_JS = """<script>
(function(){
var d=document.querySelector('details.lang');if(!d)return;
d.addEventListener('click',function(e){var a=e.target.closest('a[data-lang]');if(a){try{localStorage.setItem('ironlog-lang',a.getAttribute('data-lang'))}catch(x){}}});
document.addEventListener('click',function(e){if(d.open&&!d.contains(e.target))d.open=false});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.open=false;d.querySelector('summary').focus()}});
})();
</script>"""


def page_url(code):
    return f"{SITE}/" if code == "en" else f"{SITE}/{code}/"


def build(code):
    S, shots_dir = LANGS[code][0], HERE / "assets/shots" / code
    P = "" if code == "en" else "../"
    n_shots = len(glob.glob(str(shots_dir / "*.webp")))
    dash, log = (1, 3) if n_shots == 7 else (3, 5)
    t = lambda k: E(S[k])

    def store_buttons(where):
        play = (f'<a class="btn btn-primary" href="{PLAY_URL}">{PLAY_ICO}<span><small>{t("store_get")}</small><b>Google Play</b></span></a>')
        if APP_STORE_LIVE:
            apple = (f'<a class="btn btn-store" href="{APPLE_URL}" rel="noopener">{APPLE_ICO}<span><small>{t("store_dl")}</small><b>App Store</b></span></a>')
        else:
            apple = (f'<span class="btn btn-soon" role="note">{APPLE_ICO}<span><small>{t("store_soon")}</small><b>App Store</b></span></span>')
        return play, apple

    play_btn, apple_btn = store_buttons("hero")

    lang_items = []
    for c in ORDER:
        if code == "en":
            href = "./" if c == "en" else f"{c}/"
        else:
            href = "../" if c == "en" else f"../{c}/"
        cur = ' aria-current="true"' if c == code else ""
        lang_items.append(f'<li><a href="{href}" lang="{LANGS[c][0]["html_lang"]}" hreflang="{LANGS[c][0]["html_lang"]}" data-lang="{c}"{cur}>{E(LANGS[c][0]["name"])}</a></li>')

    gallery = "\n".join(
        f'      <li><div class="phone"><img src="{P}assets/shots/{code}/{i:02d}.webp" alt="{E(S["shot_alt"].format(n=i, total=n_shots))}" width="720" height="1565" loading="lazy"></div></li>'
        for i in range(1, n_shots + 1))

    features = "\n".join(f'        <li><h3>{t(f"f{i}h")}</h3><p>{t(f"f{i}p")}</p></li>' for i in range(1, 7))

    if APP_STORE_LIVE:
        qr_apple = f'<img class="qr" src="{P}assets/qr-app-store.svg" alt="{t("qr_alt_apple")}" width="132" height="132">'
        iphone_p = t("iphone_live")
    else:
        qr_apple = f'<div class="qr-soon" role="img" aria-label="{t("qr_soon")}">{t("qr_soon")}</div>'
        iphone_p = t("iphone_soon")

    alternates = "\n".join(f'<link rel="alternate" hreflang="{LANGS[c][0]["html_lang"]}" href="{page_url(c)}">' for c in ORDER)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{page_url("en")}">'
    ld = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": S["title"], "inLanguage": S["html_lang"],
                     "applicationCategory": "HealthApplication", "operatingSystem": "Android, iOS", "description": S["desc"],
                     "image": f"{SITE}/assets/icon-384.png", "url": page_url(code)}, ensure_ascii=False)
    redirect = (REDIRECT % json.dumps([c for c in ORDER if c != "en"])) if code == "en" else ""
    locale = S["html_lang"].replace("-", "_")

    out = f"""<!doctype html>
<html lang="{S['html_lang']}" dir="{S['dir']}" data-script="{SCRIPT[code]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t('title')}</title>
<meta name="description" content="{t('desc')}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0c0e11">
<link rel="canonical" href="{page_url(code)}">
{alternates}
<link rel="icon" type="image/png" href="{P}favicon.png">
<link rel="apple-touch-icon" href="{P}apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{t('title')}">
<meta property="og:description" content="{t('og_desc')}">
<meta property="og:url" content="{page_url(code)}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<!-- Store logos: Font Awesome Free 5 Brands, CC BY 4.0 (https://fontawesome.com/license/free). Apple and Google Play are trademarks of their respective owners. -->
<script type="application/ld+json">{ld}</script>
{redirect}
<style>{CSS.replace('@@P@@', P)}</style>
</head>
<body>
<a class="skip" href="#main">{t('skip')}</a>
<header>
  <div class="wrap">
    <a class="brand" href="#top" aria-label="{t('home_aria')}"><img class="app-icon" src="{P}assets/icon-192.png" alt="" width="38" height="38"><img src="{P}assets/logo.png" alt="IronLog" width="155" height="26"></a>
    <div class="tools">
      <nav aria-label="Main">
        <a href="#screens">{t('nav_screens')}</a>
        <a href="#features">{t('nav_features')}</a>
        <a class="nav-cta" href="#download">{t('nav_get')}</a>
      </nav>
      <details class="lang">
        <summary aria-label="{t('lang_label')}">{GLOBE}<span class="lang-name">{E(S['name'])}</span></summary>
        <ul>
          {chr(10).join(lang_items)}
        </ul>
      </details>
    </div>
  </div>
</header>

<main id="main">
  <div class="hero" id="top">
    <div class="wrap">
      <div>
        <div class="app-id"><img class="app-icon" src="{P}assets/icon-384.png" alt="{t('icon_alt')}" width="84" height="84"><div><b>IronLog</b><span>{t('appid_sub')}</span></div></div>
        <h1>{t('h1a')}<br><em>{t('h1b')}</em></h1>
        <p class="lede">{t('lede')}</p>
        <div class="cta">
          {play_btn}
          {apple_btn}
        </div>
        <ul class="facts">
          <li>{t('fact1')}</li>
          <li>{t('fact2')}</li>
          <li>{t('fact3')}</li>
        </ul>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="phone p1"><img src="{P}assets/shots/{code}/{dash:02d}.webp" alt="" width="720" height="1565"></div>
        <div class="phone p2"><img src="{P}assets/shots/{code}/{log:02d}.webp" alt="" width="720" height="1565"></div>
      </div>
    </div>
  </div>

  <section id="screens" aria-labelledby="screens-h">
    <div class="wrap">
      <h2 id="screens-h">{t('screens_h')}</h2>
      <p class="sub">{t('screens_sub')}</p>
    </div>
    <ul class="gallery" tabindex="0" aria-label="{t('gallery_label')}">
{gallery}
    </ul>
  </section>

  <section id="features" aria-labelledby="features-h">
    <div class="wrap">
      <h2 id="features-h">{t('features_h')}</h2>
      <p class="sub">{t('features_sub')}</p>
      <ul class="features">
{features}
      </ul>
    </div>
  </section>

  <section class="get" id="download" aria-labelledby="download-h">
    <div class="wrap">
      <div class="get-head"><img class="app-icon" src="{P}assets/icon-192.png" alt="" width="64" height="64"><h2 id="download-h">{t('get_h')}</h2></div>
      <p class="sub">{t('get_sub')}</p>
      <div class="stores">
        <div class="store">
          <img class="qr" src="{P}assets/qr-google-play.svg" alt="{t('qr_alt_play')}" width="132" height="132">
          <div>
            <h3>Android</h3>
            <p>{t('android_p')}</p>
            {play_btn}
          </div>
        </div>
        <div class="store">
          {qr_apple}
          <div>
            <h3>iPhone</h3>
            <p>{iphone_p}</p>
            {apple_btn}
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <span>© 2026 IronLog</span>
    <ul>
      <li><a href="https://ahmeddilshadshah.github.io/IRONLOG---PRIVACY/">{t('foot_privacy')}</a></li>
      <li><a href="https://ahmeddilshadshah.github.io/IRONLOG---PRIVACY/terms.html">{t('foot_terms')}</a></li>
      <li><a href="https://ahmeddilshadshah.github.io/IRONLOG---PRIVACY/manual.html">{t('foot_guide')}</a></li>
      <li><a href="mailto:ironlog.journal@gmail.com">{t('foot_contact')}</a></li>
    </ul>
  </div>
</footer>
{MENU_JS}
</body>
</html>
"""
    target = HERE / ("index.html" if code == "en" else f"{code}/index.html")
    target.parent.mkdir(exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return target


def sitemap():
    rows = []
    for c in ORDER:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[a][0]["html_lang"]}" href="{page_url(a)}"/>' for a in ORDER)
        rows.append(f"<url><loc>{page_url(c)}</loc>{alts}</url>")
    (HERE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")
    (HERE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    for c in ORDER:
        print("built", build(c).relative_to(HERE))
    sitemap()
    print("sitemap + robots written; APP_STORE_LIVE =", APP_STORE_LIVE)
