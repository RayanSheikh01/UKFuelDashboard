import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("UK Fuel Dashboard"), width=12)
    ], className="my-3")
], fluid=True)

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
