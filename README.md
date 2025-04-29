# Health Calculator Microservice

A Python-based microservice that calculates health metrics (BMI and BMR) using a REST API. The project is containerized with Docker and deployed to Azure using GitHub Actions for CI/CD.

## Features

- Calculate Body Mass Index (BMI)
- Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation
- REST API endpoints
- Docker containerization
- Automated testing
- CI/CD pipeline with GitHub Actions
- Azure deployment

## API Endpoints

### Health Check
- `GET /health`
- Returns the health status of the service

### BMI Calculation
- `POST /bmi`
- Request body:
```json
{
    "height": float,  // in meters
    "weight": float   // in kilograms
}
```

### BMR Calculation
- `POST /bmr`
- Request body:
```json
{
    "height": float,  // in centimeters
    "weight": float,  // in kilograms
    "age": int,      // in years
    "gender": str    // 'male' or 'female'
}
```

## Setup and Installation

1. Clone the repository
2. Install dependencies:
```bash
make init
```

3. Run the application:
```bash
make run
```

4. Run tests:
```bash
make test
```

5. Build Docker image:
```bash
make build
```



# Tester l'endpoint /health (GET) :
Tu peux utiliser curl ou même ton navigateur web.

curl http://127.0.0.1:5000/health

### Tester l'endpoint /bmi (POST) :
Cet endpoint attend des données JSON avec height (en mètres) et weight (en kg).

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"height": 1.75, "weight": 70}' \
     http://localhost:5000/bmi


### Tester l'Endpoint /bmi

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"height": 1.75, "weight": 70}' \
     http://localhost:5000/bmi





## Development

The project uses:
- Python 3.9
- Flask for the REST API
- pytest for testing
- Docker for containerization
- GitHub Actions for CI/CD
- Azure App Service for deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 

# utilisation de WSL sur windows

1- ajouter linux (ubuntu) via microsolft app
2-cela ajoutera directement linux dans le wsl
3-sur vscode aller en bas sur les deux fleches a gauche cliquer dessus et selectionné "connect to wsl"

4-installer python si pas encore fait
-sudo apt install python3-pip
-sudo apt install python3-pip
-python3 -m pip --version

installer l'envirennement virtuel

sudo apt install python3.12-venv

python3 -m venv .venv

5- activer l'env

source .venv/bin/activate

6- installer les dépendances

pip3 install -r requirements.txt

7- installer les deux extensions depuis le vscode

-jupyter
- python wsl
