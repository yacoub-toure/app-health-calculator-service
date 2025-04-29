# health_utils.py
def calculate_bmi(height: float, weight: float) -> float:
    """
    Calculate Body Mass Index (BMI) given height in meters and weight in kilograms.

    Args:
        height (float): Height in meters
        weight (float): Weight in kilograms

    Returns:
        float: BMI value
    """
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive numbers")
    return weight / (height ** 2)

def calculate_bmr(height: float, weight: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation.

    Args:
        height (float): Height in centimeters
        weight (float): Weight in kilograms
        age (int): Age in years
        gender (str): 'male' or 'female'

    Returns:
        float: BMR value
    """
    if height <= 0 or weight <= 0 or age <= 0:
        raise ValueError("Height, weight, and age must be positive numbers")

    gender_lower = gender.lower()
    if gender_lower not in ['male', 'female']:
        raise ValueError("Gender must be 'male' or 'female'")

    if gender_lower == 'male':
        # BMR = 88.362 + (13.397 x weight (kg)) + (4.799 x height (cm)) - (5.677 x age (years))
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else: # female
        # BMR = 447.593 + (9.247 x weight (kg)) + (3.098 x height (cm)) - (4.330 x age (years))
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)