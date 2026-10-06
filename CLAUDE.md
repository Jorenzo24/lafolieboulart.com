# La Folie Boulart — consignes de travail

Site statique refait à partir du WordPress d'origine (lafolieboulart.com).
Lire ce fichier en entier avant toute modification. Le `README.md` complète
avec l'architecture détaillée.

## Règle absolue : ne jamais éditer les fichiers HTML

Les 21 pages `.html` de la racine sont **générées**. Les modifier directement
ne sert à rien : elles seront écrasées au prochain build.

Tout passe par `build/` :

| Fichier | Rôle |
| --- | --- |
| `build/content.json` | contenu extrait du site d'origine — **ne pas retoucher** |
| `build/build.py` | gabarits communs : en-tête, pied de page, composants |
| `build/pages_home.py` | page d'accueil |
| `build/pages_resa.py` | demande de réservation |
| `build/pages_inner.py` | château, suites, réceptions, soins, services, évènements |
| `build/make.py` | point d'entrée |

```bash
python3 build/make.py          # régénère les 21 pages
python3 build/verify.py        # 601 fragments de texte d'origine doivent être présents
python3 build/check_assets.py  # ressources et liens internes
```

**Lancer les deux contrôles après chaque build**, avant tout commit. Ils ont
rattrapé plusieurs régressions : textes perdus, images manquantes, liens morts.

## Fidélité au contenu

Les textes viennent de `content.json` et sont lus **par index**, jamais
ressaisis. C'est ce qui garantit la reprise mot pour mot du site d'origine.
Pour ajouter un texte qui n'existe pas dans la source, l'écrire en clair dans
le gabarit — et signaler au client que c'est une formulation nouvelle.

**Ne jamais inventer de chiffre.** Tout nombre affiché (surfaces, capacités,
hectares) doit se trouver dans `content.json`. Un « jusqu'à seize personnes »
avait été déduit de 8 suites × 2 : c'était faux, et le client aurait pu se le
voir opposer.

## Règle de marque : BIARRITZ

**« Biarritz » s'écrit toujours BIARRITZ**, en capitales, dans tout le contenu
rendu : texte, `alt`, `title`, `<title>`, `meta description`.

Appliquée au rendu par la fonction `e()` de `build/build.py`, qui ne reçoit
jamais d'URL. **Ne jamais toucher aux noms de fichiers** (`plage-biarritz-1.webp`
et consorts) : les chemins casseraient. `verify.py` compare ce mot sans tenir
compte de la casse.

## Charte

| Rôle | Valeur |
| --- | --- |
| Or | `#c5952e` (échantillonné sur le logo officiel), clair `#e0bc72`, foncé `#8f6a1e` |
| Bleu nuit | `#2c4660`, variantes `#234762`, `#43687f` |
| Pied de page | `#242A34` |
| Texte | `#202020`, `#5c5c5c` |
| Typographie | Canela (titres et corps), Crimson Text en secours |

Tailles reprises de l'original : desktop 40px (titres) / 25px (chapeau) /
17px (corps). Sur mobile : 27 / 19 / 17px.

## Espacements

Un seul token : `--gap-section` (96px mobile, 90px au-delà de 900px). Il régit
`.section`, `.section--tight` et `.banner`. **Ne pas créer d'espacement
concurrent** : trois sources parallèles avaient produit des écarts de 40 à
136px là où une valeur unique était attendue.

## Responsive

- Vérifier à 360 et 390px qu'aucune page n'a de `scrollWidth` supérieur à son
  viewport. Deux débordements sont déjà passés inaperçus à l'œil.
- Sur mobile, repenser les compositions plutôt que laisser l'empilement par
  défaut : deux colonnes qui s'empilent telles quelles donnent des suites de
  deux textes ou deux images.
- Le film d'accueil est en cinémascope : cadré en 16/9 sur mobile, ce qui
  préserve les titres incrustés. Ne pas rogner davantage.

## Au début de chaque session : se synchroniser

Le client travaille depuis plusieurs appareils — ordinateur, téléphone,
navigateur. **Commencer toute session locale par `git pull`**, avant la moindre
modification.

Sans cela, une session locale repart d'une copie périmée dès que du travail a
été fait depuis un autre appareil : les modifications se perdent ou le push
échoue. En session cloud, le dépôt est cloné à chaque fois, la question ne se
pose pas.

```bash
git pull --ff-only        # rien à fusionner, donc une avance rapide suffit
git log --oneline -3      # voir ce qui a été fait ailleurs
```

Si `--ff-only` refuse, c'est qu'il y a des commits locaux non poussés : le
signaler au client plutôt que de fusionner d'autorité.

## Déploiement

GitHub Pages publie depuis `main`. Un push sur `main` déclenche le build.

Site en ligne : https://jorenzo24.github.io/lafolieboulart.com/

**Pousser directement sur `main`**, sans branche ni pull request. Le client
travaille seul sur ce site et veut voir ses retours en ligne immédiatement :
une étape de validation supplémentaire ne lui apporte rien.

Avant chaque push : `python3 build/make.py`, puis `verify.py` et
`check_assets.py`. Ce sont eux le garde-fou, pas la pull request.

Le dépôt est en **préproduction** : `STAGING = True` dans `build/build.py`
ajoute `noindex` à chaque page, et `robots.txt` bloque l'exploration, pour ne
pas concurrencer le site en ligne. À basculer le jour de la mise en production.

## Points encore ouverts

À ne pas trancher seul — demander au client :

1. **Capacité d'accueil** — chiffre absent de la source. Le plus recherché par
   les visiteurs, il manque aux chiffres clés de la page réservation.
2. **Disponibilités du calendrier** — la légende annonce « Indisponible » alors
   qu'aucune date ne l'est. Soit brancher un planning, soit retirer la mention.
3. **Envoi du formulaire** — `data-endpoint` est vide, donc le module ouvre la
   messagerie du visiteur. `reservation.php` est prêt pour le VPS ; un service
   tiers est possible. Le client doit choisir.
4. **Pages hors périmètre** — Contact, Informations, Blog, Galerie, mentions
   légales et Trésors et artistes pointent encore vers le site en ligne.

## Ton des échanges

Le client est intégrateur web : parler sans détour, en français. Quand il
signale un défaut, **le mesurer avant de le corriger** plutôt que de supposer.
Plusieurs de ses retours portaient sur des causes différentes de celles qu'on
pouvait deviner — un `clamp` mal formé, une règle CSS devenue inopérante après
restructuration, une grille qui alignait des lignes sans raison.
