# Imports
import pandas as pd
import os
import boto3
import base64
import io

# Froms
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

load_dotenv()

app = Flask(__name__)

VALID_TOKEN = os.getenv("VALID_TOKEN")
FILE_PATH = os.getenv("FILE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY") 

# Convert to 32 bits
SECRET_KEY = SECRET_KEY.encode()[:32] 

# S3
BUCKET_NAME = os.getenv("BUCKET_NAME")
CSV_FILE_KEY = os.getenv("CSV_FILE_KEY")

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name='us-east-2'
)

@app.route('/resources-training', methods=['POST'])
def date_csv():
    token = request.headers.get('Authorization')

    if token != f"Bearer {VALID_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    if not FILE_PATH:
        return jsonify({"error": "File path is required"}), 400

    if not os.path.exists(FILE_PATH):
        return jsonify({"error": "File not found"}), 404

    try:
        # df = pd.read_csv(FILE_PATH)
        # data = df.to_csv(index=False)
        # S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=CSV_FILE_KEY)
        csv_content = response['Body'].read()

        encrypted_response = encrypt_data(csv_content)

        return jsonify({"data": encrypted_response}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def encrypt_data(data: bytes) -> str:
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(SECRET_KEY[:16]), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(encrypted_data).decode('utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)

