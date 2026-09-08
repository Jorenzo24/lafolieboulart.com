#!/usr/bin/env python3
"""Point d'entrée : génère l'ensemble des pages."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pages_home
import pages_resa
import pages_inner as PI

made = []

made.append(pages_home.build())
made.append(pages_resa.build())
made.append(PI.editorial(
    'chateau', 'chateau.html', 'chateau.html', '02. Château',
    'Le Château⎮La Folie Boulart⎮Biarritz',
    "Plus d’un siècle après son édification, un château de conte de fées retrouve "
    "sa splendeur d’origine au cœur de l’élégante Biarritz.",
    intro_idx=(3,)))
made.append(PI.build_suites())

for slug in PI.SUITE_FILES:
    made.append(PI.build_suite(slug))

made.append(PI.editorial(
    'receptions', 'receptions.html', 'receptions.html', '04. Réceptions',
    'Réceptions⎮La Folie Boulart⎮Biarritz',
    "La Folie Boulart accueille les plus beaux espaces de réception de Biarritz : "
    "grand salon, salle à manger, salle de billard, salon de thé, bar, chapelle et chais.",
    intro_idx=(3,)))

made.append(PI.editorial(
    'soins', 'soins-bien-etre.html', 'soins-bien-etre.html', '05. Soins & Bien-être',
    'Soins & Bien-être⎮La Folie Boulart⎮Biarritz',
    "Le spa de La Folie Boulart : bassin de dix mètres, hammam, sauna, jacuzzi, "
    "salle de sport et salle de soins au cœur de Biarritz.",
    intro_idx=(3,)))

made.append(PI.editorial(
    'services', 'services.html', 'services.html', '06. Services',
    'Services⎮La Folie Boulart⎮Biarritz',
    "Aviation privée, chauffeur, arts de la table, conciergerie, guide touristique : "
    "à La Folie Boulart, rien d’ordinaire, tout sur mesure.",
    intro_idx=(3,)))

made.append(PI.build_philosophie())

made.append(PI.build_evenements())

made.append(PI.editorial(
    'ev-experiences', 'ev-experiences.html', 'ev-experiences.html', 'Évènements',
    'Expériences incontournables⎮La Folie Boulart⎮Biarritz',
    "Surf, golf, chasse à courre, pêche au gros, parachute, hélicoptère, pilotage "
    "et canyoning : les expériences incontournables du pays basque.",
    hero_idx=None, title_idx=0, intro_idx=(2, 3),
    hero_image=PI.first_photo('ev-experiences')))

made.append(PI.editorial(
    'ev-assiettes', 'ev-assiettes.html', 'ev-assiettes.html', 'Évènements',
    'Assiettes gourmandes⎮La Folie Boulart⎮Biarritz',
    "Les tables étoilées du pays basque et des Landes, sélectionnées par La Folie Boulart.",
    hero_idx=None, title_idx=0,
    hero_image=PI.first_photo('ev-assiettes')))

made.append(PI.editorial(
    'ev-manifestations', 'ev-manifestations.html', 'ev-manifestations.html', 'Évènements',
    'Manifestations locales⎮La Folie Boulart⎮Biarritz',
    "Ballets Malandain, cesta punta, Biarritz Piano Festival, fêtes de Bayonne, "
    "force basque et courses de trot.",
    hero_idx=None, title_idx=0,
    hero_image=PI.first_photo('ev-manifestations')))

made.append(PI.editorial(
    'ev-lieux', 'ev-lieux.html', 'ev-lieux.html', 'Évènements',
    'Lieux à visiter⎮La Folie Boulart⎮Biarritz',
    "Biarritz, Bayonne, Saint-Jean-de-Luz, Espelette, la Corniche basque, "
    "Saint-Sébastien, Bilbao et Bordeaux.",
    hero_idx=None, title_idx=0,
    hero_image=PI.first_photo('ev-lieux')))

print(f'{len(made)} pages générées :')
for m in made:
    print('  ', m)
