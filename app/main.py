# app/main.py
import time
import logging
from flask import Flask, request, jsonify, Response
from app.predict import predict, get_model, FEATURE_NAMES
from app.metrics import (
    prediction_count,
    prediction_latency,
    prediction_errors,
    get_metrics
)
from app.logging_config import setup_logging

# Initialiser le logging
logger = setup_logging()

# Creer l'application Flask
app = Flask(__name__)

@app.before_request
def log_request():
    """Log chaque requete entrante."""
    logger.info(f"Requete: {request.method} {request.path}")

@app.route("/health", methods=["GET"])
def health():
    """Endpoint de health check."""
    try:
        # Verifier que le modele est charge
        model = get_model()
        model_status = "loaded"
    except Exception as e:
        model_status = f"error: {str(e)}"
    
    response = {
        "status": "ok",
        "service": "cloudpredict-api",
        "version": "1.0.0",
        "model_status": model_status
    }
    status_code = 200 if model_status == "loaded" else 503
    return jsonify (response), status_code

@app.route("/metrics", methods=["GET"])
def metrics():
    """Endpoint Prometheus metrics."""
    metrics_data, content_type = get_metrics()
    return Response (metrics_data, mimetype=content_type)

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """Endpoint de prediction."""
    start_time = time.time()
    try:
        # Verifier le Content-Type
        if not request.is_json:
            prediction_errors.labels (error_type="invalid_content_type").inc()
            return jsonify({
                "error": "Content-Type doit etre application/json"
            }), 415
            
        # Recuperer les donnees
        data = request.get_json()
        if data is None:
            prediction_errors.labels (error_type="invalid_json").inc()
            return jsonify({
                "error": "Body JSON invalide"
            }), 400
            
        # Effectuer la prediction
        result, errors = predict(data)
        if errors:
            prediction_errors.labels (error_type="validation_error").inc()
            prediction_count.labels (status="error").inc()
            return jsonify({
                "error": "Erreur de validation",
                "details": errors
            }), 422
            
        # Succes
        latency = time.time() - start_time
        prediction_latency.observe(latency)
        prediction_count.labels (status="success").inc()
        result["latency_ms"] = round(latency * 1000, 2)
        logger.info(f"Prediction reussie: {result['prediction']} (latence: {result['latency_ms']}ms)")
        return jsonify(result), 200
        
    except Exception as e:
        prediction_errors.labels (error_type="internal_error").inc()
        prediction_count.labels(status="error").inc()
        logger.error(f"Erreur interne: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Erreur interne du serveur",
            "message": str(e)
        }), 500

@app.route("/info", methods=["GET"])
def info():
    """Retourne les informations sur le modele et les features attendues."""
    return jsonify({
        "service": "cloudpredict-api",
        "version": "1.0.0",
        "model": "Random ForestRegressor",
        "dataset": "California Housing",
        "features": FEATURE_NAMES,
        "target": "MedHouseVal (prix median en 100k USD)",
        "endpoints": {
            "GET /health": "Health check",
            "GET /metrics": "Prometheus metrics",
            "GET /info": "Informations sur l'API",
            "POST /predict": "Prediction de prix immobilier"
        }
    }), 200

@app.route("/", methods=["GET"])
def root():
    """Page d'accueil avec redirection vers /info."""
    return jsonify({
        "message": "Bienvenue sur CloudPredict API",
        "documentation": "/info"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)