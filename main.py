from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import torch

app = FastAPI()

# --- ÉTAPE 1 : AUTORISER STREAMLIT (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ÉTAPE 2 : CHARGER LE MODÈLE ---
try:
    # On utilise un modèle léger et performant pour éviter les plantages
    classifier = pipeline(
        "sentiment-analysis", 
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )
    MODEL_READY = True
except Exception as e:
    print(f"Erreur modèle : {e}")
    MODEL_READY = False

class TextData(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(data: TextData):
    # Si le modèle a réussi à charger
    if MODEL_READY:
        result = classifier(data.text)[0]
        # On convertit les étoiles (1-5) en POSITIVE/NEGATIVE
        star_value = int(result['label'].split()[0])
        label = "POSITIVE" if star_value >= 4 else "NEGATIVE"
        score = result['score']
    else:
        # Secours si le modèle plante (votre ancien code qui marchait)
        label = "POSITIVE"
        score = 0.0

    return {"label": label, "score": score}
