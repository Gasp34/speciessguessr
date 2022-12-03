# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:22:23 2022

@author: ZenbookGaspard
"""
from PIL import Image
from PIL.ImageOps import pad
from random import shuffle, randint
import unicodedata

def load_image(obs, config):
    image = Image.open(obs.photos[0].open(size=config.image_quality))
    image = image.resize((min(config.width, int(config.height / image.size[1] * image.size[0])), config.height))
    image = pad(image, (config.width, config.height), color="white")
    return image


def set_random_answers(guessr, window, species_to_guess):
    answers = [species_to_guess]
    if guessr.species_info.nb_species >= 4:
        while len(answers) != 4:
            rand_species = guessr.get_random_species()
            if rand_species not in answers:
                answers.append(rand_species)
    else:
        for i in range(3):
            answers.append(guessr.get_random_species())
    shuffle(answers)

    for i in range(4):
        window[f"A{i+1}"].update(answers[i]["preferred_common_name"].capitalize(), button_color=('#FFFFFF', '#0079d3'))
    return answers


def set_neighbor_answers(guessr, window, species_to_guess):
    answers = [species_to_guess]
    graph = guessr.species_info.graph
    conv = guessr.species_info.idx_to_graph

    if guessr.species_info.nb_species >= 4:
        order = 0
        possible_answers = []
        while len(possible_answers) < 4:
            order += 1
            possible_answers = [conv[i] for i in graph.neighborhood(conv.index(species_to_guess["id"]), order=order)
                                if conv[i] in guessr.species_info.species_ids]
        possible_answers.pop(possible_answers.index(species_to_guess["id"]))

        while len(answers) != 4:
            i = randint(0, len(possible_answers) - 1)
            species_idx = guessr.species_info.species_idx[possible_answers[i]]
            rand_species = guessr.species_info.species_list[species_idx]
            if rand_species not in answers:
                answers.append(rand_species)
    else:
        for i in range(3):
            answers.append(guessr.get_random_species())

    shuffle(answers)

    for i in range(4):
        window[f"A{i+1}"].update(answers[i]["preferred_common_name"].capitalize(), button_color=('#FFFFFF', '#0079d3'))
    return answers


def place_to_id(place, text_dict, lang):
    try:
        return int(place)
    except ValueError:
        place_ids = [6753, 97391, 162266]
        return place_ids[text_dict["places"][lang].index(place)]


def taxon_to_id(taxon, text_dict, lang):
    try:
        return int(taxon)
    except ValueError:
        place_ids = [3, 20978, 47158, 40151, 26036, 47157, 47224, 47178]
        return place_ids[text_dict["taxons"][lang].index(taxon)]


def strip_accents(s):
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def norm(s):
    return strip_accents(s.lower())


text_dict = {"language": {"fr": "Langue du logiciel", "en": "Software language"},
             "languages": {"fr": ["Français", "English"], "en": ["English", "Français"]},
             "species_language": {"fr": "Noms d'espèces", "en": "Species names"},
             "species_languages": {"fr": ["Français", "English", "Latin"], "en": ["English", "Français", "Latin"]},
             "checkbox1": {"fr": "Toutes les espèces", "en": "All species"},
             "checkbox2": {"fr": "Espèces populaires", "en": "Popular species"},
             "easy": {"fr": "Facile", "en": "Easy"},
             "hard": {"fr": "Difficile", "en": "Hard"},
             "medium": {"fr": "Moyen", "en": "Medium"},
             "change": {"fr": "Changer", "en": "Change"},
             "species": {"fr": "Espèces", "en": "Species"},
             "popular": {"fr": "Populaire", "en": "Popular"},
             "hier_acc": {"fr": "Accuracy hiérarchique", "en": "Hierarchical accuracy"},
             "config": {"fr": "Configuration", "en": "Configuration"},
             "about": {"fr": "À propos", "en": "About"},
             "taxon": {"fr": "Taxon", "en": "Taxon"},
             "taxons": {"fr": ["Oiseaux", "Amphibiens", "Insectes", "Mammifères", "Reptiles", "Papillons", "Papilionoidea", "Poissons"],
                        "en": ["Bird", "Amphibian", "Insect", "Mammals", "Reptile", "Butterfly", "Papilionoidea", "Fish"]},
             "place": {"fr": "Zone géographique", "en": "Geographical area"},
             "places": {"fr": ["France", "Europe", "Montpellier"], "en": ["France", "Europe", "Montpellier"]}}

lang_dict = {"English": "en", "Français": "fr", "Latin": "latin"}
