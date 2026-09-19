from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Yaha aapka model prediction ka code tha
    # Filhal ke liye demo result
    return render_template('index.html', prediction_text="Healthy Crop - Demo Result")

if __name__ == '__main__':
    app.run(debug=True)