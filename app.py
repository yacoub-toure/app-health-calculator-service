# app.py
from flask import Flask, request, jsonify, render_template
from health_utils import calculate_bmi, calculate_bmr
import math # Import math pour le calcul du prêt

app = Flask(__name__)

# --- Endpoint pour l'interface Web (Calculateur de Prêt) ---
@app.route("/")
def home():
    """Sert la page HTML principale."""
    return render_template("home.html")

# --- Endpoint pour le Calcul de Prêt (utilisé par l'interface Web) ---
# !!! CETTE PARTIE MANQUAIT DANS TON FICHIER !!!
@app.route('/calculate', methods=['POST'])
def calculate_loan_endpoint():
    """
    Calcule les détails d'un prêt.
    Attend les données du formulaire : loan_amount, duration, interest_rate.
    """
    try:
        # Récupère les données envoyées par le formulaire HTML via jQuery $.post
        # request.form est utilisé car jQuery envoie les données comme un formulaire
        data = request.form

        required_fields = ['loan_amount', 'duration', 'interest_rate']
        if not all(field in data for field in required_fields):
            missing = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required form fields: {', '.join(missing)}"}), 400

        loan_amount = float(data['loan_amount'])
        duration_years = int(data['duration'])
        interest_rate_percent = float(data['interest_rate'])

        if loan_amount <= 0 or duration_years <= 0 or interest_rate_percent < 0:
             raise ValueError("Loan amount, duration must be positive, and interest rate cannot be negative.")

        # Calculs
        monthly_interest_rate = (interest_rate_percent / 100) / 12
        number_of_payments = duration_years * 12

        # Gérer le cas où le taux d'intérêt est 0
        if monthly_interest_rate == 0:
            # Éviter la division par zéro si le nombre de paiements est aussi 0 (durée 0)
            if number_of_payments == 0:
                 monthly_payment = 0 # Ou gérer comme une erreur si la durée 0 n'est pas permise
            else:
                 monthly_payment = loan_amount / number_of_payments
        else:
            # Formule standard pour le paiement mensuel
            monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)

        total_cost = monthly_payment * number_of_payments

        return jsonify({
            "monthly_payment": monthly_payment,
            "total_cost": total_cost
        }), 200

    except ValueError as e:
        # Gère les erreurs de conversion (ex: texte au lieu de nombre) ou les valeurs négatives/nulles
        return jsonify({"error": f"Invalid input data: {str(e)}"}), 400
    except Exception as e:
        # Gère les autres erreurs inattendues
        app.logger.error(f"Error in /calculate: {str(e)}") # Log l'erreur pour le débogage
        return jsonify({"error": "Internal server error"}), 500
# !!! FIN DE LA PARTIE MANQUANTE !!!

# --- Endpoint de Vérification de Santé ---
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé."""
    return jsonify({"status": "healthy"}), 200

# --- Endpoint pour le Calcul du BMI ---
@app.route('/bmi', methods=['POST'])
def bmi():
    """
    Endpoint de calcul du BMI.
    Attend un JSON : {"height": float (m), "weight": float (kg)}
    """
    try:
        data = request.get_json()

        if not data or 'height' not in data or 'weight' not in data:
            return jsonify({"error": "Missing required fields: height and weight"}), 400

        height = float(data['height'])
        weight = float(data['weight'])

        bmi_value = calculate_bmi(height, weight)

        return jsonify({
            "bmi": round(bmi_value, 2),
            "height": height,
            "weight": weight
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error in /bmi: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# --- Endpoint pour le Calcul du BMR ---
@app.route('/bmr', methods=['POST'])
def bmr():
    """
    Endpoint de calcul du BMR.
    Attend un JSON : {"height": float (cm), "weight": float (kg), "age": int, "gender": str ('male'/'female')}
    """
    try:
        data = request.get_json()

        required_fields = ['height', 'weight', 'age', 'gender']
        if not data or not all(field in data for field in required_fields):
            missing = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        height = float(data['height'])
        weight = float(data['weight'])
        age = int(data['age'])
        gender = data['gender']

        bmr_value = calculate_bmr(height, weight, age, gender)

        return jsonify({
            "bmr": round(bmr_value, 2),
            "height": height,
            "weight": weight,
            "age": age,
            "gender": gender
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error in /bmr: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# --- Démarrage de l'application ---
if __name__ == '__main__':
    # Utilise le port 5000 par défaut, mais peut être surchargé par une variable d'environnement PORT
    import os
    port = int(os.environ.get('PORT', 5000))
    # Active le mode debug pour voir les erreurs plus facilement pendant le développement local
    # Ne pas utiliser debug=True en production !
    app.run(host='0.0.0.0', port=port, debug=True)