# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:07:20 2022

@author: ZenbookGaspard
"""
import PySimpleGUI as sg
from random import shuffle
from PIL import Image, ImageTk

from speciesguessr.species import SpeciesInfo
from speciesguessr.guessr import Guessr
from PIL.ImageOps import pad

def load_image(obs):
    image = Image.open(obs.photos[0].open(size="large"))
    image = image.resize((min(config.max_width, int(config.height / image.size[1] * image.size[0])), config.height))
    image = pad(image, (config.max_width, config.height), color="white")
    image = ImageTk.PhotoImage(image)
    return image

def get_new_guess(guessr):
    species_to_guess = guessr.get_random_species()
    obs = guessr.find_obs_with_photo(species_to_guess["id"])
    image = load_image(obs)
    return species_to_guess, image      

class Config():
    def __init__(self, place_id, taxon_id, language):
        self.place_id = place_id
        self.taxon_id = taxon_id
        self.language = language
        self.height = 500
        self.max_width = 1100

config = Config(6753, 3, "fr") # 162266 for mtp

species_info = SpeciesInfo(config.place_id, config.taxon_id, config.language)
guessr = Guessr(species_info)



sg.theme('Reddit')   # Add a touch of color
button_size = (20, 1)
layout = [[sg.Image(key="-IMAGE-", size=(config.max_width, config.height))],
          [sg.Button(key='A1', expand_x=True, font=('Helvetica', 13)), 
           sg.Button(key='A2', expand_x=True, font=('Helvetica', 13)),
           sg.Button(key='A3', expand_x=True, font=('Helvetica', 13)),
           sg.Button(key='A4', expand_x=True, font=('Helvetica', 13))]]

window = sg.Window('SpeciesGuessr', layout, location=(20, 30), finalize=True,
                   return_keyboard_events=True, use_default_focus=False)
window.TKroot.focus_force()

species_to_guess, image = get_new_guess(guessr)
window["-IMAGE-"].update(data=image)

def set_answers(window, species_to_guess):
    answers = [species_to_guess]
    for i in range(3):
        answers.append(guessr.get_random_species())
    shuffle(answers)
    
    for i in range(4):
        window[f"A{i+1}"].update(answers[i]["preferred_common_name"], button_color=('#FFFFFF', '#0079d3'))
    return answers

answers = set_answers(window, species_to_guess)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Escape:27':
        break
    if event == " ":
        species_to_guess, image = get_new_guess(guessr)
        window["-IMAGE-"].update(data=image)
        answers = set_answers(window, species_to_guess)

    if type(event) == str and event[0]=="A":
        i = int(event[1])
        if species_to_guess == answers[i-1]:
            window[f"A{i}"].update(button_color="green")
        else:
            window[f"A{i}"].update(button_color="red")

window.close()


