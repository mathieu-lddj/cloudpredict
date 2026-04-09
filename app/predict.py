# app/predict.py
import os
import numpy as np
import joblib
import logging
logger = logging.getLogger("cloudpredict")
# Features attendues par le modele (California Housing)
FEATURE_NAMES = [
"MedInc", # Revenu median du quartier
"HouseAge", # Age median des maisons
"AveRooms", # Nombre moyen de pieces
"AveBedrms", # Nombre moyen de chambres
"Population", # Population du quartier
"AveOccup", # Occupation moyenne
"Latitude", # Latitude
"Longitude" # Longitude
]
# Variable globale pour le modele
_model = None


def load_model():
    """Charge le modele ML depuis le fichier joblib."""
    global _model
    model_path = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "ml", "models", "model.joblib")
    )
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modele introuvable : {model_path}")
    _model = joblib.load(model_path)
    logger.info(f"Modele charge depuis {model_path}")
    return _model


def get_model():
    """Retourne le modele, en le chargeant si necessaire."""
    global _model
    if _model is None:
        load_model()
    return _model



def validate_features(data):
    """Valide que toutes les features requises sont presentes et valides."""
    errors = []
    if "features" not in data:
        return None, ["Le champ 'features' est requis dans le body JSON."]
    features = data["features"]
    # Verifier si c'est un dict avec les noms de features
    if isinstance(features, dict):
        missing = [f for f in FEATURE_NAMES if f not in features]
        if missing:
            errors.append(f"Features manquantes : {missing}")
            return None, errors
        values = [float(features[f]) for f in FEATURE_NAMES]
    # Verifier si c'est une liste de valeurs
    elif isinstance(features, list):
        if len(features) != len(FEATURE_NAMES):
            errors.append(
                f"Attendu {len(FEATURE_NAMES)} features, recu {len(features)}. "
                f"Features attendues : {FEATURE_NAMES}"
            )
            return None, errors
        values = [float(v) for v in features]
    else:
        errors.append("Le champ 'features' doit etre un dict ou une liste.")
        return None, errors
    return np.array(values).reshape(1, -1), None

def predict(data):
    """Effectue une prediction a partir des donnees d'entree."""
    # Valider les features
    features_array, errors = validate_features(data)
    if errors:
        return None, errors
    # Charger le modele et predire
    model = get_model()
    prediction = model.predict(features_array)
    result = {
    "prediction": round(float(prediction[0]), 4),
    "unit": "100k USD",
    "description": "Prix median des maisons (en centaines de milliers de dollars)",
    "features_used": FEATURE_NAMES,
    "input_values": features_array[0].tolist()
    }
    return result, None

