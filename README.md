## 🚀 Déploiement Kubernetes (Local avec Minikube)

Une fois le projet récupéré, voici les étapes pour lancer l'architecture complète (API, PostgreSQL, Redis) sur un cluster Kubernetes local.

### 1. Prérequis et Génération du Modèle
Le fichier du modèle de Machine Learning n'est pas versionné sur Git. Avant toute chose, vous devez le générer localement :
```bash
# Installer les dépendances Python locales si ce n'est pas fait
pip install -r requirements.txt

# Entraîner et générer le modèle (crée le fichier ml/models/model.joblib)
python -m ml.train