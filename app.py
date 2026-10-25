from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

# Demo ke liye kuch diseases
DISEASES = [
    "Tomato - Healthy",
    "Tomato - Late Blight", 
    "Tomato - Early Blight",
    "Potato - Healthy",
    "Potato - Late Blight"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # File upload check
    if 'image' not in request.files:
        return render_template('index.html', prediction="Please upload an image")
    
    # Demo prediction - random result (kyunki asli model Render pe nahi chalta)
    result = random.choice(DISEASES)
    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)