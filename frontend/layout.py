from dash import html, dcc
import pages.plant_info as plant_info
import pages.historical_data as historical_data
import pages.predictions as predictions

def get_layout():
    return html.Div([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='Plant Information', children=plant_info.layout, className="tab-content"),
            dcc.Tab(label='Historical Data', children=historical_data.layout, className="tab-content"),
            dcc.Tab(label='Predictions', children=predictions.layout, className="tab-content")
        ], className="tabs-container")
    ], className="app-container")
