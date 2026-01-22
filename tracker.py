import pandas as pd
from datetime import date


def log_activity(user, workout_done, calories):
    df = pd.read_csv('data/user_logs.csv')
    new_row = {
    'date': date.today(),
    'user': user,
    'workout_done': workout_done,
    'calories': calories
    }
    df = df.append(new_row, ignore_index=True)
    df.to_csv('data/user_logs.csv', index=False)