# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:07:20 2022

@author: ZenbookGaspard
"""
import PySimpleGUI as sg
from PIL import ImageTk
from time import sleep

from speciesguessr.species import SpeciesInfo
from speciesguessr.guessr import Guessr
from speciesguessr.utils import set_answers, get_new_guess

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
species_to_guess, image = get_new_guess(guessr, config)

sg.theme('Reddit') # Add a touch of color
layout = [[sg.Image(key="-IMAGE-", size=(config.max_width, config.height))],
          [sg.Button(key='A1', expand_x=True, font=('Helvetica', 13)), 
           sg.Button(key='A2', expand_x=True, font=('Helvetica', 13)),
           sg.Button(key='A3', expand_x=True, font=('Helvetica', 13)),
           sg.Button(key='A4', expand_x=True, font=('Helvetica', 13))]]

window = sg.Window('SpeciesGuessr', layout, location=(20, 30), finalize=True,
                   return_keyboard_events=True, use_default_focus=False)
window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
answers = set_answers(guessr, window, species_to_guess)
window.TKroot.focus_force()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Escape:27':
        break
    if type(event) == str and event[0]=="A":
        i = int(event[1])
        if species_to_guess == answers[i-1]:
            window[f"A{i}"].update(button_color="green")
            window.refresh()
        else:
            window[f"A{i}"].update(button_color="red")
            j = answers.index(species_to_guess)
            window[f"A{j+1}"].update(button_color="green")
            window.refresh()
            sleep(1)

        species_to_guess, image = get_new_guess(guessr, config)
        window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
        answers = set_answers(guessr, window, species_to_guess)

window.close()

