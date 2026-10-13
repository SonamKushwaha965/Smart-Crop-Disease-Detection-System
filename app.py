from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from huggingface_hub import hf_hub_download
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MODEL LOAD ----------------
model = None
class_names = []

try:
    model_path = hf_hub_download(
        repo_id="sonamkri/smart-crop-disease-model",
        filename="crop_model.h5"
    )

    model = tf.keras.models.load_model(model_path)

    with open("class_names.json", "r") as f:
        class_names = json.load(f)

    print("Model Hugging Face se load ho gaya!")

except Exception as e:
    print("Model load nahi hua:", e)


# ---------------- ADVICE ----------------
def get_advice(disease):
    d = disease.lower()

    if "healthy" in d:
        return {
            "icon": "healthy",
            "status": "No disease detected",
            "advice": "Patti healthy hai. Regular paani aur dekh-bhal jaari rakhein."
        }

    advice_map = [
        (
            "early blight",
            "Mancozeb ya Chlorothalonil spray karein. Beemar pattiyan hata dein."
        ),
        (
            "late blight",
            "Copper-based spray karein aur beemar pattiyan hata dein."
        ),
        (
            "leaf spot",
            "Beemar pattiyan hataein. Paani pattiyon par seedha na dalein."
        ),
        (
            "leaf mold",
            "Hawa ka achha prabandh karein aur beemar pattiyan hataein."
        ),
        (
            "mosaic",
            "Beemar plant ko hata dein aur fasal expert se salah lein."
        ),
        (
            "yellow",
            "Pilepan ki samasya ho sakti hai. Fasal expert se salah lein."
        ),
        (
            "blight",
            "Mancozeb ya Chlorothalonil spray karein."
        ),
        (
            "bacterial",
            "Beemar pattiyan hataein aur fasal expert se salah lein."
        ),
        (
            "spider",
            "Prabhavit pattiyon ko alag karein aur agriculture expert se salah lein."
        ),
        (
            "target spot",
            "Beemar pattiyan hataein aur fasal ki regular monitoring karein."
        )
    ]

    for key, message in advice_map:
        if key in d:
            return {
                "icon": "disease",
                "status": "Disease detected",
                "advice": message
            }

    return {
        "icon": "disease",
        "status": "Disease detected",
        "advice": "Kripya fasal expert ya agriculture officer se salah lein."
    }


# ---------------- HOME ----------------
@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None
    img_path = None

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            error = "Pehle photo select karo!"

        elif model is None:
            error = "Model load nahi hua. Please try again."

        else:
            try:

                fname = secure_filename(file.filename)

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    fname
                )

                file.save(file_path)

                img_path = "uploads/" + fname

                img = (
                    Image.open(file_path)
                    .convert("RGB")
                    .resize((224, 224))
                )

                arr = np.expand_dims(
                    np.array(img) / 255.0,
                    axis=0
                )

                predictions = model.predict(arr, verbose=0)[0]

                index = int(np.argmax(predictions))

                disease = class_names[index]

                info = get_advice(disease)

                result = {
                    "disease": disease.replace("___", " - ").replace("__", " - "),
                    "confidence": round(
                        float(predictions[index]) * 100,
                        2
                    ),
                    "status": info["status"],
                    "advice": info["advice"],
                    "icon": info["icon"]
                }

            except Exception as e:

                print("Prediction error:", e)

                error = "Image process nahi hui: " + str(e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        img_path=img_path
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )