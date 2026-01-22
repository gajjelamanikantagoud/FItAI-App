def calculate_bmi(weight, height):
    """
    weight in kg, height in cm
    """
    return round(weight / ((height / 100) ** 2), 2)


def activity_factor(level):
    factors = {
        "Sedentary": 1.2,
        "Light": 1.4,
        "Moderate": 1.6,
        "Active": 1.8
    }
    return factors.get(level, 1.2)
