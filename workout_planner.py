def generate_workout(goal, time):
    if goal == 'Fat Loss':
        return ['HIIT', 'Cardio', 'Core']
    elif goal == 'Muscle Gain':
        return ['Push', 'Pull', 'Legs']
    else:
        return ['Full Body', 'Stretching']