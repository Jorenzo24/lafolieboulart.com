"""Frise chronologique du château.

Les faits proviennent tous de `content.json` ; les formulations en sont des
condensés, écrits pour la frise et non repris mot pour mot.

Exception : **1881**, l'achèvement du château. L'année figure dans le logo
(« BIARRITZ 1881 ») mais dans aucun texte du site d'origine — c'est le client
qui l'a précisée.
"""
from build import e

CHRONOLOGIE = [
    ('1828', 'Charles Boulart naît à Linxe, dans les Landes. Il sera maître de '
             'forges à Castets et conseiller général du département.'),
    ('1865', 'Il épouse Marthe Darricau, petite-fille d’un général baron '
             'd’Empire et fille d’un intendant de Napoléon III.'),
    ('1872', 'L’acte d’achat est signé : cinq hectares à soixante-trois mètres '
             'au-dessus de l’océan, avec des bois et un lac.'),
    ('1874', 'François Roux remet à Charles Boulart la perspective de la Villa, '
             'telle qu’on peut l’admirer aujourd’hui.'),
    ('1881', 'Le château est achevé.'),
    ('1889', 'La reine Victoria est reçue au château, après le roi de Suède '
             'Oskar II et Édouard VII.'),
    ('2015', 'Les travaux de mise en valeur révèlent toiles, fresques, '
             'sculptures, mosaïques et pierres enfouies sous les enduits.'),
    ('2022', 'La demeure reçoit le premier prix SmartBuilding Europe pour sa '
             'technologie de pointe, restée invisible.'),
]


def frise(annees=None, extrait=False):
    """Rend la frise.

    annees  : n'afficher que ces dates, sinon toutes.
    extrait : marque la version courte de l'accueil.
    """
    entrees = CHRONOLOGIE
    if annees:
        entrees = [x for x in CHRONOLOGIE if x[0] in annees]

    items = []
    for i, (an, txt) in enumerate(entrees):
        delai = ' reveal-d1' if i % 2 else ''
        items.append(
            '    <li class="frise__item reveal' + delai + '">\n'
            '      <span class="frise__an">' + an + '</span>\n'
            '      <p class="frise__txt">' + e(txt) + '</p>\n'
            '    </li>')

    cls = 'frise frise--extrait' if extrait else 'frise'
    return ('<ol class="' + cls + '">\n'
            + '\n'.join(items) + '\n  </ol>')
