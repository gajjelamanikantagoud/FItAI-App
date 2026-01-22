import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib


# Sample dataset


data = {
'age': [18, 20, 22, 25],
'height': [165, 170, 175, 180],
'weight': [55, 65, 75, 85],
'activity': [1.2, 1.4, 1.6, 1.8],
'calories': [1800, 2200, 2600, 3000]
}


df = pd.DataFrame(data)
X = df[['age', 'height', 'weight', 'activity']]
y = df['calories']


model = LinearRegression()
model.fit(X, y)


joblib.dump(model, 'models/calorie_model.pkl')
print('Model trained and saved')
