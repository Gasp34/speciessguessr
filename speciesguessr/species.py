# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 20:55:57 2022

@author: ZenbookGaspard
"""
from igraph import Graph

from pyinaturalist import get_observation_species_counts
from speciesguessr.utils import norm


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
        self.species_list.sort(key=lambda d: d["preferred_common_name"].capitalize())
        self.species_name = [s["preferred_common_name"].capitalize() for s in self.species_list]

        self.nb_species = len(self.species_list)

        self.species_ids = []
        self.species_idx = {}
        edges = []
        for j, species in enumerate(self.species_list):
            ancestors = species["ancestor_ids"]
            for i in range(len(ancestors)-1):
                edges += [(ancestors[i], ancestors[i+1])]
            self.species_ids.append(species["id"])
            self.species_idx[species["id"]] = j
        self.graph = Graph(edges)

    def find_species(self):
        species_list = []
        species_name = []
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
                unique_name = norm(res["taxon"]["preferred_common_name"])

                if unique_name not in species_name:
                    species_name.append(unique_name)
                    species_list.append(res["taxon"])
                else:
                    print(unique_name)
                    idx = species_name.index(unique_name)
                    if species_list[idx]["observations_count"] < res["taxon"]["observations_count"]:
                        species_list[idx] = res["taxon"]
            while len(response["results"]) != 0:
                page += 1
                response = get_observation_species_counts(page=page, **kwargs)
                for res in response["results"]:
                    if "preferred_common_name" not in res["taxon"]:
                        continue
                    if self.latin:
                        res["taxon"]["preferred_common_name"] = res["taxon"]["name"]
                    unique_name = norm(res["taxon"]["preferred_common_name"])

                    if unique_name not in species_name:
                        species_name.append(unique_name)
                        species_list.append(res["taxon"])
                    else:
                        print(unique_name)
                        idx = species_name.index(unique_name)
                        if species_list[idx]["observations_count"] < res["taxon"]["observations_count"]:
                            species_list[idx] = res["taxon"]
            return species_list
        except:
            print("Connection with inaturalist failed")
            return None
