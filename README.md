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

#### Linux (Bash)
```bash
# Connecter le terminal au démon Docker de Minikube
eval $(minikube docker-env)

# Construire l'image (le modèle généré à l'étape 2 sera inclus)
docker build -t cloudpredict-api:latest -f docker/Dockerfile.api .
```

#### Windows (Powershell)
```powershell
# Connecter le terminal au démon Docker de Minikube
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Construire l'image
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
Ajoutez l'entrée suivante dans votre fichier hosts pour utiliser le nom de domaine local :

* **Fichier Linux/macOS :** `/etc/hosts`
* **Fichier Windows :** `C:\Windows\System32\drivers\etc\hosts`

**Commande pour récupérer l'IP :**
```bash
minikube ip
```
**Ligne à ajouter :**
`<IP_MINIKUBE> cloudpredict.local`

---

## 🧪 Tests et Validation
Une fois le déploiement terminé, testez les points d'entrée :

**Health Check :**
* **Bash/Linux :** `curl http://cloudpredict.local/health`
* **PowerShell :** `Invoke-RestMethod -Uri http://cloudpredict.local/health`

**Prédiction :**
* **Bash/Linux :**
    ```bash
    curl -X POST http://cloudpredict.local/predict \
         -H "Content-Type: application/json" \
         -d '{"features": {"surface": 75, "pieces": 3, "etage": 2, "parking": 1, "quartier": "centre-ville", "annee_construction": 2005}}'
    ```
* **PowerShell :**
    ```powershell
    $body = @{
        features = @{
            surface = 75
            pieces = 3
            etage = 2
            parking = 1
            quartier = "centre-ville"
            annee_construction = 2005
        }
    } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri http://cloudpredict.local/predict -Body $body -ContentType "application/json"
    ```

## 🛠️ Commandes Utiles
* **Surveiller les pods :** `kubectl get pods -n cloudpredict`
* **Logs de l'API :** `kubectl logs -l component=api -n cloudpredict`
* **Statut de l'autoscaling :** `kubectl get hpa -n cloudpredict`




