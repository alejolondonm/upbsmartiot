GRANT ALL PRIVILEGES ON DATABASE iot_db TO alejo;

CREATE TABLE IF NOT EXISTS mediciones (
    id SERIAL PRIMARY KEY,
    entity_id VARCHAR(255),
    time_index TIMESTAMP,
    temp FLOAT,
    humedad FLOAT,
    lat FLOAT,
    lon FLOAT
);

CREATE TABLE IF NOT EXISTS predicciones (
    prediction_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE,
    temperature_prediction FLOAT,
    humidity_prediction FLOAT
);