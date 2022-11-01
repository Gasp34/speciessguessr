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