
# Nom de l'image Docker (peut être surchargé par une variable d'environnement)  
IMAGE_NAME ?= health-calculator-service  
TAG ?= latest
# Empêche make d'interpréter ces noms comme des fichiers
.PHONY: init run test build clean

init:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Running the Flask app..."
	python app.py

test:
	@echo "Running tests..."
	pytest test.py -v

build:  
	@echo "--- Building the Docker image (${IMAGE_NAME}:${TAG}) ---"  
	docker build -t ${IMAGE_NAME}:${TAG} .

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 