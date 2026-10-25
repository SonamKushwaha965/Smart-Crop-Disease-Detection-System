import os
import json
import random
from flask import Flask, render_template, request, jsonify
from PIL import Image

app = Flask(__name__)

# JSON load karo - ye to hai tumhare pass
with open("class_names.json", "r") as f:
    class_names = json.load(f)

with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

print("✅ App Loaded (Demo Mode) - Phone pe chalega")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # File aayi ya nahi check
    if 'file' not in request.files:
        return jsonify({"error": "File nahi mili"}), 400
    
    file = request.files['file']
    # Image open karke dekh lete hai ki kharab to nahi
    try:
        img = Image.open(file).convert('RGB')
    except:
        return jsonify({"error": "Image kharab hai"}), 400

    # --- YAHAN DUMMY PREDICTION HAI (Phone demo ke liye) ---
    # Kal jab college PC pe tensorflow lagega, ye asli model se replace ho jayega
    disease_name = random.choice(class_names)
    confidence = round(random.uniform(85, 98), 1)
    info = disease_info.get(disease_name, {})

    return jsonify({
        "disease": disease_name,
        "confidence": confidence,
        "info": info,
        "note": "Demo Mode - College PC pe original model chalega"
    })

if __name__ == '__main__':
    print("Starting server for PC + Phone...")
    app.run(host='0.0.0.0', port=5000, debug=True)