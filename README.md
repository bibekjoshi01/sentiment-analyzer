# Sentiment Analyzer

AI-Powered Sentiment Analyzer API with FastAPI under the Fuse AI Fellowship and Follows the 12-Factor App principles.

---

## Prerequisites

1. Python 3.10+ installed (if running locally)  
2. Docker installed (if running with Docker)  
3. `.env` file with required environment variables set (see `.env.example`)  

---

## Running Locally (Without Docker)

1. Clone the repo

   ```bash
   git clone https://github.com/bibekjoshi01/sentiment-analyzer
   cd sentiment-analyzer

2. Create and activate a virtual environment

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate

  3. Install Dependencies

     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt

  4. Setup *.env* file (create from .env.example and fill in required variables)
  5. Start the FastAPI Server

     ```bash
     uvicorn app.main:app --reload

  **The app will be available at http://localhost:8000**
