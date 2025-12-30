from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class TextData(BaseModel):
    text: str

@app.post("/predict")
def predict_sentiment(data: TextData):
    # On simule l'IA pour débloquer votre développement Streamlit
    sentiments = ["POSITIVE", "NEGATIVE"]
    prediction = random.choice(sentiments)
    score = random.uniform(0.85, 0.99)
    
    return {"label": prediction, "score": score}