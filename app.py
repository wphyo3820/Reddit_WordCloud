import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import os
import flask
import glob
import markov

# image directories
image_directory = "wordclouds/"
list_of_images = [os.path.basename(x) for x in glob.glob(
    '{}*.png'.format(image_directory))]
static_image_route = '/static/'

# matrix directory
start_directory = "data/start/"
one_directory = "data/one/"
two_directory = "data/two/"

# data
subreddits = ["food"]
matrices = {}


def generate_drop_down(subreddits, id):
    options = [{"label": sub, "value": sub}
               for sub in subreddits]
    dd = dcc.Dropdown(
        id=id,
        options=options,
        value=options[0].get("value")
    )
    return dd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
    dbc.Container([
        dbc.Row(html.Br()),
        dbc.Row(dbc.Col(html.H1("Reddit WordClouds Dashboard"),
                        width={"offset": 1})),
        dbc.Row(dbc.Col(generate_drop_down(
            subreddits, "subreddits-dropdown"), width={"size": 6, "offset": 1})),
        dbc.Row(html.Br()),
        dbc.Row(dbc.Col(html.Img(id="wordcloud"), width={"offset": 1})),
        dbc.Row(html.Br()),
        dbc.Row(dbc.Col(dbc.Button("Generate Text", id="text-button",
                                   className="mr-2"), width={"offset": 1})),
        dbc.Row(dbc.Col(html.H2(id="output", style={
                "vertical-align": "middle"}), width={"offset": 1}))
    ], fluid=True)
])


@app.callback(
    dash.dependencies.Output("wordcloud", "src"),
    [dash.dependencies.Input("subreddits-dropdown", "value")])
def update_image_src(value):
    return f"/static/{value}.png"


@app.server.route("/static/<image_path>.png")
def serve_image(image_path):
    image_name = "{}.png".format(image_path)
    if image_name not in list_of_images:
        raise Exception(
            "'{}' is excluded from the allowed static files".format(image_path))
    return flask.send_from_directory(image_directory, image_name)


@app.callback(
    dash.dependencies.Output("output", "children"),
    [dash.dependencies.Input("text-button", "n_clicks")],
    [dash.dependencies.State("subreddits-dropdown", "value")]
)
def on_button_click(n, current_sub):
    if n is None:
        return ""
    else:
        start_df = matrices[current_sub]["start_df"]
        one_df = matrices[current_sub]["one_df"]
        two_df = matrices[current_sub]["two_df"]
        sentence = markov.generate_sentence(start_df, one_df, two_df, 1, 15)
        return sentence


if __name__ == '__main__':
    for sub in subreddits:
        sub_mat = markov.convert_json_matrix(**markov.read_json_matrix(sub))
        matrices[sub] = {
            "start_df": sub_mat[0],
            "one_df": sub_mat[1],
            "two_df": sub_mat[2]
        }
    app.run_server(debug=True)
