from flask import Flask, render_template, request
from PIL import Image
import random

app = Flask(__name__)

# Demo ke liye kuch bimariyan aur upay
DISEASES = [
    {"name": "Healthy Plant - Bilkul Swasth Hai", "treatment": "Paudha swasth hai, regular paani dete raho."},
    {"name": "Early Blight - Jhulas Rog", "treatment": "Neem ka tel ka chhidkaw karo, kharab patte hata do."},
    {"name": "Late Blight - Pachheti Jhulsa", "treatment": "Fungicide ka upyog karo, khet me paani jama na hone do."},
    {"name": "Leaf Spot - Patti par daag", "treatment": "Sankramit patte tod kar jala do, saaf safai rakho."},
    {"name": "Bacterial Spot", "treatment": "Copper based dawai ka chhidkaw karo."}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Image open karke check kar lete hai (model nahi hai to random result)
            try:
                img = Image.open(file.stream)
            except:
                pass
            
            result = random.choice(DISEASES)
            result['confidence'] = random.randint(85, 98)

    return render_template('index.html', result=result)

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)