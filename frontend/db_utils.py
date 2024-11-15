# db_utils.py
import psycopg2
import pandas as pd
import os

# Configuración de conexión a PostgreSQL
def connect_to_postgresql():
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

# Función para obtener datos específicos desde PostgreSQL
def get_data_from_postgres(query):
    connection = connect_to_postgresql()
    if connection is None:
        print("No se pudo conectar a la base de datos")
        return pd.DataFrame()  # Devuelve un DataFrame vacío si falla la conexión
    
    try:
        print(f"Ejecutando query: {query}")
        data = pd.read_sql_query(query, connection)
        print("Datos obtenidos correctamente")
        print(f"Primeras filas del DataFrame: {data.head()}")
        return data
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()
    finally:
        print("Cerrando conexión a la base de datos")
        connection.close()

# Función para obtener datos históricos con un rango de fechas
def get_historical_data(start_date=None, end_date=None):
    print(f"Obteniendo datos históricos desde {start_date} hasta {end_date}")
    query = """
    SELECT time_index, temp, humedad, lat, lon
    FROM mediciones
    """
    if start_date is not None and end_date is not None:
        query += f"WHERE time_index BETWEEN '{start_date}' AND '{end_date}'"
    


    
    print(f"Query generada: {query}")
    return get_data_from_postgres(query)
