def generate_diet(diet_type, budget):
    if diet_type == "Non-Veg":
        return {
            "Breakfast": [
                {"item": "Boiled Eggs", "grams": 100, "cal": 155},
                {"item": "Banana", "grams": 120, "cal": 105}
            ],
            "Lunch": [
                {"item": "Chicken Curry", "grams": 150, "cal": 240},
                {"item": "Rice", "grams": 200, "cal": 260}
            ],
            "Snacks": [
                {"item": "Peanuts", "grams": 50, "cal": 280}
            ],
            "Dinner": [
                {"item": "Chapati", "grams": 100, "cal": 220},
                {"item": "Curd", "grams": 100, "cal": 98}
            ]
        }
    else:
        return {
            "Breakfast": [
                {"item": "Oats", "grams": 60, "cal": 230}
            ],
            "Lunch": [
                {"item": "Dal", "grams": 150, "cal": 180},
                {"item": "Rice", "grams": 200, "cal": 260}
            ]
        }
