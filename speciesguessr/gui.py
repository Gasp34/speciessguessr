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
    def __init__(self, language):
        self.place_id = 6753 # 162266 for mtp
        self.taxon_id = 3
        self.language = language
        w, h = sg.Window.get_screen_size()
        self.height = h - 200
        self.width = w - 100
        self.image_quality = "large"
        self.popular = True


text_dict = {"language": {"fr": "Langue du logiciel", "en": "Software language"},
             "languages": {"fr": ["français", "english"], "en": ["english", "français"]},
             "species_language": {"fr": "Langue des noms d'espèces", "en": "Species language"},
             "species_languages": {"fr": ["français", "english", "latin"], "en": ["english", "français", "latin"]},
             "taxon": {"fr": "Taxon", "en": "Taxon"},
             "taxons": {"fr": ["oiseau", "reptile"], "en": ["bird", "reptile"]},
             "place": {"fr": "Zone géographique", "en": "Geographical area"},
             "places": {"fr": ["France", "Montpellier"], "en": ["France", "Montpellier"]}}

lang_dict = {"english": "en", "français": "fr", "latin": "latin"}


sg.theme('Reddit')

def create_layout(lang):
    def text(key):
        return text_dict[key][lang]
    layout = [[sg.Column(justification="center", layout=[[sg.Text(text("language")),
                           sg.Combo(text("languages"), enable_events=True, key="combo", default_value=text("languages")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("species_language")),
                           sg.Combo(text("species_languages"), key="combo_species", default_value=text("species_languages")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("place")),
                           sg.Combo(text("places"), key="places", default_value=text("places")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("taxon")),
                           sg.Combo(text("taxons"), key="taxons", default_value=text("taxons")[0])]])],
              [sg.Button("ok")]
              ]
    return layout

lang="fr"
ok = False
end = False
while not ok and not end:
    layout = create_layout(lang)
    window = sg.Window('SpeciesGuessr', layout, finalize=True,
                       return_keyboard_events=True, font=('Helvetica', 15))
    window.TKroot.focus_force()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Escape:27':
            end = True
            break
        if event == "combo":
            lang = lang_dict[values["combo"]]
            break
        if event=="ok":
            ok = True
            break
    window.close()

if ok:
    config = Config(language=lang_dict[values["combo_species"]])

# species_info = SpeciesInfo(config)
# guessr = Guessr(species_info)
# species_to_guess, image = get_new_guess(guessr, config)

# layout = [[sg.Image(key="-IMAGE-", size=(config.width, config.height))],
#           [sg.Column([[sg.Text("Score :"), sg.Text("0/0", key="-SV-"),
#                        sg.Text("  Accuracy :"), sg.Text("100%", key="-AV-")]],
#                      justification="center")],
#           [sg.B(key='A1', expand_x=True), sg.B(key='A2', expand_x=True),
#            sg.B(key='A3', expand_x=True), sg.B(key='A4', expand_x=True)]]

# sg.theme('Reddit')
# window = sg.Window('SpeciesGuessr', layout, location=(20, 20), finalize=True,
#                    return_keyboard_events=True, font=('Helvetica', 15))
# window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
# answers = set_answers(guessr, window, species_to_guess)
# window.TKroot.focus_force()

# success, fails = 0, 0
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Escape:27':
#         break
#     if type(event) == str and event[0]=="A":
#         i = int(event[1])
#         if species_to_guess == answers[i-1]:
#             fail = False
#             success += 1
#             window[f"A{i}"].update(button_color="green")
#         else:
#             fail = True
#             fails += 1
#             window[f"A{i}"].update(button_color="red")
#             j = answers.index(species_to_guess)
#             window[f"A{j+1}"].update(button_color="green")
#         window["-SV-"].update(f"{success}/{success+fails}")
#         window["-AV-"].update(f"{int(success/(success+fails)*100)}%")
#         window.refresh()
#         if fail:
#             sleep(1)

#         species_to_guess, image = get_new_guess(guessr, config)
#         window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
#         answers = set_answers(guessr, window, species_to_guess)

# window.close()

