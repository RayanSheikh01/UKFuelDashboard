import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from datetime import date

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("UK Fuel Dashboard"), width=12)
    ], className="my-3")
], fluid=True)

# Fetch data from APIs
asdaData = requests.get('https://storelocator.asda.com/fuel_prices_data.json').json()
BPData = requests.get('https://www.bp.com/en_gb/united-kingdom/home/fuelprices/fuel_prices_data.json').json()
EssoData = requests.get('https://fuelprices.esso.co.uk/latestdata.json').json()
ShellData = requests.get('https://www.shell.co.uk/fuel-prices-data.html').json()
MFGData = requests.get('https://fuel.motorfuelgroup.com/fuel_prices_data.json').json()


asdaData = asdaData['stations']
asdaData = asdaData[0]
asdaPrices = {'E10': asdaData['prices']['E10'], 'B7': asdaData['prices']['B7']}
asdaData = {'brand': 'Asda', 'prices': asdaPrices}
asdaData = pd.json_normalize(asdaData)

BPData = BPData['stations']
BPData = BPData[0]
BPPrices = {'E10': BPData['prices']['E10'], 'B7': BPData['prices']['B7']}
BPData = {'brand': 'BP', 'prices': BPPrices}
BPData = pd.json_normalize(BPData)

EssoData = EssoData['stations']
EssoData = EssoData[0]
EssoPrices = {'E10': EssoData['prices']['E10'], 'B7': EssoData['prices']['B7']}
EssoData = {'brand': 'Esso', 'prices': EssoPrices}
EssoData = pd.json_normalize(EssoData)

ShellData = ShellData['stations']
ShellData = ShellData[0]
ShellPrices = {'E10': ShellData['prices']['E10'], 'B7': ShellData['prices']['B7']}
ShellData = {'brand': 'Shell', 'prices': ShellPrices}
ShellData = pd.json_normalize(ShellData)

MFGData = MFGData['stations']
MFGData = MFGData[0]
MFGPrices = {'E10': MFGData['prices']['E10'], 'B7': MFGData['prices']['B7']}
MFGData = {'brand': 'MFG', 'prices': MFGPrices}
MFGData = pd.json_normalize(MFGData)



data = pd.concat([asdaData, BPData, EssoData, ShellData, MFGData], ignore_index=True)
Date = date.today().strftime("%d/%m/%Y")
app.layout.children.append(html.H2(f"Data last updated: {Date}"))
app.layout.children.append(html.Br())

cheapest_unleaded = data.loc[data['prices.E10'].idxmin()]
cheapest_diesel = data.loc[data['prices.B7'].idxmin()]
app.layout.children.append(html.H3(f"Cheapest Unleaded: {cheapest_unleaded['brand']} at {cheapest_unleaded['prices.E10']}p"))
app.layout.children.append(html.H3(f"Cheapest Diesel: {cheapest_diesel['brand']} at {cheapest_diesel['prices.B7']}p"))

bar_chart = dcc.Graph(
    figure={
        'data': [
            {'x': data['brand'], 'y': data['prices.E10'], 'type': 'bar', 'name': 'Unleaded Prices'},
            {'x': data['brand'], 'y': data['prices.B7'], 'type': 'bar', 'name': 'Diesel Prices'}
        ]
        ,

        'layout': {
            'title': {'text': 'Fuel Prices by Brand', 'x': 0.5, 'xanchor': 'center'},
            'xaxis': {'title': {'text': 'Brand', 'standoff': 10}},
            'yaxis': {'title': {'text': 'Price (Pence)', 'standoff': 10}},
        }
    }
)




app.layout.children.append(bar_chart)

# app.layout.children.append(dbc.Row([
#     dbc.Col(bar_chart, width=12)
# ], className="my-3"))

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
