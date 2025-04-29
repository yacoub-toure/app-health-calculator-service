from flask import Flask, request, jsonify, render_template
from health_utils import calculate_bmi, calculate_bmr

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/bmi', methods=['POST'])
def bmi():
    try:
        data = request.get_json()
        height = float(data['height'])
        weight = float(data['weight'])
        result = calculate_bmi(height, weight)
        return jsonify({'bmi': round(result, 2)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/bmr', methods=['POST'])
def bmr():
    try:
        data = request.get_json()
        height = float(data['height'])
        weight = float(data['weight'])
        age = int(data['age'])
        gender = data['gender']
        result = calculate_bmr(height, weight, age, gender)
        return jsonify({'bmr': round(result, 2)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)