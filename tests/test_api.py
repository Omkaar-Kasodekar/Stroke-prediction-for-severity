# FILE: tests/test_api.py

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
import numpy as np
import app.routes as routes

from app.db import Base, DATABASE_URL, init_db, get_db
from app.routes import _normalize_severity, SimpleFallbackModel
from app.main import app

client = TestClient(app)


def _get_engine():
    return create_engine(DATABASE_URL, future=True)


def _reset_db():
    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM predictions;"))


def setup_function():
    engine = _get_engine()
    Base.metadata.create_all(bind=engine)
    _reset_db()


# -----------------------------
# EXISTING TESTS (unchanged)
# -----------------------------

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_basic_persistence():
    payload = {
        "age": 70,
        "bmi": 33.2,
        "avg_glucose_level": 165,
        "hypertension": 1,
        "heart_disease": 1,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    prediction_id = response.json()["prediction_id"]

    resp_get = client.get(f"/predictions/{prediction_id}")
    assert resp_get.status_code == 200


def test_get_prediction_not_found():
    resp = client.get("/predictions/99999")
    assert resp.status_code == 404


# -----------------------------
# COVERAGE BOOSTERS
# -----------------------------

def test_normalize_severity_variants():
    assert _normalize_severity(0) == "mild"
    assert _normalize_severity("1") == "moderate"
    assert _normalize_severity("severe") == "severe"
    assert _normalize_severity(999) == "999"


def test_simple_fallback_model():
    model = SimpleFallbackModel()
    X = np.array([[80, 35, 200, 1, 1]])
    assert model.predict(X)[0] == "severe"
    assert model.predict_proba(X).shape == (1, 3)


def test_init_db_runs():
    init_db()


def test_get_db_closes():
    generator = get_db()
    db = next(generator)
    assert db is not None
    try:
        next(generator)
    except StopIteration:
        pass


def test_empty_predictions():
    resp = client.get("/predictions")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
