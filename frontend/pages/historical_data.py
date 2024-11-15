# app.py
from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from db_utils import get_historical_data

# Función para actualizar las figuras
def create_figures(start_date=None, end_date=None):
    print("Generando figuras con el rango de fechas:", start_date, end_date)  # Debug

    data = get_historical_data(start_date, end_date)
    
    if data.empty:
        print("No se obtuvieron datos de la base de datos.")  # Debug
    else:
        print("Datos para la creación de figuras obtenidos correctamente.")  # Debug

    # Verificar si se obtuvieron datos
    if not data.empty:
        # Ordenar los datos por time_index
        data = data.sort_values('time_index')
        print("Datos ordenados por time_index:", data.head())  # Debug

        # Interpolación de la temperatura
        timestamps = data['time_index'].astype(np.int64) // 10**9
        temperature = data['temp']
        print("Timestamps y temperaturas para interpolación:", timestamps.head(), temperature.head())  # Debug

        interp_func_temp = interp1d(timestamps, temperature, kind='linear', fill_value='extrapolate')
        new_timestamps = np.linspace(timestamps.min(), timestamps.max(), num=500)
        new_temperatures = interp_func_temp(new_timestamps)
        new_times = pd.to_datetime(new_timestamps, unit='s')

        # Crear la figura de temperatura
        temp_fig = go.Figure()
        temp_fig.add_trace(go.Scatter(x=new_times, y=new_temperatures, mode='lines+markers', name='Temperature'))
        temp_fig.update_layout(
            title='Temperature Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            xaxis_tickangle=-45
        )

        # Interpolación de la humedad
        humidity = data['humedad']
        interp_func_hum = interp1d(timestamps, humidity, kind='linear', fill_value='extrapolate')
        new_humidities = interp_func_hum(new_timestamps)

        # Crear la figura de humedad
        hum_fig = go.Figure()
        hum_fig.add_trace(go.Scatter(x=new_times, y=new_humidities, mode='lines+markers', name='Humidity'))
        hum_fig.update_layout(
            title='Humidity Over Time',
            xaxis_title='Time',
            yaxis_title='Humidity (%)',
            xaxis_tickangle=-45
        )
    else:
        # Crear figuras vacías si no hay datos
        temp_fig = go.Figure()
        temp_fig.update_layout(
            title='Temperature Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            xaxis_tickangle=-45
        )

        hum_fig = go.Figure()
        hum_fig.update_layout(
            title='Humidity Over Time',
            xaxis_title='Time',
            yaxis_title='Humidity (%)',
            xaxis_tickangle=-45
        )

    return temp_fig, hum_fig

# Layout de la página
layout = html.Div([
    html.H1("Historical Data of Temperature and Humidity"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=pd.Timestamp.now().normalize() - pd.Timedelta(days=30),
        end_date=pd.Timestamp.now().normalize(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Tabs(id="temp-hum-tabs", children=[
        dcc.Tab(label='Temperature', children=[
            dcc.Graph(id="temperature-graph")
        ], className="tab-content"),
        dcc.Tab(label='Humidity', children=[
            dcc.Graph(id="humidity-graph")
        ], className="tab-content")
    ]),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )
])

# Callback para actualizar los gráficos
@callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(n_intervals, start_date, end_date):
    print("Callback ejecutado con los parámetros:", n_intervals, start_date, end_date)  # Debug
    temp_fig, hum_fig = create_figures(start_date, end_date)
    return temp_fig, hum_fig