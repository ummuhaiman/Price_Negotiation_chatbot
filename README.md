# Price_Negotiation_chatbot_API 🤝💬
An intelligent negotiation chatbot API built with FastAPI, leveraging Hugging Face for natural language generation and NLTK's VADER for sentiment analysis. This API allows users to negotiate product prices in real-time while dynamically generating counteroffers and analyzing sentiment for a human-like interaction.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation and Setup](#installation-and-setup)
4. [API Endpoints](#api-endpoints)
   - [Start Negotiation](#1-start-negotiation)
   - [Make Offer](#2-make-offer)
   - [Get Current Price](#3-get-current-price)
   - [Sentiment Analysis](#4-sentiment-analysis)
5. [Configuration](#configuration)
6. [How It Works](#how-it-works)
7. [Future Enhancements](#future-enhancements)
8. [License](#license)

    
---

## **Features**

- **Start Negotiations**: Users can initiate a negotiation session for a product with a configurable starting price.
- **Dynamic Counteroffers**: The chatbot uses Hugging Face’s GPT-2 model to intelligently generate counteroffers during price negotiations.
- **Sentiment Analysis**: Analyze user input sentiment to assess negotiation tone (positive, negative, or neutral).
- **Real-Time Price Updates**: Keep track of the current price and negotiation status for each session.

---

## **Technologies Used**

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Fast and modern Python web framework for building APIs.
- **Natural Language Generation**: [Hugging Face GPT-2](https://huggingface.co/) - Pre-trained transformer model for generating responses.
- **Sentiment Analysis**: [NLTK VADER](https://www.nltk.org/) - A pre-built lexicon for analyzing text sentiment.
- **Environment Variables Management**: [python-dotenv](https://pypi.org/project/python-dotenv/) - For securely handling API keys.
- **HTTP Client**: [Requests](https://docs.python-requests.org/) - To interact with Hugging Face API.

---
## Step 1: Clone the Repository

     git clone https://github.com/ummuhaiman/Price_Negotiation_chatbot.git
  
     cd negotiation-chatbot-api

---
##  Step 2: Set Up Environment

   1.Install dependencies:
     
    pip install -r requirements.txt
    
   2.Create a .env file in the project root and add your Hugging Face API key:

    HUGGING_FACE_API_KEY=your_hugging_face_api_key

## Step 3: Run the Application
   - Start the FastAPI server:
    
    uvicorn main:app --reload
    Access the interactive API documentation at http://127.0.0.1:8000/docs.
---
## API Endpoints
1. Start Negotiation

 - Endpoint:POST /start-negotiation
 - Request:
   ```json
   {
      "user_id": "123"
   }

 - Response:
   ```json
   {
     "message": "Welcome! Let's negotiate the price for the Premium Laptop. The starting price is $1000.0.",
     "current_price": 1000.0,
     "status": "ongoing"
   }
2. Make Offer
 - Endpoint: POST /offer
 - Request:
   ```json
   {
    "user_id": "user123",
    "offer": 800
   }
 - Response:
   ```json
   {
    "message": "How about we settle at $850.0 for the Premium Laptop?",
    "current_price": 850.0,
    "status": "ongoing"

   }
   
   
  
4. Get Current Price
 - Endpoint: GET /current-price
 - Query Parameter: user_id=123
   ```json
   {
   "product": "Premium Laptop",
   "current_price": 850.0,
   "status": "ongoing"
   }

5. Sentiment Analysis
 - Endpoint: POST /sentiment-analysis  
 - Request:
   ```json
   {
   "text": "I think this is a fair price."
   }

 - Response:
   ```json
   {
   "neg": 0.0,
   "neu": 0.544,
   "pos": 0.456,
   "compound": 0.6369
   }


---
## Configuration

Key configurations for negotiation are defined in the source code:

- PRODUCT: Name of the product (default: Premium Laptop).
- INITIAL_PRICE: Starting price of the product (default: 1000.0 USD).
- MIN_PRICE: Minimum acceptable price (default: 700.0 USD).
- MAX_PRICE: Maximum price (default: 1200.0 USD).
- PRICE_STEP: Counteroffer increment/decrement value (default: 50.0 USD).

## How It Works

1.Session Management:
   Each negotiation session is stored in-memory using a sessions dictionary.
   A unique user_id is required to start a session.

2.Pricing Logic:
   If a user’s offer is greater than or equal to the current price, the negotiation is accepted.
   If an offer is below the minimum price, it’s rejected.
   For other offers, a counteroffer is generated.

3.Counteroffer Generation:
   GPT-2 model from Hugging Face API generates personalized responses based on user input.

4.Sentiment Analysis:
   User input is analyzed using VADER to determine sentiment (negative, neutral, positive).
        
## License
This project is licensed under the MIT License.

   
    
