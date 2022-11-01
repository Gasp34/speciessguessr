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
    def __init__(self):
        self.place_id = 6753 # 162266 for mtp
        self.taxon_id = 3
        self.language = "fr"
        w, h = sg.Window.get_screen_size()
        self.height = h - 200
        self.width = w - 100
        self.image_quality = "large"

config = Config()

species_info = SpeciesInfo(config)
guessr = Guessr(species_info)
species_to_guess, image = get_new_guess(guessr, config)

layout = [[sg.Image(key="-IMAGE-", size=(config.width, config.height))],
          [sg.Column([[sg.Text("Score :"), sg.Text("0/0", key="-SV-"),
                       sg.Text("  Accuracy :"), sg.Text("100%", key="-AV-")]],
                     justification="center")],
          [sg.B(key='A1', expand_x=True), sg.B(key='A2', expand_x=True),
           sg.B(key='A3', expand_x=True), sg.B(key='A4', expand_x=True)]]

sg.theme('Reddit')
window = sg.Window('SpeciesGuessr', layout, location=(20, 20), finalize=True,
                   return_keyboard_events=True, font=('Helvetica', 15))
window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
answers = set_answers(guessr, window, species_to_guess)
window.TKroot.focus_force()

success, fails = 0, 0
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Escape:27':
        break
    if type(event) == str and event[0]=="A":
        i = int(event[1])
        if species_to_guess == answers[i-1]:
            fail = False
            success += 1
            window[f"A{i}"].update(button_color="green")
        else:
            fail = True
            fails += 1
            window[f"A{i}"].update(button_color="red")
            j = answers.index(species_to_guess)
            window[f"A{j+1}"].update(button_color="green")
        window["-SV-"].update(f"{success}/{success+fails}")
        window["-AV-"].update(f"{int(success/(success+fails)*100)}%")
        window.refresh()
        if fail:
            sleep(1)

        species_to_guess, image = get_new_guess(guessr, config)
        window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
        answers = set_answers(guessr, window, species_to_guess)

window.close()

