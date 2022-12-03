# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from PIL import Image

from speciesguessr.species import SpeciesInfo
from speciesguessr.guessr import Guessr
from speciesguessr.utils import set_random_answers, taxon_to_id, place_to_id, text_dict, lang_dict
from speciesguessr.utils import strip_accents, set_neighbor_answers, load_image, get_random_answers


class Config():
    def __init__(self, language, place_id, taxon_id, popular):
        self.place_id = place_id
        self.taxon_id = taxon_id
        self.language = language
        self.height = 512
        self.width = 1024
        self.image_quality = "large"
        self.popular = popular


config = Config("fr", 6753, 3, False)
species_info = SpeciesInfo(config)
guessr = Guessr(species_info)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Img(style={'height': '50%', 'width': '50%'}, id="image"),
    html.Button(id='B0', n_clicks=0, children='Submit'),
    html.Button(id='B1', n_clicks=0, children='Submit'),
    html.Button(id='B2', n_clicks=0, children='Submit'),
    html.Button(id='B3', n_clicks=0, children='Submit'),

    dcc.Store(id='answers')
])


@app.callback(Output('image', 'src'),
              Output('answers', "data"),
              Input('B0', 'n_clicks'))
def update_image(n_clicks):
    species_to_guess = guessr.get_random_species()
    obs = guessr.find_obs_with_photo(species_to_guess["id"])
    photo = obs.photos[0]
    answers = get_random_answers(guessr, species_to_guess)
    return photo.url_size("large"), answers


@app.callback(Output('B0', "children"),
              Output('B1', "children"),
              Output('B2', "children"),
              Output('B3', "children"),
              Input("answers", "data"))
def update_output(answers):
    b = [answer["preferred_common_name"].capitalize() for answer in answers]
    return b[0], b[1], b[2], b[3]

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host="0.0.0.0", port="8050")