import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import os
import flask
import glob

subreddits = pd.read_csv("data/subs.csv")

image_directory = "wordclouds/"
list_of_images = [os.path.basename(x) for x in glob.glob(
    '{}*.png'.format(image_directory))]
static_image_route = '/static/'


def generate_drop_down(subreddits, id):
    options = [{"label": row["subreddits"], "value": row["subreddits"]}
               for _, row in subreddits.iterrows()]
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
        dbc.Row(dbc.Col(html.Img(id="wordcloud"), width={"offset": 1}))
    ], fluid=True)
])


@app.callback(
    dash.dependencies.Output('wordcloud', 'src'),
    [dash.dependencies.Input('subreddits-dropdown', 'value')])
def update_image_src(value):
    return f"/static/{value}.png"


@app.server.route('/static/<image_path>.png')
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)


if __name__ == '__main__':
    app.run_server(debug=True)
