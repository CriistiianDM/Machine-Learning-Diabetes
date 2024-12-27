import joblib
import os
import pandas as pd

def model_fn(model_dir):
    model_path = os.path.join(model_dir, "model.joblib")
    model = joblib.load(model_path)
    return model

def predict_fn(input_data, model):
    df = pd.DataFrame(input_data)
    predictions = model.predict(df)
    return predictions.tolist()