# Sentiment Analyzer

Sentiment Analyzer is an API built with FastAPI that automatically detects and analyzes the emotional tone and sentiment from text or images. The project follows modern best practices like the 12-Factor App principles to ensure scalability, maintainability, and ease of deployment, whether running locally or in containerized environments.

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
     python.exe -m pip install --upgrade pip
     pip install -r requirements.txt

  4. Setup *.env* file (create from .env.example and fill in required variables)

  6. Start the FastAPI Server

     ```bash
     uvicorn app.main:app --reload

  **The app will be available at http://localhost:8000**

---

## Running with Docker

1. Clone the repo

   ```bash
   git clone https://github.com/bibekjoshi01/sentiment-analyzer
   cd sentiment-analyzer

2. Create a *.env* file in the project root with required variables (see .env.example).

4. Build the docker image

   ```bash
   docker build -t sentiment-analyzer .

5. Run the docker container

   ```bash
   docker run -p 8000:8000 sentiment-analyzer

**The app will be available at http://localhost:8000**

**Note:** To stop the Docker container, use docker ps to find the container ID and then docker stop <container_id>


**Formatting and Linting Code**

   ```pre-commit install```

1. ruff check / ruff check --fix / ruff format
2. black .
3. pre-commit run --all-files
