# Imports
import os
import boto3
import joblib

# Froms
from dotenv import load_dotenv

load_dotenv()

# S3
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

"""
  Upload Model to s3
"""
class UploadModel:
        def __init__(self,model):
            self.model = model

        def upload(self):
            try:
                model_path = 'model.joblib'
                joblib.dump(self.model, model_path)

                s3.upload_file(model_path, BUCKET_NAME, f"model/{model_path}")
                print(f"Modelo subido a s3://{BUCKET_NAME}/model/{model_path}")
            except Exception as e:
                print(f"Error al subir el archivo: {e}")