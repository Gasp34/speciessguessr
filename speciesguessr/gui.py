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
        w, h = sg.Window.get_screen_size()
        self.height = h - 200
        self.width = w - 100
        self.image_quality = "large"

config = Config(6753, 3, "fr") # 162266 for mtp

species_info = SpeciesInfo(config.place_id, config.taxon_id, config.language)
guessr = Guessr(species_info)
species_to_guess, image = get_new_guess(guessr, config)

sg.theme('Reddit')
layout = [[sg.Image(key="-IMAGE-", size=(config.width, config.height))],
          [sg.Button(key='A1', expand_x=True, font=('Helvetica', 15)), 
           sg.Button(key='A2', expand_x=True, font=('Helvetica', 15)),
           sg.Button(key='A3', expand_x=True, font=('Helvetica', 15)),
           sg.Button(key='A4', expand_x=True, font=('Helvetica', 15))]]

window = sg.Window('SpeciesGuessr', layout, location=(20, 30), finalize=True,
                   return_keyboard_events=True)
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

