# tests/test_api.py
import json
import pytest
from app.main import app

@pytest.fixture
def client():
    """Cree un client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoint:
    """Tests pour l'endpoint /health."""
    def test_health_returns_200(self, client):
        """Le health check doit retourner un code 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Le health check doit retourner du JSON."""
        response = client.get("/health")
        data = response.get_json()
        assert data is not None
        assert "status" in data
        assert data["status"] == "ok"

    def test_health_contains_service_info(self, client):
        """Le health check doit contenir les informations du service."""
        response = client.get("/health")
        data = response.get_json()
        assert "service" in data
        assert data["service"] == "cloudpredict-api"
        assert "version" in data
        assert "model_status" in data

class TestPredictEndpoint:
    """Tests pour l'endpoint /predict."""
    def test_predict_with_dict_features(self, client):
        """Prediction avec un dictionnaire de features."""
        payload = {
            "features": {
                "MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984,
                "AveBedrms": 1.024,
                "Population": 322.0,
                "AveOccup": 2.556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "prediction" in data
        assert isinstance(data["prediction"], float)
        assert "unit" in data

    def test_predict_with_list_features(self, client):
        """Prediction avec une liste de valeurs."""
        payload = {
            "features": [8.3252, 41.0, 6.984, 1.024, 322.0, 2.556, 37.88, -122.23]
        }
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "prediction" in data
        assert isinstance(data["prediction"], float)

    def test_predict_missing_features(self, client):
        """Prediction sans features doit retourner une erreur 422."""
        payload = {}
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 422

    def test_predict_wrong_feature_count(self, client):
        """Prediction avec un mauvais nombre de features doit retourner une erreur."""
        payload = {
            "features": [1.0, 2.0, 3.0]
        }
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 422

    def test_predict_missing_feature_key(self, client):
        """Prediction avec une feature manquante dans le dict doit retourner une erreur."""
        payload = {
            "features": {
                "MedInc": 8.3252,
                "HouseAge": 41.0
            }
        }
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 422

    def test_predict_wrong_content_type(self, client):
        """Prediction sans Content-Type JSON doit retourner une erreur 415."""
        response = client.post(
            "/predict",
            data="not json",
            content_type="text/plain"
        )
        assert response.status_code == 415

    def test_predict_returns_latency(self, client):
        """La reponse de prediction doit contenir la latence."""
        payload = {
            "features": [8.3252, 41.0, 6.984, 1.024, 322.0, 2.556, 37.88, -122.23]
        }
        response = client.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        data = response.get_json()
        assert "latency_ms" in data

class TestMetricsEndpoint:
    """Tests pour l'endpoint /metrics."""
    def test_metrics_returns_200(self, client):
        """L'endpoint metrics doit retourner un code 200."""
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_contains_prometheus_data(self, client):
        """Les metriques doivent contenir des donnees Prometheus."""
        response = client.get("/metrics")
        content = response.data.decode("utf-8")
        assert "cloudpredict_prediction_total" in content
        assert "cloudpredict_app_info" in content

class TestInfoEndpoint:
    """Tests pour l'endpoint /info."""
    def test_info_returns_200(self, client):
        """L'endpoint info doit retourner un code 200."""
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_contains_features(self, client):
        """L'endpoint info doit lister les features attendues."""
        response = client.get("/info")
        data = response.get_json()
        assert "features" in data
        assert len(data["features"]) == 8

    def test_info_contains_endpoints(self, client):
        """L'endpoint info doit lister les endpoints disponibles."""
        response = client.get("/info")
        data = response.get_json()
        assert "endpoints" in data

class TestRootEndpoint:
    """Tests pour l'endpoint /."""
    def test_root_returns_200(self, client):
        """La racine doit retourner un code 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_message(self, client):
        """La racine doit contenir un message de bienvenue."""
        response = client.get("/")
        data = response.get_json()
        assert "message" in data