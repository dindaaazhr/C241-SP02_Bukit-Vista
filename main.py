import os
import pandas as pd
from flask import Flask, request, render_template, jsonify
import uuid
from datetime import datetime
import firebase_admin
from services.storeData import store_data
from model.similarity_model import SimilarityModel
import pickle
import requests
import tempfile
from dotenv import load_dotenv

load_dotenv()

MODEL_URL = os.getenv('MODEL_URL')

def load_pickle_model(url):
    response = requests.get(url)
    response.raise_for_status()  
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(response.content)
        tmp.flush()
        tmp.seek(0)
        model = pickle.load(tmp)
    return model

model = load_pickle_model(MODEL_URL)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return jsonify({"status": "SUCCESS", "message": "Success connect"}), 200

@app.route('/predict', methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return jsonify({"status": "FAILURE", 
                            "message": "Request body must be JSON"
                            }), 415

        data = request.get_json()

        if data is None:
            return jsonify({"status": "FAILURE", 
                            "message": "Received empty JSON"
                            }), 400
        
        unit_id = data.get('unit_id')
        if unit_id is None:
            return jsonify({"status": "FAILURE", 
                            "message": "unit_id is required"
                            }), 400

        similar_units = model.get_similar_units(unit_id)
        similar_units_json = similar_units.to_dict(orient='records')
        
        id = str(uuid.uuid4())
        createdAt = datetime.utcnow().isoformat()

        response = {
            "id": id,
            "result": similar_units_json,
            "createdAt": createdAt
        }

        store_data(id, response)

        return jsonify({"status": "SUCCESS", 
                        "data": response
                        }), 200
    
    except Exception as e:
        return jsonify({"status": "ERROR", 
                        "message": "Wrong unit_id"
                        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))