# Imports
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

"""
    Define Class Learning
"""
class Learning:

    def __init__(self, data):
        self.data = pd.read_csv(StringIO(data))

    def clean_data(self): 
        self.data = self.data.isnull().sum()

    def execute(self): 
        print("Hi!!")

    def learnig(self): 
        # Clean Data
        #self.clean_data()

        # Machine Learning
        self.data['gluc_binary'] = self.data['gluc'].apply(lambda x: 1 if x >= 3 else 0)
        X =  self.data[['age', 'gender', 'height', 'weight', 'ap_hi', 'cholesterol','smoke','alco','active','bmi']]
        y = self.data['gluc_binary']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Training Model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Evaluación
        #y_pred = model.predict(X_test)

        #return accuracy_score(y_test, y_pred)
        return model