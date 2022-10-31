# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:07:20 2022

@author: ZenbookGaspard
"""
from pyinaturalist import get_observations, Observation
from speciesguessr.species import SpeciesInfo
from random import randint
from requests import HTTPError
import json


place_id = 6753 # france
# place_id = 162266 # montpellier
taxon_id = 3 # oiseau
language = "fr"

species_info = SpeciesInfo(place_id, taxon_id, language)

class Guessr:
    def __init__(self, species_info):
        self.species_info = species_info
        
    def get_random_species(self):
        i = randint(0, len(self.species_info.species_list))
        return self.species_info.species_list[i]
    
    def get_id_and_name(self, species):
        return species["id"], species["preferred_common_name"]
    
    def find_obs_with_photo(self, species_id):
        kwargs = {"taxon_id": species_id, "locale": "language",
                  "quality_grade": "research", "photos": True}
        nb_obs = get_observations(per_page=0, **kwargs)["total_results"]

        def try_find_obs(kwargs, nb_obs):
            try:
                page = randint(0, nb_obs)
                obs = get_observations(per_page=1, page=page, **kwargs)
                return Observation.from_json_list(obs)[0]
            except HTTPError:
                print("httperror")
                with open("httperrors.json", 'r', encoding='utf-8') as f:
                    httperrors = json.load(f)
                httperrors["page"].append(page)
                httperrors["nb_page"].append(nb_obs)
                with open("httperrors.json", 'w', encoding='utf-8') as f:
                    json.dump(httperrors, f, ensure_ascii=False, indent=4)
                return None
        
        obs = try_find_obs(kwargs, nb_obs)
        while obs is None:
            obs = try_find_obs(kwargs, nb_obs)
        
        return obs

    def show_photo_and_species(self, obs, species_name):
        obs.photos[0].show()
        print(species_name)
    

guessr = Guessr(species_info)

species_to_guess = guessr.get_random_species()
species_id, species_name = guessr.get_id_and_name(species_to_guess)
obs = guessr.find_obs_with_photo(species_id)

guessr.show_photo_and_species(obs, species_name)

## histogram espece

import plotly.io as pio
pio.renderers.default = "browser"

import plotly.express as px
data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop')
fig.show()