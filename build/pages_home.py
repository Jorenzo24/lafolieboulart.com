"""Page d'accueil."""
from build import (
    T, IM, A, img_src, url, e, paras, lines, rule, btn, picture,
    slider, gallery, duo, page, EXTERNAL,
)

P = 'home'


def build():
    intro_img, intro_alt = IM(P, 4)
    entree_img, entree_alt = IM(P, 16)

    suites_gallery = [IM(P, i) for i in (25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38)]
    spa_gallery = [IM(P, i) for i in (50, 51, 52, 53, 54)]
    rec_gallery = [IM(P, i) for i in (70, 71, 72, 73, 74, 75)]

    chef_img, chef_alt = IM(P, 59)
    the_img, the_alt = IM(P, 60)
    baigneuses_img, baigneuses_alt = IM(P, 84)
    portrait_img, portrait_alt = IM(P, 85)

    # Le bloc 86 réunit le titre de la section et son premier paragraphe.
    mots = T(P, 86).split('\n\n', 1)
    mots_titre = mots[0].strip()
    mots_corps = mots[1].strip()

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
  <div class="wrap">
    <div class="section__head reveal">
      <img class="intro__logo" src="{img_src('boulart-or-aplat-exe-2-1024x636.png')}" alt="La Folie Boulart — Biarritz 1881" width="1024" height="636">
      <h1 class="intro__title">{lines(T(P, 0))}</h1>
      {rule()}
    </div>
    <div class="prose prose--center prose--lead reveal reveal-d1">
      {paras(T(P, 2))}
      {paras(T(P, 3))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-wide">
    {duo(
        picture(intro_img, intro_alt),
        f"""<h2 class="section__title">{lines(T(P, 5))}</h2>
      {rule(True, True)}
      <div class="prose">{paras(T(P, 6))}{paras(T(P, 7))}</div>
      {btn(url(A(P, 8)), T(P, 9))}""")}
  </div>
</section>

<section class="section section--paper">
  <div class="wrap-wide">
    {duo(
        picture(entree_img, entree_alt),
        f"""<h2 class="section__title">{lines(T(P, 10))}</h2>
      {rule(True, True)}
      <div class="prose">{paras(T(P, 11))}{paras(T(P, 12))}{paras(T(P, 13))}</div>
      {btn(url(A(P, 14)), T(P, 15))}""",
        reverse=True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(P, 17))}</h2>
      {rule()}
      <div class="prose">{paras(T(P, 19))}{paras(T(P, 20))}</div>
      <p style="margin-top:2rem">{btn(url(A(P, 21)), T(P, 22))}</p>
    </div>
  </div>
  <div class="wrap-wide reveal">
    {slider(suites_gallery)}
  </div>
</section>

<section class="banner">
  <div class="banner__media">{picture(img_src('plage-biarritz-1.jpeg'), 'La plage de Biarritz')}</div>
  <div class="banner__inner">
    <h2 class="banner__title reveal">{lines(T(P, 39))}</h2>
    <p class="banner__sub reveal reveal-d1">{lines(T(P, 40))}</p>
    <p class="reveal reveal-d2" style="margin-top:1.75rem">{btn(url(A(P, 41)), T(P, 42), light=True)}</p>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(P, 43))}</h2>
      {rule()}
      <div class="prose">{paras(T(P, 45))}{paras(T(P, 46))}</div>
      <p style="margin-top:2rem">{btn(url(A(P, 47)), T(P, 48))}</p>
    </div>
  </div>
  <div class="wrap-wide reveal">
    {slider(spa_gallery)}
  </div>
</section>

<section class="section">
  <div class="wrap-wide">
    {duo(
        picture(chef_img, chef_alt),
        f"""<h2 class="section__title">{lines(T(P, 55))}</h2>
      {rule(True, True)}
      <div class="prose">{paras(T(P, 56))}</div>
      {btn(url(A(P, 57)), T(P, 58))}""")}
  </div>
</section>

<section class="section section--paper">
  <div class="wrap-wide">
    {duo(
        picture(the_img, the_alt),
        f"""<h2 class="section__title">{lines(T(P, 61))}</h2>
      {rule(True, True)}
      <div class="prose">{paras(T(P, 62))}</div>
      {btn(url(A(P, 63)), T(P, 64))}""",
        reverse=True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <h2 class="section__title section__title--lg">{lines(T(P, 65))}</h2>
      {rule()}
      <div class="prose">{paras(T(P, 66))}</div>
      <p style="margin-top:2rem">{btn(url(A(P, 67)), T(P, 68))}</p>
    </div>
  </div>
  <div class="wrap-wide reveal">
    {slider(rec_gallery)}
  </div>
</section>

<section class="section section--navy">
  <div class="wrap-wide">
    <div class="stack">
      <div class="reveal">
        <h2 class="section__title">{lines(T(P, 76))}</h2>
        {rule(True, True)}
        <div class="prose">{paras(T(P, 77))}</div>
        <p style="margin-top:1.75rem">{btn(url(A(P, 78)), T(P, 79), light=True)}</p>
      </div>
      <div class="reveal reveal-d1">
        <h2 class="section__title">{lines(T(P, 80))}</h2>
        {rule(True, True)}
        <div class="prose">{paras(T(P, 81))}</div>
        <p style="margin-top:1.75rem">{btn(url(A(P, 82)), T(P, 83), light=True)}</p>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <figure class="reveal" style="margin:0">
    {picture(baigneuses_img, baigneuses_alt)}
  </figure>
</section>

<section class="section section--paper">
  <div class="wrap-wide">
    {duo(
        picture(portrait_img, portrait_alt),
        f"""<h2 class="section__title">{lines(mots_titre)}</h2>
      {rule(True, True)}
      <div class="prose">{paras(mots_corps)}{paras(T(P, 87))}{paras(T(P, 88))}</div>
      <p class="signature">{e(T(P, 89))}</p>""",
        tall=True)}
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
