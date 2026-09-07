#!/usr/bin/env python3
"""Générateur statique — La Folie Boulart.

Tous les textes sont lus depuis content.json (extrait du site d'origine),
jamais retapés : la fidélité mot pour mot est donc garantie par construction.
"""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT
IMG = 'assets/img'

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.json'), encoding='utf-8') as fh:
    C = json.load(fh)


# --------------------------------------------------------------------------
# Accès au contenu d'origine
# --------------------------------------------------------------------------
def T(page, i):
    """Texte exact du bloc i de la page."""
    b = C[page][i]
    assert b['t'] in ('txt', 'h1', 'h2', 'h3'), (page, i, b['t'])
    return b['text']


def IM(page, i):
    """(src webp, alt) du bloc image i."""
    b = C[page][i]
    assert b['t'] in ('img', 'bg'), (page, i, b['t'])
    name = os.path.splitext(b['src'])[0]
    return f'{IMG}/{name}.webp', b.get('alt', '')


def A(page, i):
    return C[page][i]['href']


def img_src(name):
    return f'{IMG}/{os.path.splitext(name)[0]}.webp'


# --------------------------------------------------------------------------
# Plan du site et réécriture des liens
# --------------------------------------------------------------------------
PAGES = {
    '': 'index.html',
    'chateau': 'chateau.html',
    'suites-chambres': 'suites.html',
    'suites-chambres/suite-edouard-vii': 'suite-edouard-vii.html',
    'suites-chambres/suite-coco': 'suite-coco.html',
    'suites-chambres/suite-wanamaker': 'suite-wanamaker.html',
    'suites-chambres/suite-les-petits-points': 'suite-les-petits-points.html',
    'suites-chambres/chambre-deluxe-oscar-ii': 'suite-oscar-ii.html',
    'suites-chambres/chambre-deluxe-le-phare': 'suite-le-phare.html',
    'suites-chambres/chambre-deluxe-les-estampes': 'suite-les-estampes.html',
    'suites-chambres/chambre-deluxe-lexplorateur': 'suite-lexplorateur.html',
    'receptions': 'receptions.html',
    'soins-bien-etre': 'soins-bien-etre.html',
    'services': 'services.html',
    'philosophie': 'philosophie.html',
    'evenements': 'evenements.html',
    'evenements/experiences-incontournables': 'ev-experiences.html',
    'evenements/assiettes-gourmandes': 'ev-assiettes.html',
    'evenements/manifestations-locales': 'ev-manifestations.html',
    'evenements/lieux-a-visiter': 'ev-lieux.html',
}

# Pages restées sur le site d'origine (non reprises dans ce périmètre)
EXTERNAL = 'https://lafolieboulart.fr/'

# Préproduction : la copie hébergée sur GitHub Pages ne doit pas être indexée,
# afin de ne pas concurrencer lafolieboulart.com. Passer à False le jour de la
# mise en production sur le domaine définitif.
STAGING = True


def url(href):
    """Réécrit une URL du site d'origine vers le fichier local correspondant."""
    m = re.match(r'https?://lafolieboulart\.(?:com|fr)/([^#?]*)(#.*)?$', href)
    if not m:
        return href
    path = m.group(1).strip('/')
    anchor = m.group(2) or ''
    # philosophie#histoire est parfois écrit sans slash final
    if path in PAGES:
        return PAGES[path] + anchor
    return EXTERNAL + (path + '/' if path else '') + anchor


def e(s):
    return html.escape(s, quote=True)


def paras(text):
    """Convertit un bloc de texte d'origine en paragraphes, sauts de ligne conservés."""
    chunks = [c.strip() for c in re.split(r'\n\s*\n', text.strip()) if c.strip()]
    out = []
    for c in chunks:
        out.append('<p>' + '<br>\n'.join(e(l.strip()) for l in c.split('\n') if l.strip()) + '</p>')
    return '\n'.join(out)


def lines(text):
    """Rend un titre multiligne en conservant ses retours."""
    return '<br>\n'.join(e(l.strip()) for l in text.strip().split('\n') if l.strip())


# --------------------------------------------------------------------------
# Fragments partagés
# --------------------------------------------------------------------------
NAV = [
    ('01', 'Accueil', 'index.html', None),
    ('02', 'Château', 'chateau.html', None),
    ('03', 'Nos suites', 'suites.html', [
        ('Suite Prestige Édouard VII', 'suite-edouard-vii.html'),
        ('Suite Prestige COCO', 'suite-coco.html'),
        ('Suite Prestige Wanamaker', 'suite-wanamaker.html'),
        ('Suite Supérieure les Petits Points', 'suite-les-petits-points.html'),
        ('Suite Deluxe Oscar II', 'suite-oscar-ii.html'),
        ('Suite Deluxe Le Phare', 'suite-le-phare.html'),
        ('Suite Deluxe Les Estampes', 'suite-les-estampes.html'),
        ('Suite Deluxe L’Explorateur', 'suite-lexplorateur.html'),
    ]),
    ('04', 'Réceptions', 'receptions.html', None),
    ('05', 'Soins & Bien-être', 'soins-bien-etre.html', None),
    ('06', 'Services', 'services.html', None),
    ('07', 'Philosophie', 'philosophie.html', None),
    ('08', 'Évènements', 'evenements.html', [
        ('Expériences Incontournables', 'ev-experiences.html'),
        ('Assiettes Gourmandes', 'ev-assiettes.html'),
        ('Manifestations Locales', 'ev-manifestations.html'),
        ('Lieux à Visiter', 'ev-lieux.html'),
    ]),
]

NAV_SHOTS = [
    '01-Accueil-modifié.jpg',
    '02-Philosophie-modifié.jpg',
    '03-Château-modifié.jpg',
    '04-Réceptions-modifié.jpg',
    '09-Club-8-modifié.jpg',
]

BOOKING = 'https://lafolieboulart.fr/wp-booking-calendar/'
LOGO_GOLD = img_src('boulart-or-aplat-exe-2-1024x636.png')
LOGO_WHITE = img_src('LFB-1881-blanc.png')


def header(current):
    return f'''<header class="header">
  <div class="header__inner">
    <div class="header__left">
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-panel">
        <span class="menu-toggle__bars" aria-hidden="true"><span></span><span></span><span></span></span>
        <span class="menu-toggle__label">Menu</span>
      </button>
    </div>
    <a class="header__brand" href="index.html" aria-label="La Folie Boulart — accueil">
      <img src="{LOGO_GOLD}" alt="La Folie Boulart" width="1024" height="636">
    </a>
    <div class="header__right">
      <a class="header__link" href="{EXTERNAL}galerie/">Galerie</a>
      <a class="header__cta" href="{BOOKING}">Réservation</a>
    </div>
  </div>
</header>

<div class="nav-panel" id="nav-panel" aria-hidden="true">
  <div class="nav-panel__inner">
    <nav aria-label="Navigation principale">
      <ul class="nav-list">
{nav_items(current)}
      </ul>
    </nav>
    <div class="nav-panel__media" aria-hidden="true">
{nav_media()}
    </div>
    <div class="nav-panel__foot">
      <a href="{EXTERNAL}contact/">Contact</a>
      <a href="{EXTERNAL}informations/">Informations</a>
      <a href="{EXTERNAL}blog/">Blog</a>
      <a href="{EXTERNAL}galerie/">Galerie</a>
      <a href="{BOOKING}">Réservation</a>
    </div>
  </div>
</div>'''


def nav_items(current):
    rows = []
    shot = 0
    for num, label, href, subs in NAV:
        cur = ' aria-current="page"' if href == current else ''
        sub_html = ''
        toggle = ''
        if subs:
            sid = 'sub-' + num
            toggle = (f'<button class="nav-sub-toggle" type="button" aria-expanded="false" '
                      f'aria-controls="{sid}" aria-label="Afficher les sous-pages de {e(label)}">'
                      f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
                      f'aria-hidden="true"><path d="M5 9l7 7 7-7"/></svg></button>')
            parts = []
            for s_label, s_href in subs:
                s_cur = ' aria-current="page"' if s_href == current else ''
                parts.append(f'            <li><a href="{s_href}"{s_cur}>{e(s_label)}</a></li>')
            items = '\n'.join(parts)
            sub_html = f'\n          <ul class="nav-sub" id="{sid}">\n{items}\n          </ul>'
        rows.append(
            f'        <li>\n'
            f'          <div class="nav-list__row">\n'
            f'            <a href="{href}" data-shot="{shot % len(NAV_SHOTS)}"{cur}>'
            f'<span class="nav-list__num">{num}.</span>{e(label)}</a>\n'
            f'            {toggle}\n'
            f'          </div>{sub_html}\n'
            f'        </li>')
        shot += 1
    return '\n'.join(rows)


def nav_media():
    out = []
    for i, name in enumerate(NAV_SHOTS):
        cls = ' class="is-active"' if i == 0 else ''
        out.append(f'      <img{cls} src="{img_src(name)}" alt="" loading="lazy" decoding="async">')
    return '\n'.join(out)


FOOTER = f'''<footer class="footer">
  <div class="footer__logo">
    <img src="{LOGO_WHITE}" alt="La Folie Boulart 1881" width="1245" height="848" loading="lazy">
  </div>
  <div class="footer__rule footer__rule--top" aria-hidden="true"></div>

  <div class="footer__cols">
    <div class="footer__mark">
      <img src="{img_src('logo-monument-historique.png')}" alt="Monument historique — Biarritz" loading="lazy">
    </div>
    <nav aria-label="Liens du pied de page">
      <ul class="footer__nav">
        <li><a href="{EXTERNAL}contact/">Contact</a></li>
        <li><a href="{EXTERNAL}informations/">Informations</a></li>
        <li><a href="{EXTERNAL}blog/">Blog</a></li>
        <li><a href="{EXTERNAL}galerie/">Galerie</a></li>
      </ul>
    </nav>
    <div class="footer__social">
      <a href="https://www.instagram.com/lafolieboulart/" aria-label="Instagram" rel="noopener" target="_blank">
        <img src="{img_src('ig-icon-1.png')}" alt="" loading="lazy">
      </a>
      <a href="https://www.youtube.com/channel/UC5Mew3mgAWNC7L8HnJZfQiA/featured" aria-label="YouTube" rel="noopener" target="_blank">
        <img src="{img_src('yt.png')}" alt="" loading="lazy">
      </a>
    </div>
  </div>

  <div class="footer__rule footer__rule--bottom" aria-hidden="true"></div>

  <p class="footer__contact">
    <a href="tel:+33559239310">+33 5 59 23 93 10</a> – 12, Allée du Château, 64200, Biarritz
  </p>

  <div class="footer__legal">
    <a href="{EXTERNAL}conditions-generales/">Conditions générales</a>
    <a href="{EXTERNAL}politique-de-confidentialite/">Politique de confidentialité</a>
  </div>

  <p class="footer__credit">
    Conception <a href="https://lawebfactory.com" rel="noopener" target="_blank">Joseph Lambert – La Web Factory</a>
  </p>
</footer>'''


def page(filename, title, description, body, current, og_image=None):
    og = og_image or img_src('Chateau-de-la-Folie-Boulart-.-Print-.-052-copie.png')
    doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{'<meta name="robots" content="noindex, nofollow">' if STAGING else ''}
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="https://lafolieboulart.com/{'' if filename == 'index.html' else filename}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="La Folie Boulart">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{img_src('cropped-cropped-logo-la-foulie-boulart-1-192x192.png')}">
<link rel="apple-touch-icon" href="{img_src('cropped-cropped-logo-la-foulie-boulart-1-180x180.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="assets/fonts/Canela-Light.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Aller au contenu</a>
{header(current)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, filename), 'w', encoding='utf-8') as fh:
        fh.write(doc)
    return filename


# --------------------------------------------------------------------------
# Briques de mise en page
# --------------------------------------------------------------------------
def btn(href, label, light=False, solid=False):
    cls = 'btn' + (' btn--light' if light else '') + (' btn--solid' if solid else '')
    return f'<a class="{cls}" href="{href}"><span>{e(label)}</span></a>'


def rule(horizontal=False, left=False):
    cls = 'rule' + (' rule--h' if horizontal else '') + (' rule--left' if left else '')
    return f'<div class="{cls}" aria-hidden="true"></div>'


def picture(src, alt, cls='', w=None, h=None, eager=False, lightbox=False):
    attrs = f' class="{cls}"' if cls else ''
    dims = f' width="{w}" height="{h}"' if w else ''
    load = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    lb = ' data-lightbox' if lightbox else ''
    return f'<img{attrs} src="{src}" alt="{e(alt)}"{dims}{load}{lb}>'


def slider(images, autoplay=5000, tall=False, lightbox=True):
    slides = '\n'.join(
        f'        <div class="slider__slide" role="group" aria-roledescription="diapositive" '
        f'aria-label="{i + 1} sur {len(images)}">{picture(src, alt, lightbox=lightbox)}</div>'
        for i, (src, alt) in enumerate(images))
    cls = 'slider slider--tall' if tall else 'slider'
    return f'''<div class="{cls}" data-slider data-autoplay="{autoplay}" tabindex="0" role="region" aria-roledescription="carrousel" aria-label="Galerie photos">
  <div class="slider__viewport">
    <div class="slider__track">
{slides}
    </div>
  </div>
  <button class="slider__btn slider__btn--prev" type="button" aria-label="Image précédente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M15 4l-8 8 8 8"/></svg></button>
  <button class="slider__btn slider__btn--next" type="button" aria-label="Image suivante"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M9 4l8 8-8 8"/></svg></button>
  <div class="slider__dots"></div>
</div>'''


def gallery(images, wide_first=False):
    items = []
    for i, (src, alt) in enumerate(images):
        cls = 'gallery__item gallery__item--wide' if (wide_first and i == 0) else 'gallery__item'
        items.append(f'  <figure class="{cls}" data-lightbox>{picture(src, alt)}</figure>')
    return '<div class="gallery">\n' + '\n'.join(items) + '\n</div>'


def page_hero(src, alt, title, eyebrow=None, h1=True):
    tag = 'h1' if h1 else 'p'
    eb = f'<p class="eyebrow reveal">{e(eyebrow)}</p>' if eyebrow else ''
    return f'''<section class="page-hero">
  <div class="page-hero__media">{picture(src, alt, eager=True)}</div>
  <div class="page-hero__inner">
    {eb}
    <{tag} class="page-hero__title reveal reveal-d1">{lines(title)}</{tag}>
    {rule(True)}
  </div>
</section>'''


def duo(media_html, body_html, reverse=False, tall=False):
    cls = 'duo duo--reverse' if reverse else 'duo'
    mcls = 'duo__media duo__media--tall' if tall else 'duo__media'
    return f'''<div class="{cls}">
  <div class="{mcls} reveal">{media_html}</div>
  <div class="duo__body reveal reveal-d1">{body_html}</div>
</div>'''


def feature(title, body, tid=None):
    idattr = f' id="{tid}"' if tid else ''
    if not title:
        return f'''<div class="prose reveal"{idattr}>{body}</div>'''
    return f'''<article class="feature reveal"{idattr}>
  <h2 class="feature__title">{lines(title)}</h2>
  <div class="prose">{body}</div>
</article>'''


# --------------------------------------------------------------------------
# Blocs repris du site d'origine
# --------------------------------------------------------------------------
CREST = img_src('logo-or2-1024x792.png')


def showcase(row2, row3, carousel_imgs=None, crest=True):
    """Bloc galerie de l'original : médaillon en débord, rangée de 2, rangée de 3,
    puis éventuellement le carrousel à trois vues."""
    crest_html = ''
    if crest:
        crest_html = (f'<div class="showcase__crest" aria-hidden="true">'
                      f'<img src="{CREST}" alt="" loading="lazy" decoding="async"></div>')

    def cells(pairs):
        return '\n'.join(
            f'      <figure class="showcase__cell" data-lightbox style="margin:0">'
            f'{picture(src, alt)}</figure>' for src, alt in pairs)

    rows = ''
    if row2:
        rows += f'\n    <div class="showcase__row showcase__row--2">\n{cells(row2)}\n    </div>'
    if row3:
        rows += f'\n    <div class="showcase__row showcase__row--3">\n{cells(row3)}\n    </div>'

    car = ''
    if carousel_imgs:
        slides = '\n'.join(
            f'        <div class="carousel__slide" role="group" aria-roledescription="diapositive" '
            f'aria-label="{i + 1} sur {len(carousel_imgs)}" data-lightbox>{picture(src, alt)}</div>'
            for i, (src, alt) in enumerate(carousel_imgs))
        car = f'''
  <div class="carousel" data-carousel data-autoplay="5000" tabindex="0" role="region"
       aria-roledescription="carrousel" aria-label="Galerie photos">
    <div class="carousel__viewport">
      <div class="carousel__track">
{slides}
      </div>
    </div>
    <button class="carousel__btn carousel__btn--prev" type="button" aria-label="Images précédentes"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M15 4l-8 8 8 8"/></svg></button>
    <button class="carousel__btn carousel__btn--next" type="button" aria-label="Images suivantes"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M9 4l8 8-8 8"/></svg></button>
    <div class="carousel__dots"></div>
  </div>'''

    return f'''<div class="showcase reveal">
  <div class="showcase__band">
    {crest_html}{rows}
  </div>{car}
</div>'''


def split(col1, col2, middle=False, ratio=None):
    """Deux colonnes, comme les sections d'origine.

    middle : centrage vertical (align-items:center dans le CSS source).
    ratio  : '45-55' pour la section Réceptions.
    """
    cls = 'split'
    if middle:
        cls += ' split--middle'
    if ratio:
        cls += f' split--{ratio}'
    return f'''<div class="{cls}">
  <div class="split__col reveal">{col1}</div>
  <div class="split__col reveal reveal-d1">{col2}</div>
</div>'''


def title(text, align='start', ink=False):
    cls = 'section__title'
    cls += ' section__title--ink' if ink else ''
    cls += ' section__title--start' if align == 'start' else (' section__title--end' if align == 'end' else '')
    return f'<h2 class="{cls}">{lines(text)}</h2>'


def btn_row(html, align='start'):
    return f'<p class="btn-row btn-row--{align}">{html}</p>'


def vimeo(video_id, label):
    return (f'<div class="video-embed">'
            f'<iframe src="https://player.vimeo.com/video/{video_id}'
            f'?autoplay=1&amp;playsinline=1&amp;autopause=0&amp;loop=1&amp;muted=1'
            f'&amp;title=0&amp;portrait=0&amp;byline=0" '
            f'title="{e(label)}" allow="autoplay; fullscreen; picture-in-picture" '
            f'allowfullscreen loading="lazy"></iframe></div>')
