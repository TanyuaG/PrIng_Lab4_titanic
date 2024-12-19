import pickle
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

app = FastAPI()

def predict_sentiment(text: str) -> str:
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)
    return "Positive" if prediction[0] == 1 else "Negative"

@app.get("/predict/{text}")
async def predict(text: str):
    sentiment = predict_sentiment(text)
    return {"sentiment": sentiment}

@app.get("/predict/")
async def predict(text: str):
    sentiment = predict_sentiment(text)
    return {"sentiment": sentiment}
