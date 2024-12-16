from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import gdown
import os
from PIL import Image
from io import BytesIO
import requests

app = Flask(__name__)

git_pipe = pipeline("image-to-text", model="microsoft/git-large-textcaps")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

flower_output = "Flower_classifier.h5"
flower_model_id = "1AlBunIPDg4HYYCqhcHtOiXxnPFhmsoSn"
flower_url = f"https://drive.google.com/uc?id={flower_model_id}"
if not os.path.exists(flower_output):
    gdown.download(flower_url, flower_output, quiet=False)
flower_model = load_model(flower_output)

bird_output = "Bird_classifier.h5"
bird_model_id = "1a6vqFERbrr_Cw-NyBqVHG7fsjU2-xKJ4"
bird_url = f"https://drive.google.com/uc?id={bird_model_id}"
if not os.path.exists(bird_output):
    gdown.download(bird_url, bird_output, quiet=False)
bird_model = load_model(bird_output)

dog_output = "DogClassifier.h5"
dog_model_id = "1UFn1NGVtP5rhvcWnAANQ_4E9YRJvDEad"
dog_url = f"https://drive.google.com/uc?id={dog_model_id}"
if not os.path.exists(dog_output):
    gdown.download(dog_url, dog_output, quiet=False)
dog_model = load_model(dog_output)

landmark_output = "LandmarkClassifierV5.h5"
landmark_model_id = "1PXixJsrUaVcHEEC-jDlv4tHT2qrCrf5c"
landmark_url = f"https://drive.google.com/uc?id={landmark_model_id}"
if not os.path.exists(landmark_output):
    gdown.download(landmark_url, landmark_output, quiet=False)
landmark_model = load_model(landmark_output)

dog_list = ["Bulldog", "Chihuahua", "Dobermann", "German Shepherd", "Golden Retriever", "Husky", "Labrador Retriever", "Pomeranian", "Pug", "Rottweiler", "Street dog"]
flower_list = ["Jasmine", "Lavender", "Lily", "Lotus", "Orchid", "Rose", "Sunflower", "Tulip", "Daisy", "Dandelion"]
bird_list = ["Crow", "Eagle", "Flamingo", "Hummingbird", "Parrot", "Peacock", "Pigeon", "Sparrow", "Swan"]
landmark_list = ["The Agra Fort", "Ajanta Caves", "Alai Darwaza", "Amarnath Temple", "The Amber Fort", "Basilica of Bom Jesus", "Brihadisvara Temple", "Charminar", "Chhatrapati Shivaji Terminus", "Dal Lake", "The Elephanta Caves", "Ellora Caves", "Fatehpur Sikri", "Gateway of India", "Golden Temple", "Hawa Mahal", "Humayun's Tomb", "India Gate", "Jagannath Temple", "Jama Masjid", "Jantar Mantar", "Kedarnath Temple", "Konark Sun Temple", "Meenakshi Temple", "Nalanda Mahavihara", "Qutb Minar", "The Red Fort", "Taj Mahal", "Victoria Memorial"]

def identify_dog(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = dog_model.predict(img_array)
    return dog_list[np.argmax(predictions[0])]

def identify_flower(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = flower_model.predict(img_array)
    return flower_list[np.argmax(predictions[0])]

def identify_bird(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = bird_model.predict(img_array)
    return bird_list[np.argmax(predictions[0])]

def identify_landmark(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = landmark_model.predict(img_array)
    return landmark_list[np.argmax(predictions[0])]

def generate_final_caption(img):
    caption_dict = git_pipe(img)
    caption = caption_dict[0]["generated_text"]
    if "building" in caption.lower():
        caption += "\nThe landmark is: " + identify_landmark(img)
    elif "flower" in caption.lower():
        caption += "\nThe flower is: " + identify_flower(img)
    elif "dog" in caption.lower() or "puppy" in caption.lower():
        caption += "\nThe dog is: " + identify_dog(img)
    elif "bird" in caption.lower():
        caption += "\nThe bird is: " + identify_bird(img)
    return caption

def get_bot_response(input_text, chat_history_ids=None):
    new_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = new_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_input_ids], dim=-1)
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

@app.route("/caption", methods=["POST"])
def caption_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image provided"}), 400
    img = Image.open(file)
    caption = generate_final_caption(img)
    return jsonify({"caption": caption})

@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    response = get_bot_response(query)
    return jsonify({"response": response})

from flask_ngrok import run_with_ngrok
run_with_ngrok(app)
app.run()
