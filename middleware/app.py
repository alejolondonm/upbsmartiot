import os
import pandas as pd
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor
import psycopg2  # type: ignore
from crate import client
from datetime import datetime, timedelta

# Conectar a CrateDB
def conectar_a_crate():
    try:
        return client.connect('http://10.38.32.137:8083', username='crate')
    except Exception as e:
        print(f"Error al conectar a CrateDB: {e}")
        return None

# Obtener datos de CrateDB
def obtener_datos():
    conexion = conectar_a_crate()
    if not conexion:
        return pd.DataFrame()
    
    cursor = conexion.cursor()
    try:
        query = """
        SELECT entity_id, time_index, temp, humedad, lat, lon
        FROM "doc"."etvariables"
        WHERE entity_id = 'alejolondonm' 
            AND temp > 0 and temp < 100 
            AND humedad > 0 and humedad < 100 
        ORDER BY time_index
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['entity_id', 'time_index', 'temp', 'humedad', 'lat', 'lon'])
        print(f"Datos recuperados de CrateDB: {len(df)} filas.")
        return df
    except Exception as e:
        print(f"Error al obtener datos de CrateDB: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conexion.close()

# Conectar a PostgreSQL
def conectar_a_postgresql():
    try:
        print("Intentando conectar a PostgreSQL...")
        connection = psycopg2.connect(
            host="postgres_db",
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "iot_db"),
            user=os.getenv("POSTGRES_USER", "alejo"),
            password=os.getenv("POSTGRES_PASSWORD", "1989")
        )
        print("Conexión exitosa a PostgreSQL")
        return connection
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

# Insertar mediciones en PostgreSQL
def insertar_mediciones(datos):
    conn = conectar_a_postgresql()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        if not datos.empty:
            cursor.execute('DELETE FROM mediciones')

            for _, row in datos.iterrows():
                timestamp = datetime.fromtimestamp(row['time_index'] / 1000.0)
                cursor.execute("""
                    INSERT INTO mediciones (entity_id, time_index, temp, humedad, lat, lon)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (row['entity_id'], timestamp, row['temp'], row['humedad'], row['lat'], row['lon']))
            
            conn.commit()
            print(f"Se insertaron {len(datos)} filas en la tabla de mediciones.")
        else:
            print("No hay datos para insertar.")
    except Exception as e:
        print(f"Error al insertar mediciones en PostgreSQL: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Guardar predicciones en PostgreSQL
def guardar_predicciones(predicciones_temp, predicciones_humedad):
    conn = conectar_a_postgresql()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM predicciones;')

        current_time = datetime.now()
        for i, (pred_temp, pred_humedad) in enumerate(zip(predicciones_temp, predicciones_humedad)):
            future_time = current_time + timedelta(hours=i)
            cursor.execute('''
                INSERT INTO predicciones (timestamp, temperature_prediction, humidity_prediction)
                VALUES (%s, %s, %s)
            ''', (future_time, pred_temp, pred_humedad))

        conn.commit()
        print(f"Predicciones guardadas: {len(predicciones_temp)} registros.")
    except Exception as e:
        print(f"Error al guardar predicciones: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Generar predicciones
def generar_predicciones(datos):
    datos["date"] = pd.to_datetime(datos["time_index"], unit='ms')
    datos = datos.sort_values("date", ascending=True).reset_index(drop=True)

    datos["minutes"] = (datos["date"] - datos["date"].min()).dt.total_seconds() / 60
    tiempo_temp = datos["minutes"].to_list()
    temperatura = datos["temp"].to_list()
    humedad = datos["humedad"].to_list()

    data_temp = pd.DataFrame({'t': tiempo_temp, 'y': temperatura})
    data_humedad = pd.DataFrame({'t': tiempo_temp, 'y': humedad})

    max_lags = min(20, len(data_temp) - 1)  # Aumentar el número de lags para mejorar la captura de patrones
    steps = 24

    # Mejorar el modelo de temperatura con RandomForestRegressor y más estimadores
    pronosticador_temp = ForecasterAutoreg(
        regressor=RandomForestRegressor(n_estimators=200, random_state=123),
        lags=max_lags
    )
    pronosticador_temp.fit(y=data_temp['y'])
    predicciones_temp = pronosticador_temp.predict(steps=steps)

    # Mejorar el modelo de humedad con RandomForestRegressor y más estimadores
    pronosticador_humedad = ForecasterAutoreg(
        regressor=RandomForestRegressor(n_estimators=200, random_state=123),
        lags=max_lags
    )
    pronosticador_humedad.fit(y=data_humedad['y'])
    predicciones_humedad = pronosticador_humedad.predict(steps=steps)

    return predicciones_temp, predicciones_humedad

# Ejecución principal
if __name__ == "__main__":
    print("Middleware iniciado...")
    datos = obtener_datos()
    
    if not datos.empty:
        insertar_mediciones(datos)
        predicciones_temp, predicciones_humedad = generar_predicciones(datos)
        guardar_predicciones(predicciones_temp, predicciones_humedad)
    else:
        print("No se obtuvieron datos para procesar.")
