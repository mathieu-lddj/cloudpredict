import os
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
def load_model(filepath):
    """Charge un modele sauvegarde avec joblib."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Modele introuvable : {filepath}")
    model = joblib.load(filepath)
    print(f"Modele charge depuis : {filepath}")
    return model
def evaluate(model, X_test, y_test):
    """Evalue le modele et affiche les metriques detaillees."""
    y_pred = model.predict(X_test)
    metrics = {
    "mae": mean_absolute_error(y_test, y_pred),
    "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
    "r2": r2_score(y_test, y_pred),
    "mean_prediction": np.mean(y_pred),
    "std_prediction": np.std(y_pred),
    "min_prediction": np.min(y_pred),
    "max_prediction": np.max(y_pred),
    }
    return metrics, y_pred
def main():
    print("=" * 60)
    print("CloudPredict - Evaluation du modele")
    print("=" * 60)
    # Charger les donnees
    print("\n[1/3] Chargement du dataset...")
    housing = fetch_california_housing()
    X = pd.DataFrame(housing.data, columns=housing.feature_names)
    y = pd.Series(housing.target, name="MedHouseVal")
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
    )
    # Charger le modele
    print("\n[2/3] Chargement du modele sauvegarde...")
    model_path = os.path.join(os.path.dirname(__file__), "models", "model.joblib")
    model = load_model(model_path)
    # Evaluer
    print("\n[3/3] Evaluation sur le jeu de test...")
    metrics, y_pred = evaluate(model, X_test, y_test)
    print("\n--- Metriques de performance ---")
    print(f" MAE : {metrics['mae']:.4f}")
    print(f" RMSE : {metrics['rmse']:.4f}")
    print(f" R2 Score : {metrics['r2']:.4f}")
    print("\n--- Statistiques des predictions ---")
    print(f" Moyenne : {metrics['mean_prediction']:.4f}")
    print(f" Ecart-type : {metrics['std_prediction']:.4f}")
    print(f" Min : {metrics['min_prediction']:.4f}")
    print(f" Max : {metrics['max_prediction']:.4f}")
    print("\n--- Comparaison valeurs reelles vs predictions (5 premiers) ---")
    for i in range(5):
        print(f" Reel: {y_test.iloc[i]:.4f} | Predit: {y_pred[i]:.4f} | Erreur: {abs(y_test.iloc[i] - y_pred[i]):.4f}")
    print("\n" + "=" * 60)
    print("Evaluation terminee !")
    print("=" * 60)
    
    
if __name__ == "__main__":
    main()