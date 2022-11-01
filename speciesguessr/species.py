# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:55:57 2022

@author: ZenbookGaspard
"""
import json
import os
from time import time

from pyinaturalist import get_observation_species_counts

class SpeciesInfo:
    def __init__(self, place_id, taxon_id, language):
        self.place_id = place_id
        self.taxon_id = taxon_id
        self.language = language

        filename = f'species_list_{self.language}_{self.place_id}_{self.taxon_id}.json'
        if os.path.exists(filename):
            self.load_species_list(filename)
        else:
            self.species_list = self.find_species()
            self.save_species_list(filename)

    def find_species(self):
        t = time()
        species_list = []
        page = 1
        kwargs = {"place_id": self.place_id, "taxon_id": self.taxon_id,
                  "locale": self.language, "captive": False, 
                  "rank": "species"}
        response = get_observation_species_counts(page=page, **kwargs)
        for res in response["results"]:
            if "preferred_common_name" not in res["taxon"]:
                continue
            species_list.append(res["taxon"])
        while len(response["results"]) != 0:
            page += 1
            response = get_observation_species_counts(page=page, **kwargs)
            for res in response["results"]:
                if "preferred_common_name" not in res["taxon"]:
                    continue
                species_list.append(res["taxon"])
        print(f"Species found in {round(time()-t, 2)}s")
        return species_list

    def save_species_list(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.species_list, f, ensure_ascii=False, indent=4)

    def load_species_list(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.species_list = json.load(f)