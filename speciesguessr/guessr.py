# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:52:57 2022

@author: ZenbookGaspard
"""
from random import randint
from pyinaturalist import get_observations, Observation
from requests import HTTPError

class Guessr:
    def __init__(self, species_info):
        self.species_info = species_info
        
    def get_random_species(self):
        i = randint(0, len(self.species_info.species_list)-1)
        return self.species_info.species_list[i]

    def find_obs_with_photo(self, species_id):
        kwargs = {"taxon_id": species_id, "locale": "language",
                  "quality_grade": "research", "photos": True}
        nb_obs = get_observations(per_page=0, **kwargs)["total_results"]
        if nb_obs == 0:
            return None

        def try_find_obs(kwargs, nb_obs):
            try:
                page = randint(0, min(nb_obs-1, 9999))
                obs = get_observations(per_page=1, page=page, **kwargs)
                return Observation.from_json_list(obs)[0]
            except HTTPError:
                return None
        
        obs = try_find_obs(kwargs, nb_obs)
        while obs is None:
            obs = try_find_obs(kwargs, nb_obs)
        return obs

    def show_photo_and_species(self, obs, species_to_guess):
        obs.photos[0].show()
        print(species_to_guess["preferred_common_name"], species_to_guess["name"], sep=", ")
