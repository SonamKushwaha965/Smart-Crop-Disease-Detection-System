from huggingface_hub import hf_hub_download

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

    print("✅ Model Hugging Face se load ho gaya!")

except Exception as e:
    print("⚠️ Model load nahi hua:", e)