import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_site_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_authticity():
    payload = {"text": "I love coding."}

    response = client.post("/api/analyze/text", json=payload)

    assert response.status_code == 401


def test_signup_login_and_analyze():
    unique_email = f"user_{uuid.uuid4()}@example.com"
    signup_payload = {
        "full_name": "Test User",
        "email": unique_email,
        "password": "testpassword123",
    }

    signup_response = client.post("/api/auth/signup", json=signup_payload)
    assert signup_response.status_code == 200

    # Login to get token
    login_payload = {"email": unique_email, "password": "testpassword123"}

    login_response = client.post("/api/auth/login", json=login_payload)
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data

    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Call authenticated /api/analyze/text
    analyze_payload = {"text": "I love coding."}

    analyze_response = client.post(
        "/api/analyze/text", json=analyze_payload, headers=headers
    )
    assert analyze_response.status_code == 200
    analyze_data = analyze_response.json()
    assert "sentiment" in analyze_data
    assert analyze_data["sentiment"] in [
        "positive",
        "negative",
        "neutral",
    ]
