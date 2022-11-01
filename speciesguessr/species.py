# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:55:57 2022

@author: ZenbookGaspard
"""
from pyinaturalist import get_observation_species_counts

class SpeciesInfo:
    def __init__(self, config):
        self.config = config
        self.place_id = config.place_id
        self.taxon_id = config.taxon_id
        self.language = config.language
        self.latin = (config.language == "latin")
        if self.latin:
            self.language = "en"

        self.species_list = self.find_species()

    def find_species(self):
        species_list = []
        page = 1
        kwargs = {"place_id": self.place_id, "taxon_id": self.taxon_id,
                  "locale": self.language, "captive": False, 
                  "rank": "species", "popular": self.config.popular}
        try:
            response = get_observation_species_counts(page=page, **kwargs)
            for res in response["results"]:
                if "preferred_common_name" not in res["taxon"]:
                    continue
                if self.latin:
                    res["taxon"]["preferred_common_name"] = res["taxon"]["name"]
                species_list.append(res["taxon"])
            while len(response["results"]) != 0:
                page += 1
                response = get_observation_species_counts(page=page, **kwargs)
                for res in response["results"]:
                    if "preferred_common_name" not in res["taxon"]:
                        continue
                    if self.latin:
                        res["taxon"]["preferred_common_name"] = res["taxon"]["name"]
                    species_list.append(res["taxon"])
            return species_list
        except:
            print("Connection with inaturalist failed")
            return None