# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from PIL import Image

from speciesguessr.species import SpeciesInfo
from speciesguessr.guessr import Guessr
from speciesguessr.utils import set_random_answers, taxon_to_id, place_to_id, text_dict, lang_dict
from speciesguessr.utils import strip_accents, set_neighbor_answers, load_image


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


def create_figure(image):
    fig = go.Figure()
    img_width = config.width
    img_height = config.height

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width],
            y=[0, img_height],
            mode="markers",
            marker_opacity=0
        )
    )
    # Configure axes
    fig.update_xaxes(visible=False, range=[0, img_width])
    fig.update_yaxes(visible=False, range=[0, img_height], scaleanchor="x")

    fig.add_layout_image(dict(x=0, sizex=img_width, y=img_height, sizey=img_height, xref="x",
                              yref="y", opacity=1.0, layer="below", sizing="stretch", source=image))
    fig.update_layout(width=img_width, height=img_height, margin={"l": 0, "r": 0, "t": 0, "b": 0})
    return fig


fig = create_figure(None)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id="image", figure=fig, config={'doubleClick': 'reset', 'displayModeBar': False}),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
])


@app.callback(Output('image', 'figure'),
              Input('submit-button-state', 'n_clicks'))
def update_output(n_clicks):
    species_to_guess, image, attribution = guessr.get_new_guess(config)
    fig = create_figure(image)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host="0.0.0.0", port="8050")