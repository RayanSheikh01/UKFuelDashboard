import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("UK Fuel Dashboard"), width=12)
    ], className="my-3")
], fluid=True)

data = pd.read_csv('uk_fuel_prices.csv')

datatable = dbc.Table.from_dataframe(data, striped=True, bordered=True, hover=True)
app.layout.children.append(datatable)

line_chart = dcc.Graph(
    figure={
        'data': [
            {'x': data['date'], 'y': data['unleaded'], 'type': 'line', 'name': 'Unleaded'},
            {'x': data['date'], 'y': data['diesel'], 'type': 'line', 'name': 'Diesel'},
        ],
        'layout': {
            'title': 'Fuel Prices Over Time'
        }
    }
)
app.layout.children.append(line_chart)

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
