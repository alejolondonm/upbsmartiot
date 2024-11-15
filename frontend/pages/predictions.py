from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine

# Conexión a PostgreSQL
db_url = 'postgresql://alejo:1989@postgres_db:5432/iot_db'
engine = create_engine(db_url)

# Función para consultar las predicciones desde PostgreSQL
def get_predictions():
    query = """
    SELECT timestamp, temperature_prediction, humidity_prediction
    FROM predicciones
    ORDER BY timestamp
    """
    try:
        with engine.connect() as conn:
            data = pd.read_sql(query, con=conn)
            print("Datos de predicciones obtenidos de la base de datos:")
            print(data.head())  # Debug: muestra las primeras filas obtenidas
    except Exception as e:
        print(f"Error al consultar la tabla de predicciones: {e}")
        data = pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

    return data

# Función para crear las figuras de predicción
def create_prediction_figures():
    data = get_predictions()

    # Verificar si se obtuvieron datos
    if not data.empty:
        # Crear la figura de predicción de temperatura
        temp_fig = go.Figure()
        temp_fig.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature_prediction'],
                                      mode='lines+markers', name='Temperature Prediction'))
        temp_fig.update_layout(
            title='Temperature Prediction Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            xaxis_tickangle=-45
        )

        # Crear la figura de predicción de humedad
        hum_fig = go.Figure()
        hum_fig.add_trace(go.Scatter(x=data['timestamp'], y=data['humidity_prediction'],
                                     mode='lines+markers', name='Humidity Prediction'))
        hum_fig.update_layout(
            title='Humidity Prediction Over Time',
            xaxis_title='Time',
            yaxis_title='Humidity (%)',
            xaxis_tickangle=-45
        )
    else:
        # Crear figuras vacías si no hay datos
        temp_fig = go.Figure()
        temp_fig.update_layout(
            title='Temperature Prediction Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            xaxis_tickangle=-45
        )

        hum_fig = go.Figure()
        hum_fig.update_layout(
            title='Humidity Prediction Over Time',
            xaxis_title='Time',
            yaxis_title='Humidity (%)',
            xaxis_tickangle=-45
        )

    return temp_fig, hum_fig

# Layout de la página
layout = html.Div([
    html.H1("Predictions"),
    dcc.Tabs(id="prediction-tabs", children=[
        dcc.Tab(label='Temperature Prediction', children=[
            dcc.Graph(id="temperature-prediction-graph")
        ], className="tab-content"),
        dcc.Tab(label='Humidity Prediction', children=[
            dcc.Graph(id="humidity-prediction-graph")
        ], className="tab-content")
    ]),
    dcc.Interval(
        id='prediction-interval',
        interval=60*1000,  # Actualiza cada minuto
        n_intervals=0
    )
])

# Callback para actualizar los gráficos
@callback(
    [Output('temperature-prediction-graph', 'figure'),
     Output('humidity-prediction-graph', 'figure')],
    [Input('prediction-interval', 'n_intervals')]
)
def update_prediction_graphs(n_intervals):
    print("Actualizando gráficos de predicción...")  # Debug
    temp_fig, hum_fig = create_prediction_figures()
    return temp_fig, hum_fig
