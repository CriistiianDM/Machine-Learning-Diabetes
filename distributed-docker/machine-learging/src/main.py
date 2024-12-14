import pandas as pd
import requests
import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv


VALID_TOKEN = os.getenv("VALID_TOKEN")
FILE_PATH = os.getenv("FILE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY") 
URL = "http://localhost:5001/resources-training"

# Load .Env
load_dotenv()

app = Flask(__name__)

@app.route('/execute', methods=['GET'])
def init():
    request_data()
    print("Holaaaa")
    return jsonify({"data": "Holi"}), 200


def request_data():
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {VALID_TOKEN}"
        }

        response = requests.post(URL, json={}, headers=headers)
        if response.status_code == 200:
            print(response.json(),"Aaa")
        else:
            print(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, host="0.0.0.0", port=port)
