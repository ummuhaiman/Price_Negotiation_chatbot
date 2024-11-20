import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Hugging Face API
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
if not HUGGING_FACE_API_KEY:
    raise ValueError("HUGGING_FACE_API_KEY is not set in environment variables.")

# Initialize NLTK's VADER
nltk.download('vader_lexicon')
sentiment_analyzer = SentimentIntensityAnalyzer()

app = FastAPI(title="Negotiation Chatbot API")

# In-memory storage for negotiation sessions
sessions = {}

# Pricing Configuration
PRODUCT = "Premium Laptop"
INITIAL_PRICE = 1000.0  # Starting price in USD
MIN_PRICE = 700.0       # Minimum acceptable price
MAX_PRICE = 1200.0      # Maximum price
PRICE_STEP = 50.0       # Increment/decrement step for counteroffers

class StartNegotiationRequest(BaseModel):
    user_id: str  # Unique identifier for the user/session

class OfferRequest(BaseModel):
    user_id: str
    offer: float

class ResponseMessage(BaseModel):
    message: str
    current_price: float
    status: str  # e.g., "ongoing", "accepted", "rejected"

@app.post("/start-negotiation", response_model=ResponseMessage)
def start_negotiation(request: StartNegotiationRequest):
    user_id = request.user_id
    if user_id in sessions:
        raise HTTPException(status_code=400, detail="Negotiation already started for this user.")

    sessions[user_id] = {
        "product": PRODUCT,
        "initial_price": INITIAL_PRICE,
        "current_price": INITIAL_PRICE,
        "status": "ongoing"
    }

    message = f"Welcome! Let's negotiate the price for the {PRODUCT}. The starting price is ${INITIAL_PRICE}."
    return ResponseMessage(message=message, current_price=INITIAL_PRICE, status="ongoing")

@app.post("/offer", response_model=ResponseMessage)
def make_offer(request: OfferRequest):
    user_id = request.user_id
    offer = request.offer

    if user_id not in sessions:
        raise HTTPException(status_code=404, detail="Negotiation session not found. Please start a negotiation first.")

    session = sessions[user_id]

    if session["status"] != "ongoing":
        raise HTTPException(status_code=400, detail=f"Negotiation already {session['status']}.")

    # Pricing Logic
    if offer >= session["current_price"]:
        session["status"] = "accepted"
        message = f"Great! We've accepted your offer of ${offer} for the {PRODUCT}."
        return ResponseMessage(message=message, current_price=offer, status=session["status"])
    elif offer < MIN_PRICE:
        session["status"] = "rejected"
        message = f"Unfortunately, we cannot accept an offer lower than ${MIN_PRICE} for the {PRODUCT}."
        return ResponseMessage(message=message, current_price=session["current_price"], status=session["status"])
    else:
        # Generate a counteroffer using Hugging Face API
        new_price = max(offer + PRICE_STEP, MIN_PRICE)
        session["current_price"] = new_price

        # Use Hugging Face API for response generation
        payload = {
            "inputs": f"User offered ${offer} for a {PRODUCT}. Counteroffer at ${new_price}."
        }
        headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error with Hugging Face API.")

        hf_response = response.json()
        bot_message = hf_response.get("generated_text", f"How about we settle at ${new_price} for the {PRODUCT}?")

        return ResponseMessage(message=bot_message, current_price=new_price, status="ongoing")

@app.get("/current-price")
def get_current_price(user_id: str):
    if user_id not in sessions:
        raise HTTPException(status_code=404, detail="Negotiation session not found.")

    session = sessions[user_id]
    return {
        "product": session["product"],
        "current_price": session["current_price"],
        "status": session["status"]
    }

@app.post("/sentiment-analysis")
def sentiment_analysis(text: str):
    scores = sentiment_analyzer.polarity_scores(text)
    return scores
