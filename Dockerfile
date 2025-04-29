# Dockerfile

# Utilise une image Python 3.12 slim comme base
FROM python:3.12-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances
COPY requirements.txt .

# Installe les dépendances
# --no-cache-dir réduit la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application dans le répertoire de travail
# Inclut app.py, health_utils.py, et le répertoire templates/
COPY . .

# Expose le port sur lequel l'application Flask écoute
EXPOSE 5000

# Commande pour exécuter l'application lorsque le conteneur démarre
# Utilise gunicorn si installé, sinon python app.py (pour la simplicité ici)
# Pour la production, préférer gunicorn:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]