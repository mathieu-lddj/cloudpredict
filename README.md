# CloudPredict - Plateforme de Prédiction Immobilière

## 🚀 Guide de Déploiement (Kubernetes)

### 1. Prérequis techniques
* **Docker** installé et fonctionnel.
* **Minikube** (version $\ge 1.32$).
* **kubectl** (version $\ge 1.28$).
* **Python 3.11** pour la phase de préparation locale.

### 2. Préparation du Modèle ML
Le modèle de prédiction (`model.joblib`) n'est pas versionné sur GitHub car il est volumineux. Vous devez le régénérer localement :
```bash
# Installation des dépendances
pip install -r requirements.txt

# Entraînement et sauvegarde du modèle
python -m ml.train
```

### 3. Démarrage du Cluster Local
Initialisez Minikube avec les ressources nécessaires et activez les addons pour le réseau et les métriques :
```bash
# Démarrage avec 4 CPU et 8 Go de RAM
minikube start --cpus 4 --memory 8192 --driver docker

# Activation du contrôleur Ingress et du Metrics Server
minikube addons enable ingress
minikube addons enable metrics-server
```

### 4. Construction de l'image dans Minikube
Il est crucial de construire l'image Docker *directement* dans l'environnement Minikube pour que le cluster puisse y accéder sans registre externe :
```bash
# Connecter le terminal au démon Docker de Minikube
eval $(minikube docker-env)

# Construire l'image (le modèle généré à l'étape 2 sera inclus)
docker build -t cloudpredict-api:latest -f docker/Dockerfile.api .
```

### 5. Déploiement des Manifestes
Appliquez les fichiers de configuration Kubernetes situés dans le dossier `k8s/` :
```bash
# 1. Création du Namespace, de la ConfigMap et du Secret
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/api/configmap.yaml
kubectl apply -f k8s/api/secret.yaml

# 2. Déploiement des bases de données (Postgres & Redis)
kubectl apply -f k8s/db/

# 3. Déploiement de l'API et du scaling (HPA)
kubectl apply -f k8s/api/deployment.yaml
kubectl apply -f k8s/api/service.yaml
kubectl apply -f k8s/api/ingress.yaml
kubectl apply -f k8s/api/hpa.yaml
```

### 6. Accès à l'application
Ajoutez l'entrée suivante dans votre fichier `/etc/hosts` (ou `C:\Windows\System32\drivers\etc\hosts`) pour utiliser le nom de domaine local :
```bash
# Récupérer l'IP de Minikube
minikube ip

# Ajouter la ligne suivante dans le fichier hosts
# <IP_MINIKUBE> cloudpredict.local
```

## 🧪 Tests et Validation
Une fois le déploiement terminé, vous pouvez tester les endpoints via l'Ingress :

* **Health Check :**
    `curl http://cloudpredict.local/health`
* **Prédiction :**
    ```bash
    curl -X POST http://cloudpredict.local/predict \
         -H "Content-Type: application/json" \
         -d '{"features": {"surface": 75, "pieces": 3, "etage": 2, "parking": 1, "quartier": "centre-ville", "annee_construction": 2005}}'
    ```

## 🛠️ Commandes Utiles
* **Surveiller les pods :** `kubectl get pods -n cloudpredict`
* **Logs de l'API :** `kubectl logs -l component=api -n cloudpredict`
* **Statut de l'autoscaling :** `kubectl get hpa -n cloudpredict`