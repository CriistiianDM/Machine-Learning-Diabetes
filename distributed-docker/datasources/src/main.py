from flask import Flask, request, jsonify
import pandas as pd
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

load_dotenv()

app = Flask(__name__)

VALID_TOKEN = os.getenv("VALID_TOKEN")
FILE_PATH = os.getenv("FILE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY") 

# Convert to 32 bits
SECRET_KEY = SECRET_KEY.encode()[:32] 

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
        df = pd.read_csv(FILE_PATH)
        data = {"sources": df.to_dict(orient="records")}
        encrypted_response = encrypt_data(str(data))

        return jsonify({"data": encrypted_response}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def encrypt_data(data: str):
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(SECRET_KEY[:16]), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(encrypted_data).decode('utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)

