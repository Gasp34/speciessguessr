# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:07:20 2022

@author: ZenbookGaspard
"""

from pyinaturalist import get_observation_species_counts
from speciesguessr.species import Species

place_id = 6753 # france
# place_id = 162266 # montpellier
taxon_id = 3 # oiseau
language = "fr"

species = Species(place_id, taxon_id, language)
species_list = species.species_list

## histogram espece