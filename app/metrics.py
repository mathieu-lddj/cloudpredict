from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Compteur de predictions
prediction_count = Counter(
    "cloudpredict_prediction_total",
    "Nombre total de predictions effectuees",
    ["status"]
)

# Histogramme de latence des predictions
prediction_latency = Histogram(
    "cloudpredict_prediction_latency_seconds",
    "Latence des predictions en secondes",
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# Compteur d'erreurs
prediction_errors = Counter(
    "cloudpredict_prediction_errors_total",
    "Nombre total d'erreurs de prediction",
    ["error_type"]
)

# Gauge pour le statut de l'application
app_info = Gauge(
    "cloudpredict_app_info",
    "Informations sur l'application",
    ["version"]
)

app_info.labels(version="1.0.0").set(1)
def get_metrics():
    """Genere les metriques au format Prometheus."""
    return generate_latest(), CONTENT_TYPE_LATEST
