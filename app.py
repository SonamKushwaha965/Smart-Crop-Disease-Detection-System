"""
Smart Crop Disease Detection - Complete Backend
Group 05 | Government Polytechnic Katihar
Run:  python app.py  ->  http://localhost:5000
"""
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from PIL import Image
import json, os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---- Model load (model na ho to bhi website chalegi) ----
model = None
class_names = []
if os.path.exists("crop_model.h5") and os.path.exists("class_names.json"):
    model = tf.keras.models.load_model("crop_model.h5")
    class_names = json.load(open("class_names.json"))
    print("✅ Model load ho gaya!")
else:
    print("⚠️  crop_model.h5 nahi mila. Pehle train_model.py chalao (Google Colab).")

def get_advice(disease):
    d = disease.lower()
    if "healthy" in d:
        return {"icon": "healthy", "status": "No disease detected",
                "advice": "Patti ekdum healthy hai. Regular paani aur dekh-bhal jaari rakhein."}
    advice_map = [
        ("early blight", "Mancozeb ya Chlorothalonil spray karein. Beemar pattiyan hata dein aur beej shudh use karein."),
        ("late blight", "Copper-based spray karein. Patta pura siya ho sakta hai. Fasal expert se salah lein."),
        ("leaf spot", "Beemar pattiyan tod kar fenk dein. Mancozeb spray karein aur paani pattiyon par na dalein."),
        ("leaf mold", "Hawa ka achha prabandh karein. Chlorothalonil spray karein."),
        ("mosaic", "Virus ka ilaaj nahi hota - beemar plant hatayein. Machhar rokne ka dhyaan rakhein."),
        ("yellow", "Pilepan ki samasya hai. Zinc/Magnesium ki kami ho sakti hai. Fasal expert se test karwayein."),
        ("rust", "Sulfur-based spray karein. Namibi kam rakhein."),
        ("scab", "Captan ya Mancozeb spray karein. Gire hue phal/patte saaf rakhein."),
        ("blight", "Mancozeb ya Chlorothalonil spray karein. Paani jama na hone dein."),
        ("spot", "Beemar pattiyan hataein aur Mancozeb spray karein."),
    ]
    for key, msg in advice_map:
        if key in d:
            return {"icon": "disease", "status": "Disease detected", "advice": msg}
    return {"icon": "disease", "status": "Disease detected",
            "advice": "Ye rog mila: " + disease + ". Kripya fasal expert (KVK/agriculture officer) se salah lein."}

@app.route("/", methods=["GET", "POST"])
def home():
    result, error, img_path = None, None, None
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            error = "Pehle photo select karo!"
        elif model is None:
            error = "Model load nahi hua. Pehle crop_model.h5 banao (train_model.py chalao)."
        else:
            try:
                fname = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, fname))
                img_path = "uploads/" + fname
                img = Image.open(os.path.join(UPLOAD_FOLDER, fname)).convert("RGB").resize((224, 224))
                arr = np.expand_dims(np.array(img) / 255.0, axis=0)
                preds = model.predict(arr)[0]
                idx = int(np.argmax(preds))
                info = get_advice(class_names[idx])
                result = {
                    "disease": class_names[idx].replace("___", " - "),
                    "confidence": round(float(preds[idx]) * 100, 2),
                    "status": info["status"],
                    "advice": info["advice"],
                    "icon": info["icon"],
                }
            except Exception as e:
                error = "Image process nahi hui: " + str(e)
    return render_template("index.html", result=result, error=error, img_path=img_path)

if __name__ == "__main__":
    app.run(debug=True)