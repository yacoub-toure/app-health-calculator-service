import pytest
import json # Import json module
from app import app # Import the Flask app instance
from health_utils import calculate_bmi, calculate_bmr

# --- Fixture pour le client de test Flask ---
# Cette fonction spéciale de pytest crée une instance du client de test
# pour notre application Flask. Elle sera utilisée par les tests d'API.
@pytest.fixture
def client():
    # Met l'application en mode test (désactive certaines fonctionnalités de production
    # comme l'interception d'erreurs pour faciliter le débogage des tests)
    app.config['TESTING'] = True
    # Crée un client de test qui peut envoyer des requêtes virtuelles à l'app
    with app.test_client() as client:
        yield client # Fournit le client aux fonctions de test

# --- Tests Unitaires pour health_utils (existants et corrigés) ---

def test_calculate_bmi():
    # Test normal case
    assert round(calculate_bmi(1.75, 70), 2) == 22.86

    # Test edge cases
    with pytest.raises(ValueError):
        calculate_bmi(-1.75, 70)
    with pytest.raises(ValueError):
        calculate_bmi(1.75, -70)
    with pytest.raises(ValueError):
        calculate_bmi(0, 70)

def test_calculate_bmr():
    # Test male BMR with correct expected value
    assert round(calculate_bmr(175, 70, 30, 'male'), 2) == 1695.67 # Valeur corrigée

    # Test female BMR with correct expected value
    assert round(calculate_bmr(175, 70, 30, 'female'), 2) == 1507.13 # Valeur corrigée

    # Test edge cases
    with pytest.raises(ValueError):
        calculate_bmr(-175, 70, 30, 'male')
    with pytest.raises(ValueError):
        calculate_bmr(175, -70, 30, 'male')
    with pytest.raises(ValueError):
        calculate_bmr(175, 70, -30, 'male')
    with pytest.raises(ValueError):
        calculate_bmr(175, 70, 30, 'invalid')

# --- Nouveaux Tests pour les Endpoints de l'API Flask ---

# Tests pour l'endpoint /bmi
def test_bmi_api_success(client):
    """Teste une requête réussie vers l'endpoint /bmi."""
    response = client.post('/bmi', json={'height': 1.75, 'weight': 70})
    data = response.get_json()

    assert response.status_code == 200 # Vérifie le code de statut HTTP
    assert 'bmi' in data
    assert data['bmi'] == 22.86 # Vérifie la valeur calculée
    assert data['height'] == 1.75
    assert data['weight'] == 70

def test_bmi_api_missing_fields(client):
    """Teste une requête vers /bmi avec des champs manquants."""
    response = client.post('/bmi', json={'height': 1.75}) # 'weight' est manquant
    data = response.get_json()

    assert response.status_code == 400 # Doit retourner Bad Request
    assert 'error' in data
    assert 'Missing required fields' in data['error'] # Vérifie le message d'erreur

def test_bmi_api_invalid_type(client):
    """Teste une requête vers /bmi avec un type de données invalide."""
    response = client.post('/bmi', json={'height': 'abc', 'weight': 70}) # 'height' n'est pas un nombre
    data = response.get_json()

    assert response.status_code == 400 # Doit retourner Bad Request (car ValueError est attrapé)
    assert 'error' in data
    # Le message exact peut varier, mais il doit indiquer un problème de conversion
    assert 'could not convert string to float' in data['error'].lower()

# Tests pour l'endpoint /bmr
def test_bmr_api_success_male(client):
    """Teste une requête réussie vers /bmr pour un homme."""
    payload = {'height': 175, 'weight': 70, 'age': 30, 'gender': 'male'}
    response = client.post('/bmr', json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert 'bmr' in data
    assert data['bmr'] == 1695.67 # Utilise la valeur corrigée
    assert data['height'] == 175
    assert data['weight'] == 70
    assert data['age'] == 30
    assert data['gender'] == 'male'

def test_bmr_api_success_female(client):
    """Teste une requête réussie vers /bmr pour une femme."""
    payload = {'height': 175, 'weight': 70, 'age': 30, 'gender': 'female'}
    response = client.post('/bmr', json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert 'bmr' in data
    assert data['bmr'] == 1507.13 # Utilise la valeur corrigée
    assert data['gender'] == 'female'

def test_bmr_api_missing_fields(client):
    """Teste une requête vers /bmr avec des champs manquants."""
    payload = {'height': 175, 'weight': 70, 'age': 30} # 'gender' est manquant
    response = client.post('/bmr', json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data
    assert 'Missing required fields' in data['error']

def test_bmr_api_invalid_gender(client):
    """Teste une requête vers /bmr avec un genre invalide."""
    payload = {'height': 175, 'weight': 70, 'age': 30, 'gender': 'other'}
    response = client.post('/bmr', json=payload)
    data = response.get_json()

    assert response.status_code == 400 # ValueError de calculate_bmr est attrapé
    assert 'error' in data
    assert "Gender must be 'male' or 'female'" in data['error']

def test_bmr_api_invalid_type(client):
    """Teste une requête vers /bmr avec un type de données invalide."""
    payload = {'height': 175, 'weight': 'abc', 'age': 30, 'gender': 'male'} # 'weight' invalide
    response = client.post('/bmr', json=payload)
    data = response.get_json()

    assert response.status_code == 400 # ValueError de float() est attrapé
    assert 'error' in data
    assert 'could not convert string to float' in data['error'].lower()

# Test pour l'endpoint /health (simple vérification)
def test_health_check_api(client):
    """Teste l'endpoint de health check."""
    response = client.get('/health')
    data = response.get_json()

    assert response.status_code == 200
    assert 'status' in data
    assert data['status'] == 'healthy'