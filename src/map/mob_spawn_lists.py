# A - alpha_maggot
# F - fly
# G - ghost
# L - legs
# M - maggot
# P - parasite
# S - slime
# W - wanderer

from entities.mobs.alpha_maggot import AlphaMaggot
from entities.mobs.boss.boss import Boss
from entities.mobs.fly import Fly
from entities.mobs.ghost import Ghost
from entities.mobs.legs import Legs
from entities.mobs.maggot import Maggot
from entities.mobs.parasite import Parasite
from entities.mobs.slime import Slime
from entities.mobs.wanderer import Wanderer


EASY = [
[Wanderer, Wanderer],
[Fly, Fly, Fly],
[Slime],
[Maggot, Maggot, Maggot],
[Maggot, Maggot, Fly, Fly],
[AlphaMaggot],
[Legs, Legs],
[Parasite, Parasite, Legs]
]

MEDIUM = [
['L','L','W','W','P'],
['P','P','P','P'],
['G','G'],
['W','L','G','F'],
['S','S','P'],
['P','P','S','F'],
['A','A','P','P'],
['M','M','G','L'],
['P','F','L','L','L']
]

HARD = [
['S','S','S','S'],
['G','G','G','L','L'],
['S','S','P','P','P'],
['L','L','P','G','W'],
['M','A','A','S','P'],
['F','F','F','F','G','G'],
['A','A','A']
]