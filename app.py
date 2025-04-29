from flask import Flask, request, jsonify
from health_utils import calculate_bmi, calculate_bmr

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/bmi', methods=['POST'])
def bmi():
    """
    Calculate BMI endpoint
    Expected JSON payload:
    {
        "height": float,  # in meters
        "weight": float   # in kilograms
    }
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
        return jsonify({"error": "Internal server error"}), 500

@app.route('/bmr', methods=['POST'])
def bmr():
    """
    Calculate BMR endpoint
    Expected JSON payload:
    {
        "height": float,  # in centimeters
        "weight": float,  # in kilograms
        "age": int,      # in years
        "gender": str    # 'male' or 'female'
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['height', 'weight', 'age', 'gender']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
            
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
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 