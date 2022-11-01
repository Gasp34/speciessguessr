# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:07:20 2022

@author: ZenbookGaspard
"""
from speciesguessr.species import SpeciesInfo
from speciesguessr.guessr import Guessr

place_id = 6753 # france
# place_id = 162266 # montpellier
taxon_id = 3 # oiseau
language = "fr"

species_info = SpeciesInfo(place_id, taxon_id, language)
guessr = Guessr(species_info)

species_to_guess = guessr.get_random_species()
obs = guessr.find_obs_with_photo(species_to_guess["id"])
guessr.show_photo_and_species(obs, species_to_guess)
