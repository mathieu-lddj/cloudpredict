# ml/train.py
import os
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def load_data():
    """Charge le dataset California Housing et retourne X, y avec les noms de features."""
    housing = fetch_california_housing()
    X = pd.DataFrame(housing.data, columns=housing.feature_names)
    y = pd.Series(housing.target, name="MedHouseVal")
    return X, y, housing.feature_names

def train_model(X_train, y_train):
    """Entraine un RandomForestRegressor sur les donnees d'entrainement."""
    model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evalue le modele et retourne les metriques."""
    y_pred = model.predict(X_test)
    metrics = {
    "mae": mean_absolute_error(y_test, y_pred),
    "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
    "r2": r2_score(y_test, y_pred)
    }
    return metrics


def save_model(model, filepath):
    """Sauvegarde le modele avec joblib."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Modele sauvegarde dans : {filepath}")
    
    
def main():
    print("=" * 60)
    print("CloudPredict - Entrainement du modele")
    print("=" * 60)
    # Charger les donnees
    print("\n[1/4] Chargement du dataset California Housing...")
    X, y, feature_names = load_data()
    print(f" - Nombre d'echantillons : {len(X)}")
    print(f" - Nombre de features : {len(feature_names)}")
    print(f" - Features : {list(feature_names)}")
    # Split train/test
    print("\n[2/4] Division train/test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
    )
    print(f" - Train : {len(X_train)} echantillons")
    print(f" - Test : {len(X_test)} echantillons")
    # Entrainer le modele
    print("\n[3/4] Entrainement du RandomForestRegressor...")
    model = train_model(X_train, y_train)
    print(" - Entrainement termine !")
    # Evaluer le modele
    print("\n[4/4] Evaluation du modele...")
    metrics = evaluate_model(model, X_test, y_test)
    print(f" - MAE : {metrics['mae']:.4f}")
    print(f" - RMSE : {metrics['rmse']:.4f}")
    print(f" - R2 : {metrics['r2']:.4f}")
    # Sauvegarder le modele
    model_path = os.path.join(os.path.dirname(__file__), "models", "model.joblib")
    save_model(model, model_path)
    print("\n" + "=" * 60)
    print("Entrainement termine avec succes !")
    print("=" * 60)
    return model, metrics



if __name__ == "__main__":   
    main()