# FlightOnTime – Predicción de Retrasos de Vuelos
## Sector de negocio

## Aviación civil / Logística / Transporte aéreo

Este proyecto está orientado a aerolíneas, aeropuertos y pasajeros que dependen de la puntualidad de los vuelos para una correcta planificación.

## Descripción del proyecto

FlightOnTime es una solución predictiva que estima si un vuelo se retrasará o no, basándose en información conocida antes del despegue (aerolínea, origen, destino, fecha y horar).

El sistema está compuesto por:

- Un modelo de Ciencia de Datos entrenado con datos históricos de vuelos.

- Una API backend que expone un endpoint /predict para realizar predicciones en tiempo real.

### Necesidad del cliente (explicación no técnica)

Los retrasos aéreos generan:

- Insatisfacción en los pasajeros.

- Costos operativos adicionales para las aerolíneas.

- Problemas logísticos en aeropuertos y conexiones.
  
Con esta solución, el cliente puede anticiparse a los retrasos y tomar decisiones informadas, como alertar pasajeros, ajustar la operación o redistribuir recursos.

## Dataset utilizado
## Fuente del dataset

El dataset original fue obtenido desde Kaggle:

## Flight Delay Dataset
https://www.kaggle.com/datasets/arvindnagaonkar/flight-delay

## Dataset original

- Filas: 30,132,631

- Periodo: 2018–2023 (abril)

- Contenido: Información histórica de vuelos comerciales (horarios, aerolínea, ciudades, tiempos y retrasos).

## Preparación y reducción del dataset
## Filtrado temporal

Para evitar distorsiones causadas por la pandemia, se utilizaron únicamente datos de los años:

- 2022

- 2023

## Prevención de fugas de información

Se eliminaron variables que contienen información posterior al despegue o que explican directamente el retraso, garantizando un escenario de predicción realista.

## Variable objetivo

A partir de la columna DepDelayMinutes, se creó la variable binaria Delay:

- Delay = 1 → Retraso mayor a 15 minutos

- Delay = 0 → Retraso de 15 minutos o menos

Dataset final de modelado

Número de filas: 7,603,890

Reducción: muestreo estratificado respecto a la variable objetivo

Periodo: 2022–2023

Variables utilizadas

| Columna                      | Descripción         |
| :----                        | :----               |
| Marketing_Airline_Network    | Aerolínea           |
| OriginCityName               | Ciudad de origen    |
| DestCityName                 | Ciudad de destino   |
| Distance                     | Distancia del vuelo |
| Month	| Mes del vuelo |
| DayofWeek |	Día de la semana |
| Holidays	| Indicador de feriado |
| CRSDepTime | Hora programada de salida |
| Delayed	| Variable objetivo (0 = Puntual, 1 = Retrasado) |

## Definición de la variable objetivo

La columna Delayed fue creada a partir de DepDelayMinutes del dataset original:

- Delayed = 1 → Retraso mayor a 15 minutos

- Delayed = 0 → Retraso de 15 minutos o menos

Todas las variables utilizadas están disponibles antes del despegue, lo que garantiza un escenario de predicción realista y compatible con una API en tiempo real.

## API – Contrato de Integración
### Endpoint principal

POST /predict

Entrada (JSON)
```
{
  "aerolinea": "AZ",
  "origen": "GIG",
  "destino": "GRU",
  "fecha_partida": "2025-11-10T14:30:00",
  "distancia_km": 350
}
```
Salida (JSON)
```
{
  "prevision": "Retrasado",
  "probabilidad": 0.78
}
```

## Entregables
## Ciencia de Datos

Notebook con:

- Limpieza y selección de variables,

- Entrenamiento del modelo,

- Evaluación con métricas de clasificación.

- Modelo exportado en formato serializado (joblib).

## Backend

- API REST desarrollada en Java (Spring Boot).

- Endpoint /predict.

- Validación de entradas.

- Respuestas estandarizadas en formato JSON.

## Reproducibilidad

- El dataset reducido se deriva directamente del dataset original de Kaggle.

- Todos los pasos de procesamiento y modelado están documentados en el notebook.

- El dataset completo puede utilizarse para extender el análisis en entornos con mayor capacidad computacional.
