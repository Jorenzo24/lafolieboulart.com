"""Page de demande de réservation.

Les deux phrases d'introduction sont celles du module d'origine
(lafolieboulart.com/wp-booking-calendar/), reprises mot pour mot.
"""
from build import img_src, rule, btn, picture, page, EXTERNAL

INTRO_1 = ("Remplissez le formulaire ci-dessous pour nous formuler "
           "une demande de réservation.")
INTRO_2 = ("Les réservations s’effectuent pour l’entièreté de la propriété "
           "et pour une durée minimum de 3 jours.")

OCCASIONS = [
    '', 'Séjour privé', 'Réception ou mariage', 'Séminaire ou événement d’entreprise',
    'Anniversaire ou fête de famille', 'Tournage ou séance photo', 'Autre',
]

ICON_INFO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
             'aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5v.5"/></svg>')
ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'aria-hidden="true"><path d="M4 12.5l5.2 5.2L20 7"/></svg>')


def chevron(direction):
    d = 'M15 4l-8 8 8 8' if direction == 'prev' else 'M9 4l8 8-8 8'
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'aria-hidden="true"><path d="{d}"/></svg>')


def field(name, label, kind='text', required=False, **kw):
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ''
    attrs = ' required' if required else ''
    for k, v in kw.items():
        attrs += f' {k.replace("_", "-")}="{v}"'
    if kind == 'textarea':
        control = f'<textarea id="{name}" name="{name}"{attrs}></textarea>'
    elif kind == 'select':
        opts = ''.join(
            f'<option value="{o}">{o or "— Précisez si vous le souhaitez —"}</option>'
            for o in OCCASIONS)
        control = f'<select id="{name}" name="{name}"{attrs}>{opts}</select>'
    else:
        control = f'<input id="{name}" name="{name}" type="{kind}"{attrs}>'
    return f'''<div class="field">
        <label class="field__label" for="{name}">{label}{req}</label>
        {control}
        <p class="field__error" data-error="{name}" role="alert"></p>
      </div>'''


def build():
    steps = ''.join(
        (f'<li class="steps__item" data-state="{"current" if i == 0 else "todo"}">'
         f'<span class="steps__num">{i + 1}</span>'
         f'<span class="steps__label">{lbl}</span></li>'
         + ('<li class="steps__sep" aria-hidden="true"></li>' if i < 2 else ''))
        for i, lbl in enumerate(['Séjour', 'Coordonnées', 'Confirmation']))

    body = f'''
<section class="page-hero">
  <div class="page-hero__media">{picture(img_src('Chateau-de-la-Folie-Boulart-.-Print-.-049-scaled.jpg'), 'La Folie Boulart', eager=True)}</div>
  <div class="page-hero__inner">
    <p class="eyebrow reveal">La Folie Boulart</p>
    <h1 class="page-hero__title reveal reveal-d1">Demande de réservation</h1>
    {rule(True)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose prose--center prose--lead reveal">
      <p>{INTRO_1}<br>{INTRO_2}</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-1140">
    <div class="resa" data-resa data-endpoint="" data-mailto="contact@lafolieboulart.com">

      <ol class="steps" aria-label="Étapes de la demande">{steps}</ol>

      <div class="notice">
        {ICON_INFO}
        <span>Il s’agit d’une <strong>demande</strong> : aucune réservation n’est confirmée à l’envoi.
        Notre équipe étudie votre projet et vous répond sous 24 heures avec une proposition
        et les conditions de séjour.</span>
      </div>

      <form novalidate>
        <div class="resa__grid">
          <div>

            <!-- Étape 1 : le séjour -->
            <div class="resa__panel is-active" aria-labelledby="lg-1">
              <h2 class="resa__legend" id="lg-1">Vos dates</h2>
              <p class="resa__hint">Sélectionnez votre arrivée puis votre départ. Séjour de trois nuits minimum, propriété entière.</p>

              <div class="cal">
                <div class="cal__head">
                  <button class="cal__nav cal__nav--prev" type="button" aria-label="Mois précédent">{chevron('prev')}</button>
                  <button class="cal__nav cal__nav--next" type="button" aria-label="Mois suivant">{chevron('next')}</button>
                </div>
                <div class="cal__months"></div>
                <div class="cal__legend">
                  <span class="cal__key"><span class="cal__chip cal__chip--free"></span> Disponible</span>
                  <span class="cal__key"><span class="cal__chip cal__chip--sel"></span> Votre séjour</span>
                  <span class="cal__key"><span class="cal__chip cal__chip--off"></span> Indisponible</span>
                </div>
              </div>
              <p class="field__error" data-error="dates" role="alert" style="margin-top:.75rem"></p>

              <h2 class="resa__legend" style="margin-top:2.5rem">Vos voyageurs</h2>
              <p class="resa__hint">La propriété accueille jusqu’à seize personnes dans ses huit suites.</p>
              <div class="field-row field-row--3">
                {field('adults', 'Adultes', 'number', True, min=1, max=16, value=2)}
                {field('children', 'Enfants', 'number', False, min=0, max=10, value=0)}
                {field('occasion', 'Occasion', 'select')}
              </div>

              <div class="resa__actions">
                <button class="btn btn--solid" type="button" data-next><span>Continuer</span></button>
              </div>
            </div>

            <!-- Étape 2 : les coordonnées -->
            <div class="resa__panel" aria-labelledby="lg-2">
              <h2 class="resa__legend" id="lg-2">Vos coordonnées</h2>
              <p class="resa__hint">Pour vous adresser une proposition personnalisée.</p>

              <div class="field-row field-row--2">
                {field('firstname', 'Prénom', 'text', True, autocomplete='given-name')}
                {field('lastname', 'Nom', 'text', True, autocomplete='family-name')}
              </div>
              <div class="field-row field-row--2">
                {field('email', 'E-mail', 'email', True, autocomplete='email')}
                {field('phone', 'Téléphone', 'tel', False, autocomplete='tel')}
              </div>
              {field('message', 'Votre projet', 'textarea', False,
                     placeholder='Dites-nous en quelques mots ce que vous imaginez : occasion, services souhaités, table du chef, soins au spa…')}

              <p style="position:absolute;left:-9999px" aria-hidden="true">
                <label for="website">Ne pas remplir</label>
                <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
              </p>

              <div class="resa__actions">
                <button class="btn btn--solid" type="button" data-next><span>Vérifier ma demande</span></button>
                <a class="link-back" href="#" data-back>Revenir aux dates</a>
              </div>
            </div>

            <!-- Étape 3 : la confirmation -->
            <div class="resa__panel" aria-labelledby="lg-3">
              <h2 class="resa__legend" id="lg-3">Vérification</h2>
              <p class="resa__hint">Relisez votre demande avant de nous l’adresser.</p>

              <div class="review" data-review></div>

              <label class="consent">
                <input type="checkbox" name="consent">
                <span>J’accepte que mes données soient utilisées pour traiter ma demande de réservation,
                conformément à la <a href="{EXTERNAL}politique-de-confidentialite/" target="_blank" rel="noopener">politique de confidentialité</a>.</span>
              </label>
              <p class="field__error" data-error="consent" role="alert"></p>

              <div class="resa__actions">
                <button class="btn btn--solid" type="submit" data-submit><span>Envoyer ma demande</span></button>
                <a class="link-back" href="#" data-back>Modifier mes coordonnées</a>
              </div>
            </div>

            <!-- Étape 4 : l'accusé de réception -->
            <div class="resa__panel" aria-labelledby="lg-4">
              <div class="done">
                <div class="done__mark">{ICON_CHECK}</div>
                <h2 class="done__title" id="lg-4">Votre demande nous est parvenue</h2>
                <p class="prose prose--center" style="max-width:52ch;margin-inline:auto">
                  Merci. Notre équipe revient vers vous sous 24 heures à l’adresse
                  <strong id="done-email"></strong> avec une proposition détaillée.
                  Aucune réservation n’est confirmée à ce stade.
                </p>
                <div class="done__recap">
                  <div class="summary__row"><span class="summary__key">Arrivée</span><span class="summary__val" id="done-arrival">—</span></div>
                  <div class="summary__row"><span class="summary__key">Départ</span><span class="summary__val" id="done-departure">—</span></div>
                  <div class="summary__row"><span class="summary__key">Durée</span><span class="summary__val" id="done-nights">—</span></div>
                </div>
                <p style="margin-top:2rem">{btn('index.html', 'Retour à l’accueil')}</p>
              </div>
            </div>

          </div>

          <!-- Récapitulatif latéral -->
          <aside class="summary" aria-label="Récapitulatif de votre séjour">
            <p class="summary__title">Votre séjour</p>
            <div class="summary__row"><span class="summary__key">Arrivée</span><span class="summary__val" id="sum-arrival">—</span></div>
            <div class="summary__row"><span class="summary__key">Départ</span><span class="summary__val" id="sum-departure">—</span></div>
            <div class="summary__row"><span class="summary__key">Voyageurs</span><span class="summary__val" id="sum-guests">—</span></div>
            <p class="summary__nights" id="sum-nights">—</p>
            <p class="summary__note">
              Location exclusive de la propriété, trois nuits minimum.
              Les tarifs varient selon la saison et les services retenus ; ils vous seront
              communiqués dans notre proposition.
            </p>
          </aside>
        </div>
      </form>

      <div class="resa__contact">
        <p>Vous préférez nous parler de vive voix ?</p>
        <a href="tel:+33559239310">+33 5 59 23 93 10</a>
        <p style="margin-top:.75rem">12, Allée du Château, 64200 Biarritz</p>
      </div>
    </div>
  </div>
</section>
'''
    return page(
        'reservation.html',
        'Demande de réservation⎮La Folie Boulart⎮Biarritz',
        'Formulez votre demande de réservation à La Folie Boulart, hôtel particulier '
        'à Biarritz. Location exclusive de la propriété, trois nuits minimum.',
        body,
        'reservation.html',
        extra_js='assets/js/reservation.js',
    )
