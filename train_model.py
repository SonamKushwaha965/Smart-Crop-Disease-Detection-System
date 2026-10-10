"""
Step 1: Model Training (Smart Crop Disease Detection)
Run this ONCE to train the CNN model and save it.
TIP: Run on Google Colab (free GPU) for faster training.
Dataset: Kaggle - "PlantVillage" (search "plantvillage dataset" on kaggle.com)
Extract it so you have a folder like:
    plantvillage/
        Apple___Apple_scab/
        Apple___healthy/
        Tomato___Early_blight/
        ...
"""
import tensorflow as tf
from tensorflow.keras import layers, models
import json

DATA_DIR = "plantvillage"      # <- apne dataset folder ka naam yahan likho
IMG_SIZE = (224, 224)
BATCH = 32
EPOCHS = 15

# Dataset load karo (80% train, 20% validation)
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="training", seed=42,
    image_size=IMG_SIZE, batch_size=BATCH)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="validation", seed=42,
    image_size=IMG_SIZE, batch_size=BATCH)

class_names = train_ds.class_names
print(f"Classes: {len(class_names)}")
print(class_names)

# Simple CNN model
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(224, 224, 3)),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(len(class_names), activation="softmax")
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# Model aur class names save karo
model.save("crop_model.h5")
with open("class_names.json", "w") as f:
    json.dump(class_names, f)

print("Done! crop_model.h5 aur class_names.json save ho gaye.")