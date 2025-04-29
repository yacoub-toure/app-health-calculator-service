# test.py
import pytest
import json
from app import app # Importe l'instance de l'application Flask
from health_utils import calculate_bmi, calculate_bmr

# --- Fixture pour le client de test Flask ---
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Crée un contexte d'application pour s'assurer que les requêtes fonctionnent correctement
    with app.app_context():
        with app.test_client() as client:
            yield client

# --- Tests Unitaires pour health_utils ---

def test_calculate_bmi():
    assert round(calculate_bmi(1.75, 70), 2) == 22.86
    with pytest.raises(ValueError, match="Height and weight must be positive numbers"):
        calculate_bmi(-1.75, 70)
    with pytest.raises(ValueError, match="Height and weight must be positive numbers"):
        calculate_bmi(1.75, 0)

def test_calculate_bmr():
    # Male
    assert round(calculate_bmr(175, 70, 30, 'male'), 2) == 1695.67
    # Female
    assert round(calculate_bmr(175, 70, 30, 'female'), 2) == 1507.13
    # Edge cases
    with pytest.raises(ValueError, match="Height, weight, and age must be positive numbers"):
        calculate_bmr(175, 70, 0, 'male')
    with pytest.raises(ValueError, match="Gender must be 'male' or 'female'"):
        calculate_bmr(175, 70, 30, 'other')

# --- Tests pour les Endpoints de l'API Flask ---

# Test pour l'endpoint / (Page d'accueil)
def test_home_page(client):
    """Teste que la page d'accueil se charge correctement."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    # Vérifie la présence d'un élément clé de la page
    assert b'<title>Loan Calculator</title>' in response.data

# Test pour l'endpoint /health
def test_health_check_api(client):
    """Teste l'endpoint de health check."""
    response = client.get('/health')
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"status": "healthy"}

# Tests pour l'endpoint /bmi
def test_bmi_api_success(client):
    response = client.post('/bmi', json={'height': 1.75, 'weight': 70})
    data = response.get_json()
    assert response.status_code == 200
    assert data['bmi'] == 22.86

def test_bmi_api_missing_fields(client):
    response = client.post('/bmi', json={'height': 1.75})
    assert response.status_code == 400
    assert 'Missing required fields' in response.get_json()['error']

def test_bmi_api_invalid_type(client):
    response = client.post('/bmi', json={'height': 'abc', 'weight': 70})
    assert response.status_code == 400 # Attrape ValueError de float()
    assert 'could not convert string to float' in response.get_json()['error'].lower()

# Tests pour l'endpoint /bmr
def test_bmr_api_success(client):
    payload = {'height': 175, 'weight': 70, 'age': 30, 'gender': 'male'}
    response = client.post('/bmr', json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data['bmr'] == 1695.67

def test_bmr_api_missing_fields(client):
    payload = {'height': 175, 'weight': 70, 'age': 30} # gender manquant
    response = client.post('/bmr', json=payload)
    assert response.status_code == 400
    assert 'Missing required fields' in response.get_json()['error']

def test_bmr_api_invalid_gender(client):
    payload = {'height': 175, 'weight': 70, 'age': 30, 'gender': 'other'}
    response = client.post('/bmr', json=payload)
    assert response.status_code == 400 # Attrape ValueError de calculate_bmr
    assert "Gender must be 'male' or 'female'" in response.get_json()['error']

# --- Nouveaux Tests pour l'Endpoint /calculate ---

def test_calculate_loan_api_success(client):
    """Teste une requête réussie vers l'endpoint /calculate."""
    # Note: On envoie les données comme 'data' car c'est un formulaire POST
    payload = {'loan_amount': '10000', 'duration': '5', 'interest_rate': '5.5'}
    response = client.post('/calculate', data=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert 'monthly_payment' in data
    assert 'total_cost' in data
    assert round(data['monthly_payment'], 2) == 191.01 # Valeur attendue pour cet exemple
    assert round(data['total_cost'], 2) == 11460.7  # Valeur attendue pour cet exemple

def test_calculate_loan_api_zero_interest(client):
    """Teste le calcul avec un taux d'intérêt de 0."""
    payload = {'loan_amount': '12000', 'duration': '2', 'interest_rate': '0'}
    response = client.post('/calculate', data=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert round(data['monthly_payment'], 2) == 500.00 # 12000 / 24
    assert round(data['total_cost'], 2) == 12000.00

def test_calculate_loan_api_missing_fields(client):
    """Teste une requête vers /calculate avec des champs manquants."""
    payload = {'loan_amount': '10000', 'duration': '5'} # interest_rate manquant
    response = client.post('/calculate', data=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data
    assert 'Missing required form fields' in data['error']
    assert 'interest_rate' in data['error']

def test_calculate_loan_api_invalid_type(client):
    """Teste une requête vers /calculate avec un type de données invalide."""
    payload = {'loan_amount': 'abc', 'duration': '5', 'interest_rate': '5.5'}
    response = client.post('/calculate', data=payload)
    data = response.get_json()

    assert response.status_code == 400 # Attrape ValueError de float()
    assert 'error' in data
    assert 'Invalid input data' in data['error']
    assert 'could not convert string to float' in data['error'].lower()

def test_calculate_loan_api_negative_value(client):
    """Teste une requête vers /calculate avec une valeur négative invalide."""
    payload = {'loan_amount': '-10000', 'duration': '5', 'interest_rate': '5.5'}
    response = client.post('/calculate', data=payload)
    data = response.get_json()

    assert response.status_code == 400 # Attrape ValueError personnalisé
    assert 'error' in data
    assert 'Invalid input data' in data['error']
    assert 'must be positive' in data['error']