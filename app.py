from flask import Flask, render_template, request
import random, os

app = Flask(__name__)

diseases = ["Tomato - Late Blight", "Tomato - Healthy", "Potato - Early Blight"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Demo prediction - model ki zarurat nahi
    result = random.choice(diseases)
    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)