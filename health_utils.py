def calculate_bmi(height, weight):
    """
    Calculate BMI given height in meters and weight in kilograms.
    """
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive numbers.")
    return weight / (height ** 2)

def calculate_bmr(height, weight, age, gender):
    """
    Calculate BMR using the Harris-Benedict equation.
    Height in cm, weight in kg, age in years, gender as 'male' or 'female'.
    """
    if height <= 0 or weight <= 0 or age <= 0:
        raise ValueError("Height, weight, and age must be positive numbers.")
    if gender.lower() == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == 'female':
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'.")