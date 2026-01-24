import joblib
import pandas as pd
import holidays

# ===============================
# Configuración
# ===============================

MODEL_PATH = "model/flight_delay_pipeline.joblib"
THRESHOLD = 0.40  # decisión de negocio

# Calendario de feriados (USA)
HOLIDAYS_CALENDAR = holidays.US()

# ===============================
# Carga del modelo
# ===============================

pipeline = joblib.load(MODEL_PATH)

# ===============================
# Feature engineering
# ===============================

def extract_features(payload: dict) -> pd.DataFrame:
    """
    Convierte un JSON de entrada en un DataFrame
    compatible con el pipeline entrenado.
    """

    # --- Validaciones mínimas ---
    required_keys = {
        "aerolinea",
        "origen",
        "destino",
        "fecha_partida",
        "distancia_km",
    }

    missing = required_keys - payload.keys()
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {missing}")

    # --- Parseo de fecha ---
    dt = pd.to_datetime(payload["fecha_partida"], errors="raise")

    features = {
        "Marketing_Airline_Network": payload["aerolinea"],
        "OriginCityName": payload["origen"],
        "DestCityName": payload["destino"],
        "Distance": float(payload["distancia_km"]),
        "Month": dt.month,
        "DayofWeek": dt.dayofweek,               # 0 = lunes
        "CRSDepTime": dt.hour * 60 + dt.minute,  # minutos desde medianoche
        "Holidays": dt.date() in HOLIDAYS_CALENDAR,
    }

    return pd.DataFrame([features])

# ===============================
# Predicción
# ===============================

def predict_delay(payload: dict) -> dict:
    """
    Recibe un JSON de vuelo y devuelve
    la predicción de retraso y su probabilidad.
    """

    # 1️⃣ JSON → DataFrame
    X = extract_features(payload)

    # 2️⃣ Probabilidad de retraso (clase 1)
    prob_delay = pipeline.predict_proba(X)[0, 1]

    # 3️⃣ Decisión final
    prediction = int(prob_delay >= THRESHOLD)

    # 4️⃣ Respuesta amigable
    return {
        "prevision": "Retrasado" if prediction == 1 else "Puntual",
        "probabilidad": round(float(prob_delay), 2),
    }
