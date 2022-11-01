# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:22:23 2022

@author: ZenbookGaspard
"""
from PIL import Image
from PIL.ImageOps import pad
from random import shuffle

def load_image(obs, config):
    image = Image.open(obs.photos[0].open(size=config.image_quality))
    image = image.resize((min(config.width, int(config.height / image.size[1] * image.size[0])), config.height))
    image = pad(image, (config.width, config.height), color="white")
    return image

def set_answers(guessr, window, species_to_guess):
    answers = [species_to_guess]
    for i in range(3):
        answers.append(guessr.get_random_species())
    shuffle(answers)
    
    for i in range(4):
        window[f"A{i+1}"].update(answers[i]["preferred_common_name"].capitalize(), button_color=('#FFFFFF', '#0079d3'))
    return answers

def get_new_guess(guessr, config):
    species_to_guess = guessr.get_random_species()
    obs = guessr.find_obs_with_photo(species_to_guess["id"])
    while obs is None:
        species_to_guess = guessr.get_random_species()
        obs = guessr.find_obs_with_photo(species_to_guess["id"])
    image = load_image(obs, config)
    return species_to_guess, image  

def place_to_id(place, text_dict, lang):
    try:
        return int(place)
    except ValueError:
        place_ids = [6753, 162266]
        return place_ids[text_dict["places"][lang].index(place)]

def taxon_to_id(taxon, text_dict, lang):
    try:
        return int(taxon)
    except ValueError:
        place_ids = [3, 34]
        return place_ids[text_dict["taxons"][lang].index(taxon)]

text_dict = {"language": {"fr": "Langue du logiciel", "en": "Software language"},
             "languages": {"fr": ["français", "english"], "en": ["english", "français"]},
             "species_language": {"fr": "Noms d'espèces", "en": "Species names"},
             "species_languages": {"fr": ["français", "english", "latin"], "en": ["english", "français", "latin"]},
             "checkbox1": {"fr": "Toutes les espèces", "en": "All species"},
             "checkbox2": {"fr": "Espèces populaires", "en": "Popular species"},
             "easy": {"fr": "Facile", "en": "Easy"},
             "hard": {"fr": "Difficile", "en": "Hard"},
             "taxon": {"fr": "Taxon", "en": "Taxon"},
             "taxons": {"fr": ["Oiseau", "Reptile"], "en": ["Bird", "Reptile"]},
             "place": {"fr": "Zone géographique", "en": "Geographical area"},
             "places": {"fr": ["France", "Montpellier"], "en": ["France", "Montpellier"]}}

lang_dict = {"english": "en", "français": "fr", "latin": "latin"}
