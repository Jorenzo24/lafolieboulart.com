"""Frise chronologique du château.

Chaque entrée est un **condensé** rédigé pour la frise : les faits viennent de
`content.json`, les formulations non. L'index de la source est indiqué en
commentaire en bout de bloc, pour qu'on puisse les recouper.

Deux choses à signaler au client, qui n'existent pas dans la source :

* **1881**, l'achèvement du château — l'année figure dans le logo
  (« BIARRITZ 1881 ») mais dans aucun texte du site d'origine, c'est le client
  qui l'a précisée (voir `CLAUDE.md`) ;
* les **titres** et les **légendes de photo**, qui sont des formulations
  nouvelles.

Les photographies sont celles du site d'origine. Les deux pièces d'archive
panoramiques — le triptyque du couple, le casino — passent en pleine largeur
sous leur texte : leur format ne supporte pas d'être recadré en 3/2.
"""
from build import e, img_src, picture

CHRONOLOGIE = [
    dict(
        an='1828',
        titre='Un maître de forges des Landes',
        txt='Charles Boulart naît à Linxe. Maître de forges à Castets, '
            'propriétaire de milliers d’hectares de pins, il est conseiller '
            'général du département. Il aime passionnément les arbres et la '
            'chasse.',                                         # philosophie[8]
    ),
    dict(
        an='1865',
        titre='Charles et Marthe',
        txt='Il épouse une Bordelaise, Marthe Darricau, petite-fille d’un '
            'général baron d’Empire et fille d’un intendant général sous '
            'Napoléon III. Proches du couple impérial, les Boulart choisissent '
            'Biarritz, la villégiature mise à la mode par l’Impératrice.',
                                                               # philosophie[9]
        img='createurs-folie-boulart.webp',
        alt='Marthe Darricau, le monogramme sculpté du couple, et Charles Boulart',
        legende='Marthe Darricau, le monogramme du couple, Charles Boulart',
        large=True,
    ),
    dict(
        an='1869',
        titre='L’architecte du Palais de Justice',
        txt='Joseph Louis Duc est lauréat du Grand Prix d’architecture créé par '
            'Napoléon III. Charles Boulart lui accordera des moyens quasiment '
            'illimités : la villa de Biarritz restera le seul chantier privé de '
            'sa carrière.',                             # philosophie[13], [14]
        img='Coupe-La-Folie-Boulart.webp',
        alt='Planche de l’Encyclopédie d’architecture : coupe de la villa',
        legende='Encyclopédie d’architecture, « Villa à Biarritz »',
        planche=True,
    ),
    dict(
        an='1872',
        court='L’acte d’achat est signé : soixante-trois mètres au-dessus de l’océan, des bois, un lac.',
        titre='Cinq hectares au-dessus de l’océan',
        txt='L’acte d’achat est signé. Il fallait un terrain et une situation '
            'exceptionnels : ce seront soixante-trois mètres au-dessus de '
            'l’océan, une vue panoramique, des bois, un lac.',
                                                               # philosophie[9]
        img='biarritz-plage-1900.webp',
        alt='Vue générale de Biarritz à la fin du XIXe siècle',
        legende='Biarritz à la fin du XIXe siècle',
    ),
    dict(
        an='1874',
        titre='La perspective de François Roux',
        txt='En novembre, les plans achevés, Roux remet à Charles Boulart une '
            'perspective qui nous montre la Villa telle qu’on peut l’admirer '
            'encore aujourd’hui, dans son élégance et sa grandeur.',
                                                              # philosophie[16]
        img='Perspectives-Villa-Mr-Boulart-scaled.webp',
        alt='Perspective de la Villa remise à Charles Boulart en novembre 1874',
        legende='« Remis à M. Boulart le 14 novembre 1874 »',
        planche=True,
    ),
    dict(
        an='1881',
        court='Des artistes de toute l’Europe, les matériaux les plus prestigieux.',
        titre='Le château est achevé',
        txt='Des artistes de toute l’Europe y sont intervenus — maître verrier, '
            'peintre, mosaïste, sculpteur — et les matériaux les plus '
            'prestigieux ont été réunis : marbres, bois précieux, pierres.',
                                                 # home[11] ; 1881 : le client
        img='Notre-dame-de-Sion-façade-Nord-Est-vers-1950.webp',
        alt='Le château photographié depuis le nord-est',
        legende='La façade nord-est',
    ),
    dict(
        an='1889',
        court='La reine Victoria est reçue au château, après bien d’autres têtes couronnées.',
        titre='La reine Victoria',
        txt='Les têtes couronnées se succèdent au château : la reine Victoria en '
            '1889, le roi de Suède Oskar II, Édouard VII, les grands-ducs russes, '
            'la duchesse de Manchester — et jusqu’à Oscar Wilde.',
                                                           # home[12], home[81]
        img='casino-biarritz-1900.webp',
        alt='Le casino de Biarritz et sa plage vers 1900',
        legende='Le casino de Biarritz à la Belle Époque',
        large=True,
    ),
    dict(
        an='2015',
        court='Sous les peintures, les moquettes et les planchers, les travaux révèlent toiles, fresques, sculptures, mosaïques.',
        titre='Les trésors enfouis',
        txt='Les travaux de mise en valeur commencent. Sous les peintures, les '
            'moquettes, les ciments et les planchers, ils révèlent toiles, '
            'fresques, sculptures, mosaïques et pierres.',          # home[87]
        img='artisanat-boulart-scaled.webp',
        alt='Un décor peint et doré révélé par les travaux',
        legende='Un décor peint révélé par les travaux',
    ),
    dict(
        an='2022',
        court='Une technologie de pointe entièrement invisible, primée en Europe.',
        titre='Une technologie invisible',
        txt='Le lustre originel retrouvé, la demeure est dotée d’une technologie '
            'de pointe entièrement invisible. Elle reçoit le 1er prix '
            'SmartBuilding Europe.',                                # home[87]
        img='chateau-boulart-nuit-1.webp',
        alt='Le château illuminé à la nuit tombée',
        legende='Le château à la nuit tombée',
    ),
]


def _entree(d, i, extrait=False):
    """Une entrée : la date, le corps, et la figure quand il y en a une."""
    cls = 'frise__item reveal'
    if i % 2:
        cls += ' reveal-d1'
    if extrait:
        # L'aperçu met tout en vignette : les pleines largeurs faisaient de
        # l'accueil une page d'histoire.
        if not d.get('img'):
            cls += ' frise__item--nu'
    elif d.get('large'):
        cls += ' frise__item--large'
    elif d.get('planche'):
        cls += ' frise__item--planche'
    elif not d.get('img'):
        cls += ' frise__item--nu'

    txt = d['court'] if extrait and d.get('court') else d['txt']

    fig = ''
    if d.get('img'):
        planche = d.get('planche') and not extrait
        cls_img = 'frise__img frise__img--planche' if planche else 'frise__img'
        img = picture(img_src(d['img']), d['alt'], cls=cls_img, lightbox='frise')
        legende = ''
        if d.get('legende'):
            legende = ('<figcaption class="frise__legende">'
                       + e(d['legende']) + '</figcaption>')
        fig = '      <figure class="frise__fig">' + img + legende + '</figure>\n'

    return ('    <li class="' + cls + '">\n'
            '      <p class="frise__an">' + d['an'] + '</p>\n'
            '      <div class="frise__corps">\n'
            '        <h3 class="frise__titre">' + e(d['titre']) + '</h3>\n'
            '        <p class="frise__txt">' + e(txt) + '</p>\n'
            '      </div>\n'
            + fig +
            '    </li>')


def frise(annees=None, extrait=False):
    """Rend la frise.

    annees  : n'afficher que ces dates, sinon toutes.
    extrait : marque la version courte de l'accueil.
    """
    entrees = CHRONOLOGIE
    if annees:
        entrees = [d for d in CHRONOLOGIE if d['an'] in annees]
        manquantes = set(annees) - {d['an'] for d in entrees}
        assert not manquantes, 'dates absentes de CHRONOLOGIE : %s' % manquantes

    cls = 'frise frise--extrait' if extrait else 'frise'
    return ('<ol class="' + cls + '">\n'
            + '\n'.join(_entree(d, i, extrait) for i, d in enumerate(entrees))
            + '\n  </ol>')
