"""Pages intérieures : château, suites, réceptions, soins, services, philosophie, évènements."""
import json
import os

from build import (
    C, T, IM, A, img_src, url, e, paras, lines, rule, btn, picture,
    slider, gallery, duo, feature, page_hero, page,
)


def blocks(p):
    return C[p]


def texts(p):
    """Indices des blocs textuels d'une page."""
    return [i for i, b in enumerate(C[p]) if b['t'] in ('txt', 'h1', 'h2', 'h3')]


def imgs(p):
    return [i for i, b in enumerate(C[p]) if b['t'] in ('img', 'bg')]


def is_rule(p, i):
    return C[p][i]['t'] == 'img' and 'barre-or' in C[p][i]['src']


def photo_indices(p):
    """Images de contenu (hors barres dorées et filets décoratifs)."""
    out = []
    for i, b in enumerate(C[p]):
        if b['t'] not in ('img', 'bg'):
            continue
        s = b['src']
        if 'barre-or' in s or 'logo-or2' in s or 'Capture-decran-2024-04-22' in s:
            continue
        out.append(i)
    return out


# --------------------------------------------------------------------------
# 03. Nos suites
# --------------------------------------------------------------------------
SUITES = [
    ('suite-edouard-vii.html', 3, 4, 5, 2),
]


def build_suites():
    p = 'suites'
    b = C[p]
    # Repérage des cartes : bg, a, titre, surface, "Visiter"
    cards = []
    i = 0
    while i < len(b):
        if b[i]['t'] == 'bg' and i + 4 < len(b) and b[i + 1]['t'] == 'a':
            src = img_src(b[i]['src'])
            href = url(b[i + 1]['href'])
            title = b[i + 2]['text']
            meta = b[i + 3]['text']
            cta = b[i + 4]['text']
            cards.append((src, href, title, meta, cta))
            i += 5
            continue
        i += 1

    cards_html = '\n'.join(
        f'''  <a class="card reveal" href="{href}">
    {picture(src, title)}
    <span class="card__body">
      <span class="card__title" style="display:block">{e(title)}</span>
      <span class="card__meta" style="display:block">{e(meta)}</span>
      <span class="card__cta">{e(cta)}</span>
    </span>
  </a>''' for src, href, title, meta, cta in cards)

    body = f'''
<section class="page-hero">
  <div class="page-hero__media">{picture(img_src('Suite-edouard-vii-de-la-Folie-Boulart-.-Print-.-029-scaled.jpg'), 'Suite Édouard VII', eager=True)}</div>
  <div class="page-hero__inner">
    <p class="eyebrow reveal">03. Nos suites</p>
    <h1 class="page-hero__title reveal reveal-d1">{lines(T(p, 0))}</h1>
    {rule(True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose prose--center prose--lead reveal">{paras(T(p, 2))}</div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap-wide">
    <div class="cards">
{cards_html}
    </div>
  </div>
</section>
'''
    return page('suites.html', 'Nos suites⎮La Folie Boulart⎮Biarritz',
                T(p, 2)[:300], body, 'suites.html')


# --------------------------------------------------------------------------
# Fiches de suite
# --------------------------------------------------------------------------
SUITE_FILES = {
    'suite-edouard-vii': ('suite-edouard-vii.html', 'Suite Prestige Édouard VII'),
    'suite-coco': ('suite-coco.html', 'Suite Prestige COCO'),
    'suite-wanamaker': ('suite-wanamaker.html', 'Suite Prestige Wanamaker'),
    'suite-les-petits-points': ('suite-les-petits-points.html', 'Suite Supérieure Les Petits Points'),
    'suite-oscar-ii': ('suite-oscar-ii.html', 'Suite Deluxe Oscar II'),
    'suite-le-phare': ('suite-le-phare.html', 'Suite Deluxe Le Phare'),
    'suite-les-estampes': ('suite-les-estampes.html', 'Suite Deluxe Les Estampes'),
    'suite-lexplorateur': ('suite-lexplorateur.html', 'Suite Deluxe L’Explorateur'),
}

SPEC_HEADS = ('CHAMBRE', 'SALLE DE BAINS', 'EQUIPEMENTS', 'DIVERS')


def build_suite(p):
    filename, label = SUITE_FILES[p]
    b = C[p]
    title = b[0]['text']
    size = b[1]['text']

    # Regroupement des caractéristiques par intitulé
    groups = []
    current = None
    for blk in b[2:]:
        if blk['t'] not in ('txt', 'h1', 'h2', 'h3'):
            continue
        txt = blk['text'].strip()
        rows = [l.strip() for l in txt.split('\n') if l.strip()]
        for row in rows:
            if row.upper() in SPEC_HEADS:
                current = (row, [])
                groups.append(current)
            elif current is not None:
                current[1].append(row)

    specs = '\n'.join(
        f'''    <div class="specs__group reveal">
      <h2 class="specs__title">{e(head)}</h2>
      <ul class="specs__list">
{chr(10).join('        <li>' + e(item) + '</li>' for item in items)}
      </ul>
    </div>''' for head, items in groups if items)

    photos = [IM(p, i) for i in photo_indices(p)]
    hero_src, hero_alt = photos[0] if photos else (img_src('suite-chateau-boulart.jpg'), title)

    gal = ''
    if len(photos) > 1:
        gal = f'''
<section class="section section--paper">
  <div class="wrap-wide reveal">
    {slider(photos, tall=True)}
  </div>
</section>'''

    body = f'''
<section class="page-hero">
  <div class="page-hero__media">{picture(hero_src, hero_alt, eager=True)}</div>
  <div class="page-hero__inner">
    <p class="eyebrow reveal">Nos suites</p>
    <h1 class="page-hero__title reveal reveal-d1">{lines(title)}</h1>
    <p class="suite-size reveal reveal-d2" style="color:var(--gold-light)">{e(size)}</p>
    {rule(True)}
  </div>
</section>

<section class="section">
  <div class="wrap-wide">
    <div class="specs">
{specs}
    </div>
    <p class="reveal" style="text-align:center;margin-top:clamp(2.5rem,6vw,4rem)">
      {btn('https://lafolieboulart.fr/wp-booking-calendar/', 'Réserver cette suite', solid=True)}
      <span style="display:inline-block;width:1rem"></span>
      {btn('suites.html', 'Toutes nos suites')}
    </p>
  </div>
</section>
{gal}
'''
    return page(filename, f'{title}⎮La Folie Boulart⎮Biarritz',
                f'{title} — {size}. La Folie Boulart, hôtel particulier à Biarritz.',
                body, filename, og_image=hero_src)


# --------------------------------------------------------------------------
# Pages éditoriales à sections (réceptions, soins, services, évènements…)
# --------------------------------------------------------------------------
def editorial(p, filename, nav_current, eyebrow, title_meta, desc,
              hero_idx=0, title_idx=1, intro_idx=(), anchors=None, extra_skip=(),
              hero_image=None):
    """Rend une page en parcourant les blocs dans l'ordre du document d'origine.

    L'alternance texte / série d'images du site source est ainsi conservée.
    """
    b = C[p]
    anchors = anchors or {}
    skip = set(intro_idx) | set(extra_skip) | {title_idx}
    if hero_idx is not None:
        skip.add(hero_idx)

    if hero_image:
        hero_src, hero_alt = hero_image
    else:
        hero_src, hero_alt = IM(p, hero_idx)
    title = T(p, title_idx)

    # Parcours séquentiel : on accumule les images d'une part, les sections de l'autre.
    out = []
    photos = []
    cur = None          # section en cours : [titre, [paragraphes]]
    pending = []        # sections en attente de rendu
    alt = [True]        # alternance des fonds de section

    def flush_sections():
        if not pending:
            return
        feats = ''.join(feature(h, ''.join(paras(x) for x in bodies), tid=anchors.get(h))
                        for h, bodies in pending)
        cls = 'section section--paper' if alt[0] else 'section'
        alt[0] = not alt[0]
        out.append(f'''
<section class="{cls}">
  <div class="wrap">
    <div class="stack">
      {feats}
    </div>
  </div>
</section>''')
        pending.clear()

    def flush_photos():
        if not photos:
            return
        shots = list(photos)
        photos.clear()
        if len(shots) >= 4:
            block = gallery(shots, wide_first=True)
        else:
            block = slider(shots, tall=len(shots) < 3)
        out.append(f'''
<section class="section--tight">
  <div class="wrap-wide reveal">
    {block}
  </div>
</section>''')

    for i, blk in enumerate(b):
        if i in skip:
            continue
        if blk['t'] in ('img', 'bg'):
            src = blk['src']
            if 'barre-or' in src or 'logo-or2' in src or 'Capture-decran-2024-04-22' in src:
                continue
            pair = IM(p, i)
            if pair[0] == hero_src:
                continue
            flush_sections()
            if pair not in photos:
                photos.append(pair)
            cur = None
        elif blk['t'] == 'h2':
            flush_photos()
            cur = [blk['text'], []]
            pending.append(cur)
        elif blk['t'] in ('txt', 'h3'):
            if cur is None:
                flush_photos()
                cur = [None, []]
                pending.append(cur)
            cur[1].append(blk['text'])
    flush_photos()
    flush_sections()

    # Les sections sans titre sont rendues en simple prose.
    body_sections = ''.join(out)

    intro_html = ''
    if intro_idx:
        intro = ''.join(paras(T(p, i)) for i in intro_idx)
        intro_html = f'''
<section class="section">
  <div class="wrap">
    <div class="prose prose--center prose--lead reveal">{intro}</div>
  </div>
</section>'''

    body = f'''
{page_hero(hero_src, hero_alt, title, eyebrow=eyebrow)}
{intro_html}
{body_sections}
'''
    return page(filename, title_meta, desc, body, nav_current, og_image=hero_src)


# --------------------------------------------------------------------------
# 07. Philosophie — trois chapitres ancrés (#histoire, #palais, #folie)
# --------------------------------------------------------------------------
def build_philosophie():
    p = 'philosophie'
    b = C[p]

    def txt(i):
        return paras(T(p, i))

    def shots(idx):
        return [IM(p, i) for i in idx]

    def media(idx):
        pics = shots(idx)
        if not pics:
            return ''
        block = gallery(pics, wide_first=True) if len(pics) >= 4 else slider(pics, tall=len(pics) < 3)
        return f'''
  <div class="wrap-wide reveal" style="margin-top:clamp(2rem,5vw,3.5rem)">
    {block}
  </div>'''

    hero_src, hero_alt = IM(p, 0)

    # Le titre du chapitre est déjà porté par le héros : on ne le répète pas.
    chap_histoire = f'''
<section class="section" id="histoire">
  <div class="wrap">
    <div class="section__head reveal">
      <div class="prose prose--lead">{txt(3)}</div>
    </div>
    <article class="feature reveal">
      <h2 class="feature__title">{lines(T(p, 4))}</h2>
      <div class="prose">{txt(5)}{txt(8)}{txt(9)}{txt(10)}</div>
    </article>
  </div>{media([6, 7])}
</section>'''

    chap_palais = f'''
<section class="section section--paper" id="palais">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(p, 11))}</h2>
      {rule()}
    </div>
    <div class="prose reveal">{txt(13)}{txt(14)}{txt(15)}{txt(16)}{txt(17)}{txt(18)}</div>
  </div>{media([19, 22, 23])}
  <div class="wrap" style="margin-top:clamp(2rem,5vw,3.5rem)">
    <div class="prose reveal">{txt(20)}{txt(21)}{txt(24)}</div>
  </div>{media([25, 26, 29, 30])}
  <div class="wrap" style="margin-top:clamp(2rem,5vw,3.5rem)">
    <div class="prose reveal">{txt(27)}{txt(28)}{txt(31)}{txt(32)}</div>
  </div>
</section>'''

    chap_folie = f'''
<section class="section" id="folie">
  <div class="wrap-wide reveal">
    <figure style="margin:0 0 clamp(2rem,5vw,3.5rem)">{picture(*IM(p, 33))}</figure>
  </div>
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(p, 34))}</h2>
      {rule()}
    </div>
    <div class="prose reveal">{txt(36)}{txt(38)}{txt(39)}</div>
  </div>{media([37, 40, 41])}
  <div class="wrap" style="margin-top:clamp(2rem,5vw,3.5rem)">
    <div class="prose reveal">{txt(42)}</div>
  </div>
</section>'''

    body = f'''
{page_hero(hero_src, hero_alt, T(p, 1), eyebrow='07. Philosophie')}
{chap_histoire}
{chap_palais}
{chap_folie}
'''
    return page('philosophie.html', 'Philosophie⎮La Folie Boulart⎮Biarritz',
                "L’histoire des maîtres des lieux, l’architecture d’un hôtel particulier "
                "et la folie mondaine d’un palais de Biarritz.",
                body, 'philosophie.html', og_image=hero_src)


# --------------------------------------------------------------------------
# 08. Évènements — galerie puis quatre accès thématiques
# --------------------------------------------------------------------------
def build_evenements():
    p = 'evenements'
    b = C[p]
    hero_src, hero_alt = IM(p, 0)

    # Les visuels de la galerie sont portés par des liens vers les fichiers d'origine.
    gal = []
    for blk in b:
        if blk['t'] != 'a':
            continue
        href = blk['href']
        if '/wp-content/uploads/' not in href:
            continue
        name = os.path.basename(href)
        gal.append((img_src(name), ''))

    # Cartes : image de fond, lien, intitulé
    cards = []
    for i, blk in enumerate(b):
        if blk['t'] == 'bg' and i + 2 < len(b) and b[i + 1]['t'] == 'a' and b[i + 2]['t'] == 'txt':
            cards.append((img_src(blk['src']), url(b[i + 1]['href']), b[i + 2]['text']))

    cards_html = '\n'.join(
        f'''    <a class="card reveal" href="{href}">
      {picture(src, title)}
      <span class="card__body">
        <span class="card__title" style="display:block">{e(title)}</span>
        <span class="card__cta" style="margin-top:.7rem">Découvrir</span>
      </span>
    </a>''' for src, href, title in cards)

    body = f'''
{page_hero(hero_src, hero_alt, T(p, 1), eyebrow='08. Évènements')}

<section class="section">
  <div class="wrap">
    <div class="prose prose--center prose--lead reveal">{paras(T(p, 3))}</div>
  </div>
</section>

<section class="section--tight">
  <div class="wrap-wide reveal">
    {gallery(gal, wide_first=True) if gal else ''}
  </div>
</section>

<section class="section section--paper">
  <div class="wrap-wide">
    <div class="cards">
{cards_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {rule()}
    <div class="prose prose--center reveal">{paras(T(p, 31))}</div>
  </div>
</section>
'''
    return page('evenements.html', 'Expériences⎮La Folie Boulart⎮Biarritz',
                "Séjourner à la Folie Boulart est une expérience intense et inoubliable, "
                "entre océan, montagnes et art de vivre du pays basque.",
                body, 'evenements.html', og_image=hero_src)


def first_photo(p):
    """Premier visuel de contenu d'une page, utilisé comme héros."""
    idx = photo_indices(p)
    return IM(p, idx[0]) if idx else (img_src('evenements-lfb.jpeg'), '')
