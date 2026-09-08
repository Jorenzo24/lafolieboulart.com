"""Page d'accueil — structure et mise en forme reprises du site d'origine."""
from build import (
    T, IM, A, img_src, url, e, paras, lines, rule, btn, picture,
    page, showcase, split, title, btn_row, vimeo,
)

P = 'home'


def build():
    # --- visuels ---
    palais_img, palais_alt = IM(P, 4)          # Print-052 (extérieur)
    entree_img, entree_alt = IM(P, 16)         # Print-049 (entrée)
    chef_img, chef_alt = IM(P, 59)             # Chef-chateau
    the_img, the_alt = IM(P, 60)               # the-salon
    colonnes = (img_src('colonnes-chateau.jpg'), 'Colonnes du hall central')
    baigneuses_img, baigneuses_alt = IM(P, 84)
    portrait_img, portrait_alt = IM(P, 85)

    # --- galeries : rangée de 2 (1024x558) puis rangée de 3 (1024x683) ---
    # « Nos Suites » : l'original n'affiche que la rangée de 2 puis le carrousel.
    suites_2 = [IM(P, 25), IM(P, 26)]
    suites_carousel = [IM(P, i) for i in (31, 32, 33, 34, 35, 36, 37, 38)]

    spa_2 = [IM(P, 50), IM(P, 51)]
    spa_3 = [IM(P, 52), IM(P, 53), IM(P, 54)]

    rec_2 = [IM(P, 70), IM(P, 71)]
    rec_3 = [IM(P, 72), IM(P, 73), IM(P, 74)]

    # Le bloc 86 réunit le titre du mot des propriétaires et son premier paragraphe.
    mots = T(P, 86).split('\n\n', 1)
    mots_titre, mots_corps = mots[0].strip(), mots[1].strip()

    body = f'''
<section class="hero hero--film">
  <div class="hero__media">
    <video data-hero-video data-src="assets/img/LFB.mp4"
           poster="assets/img/LFB-poster.webp"
           muted loop playsinline autoplay preload="none" aria-label="La Folie Boulart en vidéo"></video>
  </div>
  <div class="hero-scroll" aria-hidden="true">
    <span>Découvrir</span>
    <span class="hero-scroll__line"></span>
  </div>
</section>

<section class="section section--intro">
  <div class="wrap-1140">
    <div class="intro reveal">
      <img class="intro__logo" src="{img_src('boulart-or-aplat-exe-2-1024x636.png')}" alt="La Folie Boulart — BIARRITZ 1881" width="1024" height="636">
      <h1 class="intro__title">{lines(T(P, 0))}</h1>
      {rule()}
      <div class="prose prose--lead">{paras(T(P, 2))}{paras(T(P, 3))}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-1300">
    {split(
        picture(palais_img, palais_alt),
        f"""{title(T(P, 5), 'start')}
      <div class="prose">{paras(T(P, 6))}{paras(T(P, 7))}</div>
      {btn_row(btn(url(A(P, 8)), T(P, 9)), 'start')}""", middle=True)}
  </div>
</section>

<section class="section">
  <div class="wrap-1300">
    {split(
        f"""{title(T(P, 10), 'end')}
      <div class="prose">{paras(T(P, 11))}{paras(T(P, 12))}{paras(T(P, 13))}</div>
      {btn_row(btn(url(A(P, 14)), T(P, 15)), 'end')}""",
        picture(entree_img, entree_alt), middle=True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(P, 17))}</h2>
      {rule()}
      <div class="prose prose--center">{paras(T(P, 19))}{paras(T(P, 20))}</div>
      <p style="margin-top:1.75rem">{btn(url(A(P, 21)), T(P, 22))}</p>
    </div>
  </div>
  {showcase(suites_2, None, suites_carousel)}
</section>

<section class="banner">
  <div class="banner__media">{picture(img_src('plage-biarritz-1.jpeg'), 'La plage de Biarritz')}</div>
  <div class="banner__inner">
    <h2 class="banner__title reveal">{lines(T(P, 39))}</h2>
    <p class="banner__sub reveal reveal-d1">{lines(T(P, 40))}</p>
    <p class="reveal reveal-d2" style="margin-top:1.75rem">{btn(url(A(P, 41)), T(P, 42), light=True)}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(P, 43))}</h2>
      {rule()}
      <div class="prose prose--center">{paras(T(P, 45))}{paras(T(P, 46))}</div>
      <p style="margin-top:1.75rem">{btn(url(A(P, 47)), T(P, 48))}</p>
    </div>
  </div>
  {showcase(spa_2, spa_3)}
</section>

<section class="section">
  <div class="wrap-1140">
    {split(
        f"""{title(T(P, 55), 'start')}
      <div class="prose">{paras(T(P, 56))}</div>
      {btn_row(btn(url(A(P, 57)), T(P, 58)), 'end')}
      {picture(chef_img, chef_alt)}""",
        f"""{picture(the_img, the_alt)}
      {title(T(P, 61), 'start')}
      <div class="prose">{paras(T(P, 62))}</div>
      {btn_row(btn(url(A(P, 63)), T(P, 64)), 'end')}""")}
  </div>
</section>

<section class="section">
  <div class="wrap-1140">
    {split(
        f"""{title(T(P, 65), 'end')}
      <div class="prose">{paras(T(P, 66))}</div>
      {btn_row(btn(url(A(P, 67)), T(P, 68)), 'end')}""",
        vimeo('868256643', 'Visite 3D de La Folie Boulart'), middle=True, ratio='45-55')}
  </div>
  {showcase(rec_2, rec_3)}
</section>

<section class="section">
  <div class="wrap-1300">
    {split(
        picture(*colonnes),
        f"""{title(T(P, 76), 'start')}
      <div class="prose">{paras(T(P, 77))}</div>
      {btn_row(btn(url(A(P, 78)), T(P, 79)), 'start')}""", middle=True)}
  </div>
</section>

<section class="section">
  <div class="wrap-1300">
    {split(
        f"""{title(T(P, 80), 'end', ink=True)}
      <div class="prose">{paras(T(P, 81))}</div>
      {btn_row(btn(url(A(P, 82)), T(P, 83)), 'end')}""",
        picture(baigneuses_img, baigneuses_alt), middle=True)}
  </div>
</section>

<section class="section">
  <div class="wrap-1140">
    <div class="split split--middle owners">
      <div class="split__col reveal">
        <img class="owners__portrait" src="{portrait_img}" alt="{e(portrait_alt)}" loading="lazy" decoding="async">
      </div>
      <div class="split__col reveal reveal-d1">
        <blockquote class="quote quote--mark">
          <p>{e(mots_titre)}</p>
          {paras(mots_corps)}
        </blockquote>
      </div>
    </div>
    <div class="split" style="margin-top:clamp(2rem,5vw,3.5rem)">
      <div class="split__col reveal">
        <blockquote class="quote">{paras(T(P, 87))}</blockquote>
      </div>
      <div class="split__col reveal reveal-d1">
        <blockquote class="quote">
          {paras(T(P, 88))}
          <cite class="quote__author">{e(T(P, 89))}</cite>
        </blockquote>
      </div>
    </div>
  </div>
</section>
'''
    return page(
        'index.html',
        'La Folie Boulart⎮Hôtel Particulier Biarritz⎮Location château',
        'Au cœur de Biarritz,ouverte sur la mer et les montagnes du pays-basque,'
        'la folie Boulart renaît enfin, découvrez le.',
        body,
        'index.html',
    )
