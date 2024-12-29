# Imports
import pandas as pd
import requests
import os
import json
import base64

# Froms
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from learning.learning import Learning
from upload.upload import UploadModel

VALID_TOKEN = os.getenv("VALID_TOKEN")
FILE_PATH = os.getenv("FILE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY") 
URL = os.getenv("URL")

# Load .Env
load_dotenv()

app = Flask(__name__)

@app.route('/execute', methods=['GET'])
def init():
    dataTraining = request_data()
    decrypt = decrypt_data(dataTraining['data'])

    learning_instance = Learning(decrypt)
    accuracy = learning_instance.learnig()
    # Upload S3 Model
    # learning_instance = Learning(decrypt)
    # uploadModel = UploadModel(learning_instance)
    # uploadModel.upload()
    # accuracy = learning_instance.learnig()

    # # Upload Model to sagemaker
    # sagemarker_instance = SageMakerr()
    # sagemarker_instance.deploy_model()

    return jsonify({"accuracy": accuracy}), 200


def request_data():
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {VALID_TOKEN}"
        }
        print(URL)
        response = requests.post(URL, json={}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

def decrypt_data(encrypted_data):
    encrypted_data_bytes = base64.b64decode(encrypted_data)

    key_bytes = SECRET_KEY.encode('utf-8') if isinstance(SECRET_KEY, str) else SECRET_KEY

    key_bytes = key_bytes[:32]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(key_bytes[:16]), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

    try:
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    except ValueError as e:
        print(f"Padding error: {e}")
        return None
    return unpadded_data.decode('utf-8')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, host="0.0.0.0", port=port)
