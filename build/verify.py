#!/usr/bin/env python3
"""Contrôle : chaque texte du site d'origine doit se retrouver dans la page générée."""
import html, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, 'build', 'content.json'), encoding='utf-8'))

FILES = {
    'home': 'index.html', 'chateau': 'chateau.html', 'suites': 'suites.html',
    'receptions': 'receptions.html', 'soins': 'soins-bien-etre.html',
    'services': 'services.html', 'philosophie': 'philosophie.html',
    'evenements': 'evenements.html',
    'ev-experiences': 'ev-experiences.html', 'ev-assiettes': 'ev-assiettes.html',
    'ev-manifestations': 'ev-manifestations.html', 'ev-lieux': 'ev-lieux.html',
    'suite-edouard-vii': 'suite-edouard-vii.html', 'suite-coco': 'suite-coco.html',
    'suite-wanamaker': 'suite-wanamaker.html',
    'suite-les-petits-points': 'suite-les-petits-points.html',
    'suite-oscar-ii': 'suite-oscar-ii.html', 'suite-le-phare': 'suite-le-phare.html',
    'suite-les-estampes': 'suite-les-estampes.html',
    'suite-lexplorateur': 'suite-lexplorateur.html',
}


def norm(s):
    s = html.unescape(s)
    s = unicodedata.normalize('NFC', s)
    s = s.replace(' ', ' ').replace(' ', ' ')
    s = re.sub(r'\s+', ' ', s)
    # « Biarritz » est volontairement rendu en capitales (règle de marque) :
    # on compare donc ce mot sans tenir compte de la casse.
    s = re.sub(r'biarritz', 'Biarritz', s, flags=re.IGNORECASE)
    return s.strip()


def page_text(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return norm(s)


missing = []
checked = 0
for page, fn in FILES.items():
    path = os.path.join(ROOT, fn)
    if not os.path.exists(path):
        missing.append((page, fn, '<<FICHIER ABSENT>>'))
        continue
    text = page_text(path)
    for blk in C[page]:
        if blk['t'] not in ('txt', 'h1', 'h2', 'h3'):
            continue
        raw = blk['text']
        if 'weglot' in raw:
            continue
        for line in [l for l in re.split(r'\n', raw) if l.strip()]:
            frag = norm(line)
            if len(frag) < 3:
                continue
            checked += 1
            if frag not in text:
                missing.append((page, fn, frag))

print(f'Fragments de texte vérifiés : {checked}')
if missing:
    print(f'\n❌ {len(missing)} fragment(s) absent(s) :\n')
    for page, fn, frag in missing[:40]:
        print(f'  [{page} → {fn}] {frag[:150]}')
    sys.exit(1)
print('✅ Tous les textes du site d’origine sont présents.')
