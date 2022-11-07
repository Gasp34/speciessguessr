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
from speciesguessr.utils import set_random_answers, taxon_to_id, place_to_id, text_dict, lang_dict, set_neighbor_answers


class Config():
    def __init__(self, language, place_id, taxon_id, popular):
        self.place_id = place_id
        self.taxon_id = taxon_id
        self.language = language
        w, h = sg.Window.get_screen_size()
        self.height = h - 250
        self.width = w - 100
        self.image_quality = "large"
        self.popular = popular


def menu_layout(lang):
    def text(key):
        return text_dict[key][lang]

    layout = [[sg.Column(justification="center", layout=[[sg.Text(text("language")),
                                                          sg.Combo(text("languages"), enable_events=True, key="languages", default_value=text("languages")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("species_language")),
                                                          sg.Combo(text("species_languages"), key="species_languages", default_value=text("species_languages")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("place")),
                                                          sg.Combo(text("places"), key="places", default_value=text("places")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Text(text("taxon")),
                                                          sg.Combo(text("taxons"), key="taxons", default_value=text("taxons")[0])]])],
              [sg.Column(justification="center", layout=[[sg.Checkbox(text("checkbox1"), default=True, enable_events=True, key="C1"),
                                                          sg.Checkbox(text("checkbox2"), enable_events=True, key="C2")]])],
              [sg.Button(text("easy"), key="easy", size=(15, 3), expand_x=True),
               sg.Button(text("medium"), key="medium", size=(15, 3), expand_x=True),
               sg.Button(text("hard"), key="hard", size=(15, 3), expand_x=True)],
              [sg.ProgressBar(max_value=3, size=(42, 20), key="pb")]
              ]

    return layout


sg.theme('Reddit')
lang = "fr"
mode, end = False, False
while not mode and not end:
    layout = menu_layout(lang)
    window = sg.Window('SpeciesGuessr', layout, finalize=True,
                       return_keyboard_events=True, font=('Helvetica', 15))
    window.TKroot.focus_force()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Escape:27':
            end = True
            break
        if event == "languages":
            lang = lang_dict[values["languages"]]
            break
        if event in ["easy", "medium"]:
            mode = event
            break
        if event == "C1":
            window["C2"].update(not values["C1"])
        if event == "C2":
            window["C1"].update(not values["C2"])

if mode:
    config = Config(language=lang_dict[values["species_languages"]],
                    place_id=place_to_id(values["places"], text_dict, lang),
                    taxon_id=taxon_to_id(values["taxons"], text_dict, lang),
                    popular=values["C2"])
    # print(vars(config))
    end = False
    species_info = SpeciesInfo(config)
    window["pb"].update_bar(1)

    if species_info.species_list is None:
        end = True
        layout = [[sg.Text({"fr": "Communication avec iNaturalist impossible\nVerifier la connexion internet",
                            "en": "Failed communication with iNaturalist\nCheck internet connection"}[lang])],
                  [sg.Ok()]]
        window2 = sg.Window('SpeciesGuessr', layout, font=('Helvetica', 15), finalize=True)
        while True:
            event, values = window2.read()
            if event in (sg.WIN_CLOSED, "Ok"):
                break
        window2.close()
    else:
        guessr = Guessr(species_info)
        species_to_guess, image, attribution = guessr.get_new_guess(config, window)
    window.close()

if mode in ["easy", "medium"] and not end:
    layout = [[sg.Column([[sg.Text(f"{values['places']} - {values['taxons']} - {species_info.nb_species} {text_dict['species'][lang]}"),
                           sg.Text(f"     Photo : {attribution}", key="attribution")]], justification="center")],
              [sg.Image(key="-IMAGE-", size=(config.width, config.height))],
              [sg.Column([[sg.Text("Score :"), sg.Text("0/0", key="-SV-"),
                           sg.Text("  Accuracy :"), sg.Text("100%", key="-AV-")]],
                         justification="center")],
              [sg.B(key='A1', expand_x=True), sg.B(key='A2', expand_x=True),
               sg.B(key='A3', expand_x=True), sg.B(key='A4', expand_x=True)]]

    window = sg.Window('SpeciesGuessr', layout, location=(20, 20), finalize=True,
                       return_keyboard_events=True, font=('Helvetica', 15))
    window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
    if mode == "easy":
        answers = set_random_answers(guessr, window, species_to_guess)
    elif mode == "medium":
        answers = set_neighbor_answers(guessr, window, species_to_guess)

    window.TKroot.focus_force()

    success, fails = 0, 0
    while not end:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Escape:27':
            break
        if type(event) == str and event[0] == "A":
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

            species_to_guess, image, attribution = guessr.get_new_guess(config)
            window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
            window["attribution"].update(attribution)
            if mode == "easy":
                answers = set_random_answers(guessr, window, species_to_guess)
            elif mode == "medium":
                answers = set_neighbor_answers(guessr, window, species_to_guess)
    window.close()
