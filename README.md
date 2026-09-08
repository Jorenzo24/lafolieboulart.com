# La Folie Boulart — refonte statique

Reprise à l'identique de [lafolieboulart.com](https://lafolieboulart.com) (WordPress /
OceanWP / Elementor) sous forme de site statique, avec un travail de design et
d'UX sur la mise en forme.

**Contenu inchangé** : tous les textes et toutes les images proviennent du site
d'origine. Les couleurs, la typographie et le découpage en sections sont conservés.

## Contenu

20 pages :

| Page | Fichier |
| --- | --- |
| 01. Accueil | `index.html` |
| 02. Château | `chateau.html` |
| 03. Nos suites | `suites.html` + 8 fiches `suite-*.html` |
| 04. Réceptions | `receptions.html` |
| 05. Soins & Bien-être | `soins-bien-etre.html` |
| 06. Services | `services.html` |
| 07. Philosophie | `philosophie.html` (ancres `#histoire`, `#palais`, `#folie`) |
| 08. Évènements | `evenements.html` + 4 pages `ev-*.html` |
| Demande de réservation | `reservation.html` |

## Charte reprise du site d'origine

| Rôle | Valeur |
| --- | --- |
| Bleu nuit | `#2c4660` (variantes `#234762`, `#43687f`, `#4e6686`) |
| Or | `#bc9744` / `#d1a754` |
| Texte | `#202020`, `#5c5c5c` |
| Titres | Canela (Light 300 / Regular 400), auto-hébergée en WOFF2 |
| Textes courants | Crimson Text |

## Améliorations apportées

- En-tête fixe qui se condense au défilement, panneau de navigation plein écran
  avec aperçu visuel au survol et sous-menus dépliables.
- Carrousels et visionneuse (lightbox) réécrits en JavaScript natif : plus de
  jQuery ni de bibliothèque Elementor (~0 dépendance externe).
- Apparition progressive des blocs au défilement (`IntersectionObserver`),
  neutralisée si `prefers-reduced-motion` est actif.
- Accessibilité : lien d'évitement, `aria-*` sur les menus, carrousels et
  visionneuse, navigation au clavier, styles de focus visibles.
- Images converties en WebP et redimensionnées (164 Mo → 44 Mo), chargement
  différé ; vidéo d'accueil ré-encodée (484 Mo → 23 Mo) avec image d'attente
  et chargement différé.
- Le film d'accueil est en cinémascope : il est affiché en entier sur mobile
  plutôt que recadré.
- Barres dorées de séparation restituées en CSS (nettes à toute résolution).

## Module de demande de réservation

`reservation.html` remplace le plugin Booking Calendar. C'est une **demande** :
rien n'est confirmé à l'envoi, et le formulaire le dit explicitement.

Parcours en trois étapes — dates, coordonnées, vérification — puis accusé de
réception. Calendrier maison sur deux mois, sélection de plage, séjour de trois
nuits minimum imposé (si l'on choisit une sortie trop proche, la plage est
étendue au minimum plutôt que refusée). Récapitulatif latéral qui se met à jour
en direct, validation par champ, champ piège anti-robot.

### Brancher l'envoi

Le module lit son point d'envoi dans l'attribut `data-endpoint`
(`build/pages_resa.py`) :

| `data-endpoint` | Comportement |
| --- | --- |
| vide (par défaut) | ouvre le message pré-rempli dans la messagerie du visiteur |
| `reservation.php` | envoi serveur — script fourni, à utiliser sur le VPS |
| URL d'un service | POST JSON vers Formspree, Web3Forms… |

`reservation.php` attend le JSON, contrôle les champs et transmet la demande à
l'adresse définie dans ses constantes `DESTINATAIRE` / `EXPEDITEUR`. Il est déjà
listé dans `.cpanel.yml`. **GitHub Pages ne sert pas le PHP** : la démonstration
en ligne fonctionne donc en mode messagerie.

## Règle de marque

**« Biarritz » s'écrit toujours BIARRITZ**, en capitales, dans tout le contenu
rendu : texte, attributs `alt`/`title`, `<title>` et `<meta description>`.

La règle vit dans `build/build.py` : la fonction `e()` l'applique à tout ce
qu'elle échappe, et `e()` ne reçoit jamais d'URL — les noms de fichiers
(`plage-biarritz-1.webp`…) restent donc intacts. `build/content.json` conserve
la graphie d'origine : la règle s'applique au rendu seulement, et
`build/verify.py` compare ce mot sans tenir compte de la casse.

## Régénérer les pages

Les pages HTML sont produites par un générateur : **ne pas les modifier
directement**, elles seraient écrasées.

```bash
python3 build/make.py       # régénère les 20 pages
python3 build/verify.py     # vérifie que chaque texte d'origine est présent
python3 build/check_assets.py  # vérifie ressources et liens internes
```

- `build/content.json` — contenu extrait du site d'origine (textes et images).
  Les textes ne sont **jamais** ressaisis : le générateur les lit par index,
  ce qui garantit la fidélité mot pour mot.
- `build/build.py` — gabarits communs (en-tête, pied de page, composants).
- `build/pages_home.py`, `build/pages_inner.py` — composition de chaque page.

## Mise en production

Cette copie est en préproduction et **interdite d'indexation**, afin de ne pas
concurrencer le site en ligne. Le jour du basculement sur le domaine définitif :

1. `STAGING = False` dans `build/build.py`, puis `python3 build/make.py`
   (retire les balises `noindex`).
2. Remplacer `robots.txt` par une version autorisant l'exploration.
3. Vérifier les URL de `sitemap.xml`.

Les pages hors périmètre (Contact, Informations, Blog, Galerie, Réservation,
mentions légales, Trésors et artistes) pointent encore vers `lafolieboulart.fr`.

## Développement local

```bash
python3 -m http.server 8899
# http://127.0.0.1:8899
```
