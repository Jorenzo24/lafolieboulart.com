#!/usr/bin/env python3
"""Contrôle : toutes les ressources référencées existent, tous les liens internes pointent vers un fichier."""
import glob, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad_assets, bad_links, ok = [], [], 0

for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    s = open(f, encoding='utf-8').read()
    name = os.path.basename(f)
    for m in re.finditer(r'(?:src|href|data-src|poster)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(('http', 'mailto:', 'tel:', '#', 'data:')):
            continue
        path = urllib.parse.unquote(u.split('#')[0].split('?')[0])
        full = os.path.join(ROOT, path)
        if os.path.exists(full):
            ok += 1
        elif path.endswith('.html'):
            bad_links.append((name, u))
        else:
            bad_assets.append((name, u))

print(f'Références locales valides : {ok}')
if bad_assets:
    print(f'\n❌ {len(bad_assets)} ressource(s) manquante(s) :')
    for n, u in sorted(set(bad_assets))[:30]:
        print(f'  [{n}] {u}')
if bad_links:
    print(f'\n❌ {len(bad_links)} lien(s) interne(s) cassé(s) :')
    for n, u in sorted(set(bad_links))[:30]:
        print(f'  [{n}] {u}')
if not bad_assets and not bad_links:
    print('✅ Toutes les ressources et tous les liens internes sont valides.')
sys.exit(1 if (bad_assets or bad_links) else 0)
